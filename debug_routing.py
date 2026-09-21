#!/usr/bin/env python3
"""Debug _routing_accuracy by calling it directly on a ContinualTrainer"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import torch
from topo_swarm_agent import SwarmConfig, TopoSwarmModel, BPETokenizer
from ts_utils import import_module, make_cached_encode, make_cached_tool_token
from safetensors.torch import load_file as st_load

_HERE = Path(__file__).parent.resolve()

def _import(name, filename):
    return import_module(name, _HERE / filename, Path.cwd() / filename)

_agent = _import("topo_swarm_agent", "topo_swarm_agent.py")
trainer_mod = _import("toposwarm_continual_trainer", "toposwarm_continual_trainer.py")

SwarmConfig = _agent.SwarmConfig
TopoSwarmModel = _agent.TopoSwarmModel
BPETokenizer = _agent.BPETokenizer

# Load model and config
ckpt_dir = Path("checkpoints_toposwarm/latest")
cfg = SwarmConfig()
meta_path = ckpt_dir / "meta.json"
if meta_path.exists():
    with open(meta_path) as f:
        meta = json.load(f)
    for k, v in meta.get("config", {}).items():
        if hasattr(cfg, k):
            setattr(cfg, k, v)

model = TopoSwarmModel(cfg)
weights_path = ckpt_dir / "model.safetensors"
if weights_path.exists():
    state = st_load(str(weights_path), device="cpu")
    model.load_state_dict(state, strict=False)
model.eval()

tok = BPETokenizer(cfg)
encode = make_cached_encode(tok)
tool_token_fn = make_cached_tool_token(tok)

# Load a few records
with open("data_toolbench/lazyown_enriched.jsonl") as f:
    records = [json.loads(line) for line in f][:10]

# Replicate _routing_accuracy EXACTLY
lm_correct = total = 0
for rec in records:
    api_list = rec.get("api_list", [{}])
    tool_name = api_list[0].get("tool_name", "") if api_list else ""
    instruction = str(rec.get("instruction") or "")[:512]
    instr_ids = encode(instruction)[-cfg.MAX_SEQ_LEN:]
    if not instr_ids:
        print("SKIP: empty instr_ids")
        continue
    ids = torch.tensor([instr_ids], dtype=torch.long)
    gt_off = tool_token_fn(tool_name) - cfg.TOOL_TOKEN_OFFSET

    with torch.no_grad():
        out = model(ids, berry_phase=0.0)
        lm_logits = out["logits"][0, -1, cfg.TOOL_TOKEN_OFFSET:cfg.TOOL_TOKEN_OFFSET + cfg.TOOL_VOCAB_SIZE]
        pred = lm_logits.argmax().item()
        is_correct = pred == gt_off
        lm_correct += int(is_correct)
        print(f"tool={tool_name:<35s} gt={gt_off:<4d} pred={pred:<4d} match={is_correct}")

    total += 1

print(f"\nAccuracy: {lm_correct}/{total} = {lm_correct/max(total,1)*100:.1f}%")
