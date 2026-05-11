#!/usr/bin/env python3
"""
TopoSwarm Co-Evolution: Simultaneous Weight + Harness Optimisation
=====================================================================
Implements the "natural next step" suggested by Meta-Harness (Lee et al., 2026):
co-evolve the harness *and* the model weights so that the strategy shapes what
the model learns and vice-versa.

Architecture
------------
Outer loop (harness evolution):
    1. Maintain a population of MetaHarnessConfig variants.
    2. Mutate / crossover configs.
    3. Evaluate each variant on a validation prompt suite.

Inner loop (weight evolution):
    4. For promising harnesses, fine-tune TopoSwarm weights for N steps
       using the existing continual trainer (EWC + replay).
    5. Re-evaluate and update Pareto frontier.

Periodic proposer step:
    6. Every K generations, invoke meta_harness_proposer.py to inspect the
       experience store and suggest an intelligent code patch rather than
       a random mutation.

Usage
-----
    # Pure harness evolution (no weight updates, fast)
    python toposwarm_coevolve.py --generations 20 --no-weight-update

    # Full co-evolution (harness + weights)
    python toposwarm_coevolve.py --generations 10 --train-steps 200

    # Resume from checkpoint
    python toposwarm_coevolve.py --resume meta_coevolve_state.json

Author: Gris Iscomeback  —  GPL v3
"""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import logging
import os
import random
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Paths  ( LazyOwn directory discovery )
# ---------------------------------------------------------------------------

_HERE = Path(__file__).parent.resolve()


def _resolve_lazyown_dir() -> Path:
    """
    Discover LazyOwn installation directory.

    Priority:
      1. LAZYOWN_DIR environment variable (expanded ~).
      2. Default relative to this script: <repo>/LazyOwn.
      3. User home directory: ~/LazyOwn.
      4. Return the relative default anyway (caller will see available=False).
    """
    env_dir = os.environ.get("LAZYOWN_DIR", "")
    if env_dir:
        p = Path(env_dir).expanduser().resolve()
        if p.exists():
            return p
    rel = (_HERE.parent.parent / "LazyOwn").resolve()
    if rel.exists():
        return rel
    home = (Path.home() / "LazyOwn").resolve()
    if home.exists():
        return home
    return rel

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def _setup_logger(name: str = "TopoSwarmCoEvo", level: str = "INFO") -> logging.Logger:
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
# Validation prompt suite (LazyOwn pentest scenarios)
# ---------------------------------------------------------------------------

_DEFAULT_VALIDATION_PROMPTS: List[str] = [
    "Scan for open ports on 10.10.11.78",
    "Run a full nmap scan on 192.168.1.100",
    "Set the target host to 10.10.11.50",
    "Show all active sessions",
    "Analyze vulnerabilities found on 10.10.11.78",
    "Search for SMB exploitation techniques",
    "Generate a campaign situation report",
    "Show collected credentials",
    "Check C2 server status",
    "List all available LazyOwn modules",
    "What should be the next step after initial access?",
    "Auto-populate the configuration from target scan",
    "Run an AI agent to plan the attack on 10.10.11.78",
    "Poll for new security events",
    "Add 10.10.11.78 as a target in the campaign",
]

# ---------------------------------------------------------------------------
# Harness mutation operators
# ---------------------------------------------------------------------------

class HarnessMutation:
    """Simple mutation operators over MetaHarnessConfig dicts."""

    @staticmethod
    def mutate(cfg_dict: Dict[str, Any]) -> Dict[str, Any]:
        child = copy.deepcopy(cfg_dict)
        # Boolean toggles (low probability)
        if random.random() < 0.15:
            child["BOOTSTRAP_ENABLED"] = not child.get("BOOTSTRAP_ENABLED", True)
        if random.random() < 0.15:
            child["DRAFT_VERIFY_ENABLED"] = not child.get("DRAFT_VERIFY_ENABLED", True)
        # Continuous params (Gaussian noise, clipped)
        if random.random() < 0.3:
            child["DRAFT_VERIFY_THRESHOLD"] = _clip(
                child.get("DRAFT_VERIFY_THRESHOLD", 0.6) + random.gauss(0, 0.08),
                0.1, 0.95,
            )
        if random.random() < 0.3:
            child["BOOTSTRAP_TIMEOUT"] = _clip(
                child.get("BOOTSTRAP_TIMEOUT", 5.0) + random.gauss(0, 1.0),
                1.0, 30.0,
            )
        if random.random() < 0.3:
            child["RETRIEVAL_TOP_K"] = int(
                _clip(
                    child.get("RETRIEVAL_TOP_K", 5) + random.randint(-2, 2),
                    1, 20,
                )
            )
        if random.random() < 0.3:
            child["BOOTSTRAP_MAX_FILES"] = int(
                _clip(
                    child.get("BOOTSTRAP_MAX_FILES", 30) + random.randint(-5, 5),
                    5, 100,
                )
            )
        return child

    @staticmethod
    def crossover(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
        child = copy.deepcopy(a)
        for key in ["BOOTSTRAP_ENABLED", "DRAFT_VERIFY_ENABLED", "DRAFT_VERIFY_THRESHOLD",
                    "BOOTSTRAP_TIMEOUT", "RETRIEVAL_TOP_K", "BOOTSTRAP_MAX_FILES"]:
            child[key] = random.choice([a.get(key), b.get(key)])
        return child


def _clip(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


# ---------------------------------------------------------------------------
# Mock bridge for evaluation when LazyOwn is not installed
# ---------------------------------------------------------------------------

class MockLazyOwnBridge:
    """
    Deterministic mock of LazyOwnBridge for isolated harness evaluation.
    Returns canned responses so the orchestrator can be exercised even when
    LazyOwn is not present.
    """

    def __init__(self) -> None:
        self.lazyown_dir = Path("/mock/lazyown")
        self._available = True
        self._call_count = 0

    @property
    def available(self) -> bool:
        return True

    def run(self, command: str, timeout: Optional[int] = None) -> str:
        self._call_count += 1
        cmd = command.strip().lower()
        if "nmap" in cmd or "lazynmap" in cmd:
            return f"Mock nmap output for: {command}\nPORT STATE SERVICE\n22/tcp open ssh\n80/tcp open http"
        if "targets" in cmd:
            return "10.10.11.78\n192.168.1.100"
        if "sessions" in cmd:
            return "session_001\nsession_002"
        if "beacons" in cmd:
            return "beacon_alpha\nbeacon_beta"
        if "list" in cmd:
            return "recon\nscan\nenum\nlinux-exploit-suggester\nlazynmap"
        if "sitrep" in cmd:
            return "Campaign SITREP: 2 targets, 1 session, 0 critical alerts."
        if "creds" in cmd:
            return "admin:password123\nroot:toor"
        if "status" in cmd:
            return "C2 server: RUNNING\nListeners: 2"
        if "vuln" in cmd:
            return "CVE-2021-44228 (Log4Shell) detected on port 8080."
        return f"Mock output for command: {command}"

    def get_config(self) -> Dict[str, Any]:
        return {"rhost": "10.10.11.78", "lhost": "10.10.14.2", "lport": 4444}

    def set_config(self, key: str, value: str) -> str:
        return f"Set {key}={value} in payload.json"


# ---------------------------------------------------------------------------
# Evaluation harness
# ---------------------------------------------------------------------------

class HarnessEvaluator:
    """
    Evaluates a harness configuration by running the LazyOwn orchestrator
    on a suite of validation prompts and aggregating scores.

    Uses in-process evaluation (no subprocess) so:
    - Meta-Harness logs are written to the same filesystem store.
    - Import errors are visible immediately.
    - Latencies are realistic.
    """

    def __init__(
        self,
        prompts: List[str],
        lazyown_dir: Path,
        logger: logging.Logger,
        use_mock_bridge: bool = False,
    ) -> None:
        self.prompts = prompts
        self.lazyown_dir = lazyown_dir
        self.logger = logger
        self.use_mock_bridge = use_mock_bridge

    def evaluate(self, cfg_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run each prompt through the orchestrator and collect metrics.

        Also logs every evaluation to the Meta-Harness experience store so the
        proposer has data to diagnose.
        """
        successes = 0
        latencies: List[float] = []
        context_chars: List[int] = []
        output_chars: List[int] = []
        errors: List[str] = []

        # Build the orchestrator once per cfg evaluation
        orch = self._build_orchestrator(cfg_dict)

        for prompt in self.prompts:
            t0 = time.monotonic()
            try:
                result = orch.run(prompt)
                latency = (time.monotonic() - t0) * 1000
                latencies.append(latency)

                ok = result.tool_result.ok if result.tool_result else False
                out_len = len(result.final_answer)
                ctx_len = len(prompt) + len(result.tool_arg or "")

                context_chars.append(ctx_len)
                output_chars.append(out_len)
                if ok:
                    successes += 1
                else:
                    err = getattr(result.tool_result, "output", "unknown") if result.tool_result else "no tool result"
                    errors.append(f"{prompt}: {err[:100]}")

                # Log this run to the Meta-Harness experience store
                self._log_run(orch, prompt, result, latency, ctx_len, ok, cfg_dict)

            except Exception as exc:
                latency = (time.monotonic() - t0) * 1000
                errors.append(f"{prompt}: {exc}")
                latencies.append(latency)
                context_chars.append(0)
                output_chars.append(0)
                self.logger.debug("Evaluation exception for '%s': %s", prompt, exc, exc_info=True)

        n = len(self.prompts)
        metrics: Dict[str, Any] = {
            "success_rate": successes / n if n else 0.0,
            "latency_ms_avg": sum(latencies) / n if n else 0.0,
            "latency_ms_p95": sorted(latencies)[int(n * 0.95)] if n else 0.0,
            "context_chars_avg": sum(context_chars) / n if n else 0.0,
            "output_chars_avg": sum(output_chars) / n if n else 0.0,
            "errors": errors[:5],
        }
        return metrics

    def _build_orchestrator(self, cfg_dict: Dict[str, Any]) -> Any:
        """Build a LazyOwnOrchestrator with the given MetaHarnessConfig."""
        try:
            # Late imports to avoid circular deps and allow reloading
            from toposwarm_lazyown_orchestrator import LazyOwnOrchestrator, LazyOwnBridge, _setup_logger
            from toposwarm_infer import InferenceConfig
            from topo_swarm_agent import SwarmConfig
            from toposwarm_meta_harness import MetaHarnessConfig

            mh_cfg = MetaHarnessConfig(**cfg_dict)
            eval_logger = _setup_logger("WARNING")

            if self.use_mock_bridge:
                bridge: Any = MockLazyOwnBridge()
            else:
                bridge = LazyOwnBridge(self.lazyown_dir)
                if not bridge.available:
                    self.logger.debug("LazyOwn not found at %s — using mock bridge", self.lazyown_dir)
                    bridge = MockLazyOwnBridge()

            agent_cfg = SwarmConfig()
            inf_cfg = InferenceConfig()
            return LazyOwnOrchestrator(
                inf_cfg, agent_cfg, bridge, eval_logger,
                load_model=False, meta_cfg=mh_cfg,
            )
        except Exception as exc:
            self.logger.error("Failed to build orchestrator: %s", exc, exc_info=True)
            raise

    def _log_run(
        self,
        orch: Any,
        prompt: str,
        result: Any,
        latency_ms: float,
        ctx_len: int,
        ok: bool,
        cfg_dict: Dict[str, Any],
    ) -> None:
        """Write one evaluation to the Meta-Harness experience store."""
        try:
            mh = getattr(orch, "_mh", None)
            if mh is None:
                return
            harness_cfg = {
                "coevolve_cfg": cfg_dict,
                "tool_name": getattr(result, "tool_name", ""),
                "bootstrap_len": len(getattr(orch, "_snapshot_text", "")),
                "model_loaded": False,
            }
            trace_steps = [
                {
                    "step": 1,
                    "prompt": prompt,
                    "tool": getattr(result, "tool_name", ""),
                    "arg": getattr(result, "tool_arg", ""),
                    "output": (getattr(result.tool_result, "output", "")[:500] if result.tool_result else ""),
                    "ok": ok,
                    "t_ms": latency_ms,
                }
            ]
            score = {
                "prompt": prompt,
                "success": ok,
                "latency_ms": latency_ms,
                "context_chars": ctx_len,
                "output_chars": len(getattr(result, "final_answer", "")),
            }
            mh.log_run(harness_cfg, trace_steps, score)
        except Exception as exc:
            self.logger.debug("Failed to log run: %s", exc)


# ---------------------------------------------------------------------------
# Weight trainer wrapper
# ---------------------------------------------------------------------------

class WeightTrainer:
    """
    Thin wrapper around toposwarm_continual_trainer.py for inner-loop
    weight updates.
    """

    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger
        self._trainer = None
        self._load()

    def _load(self) -> None:
        for candidate in [_HERE / "toposwarm_continual_trainer.py",
                          Path.cwd() / "toposwarm_continual_trainer.py"]:
            if candidate.exists():
                spec = importlib.util.spec_from_file_location("toposwarm_continual_trainer", candidate)
                mod = importlib.util.module_from_spec(spec)
                sys.modules["toposwarm_continual_trainer"] = mod
                spec.loader.exec_module(mod)
                self._trainer = mod
                self.logger.info("Loaded continual trainer: %s", candidate)
                return
        self.logger.warning("toposwarm_continual_trainer.py not found — weight updates disabled.")

    def is_available(self) -> bool:
        return self._trainer is not None

    def fine_tune(self, dataset_path: Path, steps: int, learning_rate: float = 2e-5) -> Dict[str, Any]:
        """Run a short fine-tuning burst and return metrics."""
        if not self.is_available():
            return {"trained": False, "reason": "trainer unavailable"}
        try:
            cl_cfg = self._trainer.ContinualConfig(
                LAZYOWN_DATASET=str(dataset_path),
                EPOCHS=1,
                LEARNING_RATE=learning_rate,
                BATCH_SIZE=4,
                GRAD_ACCUM_STEPS=4,
                LOG_INTERVAL=9999,   # silent
                EVAL_INTERVAL=9999,
                EWC_LAMBDA=10.0,
                REPLAY_RATIO=0.20,
            )
            # Some continual trainers expose a run_for_steps method;
            # if not, we run the full pipeline and ignore early stopping.
            if hasattr(self._trainer, "run_for_steps"):
                metrics = self._trainer.run_for_steps(cl_cfg, steps)
            else:
                self._trainer.run_full_pipeline(cl_cfg, self.logger)
                metrics = {"loss": 0.0}  # placeholder
            return {"trained": True, "metrics": metrics}
        except Exception as exc:
            self.logger.error("Weight training failed: %s", exc)
            return {"trained": False, "reason": str(exc)}


# ---------------------------------------------------------------------------
# Co-evolution engine
# ---------------------------------------------------------------------------

class CoEvolutionEngine:
    """
    Outer-loop harness evolution with optional inner-loop weight co-evolution.
    """

    def __init__(
        self,
        generations: int = 20,
        population_size: int = 6,
        train_steps_per_gen: int = 0,
        proposer_interval: int = 5,
        lazyown_dir: Path = _resolve_lazyown_dir(),
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.generations = generations
        self.population_size = population_size
        self.train_steps_per_gen = train_steps_per_gen
        self.proposer_interval = proposer_interval
        self.lazyown_dir = lazyown_dir
        self.logger = logger or _setup_logger()
        self.evaluator = HarnessEvaluator(_DEFAULT_VALIDATION_PROMPTS, lazyown_dir, self.logger)
        self.weight_trainer = WeightTrainer(self.logger)
        self.state_path = Path("meta_coevolve_state.json")

        # Seed population
        from toposwarm_meta_harness import MetaHarnessConfig
        self.base_config = asdict(MetaHarnessConfig())
        self.population: List[Dict[str, Any]] = [copy.deepcopy(self.base_config) for _ in range(population_size)]
        for i, p in enumerate(self.population):
            if i > 0:
                self.population[i] = HarnessMutation.mutate(p)

        self.frontier: List[Tuple[Dict[str, Any], Dict[str, Any]]] = []
        self.history: List[Dict[str, Any]] = []

    # -----------------------------------------------------------------------
    # Main loop
    # -----------------------------------------------------------------------

    def run(self) -> None:
        # Detect whether we are running against a real LazyOwn or mock
        from toposwarm_lazyown_orchestrator import LazyOwnBridge
        real_bridge = LazyOwnBridge(self.lazyown_dir)
        mode = "REAL" if real_bridge.available else "MOCK"
        self.logger.info(
            "Starting co-evolution: gens=%d pop=%d weight_steps=%d mode=%s",
            self.generations, self.population_size, self.train_steps_per_gen, mode,
        )
        for gen in range(1, self.generations + 1):
            self.logger.info("=== Generation %d / %d ===", gen, self.generations)

            # Evaluate every member of the population
            scores: List[Tuple[Dict[str, Any], Dict[str, Any]]] = []
            for idx, cfg in enumerate(self.population):
                metrics = self.evaluator.evaluate(cfg)
                scores.append((cfg, metrics))
                self.logger.info(
                    "  Candidate %d: success=%.2f latency=%.0fms ctx=%.0f errs=%d",
                    idx,
                    metrics["success_rate"],
                    metrics["latency_ms_avg"],
                    metrics["context_chars_avg"],
                    len(metrics["errors"]),
                )
                self.history.append({"gen": gen, "idx": idx, "cfg": cfg, "metrics": metrics})

            # Update frontier
            for cfg, metrics in scores:
                if self._is_on_frontier(cfg, metrics):
                    self.frontier.append((cfg, metrics))
                    self.logger.info("  -> Added to Pareto frontier")

            # Optional weight co-evolution for the best candidate
            if self.train_steps_per_gen > 0 and self.weight_trainer.is_available():
                best_cfg, best_metrics = max(scores, key=lambda x: x[1]["success_rate"])
                self.logger.info("  Fine-tuning weights on best harness (success=%.2f)",
                                 best_metrics["success_rate"])
                dataset = Path("data_toolbench/lazyown_full.jsonl")
                if dataset.exists():
                    wresult = self.weight_trainer.fine_tune(dataset, self.train_steps_per_gen)
                    self.logger.info("  Weight result: %s", wresult)
                else:
                    self.logger.warning("  Dataset not found, skipping weight update.")

            # Proposer step every K generations
            if gen % self.proposer_interval == 0:
                self._run_proposer()

            # Build next generation: elitism + crossover + mutation
            self.population = self._next_generation(scores)
            self._save_state(gen)

        self.logger.info("Co-evolution finished. Frontier size: %d", len(self.frontier))
        self._report_frontier()

    # -----------------------------------------------------------------------
    # Generation mechanics
    # -----------------------------------------------------------------------

    def _next_generation(
        self, scores: List[Tuple[Dict[str, Any], Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        # Sort by success_rate descending
        sorted_scores = sorted(scores, key=lambda x: x[1]["success_rate"], reverse=True)
        elites = [copy.deepcopy(cfg) for cfg, _ in sorted_scores[:2]]
        next_pop: List[Dict[str, Any]] = elites

        while len(next_pop) < self.population_size:
            parent_a = self._tournament_select(sorted_scores)
            parent_b = self._tournament_select(sorted_scores)
            child = HarnessMutation.crossover(parent_a, parent_b)
            child = HarnessMutation.mutate(child)
            next_pop.append(child)
        return next_pop

    @staticmethod
    def _tournament_select(
        sorted_scores: List[Tuple[Dict[str, Any], Dict[str, Any]]],
        k: int = 3,
    ) -> Dict[str, Any]:
        contestants = random.sample(sorted_scores, min(k, len(sorted_scores)))
        best = max(contestants, key=lambda x: x[1]["success_rate"])
        return copy.deepcopy(best[0])

    def _is_on_frontier(self, cfg: Dict[str, Any], metrics: Dict[str, Any]) -> bool:
        # Simple 2-objective frontier: maximise success_rate, minimise latency
        for other_cfg, other_m in self.frontier:
            if other_cfg is cfg:
                continue
            better_or_equal = (
                other_m["success_rate"] >= metrics["success_rate"]
                and other_m["latency_ms_avg"] <= metrics["latency_ms_avg"]
            )
            strictly_better = (
                other_m["success_rate"] > metrics["success_rate"]
                or other_m["latency_ms_avg"] < metrics["latency_ms_avg"]
            )
            if better_or_equal and strictly_better:
                return False
        return True

    # -----------------------------------------------------------------------
    # Proposer invocation
    # -----------------------------------------------------------------------

    def _run_proposer(self) -> None:
        proposer_path = _HERE / "meta_harness_proposer.py"
        if not proposer_path.exists():
            self.logger.debug("Proposer script not found, skipping.")
            return
        self.logger.info("Invoking coding-agent proposer...")
        try:
            proc = subprocess.run(
                [sys.executable, str(proposer_path), "--diagnose", "--dry-run"],
                capture_output=True,
                text=True,
                timeout=300,
            )
            self.logger.info("Proposer stdout (first 500 chars): %s", proc.stdout[:500])
            if proc.returncode != 0:
                self.logger.warning("Proposer stderr: %s", proc.stderr[:500])
        except Exception as exc:
            self.logger.warning("Proposer invocation failed: %s", exc)

    # -----------------------------------------------------------------------
    # Persistence
    # -----------------------------------------------------------------------

    def _save_state(self, generation: int) -> None:
        state = {
            "generation": generation,
            "population": self.population,
            "frontier": [(c, m) for c, m in self.frontier],
            "history": self.history[-100:],  # keep last 100 records
        }
        self.state_path.write_text(json.dumps(state, indent=2, default=str), encoding="utf-8")

    def load_state(self, path: Path) -> None:
        data = json.loads(path.read_text(encoding="utf-8"))
        self.population = data.get("population", self.population)
        self.frontier = data.get("frontier", [])
        self.history = data.get("history", [])
        self.logger.info("Resumed from generation %d", data.get("generation", 0))

    def _report_frontier(self) -> None:
        print("\n=== PARETO FRONTIER ===")
        for i, (cfg, m) in enumerate(self.frontier):
            print(f"\n[{i}] success={m['success_rate']:.2f} latency={m['latency_ms_avg']:.0f}ms ctx={m['context_chars_avg']:.0f}")
            print(f"    config: {json.dumps(cfg, indent=2)}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="TopoSwarm Co-Evolution Engine")
    parser.add_argument("--generations", type=int, default=20)
    parser.add_argument("--population", type=int, default=6)
    parser.add_argument("--train-steps", type=int, default=0, help="Inner-loop weight steps per generation (0 = disabled)")
    parser.add_argument("--proposer-interval", type=int, default=5)
    parser.add_argument("--lazyown-dir", type=str, default="")
    parser.add_argument("--resume", type=str, default="", help="Path to meta_coevolve_state.json")
    parser.add_argument("--no-weight-update", action="store_true", help="Skip inner-loop weight training")
    parser.add_argument("--log-level", type=str, default="INFO")
    args = parser.parse_args()

    logger = _setup_logger(level=args.log_level)
    lazyown_dir = Path(args.lazyown_dir).expanduser().resolve() if args.lazyown_dir else _resolve_lazyown_dir()

    engine = CoEvolutionEngine(
        generations=args.generations,
        population_size=args.population,
        train_steps_per_gen=0 if args.no_weight_update else args.train_steps,
        proposer_interval=args.proposer_interval,
        lazyown_dir=lazyown_dir,
        logger=logger,
    )

    if args.resume:
        engine.load_state(Path(args.resume))

    engine.run()


if __name__ == "__main__":
    main()
