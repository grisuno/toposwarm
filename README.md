# TopoSwarm

**A micro-scale quaternionic toroidal swarm agent for tool-use reasoning.**

Trained in 3 epochs on ToolBench with low loss. The router is crystallised and can be extended to any tool domain — including offensive security via the [LazyOwn MCP](https://github.com/grisuno/LazyOwn) integration.

---

## Architecture

```
User prompt (NL)
      │
      ▼
TopoSwarmModel (~2M params, d=64, 4 layers)
  ├── Quaternionic torus topology  (4 angular × 2 radial nodes)
  ├── Spectral autoencoder bottleneck  (function-call filter)
  ├── HRM fast/slow reasoning  (L=action, H=strategy)
  └── ACT halt (Hamilton-product norm confidence)
      │
      ▼ (tool_name, tool_arg)
ToolRegistry  ──→  real tool execution
      │
      ▼
Pass-2 generation  ──→  final NL answer
```

**Swarm**: `N=3` agent instances share weights but carry distinct Berry-phase offsets on the torus, producing specialisation across disjoint API subsets.

**Training**: Phase-0 kernel calibration → Phase-1 grokking-aware main training (kappa coherence) → Phase-2 annealing. Checkpoint: safetensors + JSON metadata.

---

## Files

| File | Purpose |
|---|---|
| `topo_swarm_agent.py` | Core model, training pipeline, `SwarmOrchestrator` |
| `toposwarm_infer.py` | Inference engine with built-in tools (weather, search, calc, datetime, translate, news) |
| `toposwarm_hybrid.py` | Router + external language backend (TinyStories / custom checkpoint) |
| `toposwarm_lazyown_orchestrator.py` | **LazyOwn MCP integration** — routes NL pentesting prompts to LazyOwn tools |

---

## Quick start

```bash
pip install torch safetensors tiktoken numpy

# Train (downloads ToolBench from HuggingFace, ~5M tokens, 3 epochs)
python topo_swarm_agent.py

# Inference
python toposwarm_infer.py --prompt "What is the weather in Santiago?"
python toposwarm_infer.py --prompt "Calculate 17 * 89 + 42"
python toposwarm_infer.py --list-tools

# Hybrid mode (TopoSwarm router + TinyStories language backend)
python toposwarm_hybrid.py --backend-type tinystories \
    --backend-model roneneldan/TinyStories-33M \
    --prompt "weather in Buenos Aires"
```

---

## LazyOwn MCP Orchestrator

TopoSwarm acts as the **AI router** for [LazyOwn](https://github.com/grisuno/LazyOwn)'s full pentesting framework, routing natural-language security goals to the correct LazyOwn tool automatically.

### Setup

```bash
# Clone LazyOwn next to toposwarm
git clone https://github.com/grisuno/LazyOwn.git ../../../LazyOwn
cd ../../../LazyOwn && pip install lupa   # core dep

# Or point to your existing LazyOwn install
export LAZYOWN_DIR=/path/to/LazyOwn
```

### Usage

```bash
# Single prompt — keyword router (no GPU needed)
python toposwarm_lazyown_orchestrator.py \
    --prompt "scan for open ports on 10.10.11.78" \
    --no-model

# Full model inference (loads checkpoint)
python toposwarm_lazyown_orchestrator.py \
    --prompt "analyze vulnerabilities on 10.10.11.78"

# List all 50+ registered LazyOwn tools
python toposwarm_lazyown_orchestrator.py --list-tools --no-model

# MCP stdio server for Claude Code / Claude Web
python toposwarm_lazyown_orchestrator.py --mcp

# Generate fine-tuning dataset (34 LazyOwn traces in ToolBench format)
python toposwarm_lazyown_orchestrator.py --gen-dataset

# Fine-tune router on LazyOwn traces (1 epoch, LR=3e-5)
python toposwarm_lazyown_orchestrator.py --finetune
```

### Routing examples

| Prompt | Routed tool | Argument |
|---|---|---|
| `scan for open ports on 10.10.11.78` | `lazyown_run_command` | `set rhost 10.10.11.78\nlazynmap` |
| `show collected credentials` | `lazyown_credentials` | — |
| `analyze vulnerabilities on target` | `lazyown_c2_vuln_analysis` | target |
| `what should be the next step?` | `lazyown_recommend_next` | — |
| `search for SMB exploitation techniques` | `lazyown_c2_search_agent` | query |
| `generate a sitrep` | `lazyown_campaign_sitrep` | — |

### LazyOwn tools covered

`lazyown_run_command` · `lazyown_set_config` · `lazyown_get_config` · `lazyown_list_modules` · `lazyown_get_beacons` · `lazyown_c2_command` · `lazyown_list_sessions` · `lazyown_c2_status` · `lazyown_add_target` · `lazyown_list_targets` · `lazyown_set_active_target` · `lazyown_run_agent` · `lazyown_agent_status` · `lazyown_agent_result` · `lazyown_list_agents` · `lazyown_c2_search_agent` · `lazyown_recommend_next` · `lazyown_phase_guide` · `lazyown_campaign_sitrep` · `lazyown_c2_vuln_analysis` · `lazyown_c2_redop` · `lazyown_c2_adversary` · `lazyown_poll_events` · `lazyown_ack_event` · `lazyown_add_rule` · `lazyown_list_event_rules` · `lazyown_heartbeat_status` · `lazyown_report_update` · `lazyown_campaign_lessons` · `lazyown_c2_notes` · `lazyown_credentials` · `lazyown_timeline` · `lazyown_auto_loop` · `lazyown_auto_populate` · `lazyown_session_init` · `lazyown_session_state` · `lazyown_llm_ask` · `lazyown_create_tool` · `lazyown_inject_objective` · `lazyown_next_objective` · `lazyown_read_prompt` · `lazyown_create_addon` · `lazyown_list_addons` · `lazyown_list_plugins` · `lazyown_read_session_file` · `lazyown_run_api` · `lazyown_c2_script` · `lazyown_policy_status` · `lazyown_command_help` · `lazyown_discover_commands`

### MCP config for Claude Code

Add to `.claude/settings.json`:

```json
{
  "mcpServers": {
    "toposwarm-lazyown": {
      "command": "python",
      "args": ["/path/to/toposwarm/toposwarm_lazyown_orchestrator.py", "--mcp"],
      "env": {
        "LAZYOWN_DIR": "/path/to/LazyOwn"
      }
    }
  }
}
```

---

## Fine-tuning on LazyOwn traces

The router ships with a 34-example ToolBench-format dataset covering all major LazyOwn tool categories. Running `--finetune` trains one additional epoch (LR=3e-5) on top of the existing checkpoint — no retraining from scratch needed.

```bash
# Generate dataset then fine-tune in one shot
python toposwarm_lazyown_orchestrator.py --gen-dataset
python toposwarm_lazyown_orchestrator.py --finetune
```

The dataset format is compatible with the main `topo_swarm_agent.py` training pipeline, so you can mix LazyOwn traces with ToolBench data for continual learning.

---

## Requirements

```
torch>=2.0
safetensors
tiktoken
numpy
```

Optional (for LazyOwn orchestrator):
```
mcp          # for --mcp server mode
lupa         # LazyOwn core dependency
```

---

## License

AGPL v3 — Gris Iscomeback

## Wiki

[https://deepwiki.com/grisuno/toposwarm](https://deepwiki.com/grisuno/toposwarm)
