#!/usr/bin/env python3
"""
TopoSwarm LazyOwn Sweep — Ejecuta prompts reales contra LazyOwn para generar dataset
=====================================================================================
Este script implementa la idea del paper Meta-Harness (Lee et al., 2026):
el harness (código que decide qué tool usar) es tan importante como el modelo.

Flujo:
    1. Genera prompts naturales de pentesting
    2. Ejecuta cada prompt contra LazyOwn real via LazyOwnBridge
    3. El orchestrator logea automáticamente en meta_harness_logs/
    4. Al final, extrae los logs y genera lazyown_enriched.jsonl
    5. Opcionalmente corre continual trainer

Usage:
    python toposwarm_lazyown_sweep.py --prompts 50
    python toposwarm_lazyown_sweep.py --prompts 100 --train --epochs 1
"""
from __future__ import annotations

import argparse
import json
import logging
import random
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Añadir el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

from toposwarm_lazyown_orchestrator import LazyOwnBridge, LazyOwnOrchestrator, InferenceConfig
from topo_swarm_agent import SwarmConfig

# ---------------------------------------------------------------------------
# Prompts de pentesting por categoría
# ---------------------------------------------------------------------------

RECON_PROMPTS = [
    "scan {target}",
    "run nmap on {target}",
    "discover hosts in {target}",
    "enumerate services on {target}",
    "what ports are open on {target}",
    "check network topology for {target}",
    "find live hosts in {target}",
    "run a full port scan on {target}",
    "check for open ports on {target}",
    "network reconnaissance on {target}",
    "enumerate DNS for {target}",
    "check subdomains of {target}",
    "run traceroute to {target}",
]

EXPLOIT_PROMPTS = [
    "exploit {target}",
    "find vulnerabilities on {target}",
    "check for CVEs on {target}",
    "run exploit against {target}",
    "test for SQL injection on {target}",
    "check for XSS on {target}",
    "try RCE on {target}",
    "check for path traversal on {target}",
    "test for LFI on {target}",
    "run fuzzing on {target}",
    "check for command injection on {target}",
    "test for SSRF on {target}",
]

PAYLOAD_PROMPTS = [
    "generate reverse shell",
    "create a payload for windows",
    "create a payload for linux",
    "generate a meterpreter payload",
    "create a web shell",
    "generate shellcode",
    "create a stager",
    "generate an encoded payload",
    "create a powershell payload",
    "generate a macro payload",
]

C2_PROMPTS = [
    "start C2 server",
    "check C2 beacons",
    "list active C2 sessions",
    "send command to beacon",
    "check C2 status",
    "start listener on port {port}",
    "get C2 config",
    "poll C2 events",
]

CREDENTIAL_PROMPTS = [
    "dump credentials",
    "get password hashes",
    "check for cached credentials",
    "dump SAM database",
    "extract kerberos tickets",
    "check for plain text passwords",
    "dump LSASS",
    "get NTLM hashes",
]

MISC_PROMPTS = [
    "show help",
    "list available tools",
    "get current config",
    "check system info",
    "show targets",
    "list sessions",
    "check logs",
    "show banner",
]

ALL_PROMPT_TEMPLATES = (
    RECON_PROMPTS * 3
    + EXPLOIT_PROMPTS * 3
    + PAYLOAD_PROMPTS * 2
    + C2_PROMPTS * 2
    + CREDENTIAL_PROMPTS * 2
    + MISC_PROMPTS
)

TARGETS = ["10.10.11.78", "192.168.1.1", "172.16.0.5", "target.local", "victim.corp"]
PORTS = ["4444", "8080", "443", "80", "1337"]


def generate_prompts(n: int) -> List[str]:
    """Generate N diverse pentesting prompts."""
    prompts: List[str] = []
    templates = ALL_PROMPT_TEMPLATES[:]
    random.shuffle(templates)
    for i in range(n):
        tmpl = templates[i % len(templates)]
        prompt = tmpl.format(
            target=random.choice(TARGETS),
            port=random.choice(PORTS),
        )
        prompts.append(prompt)
    return prompts


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("LazyOwnSweep")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(logging.Formatter("%(asctime)s %(name)-20s %(levelname)-8s %(message)s"))
        logger.addHandler(h)
    return logger


def run_sweep(prompts: List[str], bridge: LazyOwnBridge, logger: logging.Logger) -> List[Dict[str, Any]]:
    """Execute prompts against LazyOwn and collect results."""
    cfg = InferenceConfig()
    agent_cfg = SwarmConfig()
    orch = LazyOwnOrchestrator(cfg, agent_cfg, bridge, logger, load_model=False)

    results: List[Dict[str, Any]] = []
    for i, prompt in enumerate(prompts):
        logger.info("[%d/%d] Prompt: %s", i + 1, len(prompts), prompt)
        try:
            result = orch.run(prompt)
            results.append({
                "prompt": prompt,
                "tool_name": result.tool_name,
                "tool_arg": result.tool_arg,
                "output": result.tool_result.output[:500] if result.tool_result else "",
                "ok": result.tool_result.ok if result.tool_result else False,
                "latency_ms": result.tool_result.latency_ms if hasattr(result.tool_result, "latency_ms") else 0,
            })
        except Exception as exc:
            logger.error("Failed for prompt %r: %s", prompt, exc)
            results.append({
                "prompt": prompt,
                "tool_name": "error",
                "tool_arg": "",
                "output": str(exc),
                "ok": False,
                "latency_ms": 0,
            })
        # Sleep briefly to avoid overwhelming LazyOwn
        time.sleep(0.5)
    return results


def write_results(results: List[Dict[str, Any]], out_path: Path) -> None:
    """Write results as JSONL for continual trainer.

    Matches the format of lazyown_dataset_generator.py:
    - instruction: the prompt
    - api_list: minimal tool metadata
    - answer: [TOOL_CALL: tool_name(arg)]
    - domain: Security/RealSuccess or Security/RealFailure
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for r in results:
            tool_name = r["tool_name"]
            tool_arg = r["tool_arg"]
            # Clean arg for display: strip newlines, truncate
            arg_display = tool_arg.replace("\n", " ")[:80]
            record = {
                "instruction": r["prompt"],
                "api_list": [
                    {
                        "tool_name": tool_name,
                        "api_name": f"{tool_name}_endpoint",
                        "api_description": f"LazyOwn {tool_name} tool",
                        "required_parameters": [{"name": "arg", "type": "STRING", "description": "tool argument"}],
                        "optional_parameters": [],
                    }
                ],
                "answer": f"[TOOL_CALL: {tool_name}({arg_display})] [result captured during pentest]",
                "domain": "Security/RealSuccess" if r["ok"] else "Security/RealFailure",
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"[sweep] Wrote {len(results)} records → {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="LazyOwn Sweep — real execution dataset generator")
    parser.add_argument("--prompts", type=int, default=20, help="Number of prompts to generate")
    parser.add_argument("--output", type=str, default="data_toolbench/lazyown_sweep.jsonl", help="Output JSONL path")
    parser.add_argument("--lazyown-dir", type=str, default="", help="LazyOwn directory")
    parser.add_argument("--train", action="store_true", help="Run continual trainer after sweep")
    parser.add_argument("--epochs", type=int, default=1, help="Training epochs")
    args = parser.parse_args()

    logger = setup_logger()
    bridge = LazyOwnBridge(
        lazyown_dir=Path(args.lazyown_dir) if args.lazyown_dir else Path.home() / "LazyOwn"
    )
    logger.info("LazyOwn dir: %s (available=%s)", bridge.lazyown_dir, bridge.available)

    if not bridge.available:
        logger.error("LazyOwn not found at %s", bridge.lazyown_dir)
        sys.exit(1)

    prompts = generate_prompts(args.prompts)
    logger.info("Generated %d prompts", len(prompts))

    results = run_sweep(prompts, bridge, logger)

    ok_count = sum(1 for r in results if r["ok"])
    logger.info("Sweep complete: %d/%d successful (%.1f%%)", ok_count, len(results), 100 * ok_count / len(results))

    write_results(results, Path(args.output))

    if args.train:
        logger.info("Running continual trainer...")
        import subprocess
        subprocess.run([
            sys.executable, "toposwarm_continual_trainer.py",
            "--train", "--epochs", str(args.epochs),
            "--dataset", args.output,
        ])


if __name__ == "__main__":
    main()
