# TopoSwarm — Claude Code Instructions

## What this project is

TopoSwarm is a micro-scale (~2M params) quaternionic toroidal swarm agent trained on ToolBench for tool-use reasoning. It acts as the **AI router / orchestrator** for [LazyOwn](https://github.com/grisuno/LazyOwn)'s pentesting MCP.

## Key files

| File | Role |
|---|---|
| `topo_swarm_agent.py` | Core model + training pipeline |
| `toposwarm_infer.py` | Inference engine + built-in tool registry |
| `toposwarm_hybrid.py` | Router + external language backend |
| `toposwarm_lazyown_orchestrator.py` | LazyOwn MCP orchestrator (main integration) |
| `skills/toposwarm.md` | Operator guide loaded as MCP context |
| `.claude/settings.json` | MCP server registration |

## Running the orchestrator

```bash
# Keyword routing only (no GPU)
python toposwarm_lazyown_orchestrator.py --prompt "scan 10.10.11.78" --no-model

# Full model inference
python toposwarm_lazyown_orchestrator.py --prompt "analyze vulns on 10.10.11.78"

# MCP stdio server
python toposwarm_lazyown_orchestrator.py --mcp

# Generate fine-tune dataset
python toposwarm_lazyown_orchestrator.py --gen-dataset

# Fine-tune on LazyOwn traces (1 epoch)
python toposwarm_lazyown_orchestrator.py --finetune
```

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `LAZYOWN_DIR` | `../../LazyOwn` | Path to LazyOwn repo root |

## Architecture invariants

- `D_MODEL` must be divisible by 4 (quaternions) and by `N_HEADS`
- `TOOL_TOKEN_OFFSET` must be ≥ 50257 (GPT-2 vocab size)
- Checkpoints saved as safetensors + `meta.json` in `checkpoints_toposwarm/latest/`
- Fine-tuning uses LR=3e-5 (10× lower than pretraining) to preserve routing

## When modifying the orchestrator

- New LazyOwn tools go in `LazyOwnToolRegistry._register_lazyown_tools()`
- New keyword clusters go in `LazyOwnToolRegistry._KEYWORD_MAP`
- New fine-tune examples go in `_LAZYOWN_TRACES` list
- After adding tools, regenerate dataset: `python toposwarm_lazyown_orchestrator.py --gen-dataset`
