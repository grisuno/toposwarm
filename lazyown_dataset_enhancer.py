#!/usr/bin/env python3
"""
LazyOwn Dataset Enhancer — Enrich training data with real execution traces
=============================================================================
Reads the Meta-Harness experience store (`meta_harness_logs/`) and generates
high-quality, curriculum-sorted training examples that reflect real LazyOwn
inputs/outputs, error patterns, and multi-turn contexts.

Why this helps
--------------
- The synthetic dataset uses `[TOOL_CALL: tool(arg)] [placeholder]` answers.
  The model never sees real LazyOwn output during training, so at inference
  it hallucinates or collapses.
- The experience store contains *actual* executions: real prompts, real tool
  outputs (including LazyOwn's noisy "Environment Activated" logs), and real
  success/failure signals.
- By mining these traces, we create training examples whose `answer` field
  contains real observed output, teaching the model what to expect.

Pipeline
--------
1. Read all runs from `meta_harness_logs/`.
2. Extract (instruction, tool, arg, output) tuples from traces.
3. Generate **error-recovery** examples: when a run failed, create a
   counterfactual with the correct tool.
4. Generate **multi-turn** examples: chain 2-3 real prompts into a single
   context window.
5. Sort by curriculum: simple (1 tool, short output) → complex.
6. Write enriched JSONL ready for `toposwarm_continual_trainer.py`.

Usage
-----
    # Enhance from experience store (default)
    python lazyown_dataset_enhancer.py

    # Specify custom paths
    python lazyown_dataset_enhancer.py --log-dir meta_harness_logs --out data_toolbench/lazyown_enriched.jsonl

    # Combine with existing synthetic dataset
    python lazyown_dataset_enhancer.py --merge-with data_toolbench/lazyown_full.jsonl

    # Stats only
    python lazyown_dataset_enhancer.py --stats

Author: Gris Iscomeback  —  GPL v3
"""

from __future__ import annotations

import argparse
import json
import random
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

random.seed(42)


# ---------------------------------------------------------------------------
# Curriculum difficulty scorer
# ---------------------------------------------------------------------------

def _difficulty(record: Dict[str, Any]) -> float:
    """
    Lower = easier.  Factors:
      - prompt length (shorter = easier)
      - number of words (fewer = easier)
      - output length (shorter = easier)
      - has error markers (harder)
    """
    prompt = record.get("instruction", "")
    answer = record.get("answer", "")
    score = 0.0
    score += len(prompt) * 0.01
    score += len(answer) * 0.005
    score += len(prompt.split()) * 0.1
    if "error" in answer.lower() or "fail" in answer.lower():
        score += 5.0
    return score


# ---------------------------------------------------------------------------
# Experience store reader
# ---------------------------------------------------------------------------

class ExperienceStoreReader:
    def __init__(self, log_dir: Path) -> None:
        self.log_dir = log_dir

    def list_runs(self) -> List[Path]:
        return sorted(
            (p for p in self.log_dir.iterdir() if p.is_dir() and p.name.startswith("run_")),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )

    def read_trace(self, run_dir: Path) -> List[Dict[str, Any]]:
        tp = run_dir / "trace.jsonl"
        if not tp.exists():
            return []
        traces = []
        with tp.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        traces.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
        return traces

    def read_score(self, run_dir: Path) -> Optional[Dict[str, Any]]:
        sp = run_dir / "score.json"
        if not sp.exists():
            return None
        try:
            return json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            return None

    def read_harness(self, run_dir: Path) -> Optional[Dict[str, Any]]:
        hp = run_dir / "harness.json"
        if not hp.exists():
            return None
        try:
            return json.loads(hp.read_text(encoding="utf-8"))
        except Exception:
            return None


# ---------------------------------------------------------------------------
# Record builders
# ---------------------------------------------------------------------------

def _sanitize_output(text: str) -> str:
    """Redact potential PII / sensitive data from LazyOwn output traces."""
    # IP addresses (IPv4)
    text = re.sub(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", "[REDACTED_IP]", text)
    # Passwords / hashes / keys
    text = re.sub(r"(?i)(password|passwd|pwd|hash|secret|key|token)\s*[=:]\s*\S+", r"\1=[REDACTED]", text)
    # NTLM hashes (32 hex chars)
    text = re.sub(r"\b[a-fA-F0-9]{32}\b", "[REDACTED_HASH]", text)
    # Email addresses
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[REDACTED_EMAIL]", text)
    return text


def _build_toolbench_record(instruction: str, tool_name: str, arg: str, answer: str, domain: str = "Security/Real") -> Dict[str, Any]:
    """Standard ToolBench-format record."""
    return {
        "instruction": instruction,
        "api_list": [{
            "tool_name": tool_name,
            "api_name": f"{tool_name}_endpoint",
            "api_description": tool_name.replace("lazyown_", "").replace("_", " "),
            "required_parameters": [{"name": "arg", "type": "STRING"}],
            "optional_parameters": [],
        }],
        "answer": f"[TOOL_CALL: {tool_name}({arg})] {answer}",
        "domain": domain,
    }


class DatasetEnhancer:
    def __init__(self, log_dir: Path, max_runs: int = 500) -> None:
        self.log_dir = log_dir
        self.reader = ExperienceStoreReader(log_dir)
        self.max_runs = max_runs

    def enhance(self) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []
        runs = self.reader.list_runs()[:self.max_runs]

        for run_dir in runs:
            traces = self.reader.read_trace(run_dir)
            score = self.reader.read_score(run_dir)
            harness = self.reader.read_harness(run_dir)

            if not traces:
                continue

            # Build records from each trace step
            for step in traces:
                prompt = step.get("prompt", "")
                tool = step.get("tool", "")
                arg = step.get("arg", "")
                output = step.get("output", "")
                ok = step.get("ok", False)

                if not prompt or not tool:
                    continue

                # 1. Real execution record
                domain = "Security/RealSuccess" if ok else "Security/RealFailure"
                safe_output = _sanitize_output(output)
                records.append(_build_toolbench_record(prompt, tool, arg, safe_output, domain))

                # 2. If failed and we have harness info with the "right" tool, create error-recovery
                if not ok and harness:
                    correct_tool = harness.get("tool_name", tool)
                    if correct_tool != tool:
                        recovery_prompt = f"CORRECT: {prompt}"
                        records.append(_build_toolbench_record(
                            recovery_prompt, correct_tool, arg,
                            f"[Recovered from {tool} failure] {safe_output}",
                            "Security/ErrorRecovery"
                        ))

                # 3. Create a "clean prompt" variant by stripping the snapshot if present
                clean_prompt = re.sub(r"\[Environment Snapshot\].*?\n\n", "", prompt, flags=re.DOTALL).strip()
                if clean_prompt and clean_prompt != prompt:
                    records.append(_build_toolbench_record(clean_prompt, tool, arg, safe_output, domain))

            # 4. Multi-turn: chain consecutive traces from the same run
            if len(traces) >= 2:
                for i in range(len(traces) - 1):
                    t1, t2 = traces[i], traces[i + 1]
                    safe_out1 = _sanitize_output(t1.get("output", "")[:200])
                    safe_out2 = _sanitize_output(t2.get("output", ""))
                    multi_prompt = (
                        f"{t1.get('prompt', '')}\n"
                        f"[Result: {safe_out1}]\n"
                        f"Now: {t2.get('prompt', '')}"
                    )
                    records.append(_build_toolbench_record(
                        multi_prompt,
                        t2.get("tool", ""),
                        t2.get("arg", ""),
                        safe_out2,
                        "Security/MultiTurn"
                    ))

        return records

    def add_negative_examples(self, records: List[Dict[str, Any]], n: int = 50) -> List[Dict[str, Any]]:
        """
        Add examples where the prompt is ambiguous and the model must NOT
        pick a random tool, or where the user asks something outside LazyOwn's scope.
        """
        negatives = [
            ("What is the weather in Paris?", "search_web", "weather Paris"),
            ("Calculate 17 * 89 + 42", "calc_expr", "17 * 89 + 42"),
            ("Translate 'hello' to Spanish", "translate", "hello to spanish"),
            ("What time is it now?", "get_datetime", "UTC"),
            ("Who is the president of France?", "search_web", "president of France"),
            ("How do I bake a cake?", "search_web", "how to bake a cake"),
            ("Write a poem about cybersecurity", "search_web", "cybersecurity poem"),
            ("Explain quantum computing", "search_web", "quantum computing explanation"),
            ("What is the capital of Japan?", "search_web", "capital of Japan"),
            ("Play me some music", "search_web", "play music"),
        ]
        for instruction, tool, arg in negatives:
            records.append(_build_toolbench_record(
                instruction, tool, arg,
                "This query is outside the pentesting scope; routed to general search.",
                "Security/OutOfScope"
            ))
        return records

    def curriculum_sort(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort by difficulty (easy → hard)."""
        return sorted(records, key=_difficulty)

    def deduplicate(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate by instruction text only (same prompt can have different outputs)."""
        seen: set = set()
        out: List[Dict[str, Any]] = []
        for r in records:
            key = r.get("instruction", "").strip()
            if key not in seen:
                seen.add(key)
                out.append(r)
        return out

    def augment_simple(self, records: List[Dict[str, Any]], multiplier: int = 2) -> List[Dict[str, Any]]:
        """
        Lightweight augmentation: replace IP addresses, hostnames, and common
        keywords with variants to increase diversity without an LLM.
        """
        augmented = []
        ip_variants = ["10.10.11.78", "192.168.1.100", "172.16.0.5", "10.10.10.5", "10.10.11.200"]
        for rec in records:
            augmented.append(rec)
            for _ in range(multiplier - 1):
                inst = rec["instruction"]
                ans = rec["answer"]
                # Replace IP addresses with random variants
                for old_ip in ["10.10.11.78", "192.168.1.100", "172.16.0.5", "10.10.10.5", "10.10.11.200"]:
                    if old_ip in inst or old_ip in ans:
                        new_ip = random.choice(ip_variants)
                        inst = inst.replace(old_ip, new_ip)
                        ans = ans.replace(old_ip, new_ip)
                if inst != rec["instruction"]:
                    new_rec = dict(rec)
                    new_rec["instruction"] = inst
                    new_rec["answer"] = ans
                    augmented.append(new_rec)
        return augmented

    def run(self, merge_with: Optional[Path] = None) -> List[Dict[str, Any]]:
        print(f"[enhancer] Reading experience store: {self.log_dir}")
        records = self.enhance()
        print(f"[enhancer] Raw mined records: {len(records)}")

        records = self.deduplicate(records)
        print(f"[enhancer] After dedup: {len(records)}")

        records = self.add_negative_examples(records)
        print(f"[enhancer] After negatives: {len(records)}")

        records = self.augment_simple(records, multiplier=3)
        print(f"[enhancer] After augmentation: {len(records)}")

        # Auto-merge with synthetic dataset if available and not explicitly disabled
        synthetic_path = merge_with
        if synthetic_path is None:
            default_synth = Path("data_toolbench/lazyown_full.jsonl")
            if default_synth.exists():
                synthetic_path = default_synth

        if synthetic_path and synthetic_path.exists():
            synthetic = []
            with synthetic_path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            synthetic.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass
            print(f"[enhancer] Merging {len(synthetic)} synthetic records from {synthetic_path}")
            # Deduplicate synthetic against real records
            real_instructions = {r.get("instruction", "").strip() for r in records}
            unique_synthetic = [s for s in synthetic if s.get("instruction", "").strip() not in real_instructions]
            print(f"[enhancer] {len(unique_synthetic)} synthetic records are unique")
            records = records + unique_synthetic

        records = self.curriculum_sort(records)
        print(f"[enhancer] Final curriculum-sorted records: {len(records)}")
        return records


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------

def print_stats(records: List[Dict[str, Any]]) -> None:
    domains: Dict[str, int] = {}
    tools: Dict[str, int] = {}
    total_inst = 0
    total_ans = 0
    for r in records:
        domains[r.get("domain", "Unknown")] = domains.get(r.get("domain", "Unknown"), 0) + 1
        api = r.get("api_list", [{}])[0]
        tools[api.get("tool_name", "?")] = tools.get(api.get("tool_name", "?"), 0) + 1
        total_inst += len(r.get("instruction", ""))
        total_ans += len(r.get("answer", ""))
    n = len(records)
    print(f"\n=== Dataset Stats ({n} records) ===")
    print(f"Avg instruction length: {total_inst / n:.0f} chars")
    print(f"Avg answer length: {total_ans / n:.0f} chars")
    print(f"\nTop domains:")
    for d, c in sorted(domains.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {d}: {c}")
    print(f"\nTop tools:")
    for t, c in sorted(tools.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {t}: {c}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="LazyOwn Dataset Enhancer")
    parser.add_argument("--log-dir", type=str, default="meta_harness_logs", help="Meta-Harness experience store")
    parser.add_argument("--out", type=str, default="data_toolbench/lazyown_enriched.jsonl", help="Output JSONL")
    parser.add_argument("--merge-with", type=str, default="", help="Merge with existing synthetic dataset")
    parser.add_argument("--max-runs", type=int, default=500, help="Max runs to read from store")
    parser.add_argument("--stats", action="store_true", help="Print stats and exit")
    args = parser.parse_args()

    log_dir = Path(args.log_dir)
    out_path = Path(args.out)
    merge_path = Path(args.merge_with) if args.merge_with else None

    enhancer = DatasetEnhancer(log_dir, max_runs=args.max_runs)
    records = enhancer.run(merge_with=merge_path)

    if args.stats:
        print_stats(records)
        return

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"[enhancer] Wrote {len(records)} records → {out_path}")
    print_stats(records)


if __name__ == "__main__":
    main()
