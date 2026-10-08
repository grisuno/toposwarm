# root: topo_swarm_agent

*Community 0 | 5 files | cohesion 0.75*

## Definition

This community groups 5 file(s) rooted at `root` with dominant language py (cohesion 0.75). Central symbols: `BPETokenizer`, `CheckpointManager`, `ContinualConfig`, `ContinualTrainer`, `EWC`, `EpisodicMemory`, `HRMModule`, `KappaDetector`. Core file: `topo_swarm_agent.py` (104 symbols). Documented purpose: Debug _routing_accuracy by calling it directly on a ContinualTrainer.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `debug_routing.py` | py | utility | 1 | yes |
| `diagnose_accuracy.py` | py | utility | 2 | yes |
| `topo_swarm_agent.py` | py | utility | 104 | yes |
| `toposwarm_continual_trainer.py` | py | utility | 51 | yes |
| `ts_utils.py` | py | utility | 7 | yes |

## Key Symbols

- `_import` (function, `debug_routing.py:14`) `def _import(name, filename)`
- `load_model` (function, `diagnose_accuracy.py:13`) `def load_model()`
- `main` (function, `diagnose_accuracy.py:33`) `def main()`
- `SwarmConfig` (class, `topo_swarm_agent.py:85`) `class SwarmConfig` - All architectural and training hyper-parameters in one place.
- `__post_init__` (method, `topo_swarm_agent.py:212`) `def __post_init__(self)`
- `_setup_logger` (method, `topo_swarm_agent.py:265`) `def _setup_logger(name, level)` - Return an idempotent logger. Delegates to ts_utils.setup_logger.
- `_set_seed` (method, `topo_swarm_agent.py:283`) `def _set_seed(seed, device)` - Deterministic seed across torch, numpy, and CUDA.
- `_param_count` (method, `topo_swarm_agent.py:293`) `def _param_count(module)` - Return total and trainable parameter counts.
- `_get_torus_positions` (method, `topo_swarm_agent.py:304`) `def _get_torus_positions(n_angular, n_radial, device)` - Cached angular / radial position linspaces for soft torus assignment.
- `QuaternionOps` (class, `topo_swarm_agent.py:322`) `class QuaternionOps` - Pure-functional quaternion operations over arbitrary leading batch dims.
- `hamilton_product` (method, `topo_swarm_agent.py:329`) `def hamilton_product(q1, q2)` - Hamilton (cross) product q1 ⊗ q2 for tensors of shape [..., 4].
- `normalize` (method, `topo_swarm_agent.py:344`) `def normalize(q, eps)` - Unit-normalise quaternion tensors.
- `berry_phase_rotation` (method, `topo_swarm_agent.py:349`) `def berry_phase_rotation(q, phase)` - Apply a Berry-phase rotation around the w-axis of the quaternion manifold.
- `QuaternionLinear` (class, `topo_swarm_agent.py:370`) `class QuaternionLinear(Module)` - Linear map in the quaternion algebra.
- `__init__` (method, `topo_swarm_agent.py:381`) `def __init__(self, in_features, out_features, bias, init_std)` - Initialise quaternion weight matrices.
- `forward` (method, `topo_swarm_agent.py:410`) `def forward(self, x)` - Fused Hamilton product via a single batched einsum.
- `SpectralBottleneck` (class, `topo_swarm_agent.py:434`) `class SpectralBottleneck(Module)` - 1-D spectral autoencoder acting as the function-call signal filter.
- `__init__` (method, `topo_swarm_agent.py:446`) `def __init__(self, cfg)` - Build encoder/decoder spectral kernels and quaternion projections.
- `_filter` (method, `topo_swarm_agent.py:468`) `def _filter(self, x, kr, ki)` - Apply a learned complex spectral filter in the rfft domain.
- `forward` (method, `topo_swarm_agent.py:476`) `def forward(self, x)` - Encode x through the spectral bottleneck.
- `RMSNorm` (class, `topo_swarm_agent.py:505`) `class RMSNorm(Module)` - Root Mean Square Layer Normalisation (LLaMA-style, no bias).
- `__init__` (method, `topo_swarm_agent.py:508`) `def __init__(self, d_model, eps)` - Args:
- `forward` (method, `topo_swarm_agent.py:518`) `def forward(self, x)` - Normalise by the RMS of x and rescale by learned weight.
- `RotaryEmbedding` (class, `topo_swarm_agent.py:529`) `class RotaryEmbedding(Module)` - NTK-aware Rotary Position Embeddings.
- `__init__` (method, `topo_swarm_agent.py:537`) `def __init__(self, d_head, max_seq_len, base, ntk_factor)` - Args:
- `_build_cache` (method, `topo_swarm_agent.py:562`) `def _build_cache(self, seq_len)` - Pre-compute cos/sin tables up to seq_len.
- `_rotate_half` (method, `topo_swarm_agent.py:570`) `def _rotate_half(self, x)`
- `forward` (method, `topo_swarm_agent.py:574`) `def forward(self, x, seq_len)` - Apply rotary embedding to query or key tensor [B, H, S, d_head].
- `SwiGLU` (class, `topo_swarm_agent.py:588`) `class SwiGLU(Module)` - SwiGLU feed-forward: SiLU(gate(x)) * up(x) → down(...).
- `__init__` (method, `topo_swarm_agent.py:591`) `def __init__(self, d_model, hidden_dim, dropout)` - Args:

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 7
- Cross-boundary resolved imports (EXTRACTED): 2

## Connections

- [EXTRACTED] depends_on community 1 <-> 0 (strength 0.9): Extracted import edge crosses communities: toposwarm_coevolve.py imports topo_swarm_agent.py.
- [EXTRACTED] depends_on community 2 <-> 0 (strength 0.9): Extracted import edge crosses communities: toposwarm_lazyown_sweep.py imports topo_swarm_agent.py.
- [INFERRED] bridges community 0 <-> 1 (strength 0.6): Inferred cross-community bridge: debug_routing.py reaches meta_harness_proposer.py in 4 hops.
- [INFERRED] bridges community 0 <-> 2 (strength 0.6): Inferred cross-community bridge: debug_routing.py reaches tests/test_orchestrator.py in 4 hops.
- [INFERRED] bridges community 0 <-> 1 (strength 0.6): Inferred cross-community bridge: diagnose_accuracy.py reaches meta_harness_proposer.py in 4 hops.
- [INFERRED] bridges community 1 <-> 0 (strength 0.5): Inferred cross-community bridge: meta_harness_proposer.py reaches toposwarm_continual_trainer.py in 5 hops.
- [INFERRED] bridges community 2 <-> 0 (strength 0.5): Inferred cross-community bridge: tests/test_orchestrator.py reaches toposwarm_continual_trainer.py in 5 hops.
- [INFERRED] shares_context community 0 <-> 3 (strength 0.5): Inferred shared context (language py and layer utility) with no import path between community 0 (root: topo_swarm_agent) and community 3 (orphans).

## Risks

- [taint high] `toposwarm_coevolve.py` -> `topo_swarm_agent.py` via `subprocess` (1 hops)
- [taint high] `toposwarm_coevolve.py` -> `ts_utils.py` via `subprocess` (2 hops)

## Open Questions

- What would break if the most connected file in root: topo_swarm_agent changed?
- Should root: topo_swarm_agent be split, given cohesion 0.75?

## Sources

- `debug_routing.py`
- `diagnose_accuracy.py`
- `topo_swarm_agent.py`
- `toposwarm_continual_trainer.py`
- `ts_utils.py`
