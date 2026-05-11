#!/usr/bin/env python3
"""
TopoSwarm Meta-Harness: End-to-End Optimization of LazyOwn Orchestrator Harnesses
===================================================================================
Inspired by "Meta-Harness: End-to-End Optimization of Model Harnesses"
(Lee et al., Stanford/MIT, 2026).

This module upgrades TopoSwarm's LazyOwn orchestrator with three core
Meta-Harness ideas:

1.  **Filesystem Experience Store** — every tool execution is logged as a
    first-class artifact (code snapshot + execution trace + score) so future
    proposers (human or coding-agent) can grep/cat the raw history instead of
    relying on lossy summaries.

2.  **Environment Bootstrap** — before the first LLM / router turn we gather a
    sandbox snapshot (LazyOwn config, targets, sessions, beacons, modules) and
    inject it into the prompt.  This eliminates 2-4 wasted exploratory turns on
    dependency-heavy pentest tasks (exactly the pattern Meta-Harness discovered
    on TerminalBench-2).

3.  **Draft-Verification Routing** — for ambiguous prompts we run a lightweight
    draft router, then retrieve confirmers/challengers from the experience store
    to verify or revise the draft before executing the tool.

The module is self-contained, has zero heavy dependencies beyond the Python
standard library + numpy, and is designed to be imported by
`toposwarm_lazyown_orchestrator.py`.

Author: Gris Iscomeback  —  GPL v3
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import os
import re
import sys
import time
from collections import deque
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

try:
    import numpy as np
except ImportError:
    np = None  # type: ignore


# ===========================================================================
# CONFIGURATION
# ===========================================================================


@dataclass
class MetaHarnessConfig:
    """All Meta-Harness hyper-parameters in one place."""

    # --- Filesystem experience store ----------------------------------------
    LOG_DIR: str = "meta_harness_logs"
    MAX_LOGGED_RUNS: int = 500
    COMPRESS_OLD_TRACES: bool = False  # gzip traces older than N runs

    # --- Environment bootstrap ----------------------------------------------
    BOOTSTRAP_ENABLED: bool = True
    BOOTSTRAP_MAX_FILES: int = 30      # max files listed in /app or sessions
    BOOTSTRAP_TIMEOUT: float = 5.0     # seconds to wait for LazyOwn status

    # --- Draft-verification routing -----------------------------------------
    DRAFT_VERIFY_ENABLED: bool = True
    DRAFT_VERIFY_THRESHOLD: float = 0.6   # confidence below → trigger verify
    RETRIEVAL_TOP_K: int = 5              # prior episodes to retrieve

    # --- Pareto frontier ----------------------------------------------------
    FRONTIER_MAX_SIZE: int = 20
    FRONTIER_METRICS: Tuple[str, ...] = ("success_rate", "latency_ms", "context_chars")

    # --- Episodic memory ----------------------------------------------------
    MEMORY_CAPACITY: int = 2000
    MEMORY_HALFLIFE: int = 100

    # --- Logging ------------------------------------------------------------
    LOG_LEVEL: str = "INFO"


# ===========================================================================
# UTILITIES
# ===========================================================================


def _setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    if not logger.handlers:
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(logging.Formatter(
            "%(asctime)s %(name)-24s %(levelname)-8s %(message)s"
        ))
        logger.addHandler(h)
    return logger


def _stable_id(text: str) -> str:
    """Short stable hash for naming log directories."""
    return hashlib.sha256(text.encode()).hexdigest()[:12]


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


# ===========================================================================
# META-HARNESS LOGGER  (filesystem experience store)
# ===========================================================================


class MetaHarnessLogger:
    """
    Append-only filesystem store for harness code, execution traces, and scores.

    Each evaluated harness run gets its own directory:

        meta_harness_logs/
          run_0001_<hash>/
            harness.json   – config / code snapshot
            trace.jsonl    – step-by-step execution trace
            score.json     – metrics (success, latency, token count, ...)
            reasoning.txt  – optional proposer reasoning

    The store is intentionally plain-text / JSON so a coding-agent proposer can
    navigate it with standard tools (`grep`, `cat`, `ls`) without bespoke APIs.
    """

    def __init__(self, cfg: MetaHarnessConfig, logger: Optional[logging.Logger] = None) -> None:
        self.cfg = cfg
        self.log_dir = Path(cfg.LOG_DIR)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logger or _setup_logger("MetaHarnessLogger", cfg.LOG_LEVEL)
        self._run_counter = self._count_existing_runs()

    # -----------------------------------------------------------------------
    # Internal helpers
    # -----------------------------------------------------------------------

    def _count_existing_runs(self) -> int:
        return sum(1 for p in self.log_dir.iterdir() if p.is_dir() and p.name.startswith("run_"))

    def _next_run_dir(self, hint: str = "") -> Path:
        self._run_counter += 1
        suffix = _stable_id(hint or str(time.time()))
        name = f"run_{self._run_counter:04d}_{suffix}"
        return self.log_dir / name

    def _prune_old(self) -> None:
        """Keep only the most recent MAX_LOGGED_RUNS directories."""
        dirs = sorted(
            (p for p in self.log_dir.iterdir() if p.is_dir()),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        for old in dirs[self.cfg.MAX_LOGGED_RUNS :]:
            try:
                import shutil
                shutil.rmtree(old)
            except Exception:
                pass

    # -----------------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------------

    def log_run(
        self,
        harness_snapshot: Dict[str, Any],
        trace_steps: List[Dict[str, Any]],
        score: Dict[str, Any],
        reasoning: str = "",
    ) -> Path:
        """
        Persist one complete harness evaluation.

        Args:
            harness_snapshot: JSON-serialisable dict describing the harness
                config / code (e.g. {"orchestrator_version": "2.1", ...}).
            trace_steps: List of step dicts, each with keys like
                { "step": int, "prompt": str, "tool": str, "output": str, "t_ms": float }.
            score: Dict of metrics, e.g.
                { "success": true, "latency_ms": 120, "context_chars": 450 }.
            reasoning: Optional free-text proposer reasoning.

        Returns:
            Path to the newly created run directory.
        """
        run_dir = self._next_run_dir(hint=score.get("prompt", ""))
        run_dir.mkdir(parents=True, exist_ok=True)

        # harness snapshot
        (run_dir / "harness.json").write_text(
            json.dumps(harness_snapshot, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # trace
        with (run_dir / "trace.jsonl").open("w", encoding="utf-8") as f:
            for step in trace_steps:
                f.write(json.dumps(step, ensure_ascii=False) + "\n")

        # score
        score_out = {"timestamp": _now_iso(), **score}
        (run_dir / "score.json").write_text(
            json.dumps(score_out, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # reasoning
        if reasoning:
            (run_dir / "reasoning.txt").write_text(reasoning, encoding="utf-8")

        self.logger.info("Logged Meta-Harness run → %s", run_dir.name)
        self._prune_old()
        return run_dir

    # -----------------------------------------------------------------------
    # Query API  (coding-agent friendly)
    # -----------------------------------------------------------------------

    def list_runs(self, n: Optional[int] = None) -> List[Path]:
        """Return run directories newest-first."""
        dirs = sorted(
            (p for p in self.log_dir.iterdir() if p.is_dir() and p.name.startswith("run_")),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        return dirs[:n] if n else dirs

    def grep_traces(self, pattern: str, max_results: int = 20) -> List[Tuple[Path, int, str]]:
        """
        Simple regex search across all trace.jsonl files.
        Returns list of (run_dir, line_no, matched_line).
        """
        rx = re.compile(pattern, re.IGNORECASE)
        hits: List[Tuple[Path, int, str]] = []
        for run_dir in self.list_runs():
            trace_path = run_dir / "trace.jsonl"
            if not trace_path.exists():
                continue
            with trace_path.open("r", encoding="utf-8") as f:
                for lineno, line in enumerate(f, 1):
                    if rx.search(line):
                        hits.append((run_dir, lineno, line.rstrip()))
                        if len(hits) >= max_results:
                            return hits
        return hits

    def get_scores(self) -> List[Dict[str, Any]]:
        """Load every score.json into a list."""
        scores = []
        for run_dir in self.list_runs():
            sp = run_dir / "score.json"
            if sp.exists():
                try:
                    scores.append(json.loads(sp.read_text(encoding="utf-8")))
                except Exception:
                    pass
        return scores

    def get_pareto_runs(self, metrics: Optional[Tuple[str, ...]] = None) -> List[Path]:
        """
        Return run directories that are on the Pareto frontier.

        By default maximises success_rate and minimises latency_ms + context_chars.
        """
        metrics = metrics or self.cfg.FRONTIER_METRICS
        entries: List[Tuple[Path, Dict[str, Any]]] = []
        for run_dir in self.list_runs():
            sp = run_dir / "score.json"
            if not sp.exists():
                continue
            try:
                sc = json.loads(sp.read_text(encoding="utf-8"))
                if all(m in sc for m in metrics):
                    entries.append((run_dir, sc))
            except Exception:
                pass

        if not entries:
            return []

        # maximise: success_rate; minimise: latency_ms, context_chars
        maximise = {"success_rate"}
        pareto: List[Tuple[Path, Dict[str, Any]]] = []
        for rd, sc in entries:
            dominated = False
            for _, other in entries:
                if other is sc:
                    continue
                better_or_equal = True
                strictly_better = False
                for m in metrics:
                    direction = 1 if m in maximise else -1
                    diff = direction * (other[m] - sc[m])
                    if diff < 0:
                        better_or_equal = False
                        break
                    if diff > 0:
                        strictly_better = True
                if better_or_equal and strictly_better:
                    dominated = True
                    break
            if not dominated:
                pareto.append((rd, sc))
        return [rd for rd, _ in pareto]


# ===========================================================================
# DENSE MEMORY RETRIEVER  (semantic + lexical fallback)
# ===========================================================================


class DenseMemoryRetriever:
    """
    Semantic episodic retrieval with graceful degradation.

    Priority:
        1. sentence-transformers dense embeddings (best quality).
        2. sklearn TF-IDF + cosine similarity (no GPU, good quality).
        3. Return None so caller falls back to Jaccard token overlap.

    The retriever is rebuildable incrementally: call `add()` for each new
    episode, then `search()` for retrieval.
    """

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or _setup_logger("DenseRetriever")
        self._mode: str = "none"
        self._docs: List[str] = []
        self._episodes: List[Dict[str, Any]] = []

        # Try sentence-transformers
        try:
            from sentence_transformers import SentenceTransformer  # type: ignore
            self._encoder = SentenceTransformer("all-MiniLM-L6-v2")
            self._mode = "sentence_transformers"
            self.logger.info("Dense retriever: sentence-transformers (all-MiniLM-L6-v2)")
        except Exception:
            # Try sklearn TF-IDF
            try:
                from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
                from sklearn.metrics.pairwise import cosine_similarity  # type: ignore
                self._vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
                self._mode = "sklearn_tfidf"
                self.logger.info("Dense retriever: sklearn TF-IDF")
            except Exception:
                self.logger.warning("Dense retriever: no backend available (fall back to Jaccard)")

    # -----------------------------------------------------------------------
    # Indexing
    # -----------------------------------------------------------------------

    def add(self, text: str, episode: Dict[str, Any]) -> None:
        self._docs.append(text)
        self._episodes.append(episode)
        if self._mode == "sklearn_tfidf" and len(self._docs) >= 2:
            self._rebuild_tfidf()

    def _rebuild_tfidf(self) -> None:
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
            self._vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
            self._tfidf_matrix = self._vectorizer.fit_transform(self._docs)
        except Exception as exc:
            self.logger.debug("TF-IDF rebuild failed: %s", exc)

    def bulk_index(self, texts: List[str], episodes: List[Dict[str, Any]]) -> None:
        self._docs = texts
        self._episodes = episodes
        if self._mode == "sentence_transformers":
            try:
                self._embeddings = self._encoder.encode(self._docs, convert_to_numpy=True, show_progress_bar=False)
            except Exception as exc:
                self.logger.warning("Embedding failed: %s", exc)
                self._mode = "none"
        elif self._mode == "sklearn_tfidf":
            self._rebuild_tfidf()

    # -----------------------------------------------------------------------
    # Search
    # -----------------------------------------------------------------------

    def search(self, query: str, top_k: int = 5) -> List[Tuple[float, Dict[str, Any]]]:
        if not self._docs:
            return []
        if self._mode == "sentence_transformers":
            return self._search_st(query, top_k)
        if self._mode == "sklearn_tfidf":
            return self._search_tfidf(query, top_k)
        return []

    def _search_st(self, query: str, top_k: int) -> List[Tuple[float, Dict[str, Any]]]:
        try:
            import numpy as np
            q_emb = self._encoder.encode([query], convert_to_numpy=True)
            sims = cosine_similarity(q_emb, self._embeddings)[0]
            idxs = np.argsort(sims)[::-1][:top_k]
            return [(float(sims[i]), self._episodes[i]) for i in idxs]
        except Exception as exc:
            self.logger.debug("ST search failed: %s", exc)
            return []

    def _search_tfidf(self, query: str, top_k: int) -> List[Tuple[float, Dict[str, Any]]]:
        try:
            from sklearn.metrics.pairwise import cosine_similarity  # type: ignore
            import numpy as np
            q_vec = self._vectorizer.transform([query])
            sims = cosine_similarity(q_vec, self._tfidf_matrix)[0]
            idxs = np.argsort(sims)[::-1][:top_k]
            return [(float(sims[i]), self._episodes[i]) for i in idxs]
        except Exception as exc:
            self.logger.debug("TF-IDF search failed: %s", exc)
            return []


# ===========================================================================
# META-HARNESS MEMORY  (external, queryable episodic memory)
# ===========================================================================


class MetaHarnessMemory:
    """
    Persistent episodic memory backed by the filesystem log store.

    Unlike the in-RAM EpisodicMemory in topo_swarm_agent.py, this memory:
    - Survives process restarts.
    - Can be queried by keyword overlap, tool name, or simple TF-IDF cosine.
    - Returns raw execution traces (not compressed summaries) so a proposer can
      perform causal diagnosis.
    """

    def __init__(self, logger: MetaHarnessLogger, capacity: int = 2000, dense: Optional[DenseMemoryRetriever] = None) -> None:
        self.logger = logger
        self.capacity = capacity
        # In-RAM index of recent episodes for fast retrieval
        self._index: deque = deque(maxlen=capacity)
        self._dense = dense
        self._build_index()

    # -----------------------------------------------------------------------
    # Index management
    # -----------------------------------------------------------------------

    def _build_index(self) -> None:
        episodes = []
        for run_dir in self.logger.list_runs(n=self.capacity):
            ep = self._load_episode(run_dir)
            if ep:
                self._index.append(ep)
                episodes.append(ep)
        if self._dense is not None and episodes:
            texts = [ep["text"] for ep in episodes]
            self._dense.bulk_index(texts, episodes)

    def _load_episode(self, run_dir: Path) -> Optional[Dict[str, Any]]:
        sp = run_dir / "score.json"
        tp = run_dir / "trace.jsonl"
        if not sp.exists() or not tp.exists():
            return None
        try:
            score = json.loads(sp.read_text(encoding="utf-8"))
            traces = [json.loads(line) for line in tp.read_text(encoding="utf-8").splitlines() if line.strip()]
            return {
                "run_id": run_dir.name,
                "score": score,
                "traces": traces,
                "text": self._episode_text(score, traces),
            }
        except Exception:
            return None

    @staticmethod
    def _episode_text(score: Dict[str, Any], traces: List[Dict[str, Any]]) -> str:
        parts = [score.get("prompt", "")]
        for t in traces:
            parts.append(t.get("tool", ""))
            parts.append(t.get("output", "")[:200])
        return " ".join(parts).lower()

    # -----------------------------------------------------------------------
    # Retrieval
    # -----------------------------------------------------------------------

    def store(self, score: Dict[str, Any], traces: List[Dict[str, Any]]) -> None:
        """Index a newly logged episode."""
        ep = {
            "run_id": score.get("run_id", _stable_id(str(time.time()))),
            "score": score,
            "traces": traces,
            "text": self._episode_text(score, traces),
        }
        self._index.append(ep)
        if self._dense is not None:
            self._dense.add(ep["text"], ep)

    def retrieve_similar(
        self,
        prompt: str,
        tool_hint: Optional[str] = None,
        top_k: int = 5,
        min_score: float = 0.0,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve the top-k most similar prior episodes.

        Uses dense semantic retrieval when available (sentence-transformers or
        sklearn TF-IDF), then falls back to token-overlap Jaccard for anything
        not covered by the dense index.  Results are fused by max-of-scores.
        """
        # --- Dense retrieval -------------------------------------------------
        dense_scores: Dict[str, Tuple[float, Dict[str, Any]]] = {}
        if self._dense is not None:
            for sim, ep in self._dense.search(prompt, top_k=top_k * 3):
                dense_scores[ep["run_id"]] = (sim, ep)

        # --- Lexical (Jaccard) fallback --------------------------------------
        query_tokens = set(self._tokenise(prompt))
        if tool_hint:
            query_tokens.add(tool_hint.lower())

        for ep in self._index:
            rid = ep["run_id"]
            ep_tokens = set(self._tokenise(ep["text"]))
            inter = len(query_tokens & ep_tokens)
            union = len(query_tokens | ep_tokens)
            jaccard = inter / union if union else 0.0
            if tool_hint and tool_hint.lower() in ep["text"]:
                jaccard += 0.1
            # Fuse: keep max score
            if rid in dense_scores:
                old_sim, _ = dense_scores[rid]
                dense_scores[rid] = (max(old_sim, jaccard), ep)
            else:
                dense_scores[rid] = (jaccard, ep)

        scored = [(s, ep) for s, ep in dense_scores.values() if s >= min_score]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [ep for _, ep in scored[:top_k]]

    def retrieve_confirmers_and_challengers(
        self,
        draft_tool: str,
        prompt: str,
        top_k: int = 5,
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Split retrieved episodes into confirmers (same tool, success) and
        challengers (different tool or failure).
        """
        similar = self.retrieve_similar(prompt, tool_hint=draft_tool, top_k=top_k * 3)
        confirmers = []
        challengers = []
        for ep in similar:
            traces = ep.get("traces", [])
            tool_used = traces[0].get("tool", "") if traces else ""
            success = ep.get("score", {}).get("success", False)
            if tool_used == draft_tool and success:
                confirmers.append(ep)
            else:
                challengers.append(ep)
        return confirmers[:top_k], challengers[:top_k]

    @staticmethod
    def _tokenise(text: str) -> List[str]:
        """Very simple whitespace + punctuation tokeniser."""
        return re.findall(r"[a-z0-9_]+", text.lower())


# ===========================================================================
# ENVIRONMENT BOOTSTRAPPER  (TerminalBench-2 style)
# ===========================================================================


class EnvironmentBootstrapper:
    """
    Gathers a sandbox snapshot *before* the first router/tool turn and formats
    it as a compact [Environment Snapshot] block.

    This eliminates the 2-4 exploratory turns that the LazyOwn agent typically
    spends discovering what targets, sessions, and modules are available.
    """

    def __init__(self, cfg: MetaHarnessConfig, logger: Optional[logging.Logger] = None) -> None:
        self.cfg = cfg
        self.logger = logger or _setup_logger("EnvBootstrap", cfg.LOG_LEVEL)

    def gather_snapshot(self, bridge: Any) -> Dict[str, Any]:
        """
        Collect environment state via the LazyOwnBridge.

        Returns a dict with keys:
            working_dir, lazyown_dir, config, targets, sessions,
            modules_available, beacons, languages, memory_estimate.
        """
        snapshot: Dict[str, Any] = {
            "timestamp": _now_iso(),
            "working_dir": str(getattr(bridge, "lazyown_dir", "")),
            "lazyown_dir": str(getattr(bridge, "lazyown_dir", "")),
        }

        # Config
        try:
            snapshot["config"] = bridge.get_config()
        except Exception as exc:
            snapshot["config"] = {"error": str(exc)}

        # Targets (if bridge exposes a targets command)
        try:
            targets_raw = bridge.run("targets", timeout=self.cfg.BOOTSTRAP_TIMEOUT)
            snapshot["targets"] = self._parse_list(targets_raw)
        except Exception as exc:
            snapshot["targets"] = [f"error: {exc}"]

        # Sessions
        try:
            sessions_raw = bridge.run("sessions", timeout=self.cfg.BOOTSTRAP_TIMEOUT)
            snapshot["sessions"] = self._parse_list(sessions_raw)
        except Exception as exc:
            snapshot["sessions"] = [f"error: {exc}"]

        # Beacons
        try:
            beacons_raw = bridge.run("beacons", timeout=self.cfg.BOOTSTRAP_TIMEOUT)
            snapshot["beacons"] = self._parse_list(beacons_raw)
        except Exception as exc:
            snapshot["beacons"] = [f"error: {exc}"]

        # Modules list (truncated)
        try:
            modules_raw = bridge.run("list", timeout=self.cfg.BOOTSTRAP_TIMEOUT)
            modules = self._parse_list(modules_raw)
            snapshot["modules_available"] = modules[: self.cfg.BOOTSTRAP_MAX_FILES]
            snapshot["modules_total"] = len(modules)
        except Exception as exc:
            snapshot["modules_available"] = [f"error: {exc}"]
            snapshot["modules_total"] = 0

        # Quick system info (best effort)
        try:
            import subprocess, shutil
            langs = []
            for cmd, name in [
                ("python3 --version", "python"),
                ("gcc --version", "gcc"),
                ("node --version", "node"),
                ("java -version", "java"),
                ("rustc --version", "rust"),
                ("go version", "go"),
            ]:
                if shutil.which(cmd.split()[0]):
                    try:
                        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True, timeout=2)
                        langs.append(f"{name}: {out.splitlines()[0].strip()}")
                    except Exception:
                        langs.append(f"{name}: present")
            snapshot["languages"] = langs
        except Exception:
            snapshot["languages"] = []

        # Memory estimate
        try:
            import psutil
            mem = psutil.virtual_memory()
            snapshot["memory_mb"] = mem.available // (1024 * 1024)
        except Exception:
            snapshot["memory_mb"] = -1

        return snapshot

    @staticmethod
    def _parse_list(raw: str) -> List[str]:
        """Best-effort parse of newline / comma list output."""
        if not raw:
            return []
        lines = [ln.strip() for ln in raw.replace(",", "\n").splitlines() if ln.strip()]
        return lines

    def format_snapshot(self, snapshot: Dict[str, Any], max_chars: int = 1500) -> str:
        """
        Render the snapshot as a compact [Environment Snapshot] block suitable
        for injection into a prompt.
        """
        lines = ["[Environment Snapshot]"]

        cfg = snapshot.get("config", {})
        if cfg and "error" not in cfg:
            lines.append("Config:")
            for k, v in list(cfg.items())[:8]:
                lines.append(f"  {k} = {v}")

        targets = snapshot.get("targets", [])
        if targets and not any(t.startswith("error") for t in targets):
            lines.append(f"Targets ({len(targets)}): {', '.join(targets[:5])}")

        sessions = snapshot.get("sessions", [])
        if sessions and not any(s.startswith("error") for s in sessions):
            lines.append(f"Sessions ({len(sessions)}): {', '.join(sessions[:5])}")

        beacons = snapshot.get("beacons", [])
        if beacons and not any(b.startswith("error") for b in beacons):
            lines.append(f"Beacons ({len(beacons)}): {', '.join(beacons[:5])}")

        mods = snapshot.get("modules_available", [])
        total = snapshot.get("modules_total", len(mods))
        if mods and not any(m.startswith("error") for m in mods):
            lines.append(f"Modules ({total} total, {len(mods)} shown):")
            for m in mods[:10]:
                lines.append(f"  - {m}")

        langs = snapshot.get("languages", [])
        if langs:
            lines.append("Languages: " + ", ".join(langs[:5]))

        mem = snapshot.get("memory_mb", -1)
        if mem > 0:
            lines.append(f"Available memory: ~{mem} MB")

        text = "\n".join(lines)
        if len(text) > max_chars:
            text = text[:max_chars] + "\n... (truncated)"
        return text


# ===========================================================================
# DRAFT-VERIFICATION ROUTER
# ===========================================================================


class DraftVerifier:
    """
    Two-stage routing inspired by Meta-Harness's text-classification harness.

    Stage 1 (Draft):  Produce an initial tool proposal using fast keyword
                      heuristics (same as the existing infer_lazyown_tool).

    Stage 2 (Verify): Retrieve confirmers (same tool, past successes) and
                      challengers (different tool / failures) from the
                      MetaHarnessMemory, then decide whether to keep or revise
                      the draft.

    This is lightweight — no LLM call — but gives the harness a structured
    way to learn from prior executions without retraining model weights.
    """

    def __init__(
        self,
        cfg: MetaHarnessConfig,
        memory: MetaHarnessMemory,
        keyword_router: Callable[[str], Tuple[str, str]],
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.cfg = cfg
        self.memory = memory
        self.keyword_router = keyword_router
        self.logger = logger or _setup_logger("DraftVerifier", cfg.LOG_LEVEL)

    def route(self, prompt: str, snapshot_text: str = "") -> Tuple[str, str, float]:
        """
        Draft-verify routing.

        Returns:
            Tuple of (tool_name, tool_arg, confidence).
        """
        # --- Stage 1: Draft --------------------------------------------------
        draft_tool, draft_arg = self.keyword_router(prompt)
        confidence = 0.8  # baseline confidence for keyword routing

        if not self.cfg.DRAFT_VERIFY_ENABLED:
            return draft_tool, draft_arg, confidence

        # --- Stage 2: Verification -------------------------------------------
        confirmers, challengers = self.memory.retrieve_confirmers_and_challengers(
            draft_tool, prompt, top_k=self.cfg.RETRIEVAL_TOP_K
        )

        # If we have strong confirmers and no strong challengers, boost confidence
        conf_success = sum(1 for c in confirmers if c.get("score", {}).get("success", False))
        chall_failures = sum(1 for c in challengers if not c.get("score", {}).get("success", False))

        if confirmers and not challengers:
            confidence = min(0.99, confidence + 0.15)
        elif challengers and not confirmers:
            confidence = max(0.2, confidence - 0.25)
            # Try to find the most common successful tool among challengers
            tool_votes: Dict[str, int] = {}
            for ch in challengers:
                tr = ch.get("traces", [])
                tname = tr[0].get("tool", "") if tr else ""
                if tname:
                    tool_votes[tname] = tool_votes.get(tname, 0) + 1
            if tool_votes:
                best_alt = max(tool_votes, key=tool_votes.get)
                if best_alt != draft_tool:
                    self.logger.info(
                        "DraftVerifier: revised %s → %s (challenger evidence)",
                        draft_tool, best_alt,
                    )
                    draft_tool = best_alt
                    # Keep original arg unless the alternative implies a different extraction
                    draft_arg = self._reextract_arg(prompt, draft_tool, draft_arg)
        else:
            # Mixed evidence — neutral confidence
            confidence = 0.6 + 0.1 * (conf_success - chall_failures)
            confidence = max(0.3, min(0.9, confidence))

        # Snapshot is kept in prompt context; never inject into tool_arg
        # (injecting it breaks command parsing and bloats arguments)
        return draft_tool, draft_arg, confidence

    @staticmethod
    def _reextract_arg(prompt: str, tool_name: str, fallback: str) -> str:
        """Best-effort arg re-extraction when the tool changes."""
        # For most tools the full prompt is a safe fallback
        if tool_name in {
            "lazyown_c2_search_agent",
            "lazyown_llm_ask",
            "lazyown_recommend_next",
        }:
            return prompt
        return fallback


# ===========================================================================
# PARETO FRONTIER  (multi-objective harness selection)
# ===========================================================================


class ParetoFrontier:
    """
    Maintain a population of harness configurations and their evaluation scores.

    The frontier is updated after every evaluation so the orchestrator can
    dynamically switch to the best harness variant for the current task context
    (accuracy vs. latency vs. context-cost trade-offs).
    """

    def __init__(
        self,
        cfg: MetaHarnessConfig,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.cfg = cfg
        self.logger = logger or _setup_logger("ParetoFrontier", cfg.LOG_LEVEL)
        self._population: List[Dict[str, Any]] = []  # { "config": dict, "metrics": dict }

    def add(self, config: Dict[str, Any], metrics: Dict[str, Any]) -> bool:
        """
        Add a candidate to the population and return True if it lies on the
        current Pareto frontier.
        """
        entry = {"config": config, "metrics": metrics, "timestamp": _now_iso()}
        self._population.append(entry)
        if len(self._population) > self.cfg.FRONTIER_MAX_SIZE * 2:
            self._prune()

        on_frontier = self._is_on_frontier(entry)
        if on_frontier:
            self.logger.info(
                "Pareto frontier: new candidate (success=%.2f, latency=%.0fms, ctx=%d)",
                metrics.get("success_rate", 0.0),
                metrics.get("latency_ms", 0.0),
                metrics.get("context_chars", 0),
            )
        return on_frontier

    def select_best(
        self,
        preference: Optional[Dict[str, float]] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Select the best harness config according to a scalarised preference.

        preference maps metric name → weight (positive = maximise, negative = minimise).
        Default: maximise success_rate, minimise latency_ms and context_chars.
        """
        if not self._population:
            return None
        preference = preference or {
            "success_rate": 1.0,
            "latency_ms": -0.001,
            "context_chars": -0.0001,
        }
        best_entry = None
        best_score = float("-inf")
        for entry in self._population:
            sc = 0.0
            for m, w in preference.items():
                v = entry["metrics"].get(m, 0.0)
                # Normalise crudely by the max seen so far to keep weights interpretable
                vals = [e["metrics"].get(m, 1.0) for e in self._population if m in e["metrics"]]
                norm = max(vals) if vals else 1.0
                sc += w * (v / norm)
            if sc > best_score:
                best_score = sc
                best_entry = entry
        return best_entry["config"] if best_entry else None

    def frontier_configs(self) -> List[Dict[str, Any]]:
        """Return all configs currently on the Pareto frontier."""
        return [e["config"] for e in self._population if self._is_on_frontier(e)]

    def _is_on_frontier(self, candidate: Dict[str, Any]) -> bool:
        metrics = self.cfg.FRONTIER_METRICS
        cand_m = candidate["metrics"]
        for other in self._population:
            if other is candidate:
                continue
            other_m = other["metrics"]
            better_or_equal = True
            strictly_better = False
            for m in metrics:
                maximise = m in {"success_rate"}
                direction = 1 if maximise else -1
                diff = direction * (other_m.get(m, 0.0) - cand_m.get(m, 0.0))
                if diff < 0:
                    better_or_equal = False
                    break
                if diff > 0:
                    strictly_better = True
            if better_or_equal and strictly_better:
                return False
        return True

    def _prune(self) -> None:
        """Remove oldest non-frontier entries when population grows too large."""
        frontier_ids = {id(e) for e in self._population if self._is_on_frontier(e)}
        kept = []
        for entry in self._population:
            if id(entry) in frontier_ids or len(kept) < self.cfg.FRONTIER_MAX_SIZE:
                kept.append(entry)
        self._population = kept


# ===========================================================================
# META-HARNESS OPTIMIZER  (orchestrates the full Meta-Harness loop)
# ===========================================================================


class MetaHarnessOptimizer:
    """
    Single entry-point that wires together Logger, Memory, Bootstrapper,
    DraftVerifier, and ParetoFrontier.

    Usage inside LazyOwnOrchestrator:

        mh = MetaHarnessOptimizer(MetaHarnessConfig())
        snapshot = mh.bootstrap.gather_snapshot(bridge)
        snapshot_text = mh.bootstrap.format_snapshot(snapshot)
        tool, arg, conf = mh.draft_verifier.route(prompt, snapshot_text)
        ... execute tool ...
        mh.log_run(harness_cfg, trace_steps, score)
        mh.memory.store(score, trace_steps)
        mh.frontier.add(harness_cfg, score)
    """

    def __init__(self, cfg: Optional[MetaHarnessConfig] = None) -> None:
        self.cfg = cfg or MetaHarnessConfig()
        self.logger = _setup_logger("MetaHarness", self.cfg.LOG_LEVEL)
        self.fs_logger = MetaHarnessLogger(self.cfg, self.logger)
        self.dense_retriever = DenseMemoryRetriever(self.logger)
        self.memory = MetaHarnessMemory(
            self.fs_logger,
            capacity=self.cfg.MEMORY_CAPACITY,
            dense=self.dense_retriever,
        )
        self.bootstrap = EnvironmentBootstrapper(self.cfg, self.logger)
        self.frontier = ParetoFrontier(self.cfg, self.logger)
        # draft_verifier is injected later because it needs the keyword_router
        self.draft_verifier: Optional[DraftVerifier] = None

    def set_router(self, keyword_router: Callable[[str], Tuple[str, str]]) -> None:
        """Bind the draft verifier to the existing keyword router."""
        self.draft_verifier = DraftVerifier(
            self.cfg, self.memory, keyword_router, self.logger
        )

    def log_run(
        self,
        harness_snapshot: Dict[str, Any],
        trace_steps: List[Dict[str, Any]],
        score: Dict[str, Any],
        reasoning: str = "",
    ) -> Path:
        """Persist one run and update in-memory indexes."""
        run_dir = self.fs_logger.log_run(harness_snapshot, trace_steps, score, reasoning)
        self.memory.store(score, trace_steps)
        self.frontier.add(harness_snapshot, score)
        return run_dir

    def get_best_harness_config(self) -> Optional[Dict[str, Any]]:
        """Return the current Pareto-best harness configuration."""
        return self.frontier.select_best()

    def query_experience(self, prompt: str, tool_hint: str = "", top_k: int = 5) -> List[Dict[str, Any]]:
        """Ad-hoc retrieval of prior episodes for prompt engineering."""
        return self.memory.retrieve_similar(prompt, tool_hint=tool_hint, top_k=top_k)


# ===========================================================================
# CLI sanity check
# ===========================================================================


def _demo() -> None:
    print("Meta-Harness module loaded OK.")
    cfg = MetaHarnessConfig()
    mh = MetaHarnessOptimizer(cfg)
    print("Log dir:", mh.fs_logger.log_dir)
    print("Runs so far:", len(mh.fs_logger.list_runs()))


if __name__ == "__main__":
    _demo()
