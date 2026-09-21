#!/usr/bin/env python3
"""Diagnose why routing accuracy is 0%"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import torch
from topo_swarm_agent import SwarmConfig, TopoSwarmModel, BPETokenizer
from ts_utils import import_module, make_cached_encode, make_cached_tool_token

def load_model():
    ckpt_dir = Path("checkpoints_toposwarm/latest")
    meta_path = ckpt_dir / "meta.json"
    cfg = SwarmConfig()
    if meta_path.exists():
        import json
        with open(meta_path) as f:
            meta = json.load(f)
        for k, v in meta.get("config", {}).items():
            if hasattr(cfg, k):
                setattr(cfg, k, v)
    from safetensors.torch import load_file as st_load
    model = TopoSwarmModel(cfg)
    weights_path = ckpt_dir / "model.safetensors"
    if weights_path.exists():
        state = st_load(str(weights_path), device="cpu")
        model.load_state_dict(state, strict=False)
    model.eval()
    return model, cfg

def main():
    model, cfg = load_model()
    tok = BPETokenizer(cfg)
    encode = make_cached_encode(tok)
    tool_token = make_cached_tool_token(tok)

    with open("data_toolbench/lazyown_enriched.jsonl") as f:
        records = [json.loads(line) for line in f][:20]

    print("Checking first 20 predictions:")
    correct = 0
    for rec in records:
        tool_name = rec["api_list"][0]["tool_name"]
        instruction = rec["instruction"]
        instr_ids = encode(instruction)[-cfg.MAX_SEQ_LEN:]
        ids = torch.tensor([instr_ids], dtype=torch.long)
        gt_off = tool_token(tool_name) - cfg.TOOL_TOKEN_OFFSET

        with torch.no_grad():
            out = model(ids, berry_phase=0.0)
            lm_logits = out["logits"][0, -1, cfg.TOOL_TOKEN_OFFSET:cfg.TOOL_TOKEN_OFFSET + cfg.TOOL_VOCAB_SIZE]
            pred = lm_logits.argmax().item()
            top5 = lm_logits.topk(5).indices.tolist()

        is_correct = pred == gt_off
        correct += is_correct
        status = "✓" if is_correct else "✗"
        print(f"{status} {tool_name:<35s} gt={gt_off:<4d} pred={pred:<4d} top5={top5}")

    print(f"\nAccuracy on 20 samples: {correct}/20 = {correct/20*100:.1f}%")

    # Also check: what does the model output for a blank input?
    print("\nBlank input prediction:")
    with torch.no_grad():
        blank_ids = torch.tensor([[tok.encode("")]], dtype=torch.long)
        out = model(blank_ids, berry_phase=0.0)
        lm_logits = out["logits"][0, -1, cfg.TOOL_TOKEN_OFFSET:cfg.TOOL_TOKEN_OFFSET + cfg.TOOL_VOCAB_SIZE]
        print(f"  argmax={lm_logits.argmax().item()}  top5={lm_logits.topk(5).indices.tolist()}")

if __name__ == "__main__":
    main()
