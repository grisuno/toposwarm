# Graph Report - .  (2026-04-27)

## Corpus Check
- Corpus is ~39,714 words - fits in a single context window. You may not need a graph.

## Summary
- 621 nodes · 1017 edges · 26 communities detected
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 91 edges (avg confidence: 0.71)
- Token cost: 3,200 input · 2,800 output

## Community Hubs (Navigation)
- [[_COMMUNITY_TopoGPT2 Quaternion Attention|TopoGPT2 Quaternion Attention]]
- [[_COMMUNITY_SwarmAgent BPE Tokenizer|SwarmAgent BPE Tokenizer]]
- [[_COMMUNITY_TopoGPT2 Training & Metrics|TopoGPT2 Training & Metrics]]
- [[_COMMUNITY_HRM Reasoning & Quaternion Ops|HRM Reasoning & Quaternion Ops]]
- [[_COMMUNITY_Hybrid Router Orchestrator|Hybrid Router Orchestrator]]
- [[_COMMUNITY_LazyOwn Dataset Pipeline|LazyOwn Dataset Pipeline]]
- [[_COMMUNITY_Tool Registry & Swarm Trainer|Tool Registry & Swarm Trainer]]
- [[_COMMUNITY_Project Config & MCP Setup|Project Config & MCP Setup]]
- [[_COMMUNITY_TopoGPT2 Tokenizer & Corpus|TopoGPT2 Tokenizer & Corpus]]
- [[_COMMUNITY_Inference Engine|Inference Engine]]
- [[_COMMUNITY_Quaternionic Torus Geometry|Quaternionic Torus Geometry]]
- [[_COMMUNITY_TopoGPT2 Checkpoint Manager|TopoGPT2 Checkpoint Manager]]
- [[_COMMUNITY_Training Evaluation & Kappa|Training Evaluation & Kappa]]
- [[_COMMUNITY_Design Rationale Notes|Design Rationale Notes]]
- [[_COMMUNITY_Checkpoint Documentation|Checkpoint Documentation]]
- [[_COMMUNITY_Isolated Rationale|Isolated Rationale]]
- [[_COMMUNITY_Isolated Rationale|Isolated Rationale]]
- [[_COMMUNITY_Isolated Rationale|Isolated Rationale]]
- [[_COMMUNITY_Isolated Rationale|Isolated Rationale]]
- [[_COMMUNITY_Isolated Rationale|Isolated Rationale]]
- [[_COMMUNITY_Isolated Rationale|Isolated Rationale]]
- [[_COMMUNITY_Isolated Rationale|Isolated Rationale]]
- [[_COMMUNITY_Isolated Rationale|Isolated Rationale]]
- [[_COMMUNITY_Isolated Rationale|Isolated Rationale]]
- [[_COMMUNITY_Isolated Rationale|Isolated Rationale]]
- [[_COMMUNITY_Isolated Rationale|Isolated Rationale]]

## God Nodes (most connected - your core abstractions)
1. `SwarmTrainer` - 24 edges
2. `CheckpointManager` - 21 edges
3. `ToolResult` - 19 edges
4. `main()` - 18 edges
5. `MechanisticMetrics` - 18 edges
6. `main()` - 16 edges
7. `run_full_pipeline()` - 16 edges
8. `TopoSwarmModel (~2M params, d=64, 4 layers)` - 14 edges
9. `main()` - 13 edges
10. `main()` - 12 edges

## Surprising Connections (you probably didn't know these)
- `Routing Table: Natural Language → LazyOwn Tool` --semantically_similar_to--> `LazyOwnToolRegistry._KEYWORD_MAP — Keyword Routing Clusters`  [INFERRED] [semantically similar]
  skills/toposwarm.md → CLAUDE.md
- `EWC (Elastic Weight Consolidation) — Fisher Diagonal Penalty` --semantically_similar_to--> `Fine-tuning LR=3e-5 (10x lower than pretraining)`  [INFERRED] [semantically similar]
  README.md → CLAUDE.md
- `main()` --calls--> `InferenceConfig`  [INFERRED]
  toposwarm_lazyown_orchestrator.py → toposwarm_infer.py
- `main()` --calls--> `SwarmConfig`  [INFERRED]
  toposwarm_lazyown_orchestrator.py → topo_swarm_agent.py
- `build_model_and_tok()` --calls--> `SwarmConfig`  [INFERRED]
  toposwarm_continual_trainer.py → topo_swarm_agent.py

## Hyperedges (group relationships)
- **TopoSwarm Inference Pipeline: Model → ToolRegistry → Pass-2 Generation** — readme_toposwarm_model, readme_tool_registry, readme_pass2_generation, readme_spectral_autoencoder, readme_act_halt [EXTRACTED 0.95]
- **Continual Learning Strategy: EWC + Experience Replay + Low LR** — readme_ewc, readme_experience_replay, readme_toposwarm_continual_trainer, claude_md_finetune_lr, readme_ewc_vs_lora_rationale [EXTRACTED 0.92]
- **LazyOwn MCP Integration: Orchestrator + Registry + Keyword Map + Traces** — claude_md_toposwarm_lazyown_orchestrator, claude_md_lazyown_tool_registry, claude_md_keyword_map, claude_md_lazyown_traces, skills_toposwarm_query_fn [EXTRACTED 0.90]

## Communities

### Community 0 - "TopoGPT2 Quaternion Attention"
Cohesion: 0.04
Nodes (46): conjugate(), generate(), hamilton_product(), MultiHeadAttention, normalize(), Phase4_AnnealingRefiner, QuaternionLinear, QuaternionOps (+38 more)

### Community 1 - "SwarmAgent BPE Tokenizer"
Cohesion: 0.04
Nodes (50): BPETokenizer, build_dataloaders(), CheckpointManager, _chunked_ce(), EpisodicMemory, generate(), infer(), main() (+42 more)

### Community 2 - "TopoGPT2 Training & Metrics"
Cohesion: 0.05
Nodes (33): evaluate(), MechanisticMetrics, Phase0_KernelOptimizer, Phase1_BatchProspector, Phase2_SeedMiner, Entrenador acumulativo y resumible.      Caracteristicas:     - Checkpoint autom, Carga el ultimo checkpoint disponible.         Restaura: pesos del modelo, estad, Cosine decay con warmup. El schedule es relativo a la sesion actual. (+25 more)

### Community 3 - "HRM Reasoning & Quaternion Ops"
Cohesion: 0.05
Nodes (31): HRMModule, QuaternionAttention, QuaternionLinear, Args:             cfg: Swarm configuration., Args:             model: TopoSwarmModel instance.             cfg: Swarm configu, Linear map in the quaternion algebra.      Implements W ⊗ x via a single batched, Initialise quaternion weight matrices.          Args:             in_features: M, Fused Hamilton product via a single batched einsum. (+23 more)

### Community 4 - "Hybrid Router Orchestrator"
Cohesion: 0.06
Nodes (32): HybridConfig, HybridOrchestrator, HybridResult, _import_agent(), _is_useful_output(), main(), Execute the full hybrid pipeline for one user prompt.          Args:, CLI entry point.      Flags     -----     --prompt TEXT              : User requ (+24 more)

### Community 5 - "LazyOwn Dataset Pipeline"
Cohesion: 0.09
Nodes (28): build_dataset(), main(), _make_record(), print_stats(), write_jsonl(), build_model_and_tok(), ContinualConfig, ContinualTrainer (+20 more)

### Community 6 - "Tool Registry & Swarm Trainer"
Cohesion: 0.1
Nodes (28): ToolRegistry, Three-phase training pipeline for the TopoSwarm agent.      Phase 0 (Kernel Cali, SwarmTrainer, Structured result returned by every tool executor., Args:             tool_name: Name of the tool that was called.             arg:, Execute a tool by name with the given argument string.          Args:, ToolResult, _extract_arg() (+20 more)

### Community 7 - "Project Config & MCP Setup"
Cohesion: 0.05
Nodes (43): .claude/settings.json — MCP Server Registration, Architecture Invariant: D_MODEL divisible by 4 and N_HEADS, Fine-tuning LR=3e-5 (10x lower than pretraining), LazyOwnToolRegistry._KEYWORD_MAP — Keyword Routing Clusters, Environment Variable: LAZYOWN_DIR, LazyOwnToolRegistry — Tool Registration Class, _LAZYOWN_TRACES — Fine-tune Example List, skills/toposwarm.md — Operator Guide (MCP Context) (+35 more)

### Community 8 - "TopoGPT2 Tokenizer & Corpus"
Cohesion: 0.06
Nodes (21): BPETokenizer, CorpusDownloader, main(), token_ids: [B, S]  (enteros)         past_kvs:  lista de (K, V) por capa, o None, Wrapper alrededor de tiktoken (GPT-2 compatible)., Descarga corpus de texto para entrenamiento.      Soporta:     - 'tinystories':, Devuelve el texto del corpus. Descarga si es necesario., Dataset de tokens para language modeling (next-token prediction).      Guarda lo (+13 more)

### Community 9 - "Inference Engine"
Cohesion: 0.07
Nodes (26): Evaluate a math expression safely via AST — no eval()., _safe_eval(), _import_agent(), InferenceConfig, InferenceResult, main(), Evaluate a mathematical expression without using eval() on arbitrary code., Registry of executable tools.      Each tool is a callable(arg: str) -> str.  Re (+18 more)

### Community 10 - "Quaternionic Torus Geometry"
Cohesion: 0.08
Nodes (20): berry_phase_rotation(), _get_torus_positions(), hamilton_product(), normalize(), QuaternionTorusBrain, Cached angular / radial position linspaces for soft torus assignment., 1-D spectral autoencoder acting as the function-call signal filter.      Compres, Apply a learned complex spectral filter in the rfft domain. (+12 more)

### Community 11 - "TopoGPT2 Checkpoint Manager"
Cohesion: 0.14
Nodes (7): CheckpointManager, Gestiona checkpoints de forma acumulativa y segura.      Estructura en disco:, Lee el checkpoint 'latest' y ajusta cfg.N_KV_HEADS / cfg.GQA_GROUPS         para, Guarda checkpoint completo.          state debe contener al menos: completed_epo, Carga el ultimo checkpoint guardado.         Devuelve el state dict (vacio si no, Carga el mejor modelo guardado (solo pesos, sin optimizador)., Load weights from the latest checkpoint directory.

### Community 12 - "Training Evaluation & Kappa"
Cohesion: 0.12
Nodes (11): _evaluate(), KappaDetector, Save model weights and metadata if the interval has elapsed.          Args:, Tracks the kappa coherence metric over a sliding window to detect grokking., Args:             cfg: Swarm configuration (window and threshold)., Update the detector with the latest loss value.          Args:             loss:, Build AdamW with weight decay applied only to non-bias, non-norm params., Apply warmup + cosine decay learning rate schedule. (+3 more)

### Community 13 - "Design Rationale Notes"
Cohesion: 0.19
Nodes (7): ToolBench "Instruction-Tool-Result" dataset loader.      Attempts to load from H, Args:             cfg: Swarm configuration.             tokenizer: BPETokenizer, Load and tokenise tool traces with three-level fallback.          Level 1 – Maur, Encode a tool-trace record to token ids.          Handles three schemas:, Generate n synthetic tool-trace stubs safe for dry-run training.          All to, Return a (input_ids, target_ids) pair of length MAX_SEQ_LEN.          Token ids, ToolBenchDataset

### Community 14 - "Checkpoint Documentation"
Cohesion: 1.0
Nodes (2): Checkpoint: optimizer.pt.zip (GitHub size constraint), Checkpoint Format: safetensors + meta.json

### Community 15 - "Isolated Rationale"
Cohesion: 1.0
Nodes (1): Hamilton (cross) product q1 ⊗ q2 for tensors of shape [..., 4].

### Community 16 - "Isolated Rationale"
Cohesion: 1.0
Nodes (1): Unit-normalise quaternion tensors.

### Community 17 - "Isolated Rationale"
Cohesion: 1.0
Nodes (1): Apply a Berry-phase rotation around the w-axis of the quaternion manifold.

### Community 18 - "Isolated Rationale"
Cohesion: 1.0
Nodes (1): Autoregressive generation with ACT-driven early stopping.          The model sto

### Community 19 - "Isolated Rationale"
Cohesion: 1.0
Nodes (1): Surprise = cross-entropy × (1 - gate_mean), clipped to [0, 10].          A high

### Community 20 - "Isolated Rationale"
Cohesion: 1.0
Nodes (1): Run swarm inference and return the decoded output string.          Args:

### Community 21 - "Isolated Rationale"
Cohesion: 1.0
Nodes (1): Compute mean validation loss over the first EVAL_INTERVAL_STEPS batches.

### Community 22 - "Isolated Rationale"
Cohesion: 1.0
Nodes (1): Producto de Hamilton q1 ⊗ q2. Ambos [..., 4].

### Community 23 - "Isolated Rationale"
Cohesion: 1.0
Nodes (1): Rota vector 3D v por cuaternión unitario q. v:[...,3] q:[...,4]

### Community 24 - "Isolated Rationale"
Cohesion: 1.0
Nodes (1): Generacion autoregresiva con KV cache y muestreo top-k.         En el primer pas

### Community 25 - "Isolated Rationale"
Cohesion: 1.0
Nodes (1): Genera una muestra de texto al final de cada epoch para monitorear         la ca

## Knowledge Gaps
- **244 isolated node(s):** `Import topo_swarm_agent, searching script dir then cwd.`, `All hyper-parameters for the hybrid system — zero magic numbers.`, `Idempotent logger with a single StreamHandler.`, `Evaluate a math expression safely via AST — no eval().`, `Structured result from a tool call.` (+239 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Checkpoint Documentation`** (2 nodes): `Checkpoint: optimizer.pt.zip (GitHub size constraint)`, `Checkpoint Format: safetensors + meta.json`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Isolated Rationale`** (1 nodes): `Hamilton (cross) product q1 ⊗ q2 for tensors of shape [..., 4].`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Isolated Rationale`** (1 nodes): `Unit-normalise quaternion tensors.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Isolated Rationale`** (1 nodes): `Apply a Berry-phase rotation around the w-axis of the quaternion manifold.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Isolated Rationale`** (1 nodes): `Autoregressive generation with ACT-driven early stopping.          The model sto`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Isolated Rationale`** (1 nodes): `Surprise = cross-entropy × (1 - gate_mean), clipped to [0, 10].          A high`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Isolated Rationale`** (1 nodes): `Run swarm inference and return the decoded output string.          Args:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Isolated Rationale`** (1 nodes): `Compute mean validation loss over the first EVAL_INTERVAL_STEPS batches.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Isolated Rationale`** (1 nodes): `Producto de Hamilton q1 ⊗ q2. Ambos [..., 4].`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Isolated Rationale`** (1 nodes): `Rota vector 3D v por cuaternión unitario q. v:[...,3] q:[...,4]`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Isolated Rationale`** (1 nodes): `Generacion autoregresiva con KV cache y muestreo top-k.         En el primer pas`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Isolated Rationale`** (1 nodes): `Genera una muestra de texto al final de cada epoch para monitorear         la ca`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BPETokenizer` connect `TopoGPT2 Tokenizer & Corpus` to `TopoGPT2 Quaternion Attention`, `SwarmAgent BPE Tokenizer`, `LazyOwn Dataset Pipeline`?**
  _High betweenness centrality (0.137) - this node is a cross-community bridge._
- **Why does `SwarmConfig` connect `SwarmAgent BPE Tokenizer` to `Inference Engine`, `LazyOwn Dataset Pipeline`, `Tool Registry & Swarm Trainer`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **Why does `build_model_and_tok()` connect `LazyOwn Dataset Pipeline` to `TopoGPT2 Tokenizer & Corpus`, `SwarmAgent BPE Tokenizer`, `TopoGPT2 Checkpoint Manager`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `SwarmTrainer` (e.g. with `LazyOwnBridge` and `LazyOwnToolRegistry`) actually correct?**
  _`SwarmTrainer` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `CheckpointManager` (e.g. with `._load()` and `.__init__()`) actually correct?**
  _`CheckpointManager` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `ToolResult` (e.g. with `LazyOwnBridge` and `LazyOwnToolRegistry`) actually correct?**
  _`ToolResult` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `main()` (e.g. with `build_dataset()` and `write_jsonl()`) actually correct?**
  _`main()` has 3 INFERRED edges - model-reasoned connections that need verification._