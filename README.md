# TopoSwarm

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18072858.svg)](https://doi.org/10.5281/zenodo.18072858)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPLv3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

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
| `lazyown_dataset_generator.py` | Rich ToolBench-format dataset: 422 examples across all 80 LazyOwn tools |
| `toposwarm_continual_trainer.py` | **EWC + Experience Replay** continual learning — fine-tune without catastrophic forgetting |
| `skills/toposwarm.md` | Operator guide loaded as MCP context |
| `.claude/settings.json` | MCP server registration for Claude Code |

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

## Continual Learning — EWC + Experience Replay

The recommended way to fine-tune TopoSwarm on LazyOwn without losing ToolBench generalisation.

### Strategy

Two complementary techniques run together every training step:

| Technique | What it does | Why |
|---|---|---|
| **EWC** (Elastic Weight Consolidation) | Computes Fisher diagonal on ToolBench; adds quadratic penalty `λ/2·Σ F_i·(θ_i−θ*_i)²` | Anchors weights critical for weather/calc/search routing |
| **Experience Replay** | 20% of every batch = real ToolBench samples | Exact gradient signal from the original task distribution |
| **LR = 2e-5** | 15× lower than pretraining (3e-4) | Conservative updates preserve existing representations |

### Quick start

```bash
# Full pipeline in one command
python toposwarm_continual_trainer.py --full

# Step by step
python toposwarm_continual_trainer.py --gen-dataset      # 422 LazyOwn examples
python toposwarm_continual_trainer.py --compute-fisher   # Fisher diagonal on ToolBench
python toposwarm_continual_trainer.py --train            # EWC + Replay fine-tuning
python toposwarm_continual_trainer.py --eval             # routing accuracy on both datasets

# Tune the anti-forgetting strength
python toposwarm_continual_trainer.py --full --ewc-lambda 600 --replay-ratio 0.25
```

### Dataset

`lazyown_dataset_generator.py` generates **422 ToolBench-format examples** across all 80 LazyOwn MCP tools:

```bash
python lazyown_dataset_generator.py --stats
```

```
Total examples : 422   Unique tools : 80

By domain:
  Security/Intel        74    Security/Report       53
  Security/Config       38    Security/Execution    37
  Security/C2           36    Security/Hive         32
  Security/Events       26    Security/Automation   25
  Security/Agents       24    Security/Autonomous   21
```

Each tool has 5–10 phrasings covering: expert language, beginner language, Spanish, context-aware post-action prompts (`"vsftpd exploit worked, I have a shell — dump credentials"`), and multi-step chain examples (`recon → exploit → creds → AD → report`).

### Why EWC over LoRA?

LoRA adds rank-decomposed adapters and freezes base weights — ideal for 7B+ transformers. For a 2M-param model trained from scratch, EWC achieves the same "protect original weights" goal via a loss penalty with zero architectural overhead. Combined with replay, it outperforms LoRA on small custom models.

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

## Previous work

### TopoGPT2

- [https://github.com/grisuno/TopoGPT2](https://github.com/grisuno/TopoGPT2)

### Algorithmic Induction via Structural Weight Transfer

- [https://doi.org/10.5281/zenodo.18072858](https://doi.org/10.5281/zenodo.18072858)

### From Boltzmann Stochasticity to Hamiltonian Integrability: Emergence of Topological Crystals and Synthetic Planck Constants

- [https://doi.org/10.5281/zenodo.18407920](https://doi.org/10.5281/zenodo.18407920)

### The Dirac Discrete Crystal

- [https://doi.org/10.5281/zenodo.18810160](https://doi.org/10.5281/zenodo.18810160)

### Schrödinger Topological Crystallization: Phase Space Discovery in Hamiltonian Neural Networks

- [https://doi.org/10.5281/zenodo.18725428](https://doi.org/10.5281/zenodo.18725428)

### Constraint Preservation in a Neural Quantum Simulator

- [https://doi.org/10.5281/zenodo.18795537](https://doi.org/10.5281/zenodo.18795537)

  

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) [![License: AGPL v3](https://img.shields.io/badge/License-AGPLv3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y2Z73AV)
