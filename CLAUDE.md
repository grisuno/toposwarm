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
| `toposwarm_meta_harness.py` | Meta-Harness optimizer: filesystem experience store, env bootstrap, draft-verify routing, Pareto frontier, dense retrieval |
| `meta_harness_proposer.py` | Coding-agent proposer: reads logs, diagnoses failures, writes code patches via LLM |
| `toposwarm_coevolve.py` | Co-evolution engine: simultaneous weight + harness optimisation |
| `lazyown_dataset_generator.py` | Synthetic dataset generator (~1500 examples covering 79 tools) |
| `lazyown_dataset_enhancer.py` | **Dataset enhancer**: mines real execution traces from experience store, adds error recovery, multi-turn, and curriculum learning |
| `toposwarm_lazyown_sweep.py` | **LazyOwn sweep**: executes real prompts against LazyOwn to generate live training data |
| `toposwarm_continual_trainer.py` | Continual learning trainer: EWC + experience replay + surprise buffer |
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

## Meta-Harness integration (new)

The orchestrator now embeds a **Meta-Harness** outer-loop inspired by Lee et al.
(Stanford/MIT, 2026).  This does not change model weights; it optimises the
*harness* — the code that decides what to store, retrieve, and present to the
router.

### What Meta-Harness adds

1. **Filesystem Experience Store** (`meta_harness_logs/`)
   - Every tool execution is logged as a directory containing:
     - `harness.json` — config snapshot
     - `trace.jsonl` — step-by-step execution trace
     - `score.json` — metrics (success, latency, context size)
   - Future coding-agent proposers can `grep` / `cat` raw history instead of
     relying on lossy summaries.

2. **Environment Bootstrap**
   - Before the first router turn the orchestrator gathers a LazyOwn sandbox
     snapshot (config, targets, sessions, beacons, modules, languages).
   - Injects a compact `[Environment Snapshot]` block into the prompt.
   - Eliminates 2-4 wasted exploratory turns on dependency-heavy tasks.

3. **Draft-Verification Routing**
   - **Draft**: fast keyword heuristic proposes an initial tool.
   - **Verify**: MetaHarnessMemory retrieves *confirmers* (same tool, past
     successes) and *challengers* (different tool or failure) from the
     experience store.
   - The draft is kept, boosted, or revised based on prior episode evidence.

4. **Pareto Frontier**
   - Maintains a population of harness variants trading off success rate,
     latency, and context cost.
   - The orchestrator can switch to the Pareto-optimal harness for the
     current task context.

### Configuring Meta-Harness

```python
from toposwarm_meta_harness import MetaHarnessConfig

cfg = MetaHarnessConfig(
    BOOTSTRAP_ENABLED=True,      # gather env snapshot before first turn
    DRAFT_VERIFY_ENABLED=True,   # two-stage routing with memory retrieval
    LOG_DIR="meta_harness_logs", # filesystem experience store path
)
```

### Inspecting the experience store

```bash
# List recent runs
ls -lt meta_harness_logs/ | head

# Search traces for a specific tool
grep -r "lazyown_run_command" meta_harness_logs/*/trace.jsonl

# View scores of all runs
for f in meta_harness_logs/*/score.json; do echo "$f:"; cat "$f"; done
```

## Dense Memory Retrieval (new)

`MetaHarnessMemory` now supports **semantic retrieval** via `DenseMemoryRetriever`:

1. **sentence-transformers** (`all-MiniLM-L6-v2`) — best quality, GPU-optional.
2. **sklearn TF-IDF + cosine** — zero-extra-deps fallback (already active).
3. **Jaccard token overlap** — last-resort fallback.

Retrieval in `retrieve_similar()` fuses dense + lexical scores automatically.
To force a specific backend, set environment variables before import:

```bash
# If sentence-transformers is installed, it will be picked automatically
pip install sentence-transformers
```

## Coding-Agent Proposer (new)

`meta_harness_proposer.py` is a standalone coding agent that implements the
"agentic proposer" from the Meta-Harness paper:

- Reads raw `meta_harness_logs/` (code + traces + scores).
- Builds a diagnostic context with failures vs. successes.
- Sends it to an OpenAI-compatible LLM endpoint (Ollama, Groq, OpenAI, etc.).
- Validates proposed patches with `py_compile` before writing.
- Logs its own reasoning as a new run for the outer loop to evaluate.

### Usage

```bash
# Diagnose last 20 runs and propose a patch (dry-run)
python meta_harness_proposer.py --diagnose --dry-run --target toposwarm_lazyown_orchestrator.py

# Apply the proposed patch for real
python meta_harness_proposer.py --diagnose --target toposwarm_lazyown_orchestrator.py

# Use a remote endpoint (falls back to local Ollama automatically on 401/403/404)
export META_PROPOSER_API_URL="https://api.groq.com/openai/v1/chat/completions"
export META_PROPOSER_API_KEY="gsk_..."
export META_PROPOSER_MODEL="llama-3.1-70b-versatile"
python meta_harness_proposer.py --diagnose --dry-run

# Force local Ollama only
export META_PROPOSER_API_URL="http://localhost:11434/v1/chat/completions"
export META_PROPOSER_MODEL="granite4.1:3b"
python meta_harness_proposer.py --diagnose --dry-run
```

> **Note:** The proposer now auto-detects Ollama on `localhost:11434` and falls back automatically if the primary endpoint returns 401/403/404.  Patches that cannot be applied exactly are printed to the log for manual copy-paste.
> **Groq key note:** If you see `403 Forbidden`, the API key may be revoked or the account lacks credits.  The fallback to Ollama will still work.

## LazyOwn Sweep (new)

`toposwarm_lazyown_sweep.py` ejecuta prompts reales de pentesting contra LazyOwn
para generar datos de entrenamiento en vivo. Esto implementa la idea central del
paper Meta-Harness: el harness (código que decide qué tool usar) es tan
importante como el modelo en sí.

### What it does

1. Genera prompts naturales de pentesting (recon, exploit, payload, C2, credentials)
2. Ejecuta cada prompt contra LazyOwn real via LazyOwnBridge
3. El orchestrator logea automáticamente en `meta_harness_logs/`
4. Escribe un `.jsonl` listo para el continual trainer

### Usage

```bash
# Ejecutar 20 prompts de prueba
python toposwarm_lazyown_sweep.py --prompts 20

# Ejecutar 100 prompts y entrenar inmediatamente
python toposwarm_lazyown_sweep.py --prompts 100 --train --epochs 1

# Guardar en path custom
python toposwarm_lazyown_sweep.py --prompts 50 --output data_toolbench/my_sweep.jsonl
```

## Co-Evolution Engine (new)

`toposwarm_coevolve.py` runs the outer loop that Meta-Harness calls the
"natural next step": **co-evolve harness config and model weights**.

### Outer loop (harness evolution)
- Maintains a population of `MetaHarnessConfig` variants.
- Mutates / crossovers configs each generation.
- Evaluates every candidate on a 15-prompt LazyOwn validation suite.
- Updates a Pareto frontier trading off success rate vs. latency vs. context.

### Inner loop (weight evolution)
- For the best harness of each generation, runs a short EWC+Replay fine-tuning
  burst via `toposwarm_continual_trainer.py`.
- Re-evaluates the *same* harness with updated weights.

### Periodic proposer
- Every K generations invokes `meta_harness_proposer.py` to suggest
  intelligent code mutations rather than random config noise.

### Usage

```bash
# Pure harness evolution (fast, no GPU)
python toposwarm_coevolve.py --generations 20 --no-weight-update

# Full co-evolution (harness + weights)
python toposwarm_coevolve.py --generations 10 --train-steps 200

# Resume from checkpoint
python toposwarm_coevolve.py --resume meta_coevolve_state.json
```

The engine writes `meta_coevolve_state.json` after every generation so crashes
are recoverable.

### Mock bridge for evaluation

When LazyOwn is not installed, the evaluator automatically falls back to a
`MockLazyOwnBridge` that returns deterministic canned responses for every
LazyOwn command. This lets you evolve the harness even without the red-team
framework present. The mode is logged at startup (`mode=MOCK` or `mode=REAL`).

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
- Meta-Harness tuning: adjust `MetaHarnessConfig` in `toposwarm_meta_harness.py`
- After adding tools, regenerate dataset: `python toposwarm_lazyown_orchestrator.py --gen-dataset`
- Generate live training data: `python toposwarm_lazyown_sweep.py --prompts 50`
