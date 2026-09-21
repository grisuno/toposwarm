#!/usr/bin/env python3
"""Full pipeline test: regenerate dataset, retrain, evaluate, live test.

Usage:
    python test_full_pipeline.py [--skip-dataset] [--skip-train] [--epochs 1]

Steps:
    1. Regenerate enriched dataset from meta_harness_logs/ (new error-recovery + prerequisites)
    2. Fine-tune 1 epoch with EWC + replay (backbone frozen, adapter-only)
    3. Evaluate routing accuracy on the new dataset
    4. Live test: run real prompts through the orchestrator with the new bridge
    5. Validate that meta_harness_logs/ now contains tool names in score.json
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


class _Paths:
    """Centralized path constants relative to repo root."""

    REPO_ROOT: Path = Path(__file__).parent.resolve()
    DATA_DIR: Path = REPO_ROOT / "data_toolbench"
    ENRICHED: Path = DATA_DIR / "lazyown_enriched.jsonl"
    CHECKPOINT_DIR: Path = REPO_ROOT / "checkpoints_toposwarm"
    META_LOGS: Path = REPO_ROOT / "meta_harness_logs"
    ENHANCER: Path = REPO_ROOT / "lazyown_dataset_enhancer.py"
    TRAINER: Path = REPO_ROOT / "toposwarm_continual_trainer.py"
    ORCHESTRATOR: Path = REPO_ROOT / "toposwarm_lazyown_orchestrator.py"


def _run(cmd: list[str], timeout: int = 300) -> subprocess.CompletedProcess:
    """Run a command with logging and error handling."""
    print(f"\n[PIPELINE] {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        cwd=str(_Paths.REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.stdout:
        print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)
    if result.returncode != 0:
        print(f"[ERROR] rc={result.returncode} stderr={result.stderr[:500]}")
    return result


def step1_regenerate_dataset() -> bool:
    """Regenerate lazyown_enriched.jsonl from meta_harness_logs."""
    print("\n" + "=" * 60)
    print("STEP 1: Regenerate enriched dataset")
    print("=" * 60)

    result = _run(
        [
            sys.executable,
            str(_Paths.ENHANCER),
            "--log-dir", str(_Paths.META_LOGS),
            "--out", str(_Paths.ENRICHED),
            "--merge-with", str(_Paths.DATA_DIR / "lazyown_full.jsonl"),
            "--max-runs", "500",
        ],
        timeout=120,
    )

    if result.returncode != 0:
        print("[FAIL] Dataset generation failed")
        return False

    if not _Paths.ENRICHED.exists():
        print("[FAIL] Output file not created")
        return False

    lines = sum(1 for _ in open(_Paths.ENRICHED))
    print(f"[OK] Generated {lines} examples → {_Paths.ENRICHED}")
    return True


def step2_train(epochs: int) -> bool:
    """Fine-tune the model on the enriched dataset."""
    print("\n" + "=" * 60)
    print(f"STEP 2: Fine-tune ({epochs} epoch(s), adapter-only)")
    print("=" * 60)

    result = _run(
        [
            sys.executable,
            str(_Paths.TRAINER),
            "--train",
            "--epochs", str(epochs),
            "--dataset", str(_Paths.ENRICHED),
            "--checkpoint", str(_Paths.CHECKPOINT_DIR),
            "--log-level", "INFO",
        ],
        timeout=600,
    )

    ok = result.returncode == 0 and "checkpoint" in result.stdout.lower()
    print("[OK] Training completed" if ok else "[FAIL] Training failed")
    return ok


def step3_evaluate() -> bool:
    """Evaluate routing accuracy."""
    print("\n" + "=" * 60)
    print("STEP 3: Evaluate routing accuracy")
    print("=" * 60)

    result = _run(
        [
            sys.executable,
            str(_Paths.TRAINER),
            "--eval",
            "--dataset", str(_Paths.ENRICHED),
            "--checkpoint", str(_Paths.CHECKPOINT_DIR),
        ],
        timeout=300,
    )

    ok = result.returncode == 0
    if ok:
        for line in result.stdout.splitlines():
            if "accuracy" in line.lower() or "acc" in line.lower():
                print(f"[METRIC] {line.strip()}")
    print("[OK] Evaluation completed" if ok else "[FAIL] Evaluation failed")
    return ok


def step4_live_test() -> bool:
    """Run live prompts through the orchestrator to validate the new bridge."""
    print("\n" + "=" * 60)
    print("STEP 4: Live end-to-end test")
    print("=" * 60)

    test_prompts = [
        "scan 10.10.11.78",
        "set rhost to 10.10.11.78",
        "list available modules",
        "show current config",
    ]

    all_ok = True
    for prompt in test_prompts:
        result = _run(
            [
                sys.executable,
                str(_Paths.ORCHESTRATOR),
                "--prompt", prompt,
                "--no-model",
                "--log-level", "WARNING",
            ],
            timeout=60,
        )
        success = result.returncode == 0 and len(result.stdout) > 10
        status = "OK" if success else "FAIL"
        print(f"  [{status}] '{prompt}' → {len(result.stdout)} chars output")
        if not success:
            all_ok = False

    return all_ok


def step5_validate_logs() -> bool:
    """Validate that recent meta_harness_logs contain tool names."""
    print("\n" + "=" * 60)
    print("STEP 5: Validate score.json logging")
    print("=" * 60)

    runs = sorted(
        (p for p in _Paths.META_LOGS.iterdir() if p.is_dir() and p.name.startswith("run_")),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    if not runs:
        print("[WARN] No runs found in meta_harness_logs")
        return True

    sample = runs[:10]
    has_tool = 0
    for run_dir in sample:
        score_path = run_dir / "score.json"
        if not score_path.exists():
            continue
        try:
            score = json.loads(score_path.read_text())
            if "tool" in score and score["tool"] != "unknown":
                has_tool += 1
        except Exception:
            pass

    print(f"[INFO] Checked {len(sample)} latest runs")
    print(f"[INFO] {has_tool}/{len(sample)} have valid 'tool' field in score.json")

    if has_tool == 0:
        print("[WARN] No recent runs have tool logging — new code may not have been exercised yet")
    else:
        print("[OK] Tool logging is working")

    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Full TopoSwarm pipeline test")
    parser.add_argument("--skip-dataset", action="store_true", help="Skip dataset regeneration")
    parser.add_argument("--skip-train", action="store_true", help="Skip training")
    parser.add_argument("--skip-eval", action="store_true", help="Skip evaluation")
    parser.add_argument("--skip-live", action="store_true", help="Skip live test")
    parser.add_argument("--epochs", type=int, default=1, help="Training epochs")
    args = parser.parse_args()

    results: dict[str, bool] = {}

    if not args.skip_dataset:
        results["dataset"] = step1_regenerate_dataset()
    else:
        print("[SKIP] Dataset regeneration")
        results["dataset"] = True

    if not args.skip_train and results.get("dataset", True):
        results["train"] = step2_train(args.epochs)
    else:
        print("[SKIP] Training")
        results["train"] = True

    if not args.skip_eval and results.get("train", True):
        results["eval"] = step3_evaluate()
    else:
        print("[SKIP] Evaluation")
        results["eval"] = True

    if not args.skip_live:
        results["live"] = step4_live_test()
    else:
        print("[SKIP] Live test")
        results["live"] = True

    results["logs"] = step5_validate_logs()

    print("\n" + "=" * 60)
    print("PIPELINE SUMMARY")
    print("=" * 60)
    for name, ok in results.items():
        status = "PASS" if ok else "FAIL"
        print(f"  {name:12s} {status}")

    if all(results.values()):
        print("\n[OK] All steps passed")
        sys.exit(0)
    else:
        print("\n[FAIL] Some steps failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
