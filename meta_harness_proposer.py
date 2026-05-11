#!/usr/bin/env python3
"""
Meta-Harness Proposer: Coding-Agent that diagnoses harness failures and edits code.
====================================================================================
Inspired by Meta-Harness (Lee et al., 2026) — the proposer is a coding agent
that reads the filesystem experience store, inspects raw traces & scores,
forms causal hypotheses about why the harness failed, and writes targeted code
patches.

Design goals
------------
- Zero heavy dependencies: only stdlib + urllib for LLM calls.
- Works with any OpenAI-compatible endpoint (Ollama, Groq, OpenAI, etc.).
- Validates every proposed patch with py_compile before writing.
- Logs its own reasoning as a "proposed" run so the outer loop can evaluate it.

Usage
-----
    # Diagnose the last 20 runs and propose a patch
    python meta_harness_proposer.py -- diagnose --top-k 20 --target toposwarm_lazyown_orchestrator.py

    # Dry-run (print patch, do not write)
    python meta_harness_proposer.py --diagnose --dry-run

    # Apply a specific patch file
    python meta_harness_proposer.py --apply-patch my_patch.py --target toposwarm_lazyown_orchestrator.py

Environment variables
---------------------
    META_PROPOSER_API_URL   OpenAI-compatible chat completions endpoint
    META_PROPOSER_API_KEY   API key (optional for local Ollama)
    META_PROPOSER_MODEL     Model name (default: llama3.1)
    META_PROPOSER_MAX_TOKENS  Max tokens for generation (default: 4096)

Author: Gris Iscomeback  —  GPL v3
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import py_compile
import re
import sys
import tempfile
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def _setup_logger(name: str = "MetaHarnessProposer", level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    if not logger.handlers:
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(logging.Formatter(
            "%(asctime)s %(name)-24s %(levelname)-8s %(message)s"
        ))
        logger.addHandler(h)
    return logger


# ---------------------------------------------------------------------------
# LLM client (OpenAI-compatible, stdlib only)
# ---------------------------------------------------------------------------

@dataclass
class LLMConfig:
    api_url: str = "http://localhost:11434/v1/chat/completions"
    api_key: str = ""
    model: str = "llama3.1"
    max_tokens: int = 4096
    temperature: float = 0.3
    timeout: int = 120
    fallback_url: str = "http://localhost:11434/v1/chat/completions"
    fallback_model: str = "granite4.1:3b"


class LLMClient:
    """Minimal OpenAI-compatible chat client using only urllib.

    Auto-falls back to local Ollama if the primary endpoint returns
    401/403/404 (auth or routing errors).
    """

    def __init__(self, cfg: LLMConfig, logger: logging.Logger) -> None:
        self.cfg = cfg
        self.logger = logger

    def _try_chat(self, api_url: str, model: str, system: str, user: str) -> str:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": self.cfg.temperature,
            "max_tokens": self.cfg.max_tokens,
        }
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.cfg.api_key and api_url == self.cfg.api_url:
            headers["Authorization"] = f"Bearer {self.cfg.api_key}"
        req = urllib.request.Request(
            api_url, data=data, headers=headers, method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.cfg.timeout) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        choices = result.get("choices", [])
        if choices:
            return choices[0].get("message", {}).get("content", "")
        return ""

    def chat(self, system: str, user: str) -> str:
        """Send a chat request and return the assistant message content."""
        # Try primary endpoint first
        try:
            return self._try_chat(self.cfg.api_url, self.cfg.model, system, user)
        except urllib.error.HTTPError as exc:
            if exc.code in (401, 403, 404):
                self.logger.warning(
                    "Primary LLM endpoint returned %d — falling back to local Ollama (%s)",
                    exc.code, self.cfg.fallback_url,
                )
            else:
                self.logger.error("LLM request failed: %s", exc)
                return ""
        except Exception as exc:
            self.logger.error("LLM request failed: %s", exc)
            return ""
        # Fallback to local Ollama
        try:
            return self._try_chat(self.cfg.fallback_url, self.cfg.fallback_model, system, user)
        except Exception as exc:
            self.logger.error("Fallback LLM request failed: %s", exc)
            return ""


# ---------------------------------------------------------------------------
# File-system experience reader
# ---------------------------------------------------------------------------

class ExperienceReader:
    """Reads meta_harness_logs/ and builds diagnostic context."""

    def __init__(self, log_dir: Path, logger: logging.Logger) -> None:
        self.log_dir = log_dir
        self.logger = logger

    def list_runs(self, n: Optional[int] = None) -> List[Path]:
        dirs = sorted(
            (p for p in self.log_dir.iterdir() if p.is_dir() and p.name.startswith("run_")),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        return dirs[:n] if n else dirs

    def load_run(self, run_dir: Path) -> Optional[Dict[str, Any]]:
        harness_path = run_dir / "harness.json"
        trace_path = run_dir / "trace.jsonl"
        score_path = run_dir / "score.json"
        reasoning_path = run_dir / "reasoning.txt"
        if not harness_path.exists() or not score_path.exists():
            return None
        try:
            run = {
                "id": run_dir.name,
                "harness": json.loads(harness_path.read_text(encoding="utf-8")),
                "score": json.loads(score_path.read_text(encoding="utf-8")),
                "traces": [],
                "reasoning": "",
            }
            if trace_path.exists():
                run["traces"] = [
                    json.loads(line)
                    for line in trace_path.read_text(encoding="utf-8").splitlines()
                    if line.strip()
                ]
            if reasoning_path.exists():
                run["reasoning"] = reasoning_path.read_text(encoding="utf-8")
            return run
        except Exception as exc:
            self.logger.debug("Failed to load run %s: %s", run_dir.name, exc)
            return None

    def build_diagnostic_context(self, top_k: int = 20) -> str:
        """
        Build a rich diagnostic string containing:
        - failed runs with their traces
        - successful runs for contrast
        - aggregate statistics
        """
        runs = [r for r in (self.load_run(rd) for rd in self.list_runs(top_k * 2)) if r]
        if not runs:
            return "No runs found in experience store."

        failures = [r for r in runs if not r["score"].get("success", True)]
        successes = [r for r in runs if r["score"].get("success", True)]

        lines = ["=== META-HARNESS DIAGNOSTIC CONTEXT ===", ""]
        lines.append(f"Total runs inspected: {len(runs)}")
        lines.append(f"Failures: {len(failures)} | Successes: {len(successes)}")
        lines.append("")

        # Aggregate stats
        latencies = [r["score"].get("latency_ms", 0) for r in runs]
        if latencies:
            lines.append(f"Latency — min: {min(latencies):.0f}ms, max: {max(latencies):.0f}ms, avg: {sum(latencies)/len(latencies):.0f}ms")
        lines.append("")

        # Show failures first (most important for diagnosis)
        lines.append("--- FAILED RUNS (most recent first) ---")
        for r in failures[:top_k]:
            lines.append(f"\nRun: {r['id']}")
            lines.append(f"Prompt: {r['score'].get('prompt', 'N/A')}")
            lines.append(f"Tool: {r['harness'].get('tool_name', 'N/A')}")
            lines.append(f"Latency: {r['score'].get('latency_ms', 0):.0f}ms | Context chars: {r['score'].get('context_chars', 0)}")
            for t in r["traces"]:
                lines.append(f"  Step {t.get('step')}: {t.get('tool')} → ok={t.get('ok')} | {t.get('output', '')[:200]}")
            if r["reasoning"]:
                lines.append(f"  Prior reasoning: {r['reasoning'][:300]}")

        lines.append("")
        lines.append("--- SUCCESSFUL RUNS (contrast) ---")
        for r in successes[:top_k // 2]:
            lines.append(f"\nRun: {r['id']} | Tool: {r['harness'].get('tool_name')} | Latency: {r['score'].get('latency_ms', 0):.0f}ms")
            lines.append(f"  Prompt: {r['score'].get('prompt', 'N/A')}")

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Patch engine
# ---------------------------------------------------------------------------

class PatchEngine:
    """Applies code patches safely."""

    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger

    def validate_syntax(self, code: str) -> Tuple[bool, str]:
        """Return (ok, error_message)."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            tmp = f.name
        try:
            py_compile.compile(tmp, doraise=True)
            return True, ""
        except py_compile.PyCompileError as exc:
            return False, str(exc)
        finally:
            try:
                os.unlink(tmp)
            except OSError:
                pass

    def apply_full_rewrite(self, target_path: Path, new_code: str, dry_run: bool = False) -> bool:
        """Validate and optionally write a full file rewrite."""
        ok, err = self.validate_syntax(new_code)
        if not ok:
            self.logger.error("Proposed code failed syntax check: %s", err)
            return False
        if dry_run:
            self.logger.info("[DRY-RUN] Would rewrite %s (%d chars)", target_path, len(new_code))
            return True
        backup = target_path.with_suffix(".py.bak")
        try:
            target_path.rename(backup)
        except Exception:
            pass
        target_path.write_text(new_code, encoding="utf-8")
        self.logger.info("Rewrote %s (backup: %s)", target_path, backup)
        return True

    def _strip_line_numbers(self, s: str) -> str:
        """Remove leading ' 123: ' line numbers that the LLM may copy."""
        return "\n".join(re.sub(r"^\s*\d+:\s", "", line) for line in s.splitlines())

    def apply_line_range(self, target_path: Path, line_start: int, line_end: int, new_string: str, dry_run: bool = False) -> bool:
        """Replace a range of lines (1-indexed) with new text."""
        original = target_path.read_text(encoding="utf-8")
        lines = original.splitlines()
        if line_start < 1 or line_end > len(lines) or line_start > line_end:
            self.logger.error("Invalid line range %d-%d in %s (file has %d lines)", line_start, line_end, target_path, len(lines))
            return False
        candidate_lines = lines[:line_start - 1] + new_string.splitlines() + lines[line_end:]
        candidate = "\n".join(candidate_lines)
        if original.endswith("\n") and not candidate.endswith("\n"):
            candidate += "\n"
        elif not original.endswith("\n") and candidate.endswith("\n"):
            candidate = candidate[:-1]
        ok, err = self.validate_syntax(candidate)
        if not ok:
            self.logger.error("Patch failed syntax check: %s", err)
            return False
        if dry_run:
            self.logger.info("[DRY-RUN] Would replace lines %d-%d in %s", line_start, line_end, target_path)
            return True
        backup = target_path.with_suffix(".py.bak")
        try:
            target_path.rename(backup)
        except Exception:
            pass
        target_path.write_text(candidate, encoding="utf-8")
        self.logger.info("Patched %s lines %d-%d (backup: %s)", target_path, line_start, line_end, backup)
        return True

    def apply_diff_hunk(self, target_path: Path, old_string: str, new_string: str, dry_run: bool = False) -> bool:
        """Apply a targeted string replacement after validation.

        Tries exact match first, then fuzzy match (ignoring leading/trailing
        whitespace per line), then without line numbers.  If all fail, prints
        the patch for manual apply.
        """
        original = target_path.read_text(encoding="utf-8")
        candidate = None

        # 1. Exact match
        if old_string in original:
            candidate = original.replace(old_string, new_string, 1)
        else:
            # 2. Fuzzy match: normalize whitespace on each line
            def _norm(s: str) -> str:
                return "\n".join(line.strip() for line in s.splitlines())
            norm_original = _norm(original)
            norm_old = _norm(old_string)
            if norm_old in norm_original:
                orig_lines = original.splitlines()
                old_lines = old_string.splitlines()
                for i in range(len(orig_lines) - len(old_lines) + 1):
                    if _norm("\n".join(orig_lines[i:i + len(old_lines)])) == norm_old:
                        candidate = "\n".join(
                            orig_lines[:i] + new_string.splitlines() + orig_lines[i + len(old_lines):]
                        )
                        if not original.endswith("\n") and candidate.endswith("\n"):
                            candidate = candidate[:-1]
                        break
            else:
                # 3. Try without line numbers
                old_no_nums = self._strip_line_numbers(old_string)
                if old_no_nums in original:
                    candidate = original.replace(old_no_nums, new_string, 1)
                else:
                    norm_old_no_nums = _norm(old_no_nums)
                    if norm_old_no_nums in norm_original:
                        orig_lines = original.splitlines()
                        old_lines = old_no_nums.splitlines()
                        for i in range(len(orig_lines) - len(old_lines) + 1):
                            if _norm("\n".join(orig_lines[i:i + len(old_lines)])) == norm_old_no_nums:
                                candidate = "\n".join(
                                    orig_lines[:i] + new_string.splitlines() + orig_lines[i + len(old_lines):]
                                )
                                if not original.endswith("\n") and candidate.endswith("\n"):
                                    candidate = candidate[:-1]
                                break

        if candidate is None:
            self.logger.error("old_string not found in %s — cannot apply diff", target_path)
            self.logger.info("--- PATCH (manual apply) ---")
            self.logger.info("### FIND ###\n%s\n### REPLACE ###\n%s", old_string, new_string)
            self.logger.info("--- END PATCH ---")
            return False
        ok, err = self.validate_syntax(candidate)
        if not ok:
            self.logger.error("Patch failed syntax check: %s", err)
            return False
        if dry_run:
            self.logger.info("[DRY-RUN] Would patch %s", target_path)
            return True
        backup = target_path.with_suffix(".py.bak")
        try:
            target_path.rename(backup)
        except Exception:
            pass
        target_path.write_text(candidate, encoding="utf-8")
        self.logger.info("Patched %s (backup: %s)", target_path, backup)
        return True


# ---------------------------------------------------------------------------
# Proposer
# ---------------------------------------------------------------------------

class MetaHarnessProposer:
    """
    Coding-agent proposer for harness optimisation.

    Workflow:
        1. Read experience store (scores + traces).
        2. Build diagnostic context.
        3. Read current harness source.
        4. Prompt LLM to propose a patch.
        5. Validate & apply patch.
        6. Log the proposal as a new run.
    """

    SYSTEM_PROMPT = """You are a harness-engineering coding agent.
Your job is to inspect execution traces and scores from prior harness runs,
identify failure modes, and propose minimal, safe code patches.

Rules:
- Prefer small, targeted edits over full rewrites.
- Never change model weights or training logic.
- Only modify harness-level code: routing rules, prompt construction,
  retrieval logic, or environment bootstrap.
- When uncertain, propose an additive change rather than deleting logic.
- Output Python code ONLY, inside triple backticks.

PATCH FORMAT (use exactly this format):
```
LINE_START: 42
LINE_END: 44
### REPLACE ###
<the new lines that should replace lines 42-44>
```

How to choose LINE_START and LINE_END:
1. Look at the numbered code below.
2. Pick the first line number you want to change → LINE_START.
3. Pick the last line number you want to change → LINE_END.
4. Write the replacement code under ### REPLACE ###.
5. Keep the replacement as small as possible (3-15 lines ideally).
6. Preserve indentation exactly.
"""

    def __init__(
        self,
        log_dir: Path = Path("meta_harness_logs"),
        llm_cfg: Optional[LLMConfig] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.logger = logger or _setup_logger()
        self.reader = ExperienceReader(log_dir, self.logger)
        self.llm = LLMClient(llm_cfg or LLMConfig(), self.logger)
        self.patcher = PatchEngine(self.logger)

    def propose_patch(self, target_path: Path, top_k: int = 20, dry_run: bool = False) -> bool:
        """
        End-to-end propose-and-apply cycle.

        Returns True if a patch was successfully applied (or validated in dry-run).
        """
        diag = self.reader.build_diagnostic_context(top_k=top_k)
        if "No runs found" in diag:
            self.logger.warning("Experience store is empty — nothing to diagnose.")
            return False

        if not target_path.exists():
            self.logger.error("Target file not found: %s", target_path)
            return False

        current_code = target_path.read_text(encoding="utf-8")

        # Include line numbers so the LLM can copy exact text
        numbered_lines = "\n".join(
            f"{i+1:4d}: {line}" for i, line in enumerate(current_code.splitlines())
        )
        user_prompt = (
            f"Current harness file: {target_path.name}\n\n"
            f"{diag}\n\n"
            "--- CURRENT HARNESS CODE (first 150 lines) ---\n"
            f"{numbered_lines[:4000]}\n\n"
            "--- END CODE ---\n\n"
            "Task: propose a minimal patch that improves the harness based on the failures above. "
            "If the failures are caused by missing keywords in a routing map, add them. "
            "If the failures are caused by poor argument extraction, fix the extraction regex. "
            "If the failures show high latency, suggest a cheaper retrieval or bootstrap strategy. "
            "Return only the patch inside triple backticks using the ### FIND ### / ### REPLACE ### format."
        )

        self.logger.info("Querying LLM for patch proposal...")
        t0 = time.monotonic()
        response = self.llm.chat(self.SYSTEM_PROMPT, user_prompt)
        latency = (time.monotonic() - t0) * 1000
        self.logger.info("LLM responded in %.0f ms (%d chars)", latency, len(response))

        if not response.strip():
            self.logger.warning("Empty LLM response — no patch proposed.")
            return False

        # Extract code from markdown fences
        code_blocks = re.findall(r"```python\n(.*?)```", response, re.DOTALL)
        if not code_blocks:
            code_blocks = re.findall(r"```\n(.*?)```", response, re.DOTALL)

        applied = False
        for block in code_blocks:
            block = block.strip()
            if not block:
                continue
            # Detect LINE_START / LINE_END / REPLACE format (new preferred)
            line_range_match = re.search(
                r"LINE_START:\s*(\d+)\s*\nLINE_END:\s*(\d+)\s*\n###\s*REPLACE\s*###\n(.*)",
                block, re.DOTALL,
            )
            if line_range_match:
                line_start = int(line_range_match.group(1))
                line_end = int(line_range_match.group(2))
                new_str = line_range_match.group(3).rstrip("\n")
                if self.patcher.apply_line_range(target_path, line_start, line_end, new_str, dry_run=dry_run):
                    applied = True
                continue
            # Fallback: FIND/REPLACE format
            find_match = re.search(r"###\s*FIND\s*###\n(.*?)###\s*REPLACE\s*###\n(.*?)(?:\n###|$)", block, re.DOTALL)
            if find_match:
                old_str = find_match.group(1).rstrip("\n")
                new_str = find_match.group(2).rstrip("\n")
                if self.patcher.apply_diff_hunk(target_path, old_str, new_str, dry_run=dry_run):
                    applied = True
                continue
            # Fallback: OLD/NEW format (legacy)
            old_match = re.search(r"###\s*OLD\s*###\n(.*?)###\s*NEW\s*###\n(.*?)(?:\n###|$)", block, re.DOTALL)
            if old_match:
                old_str = old_match.group(1).rstrip("\n")
                new_str = old_match.group(2).rstrip("\n")
                if self.patcher.apply_diff_hunk(target_path, old_str, new_str, dry_run=dry_run):
                    applied = True
                continue
            # Treat as full rewrite only if explicitly requested or very short file
            if len(block) > len(current_code) * 0.8:
                if self.patcher.apply_full_rewrite(target_path, block, dry_run=dry_run):
                    applied = True
            else:
                self.logger.warning("Code block looks like a snippet but no LINE_START/END markers found; skipping.")

        # Log the proposal itself as a run
        self._log_proposal(target_path, response, applied, diag)
        return applied

    def _log_proposal(self, target_path: Path, response: str, applied: bool, diag: str) -> None:
        """Store the proposer's reasoning so future loops can evaluate it."""
        # Re-use MetaHarnessLogger if available
        try:
            from toposwarm_meta_harness import MetaHarnessLogger, MetaHarnessConfig

            mh_cfg = MetaHarnessConfig()
            mh_logger = MetaHarnessLogger(mh_cfg, self.logger)
            harness_snap = {
                "proposer": True,
                "target": str(target_path),
                "applied": applied,
                "model": self.llm.cfg.model,
            }
            trace_steps = [
                {"step": 1, "prompt": "propose_patch", "tool": "llm", "output": response[:500], "ok": applied, "t_ms": 0}
            ]
            score = {
                "prompt": f"Propose patch for {target_path.name}",
                "success": applied,
                "latency_ms": 0,
                "context_chars": len(diag),
                "output_chars": len(response),
            }
            mh_logger.log_run(harness_snap, trace_steps, score, reasoning=response[:2000])
            self.logger.info("Proposer run logged to experience store.")
        except Exception as exc:
            self.logger.debug("Could not log proposal: %s", exc)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Meta-Harness Coding-Agent Proposer")
    parser.add_argument("--diagnose", action="store_true", help="Run diagnosis + propose patch")
    parser.add_argument("--target", type=str, default="toposwarm_lazyown_orchestrator.py", help="File to patch")
    parser.add_argument("--top-k", type=int, default=20, help="Number of runs to inspect")
    parser.add_argument("--dry-run", action="store_true", help="Print patch but do not write")
    parser.add_argument("--apply-patch", type=str, default="", help="Apply a Python patch file directly")
    parser.add_argument("--log-dir", type=str, default="meta_harness_logs")
    parser.add_argument("--model", type=str, default=os.getenv("META_PROPOSER_MODEL", "llama3.1"))
    parser.add_argument("--api-url", type=str, default=os.getenv("META_PROPOSER_API_URL", "http://localhost:11434/v1/chat/completions"))
    parser.add_argument("--api-key", type=str, default=os.getenv("META_PROPOSER_API_KEY", ""))
    args = parser.parse_args()

    logger = _setup_logger()
    target = Path(args.target)
    log_dir = Path(args.log_dir)

    llm_cfg = LLMConfig(
        api_url=args.api_url,
        api_key=args.api_key,
        model=args.model,
    )
    proposer = MetaHarnessProposer(log_dir=log_dir, llm_cfg=llm_cfg, logger=logger)

    if args.apply_patch:
        patch_path = Path(args.apply_patch)
        if not patch_path.exists():
            logger.error("Patch file not found: %s", patch_path)
            sys.exit(1)
        new_code = patch_path.read_text(encoding="utf-8")
        ok = proposer.patcher.apply_full_rewrite(target, new_code, dry_run=args.dry_run)
        sys.exit(0 if ok else 1)

    if args.diagnose:
        ok = proposer.propose_patch(target, top_k=args.top_k, dry_run=args.dry_run)
        sys.exit(0 if ok else 1)

    parser.print_help()


if __name__ == "__main__":
    main()
