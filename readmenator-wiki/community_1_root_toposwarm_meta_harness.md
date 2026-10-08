# root: toposwarm_meta_harness

*Community 1 | 4 files | cohesion 0.60*

## Definition

This community groups 4 file(s) rooted at `root` with dominant language py (cohesion 0.60). Central symbols: `CoEvolutionEngine`, `DenseMemoryRetriever`, `DraftVerifier`, `EnvironmentBootstrapper`, `ExperienceReader`, `HarnessEvaluator`, `HarnessMutation`, `InferenceConfig`. Core file: `toposwarm_meta_harness.py` (56 symbols). Documented purpose: Meta-Harness Proposer: Coding-Agent that diagnoses harness failures and edits code..

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `meta_harness_proposer.py` | py | utility | 24 | yes |
| `toposwarm_coevolve.py` | py | utility | 33 | yes |
| `toposwarm_infer.py` | py | utility | 37 | yes |
| `toposwarm_meta_harness.py` | py | utility | 56 | yes |

## Key Symbols

- `_setup_logger` (function, `meta_harness_proposer.py:58`) `def _setup_logger(name, level)`
- `LLMConfig` (class, `meta_harness_proposer.py:75`) `class LLMConfig`
- `LLMClient` (class, `meta_harness_proposer.py:86`) `class LLMClient` - Minimal OpenAI-compatible chat client using only urllib.
- `__init__` (method, `meta_harness_proposer.py:93`) `def __init__(self, cfg, logger)`
- `_try_chat` (method, `meta_harness_proposer.py:97`) `def _try_chat(self, api_url, model, system, user)`
- `chat` (method, `meta_harness_proposer.py:121`) `def chat(self, system, user)` - Send a chat request and return the assistant message content.
- `ExperienceReader` (class, `meta_harness_proposer.py:150`) `class ExperienceReader` - Reads meta_harness_logs/ and builds diagnostic context.
- `__init__` (method, `meta_harness_proposer.py:153`) `def __init__(self, log_dir, logger)`
- `list_runs` (method, `meta_harness_proposer.py:157`) `def list_runs(self, n)`
- `load_run` (method, `meta_harness_proposer.py:165`) `def load_run(self, run_dir)`
- `build_diagnostic_context` (method, `meta_harness_proposer.py:193`) `def build_diagnostic_context(self, top_k)` - Build a rich diagnostic string containing:
- `PatchEngine` (class, `meta_harness_proposer.py:243`) `class PatchEngine` - Applies code patches safely.
- `__init__` (method, `meta_harness_proposer.py:246`) `def __init__(self, logger)`
- `validate_syntax` (method, `meta_harness_proposer.py:249`) `def validate_syntax(self, code)` - Return (ok, error_message).
- `apply_full_rewrite` (method, `meta_harness_proposer.py:265`) `def apply_full_rewrite(self, target_path, new_code, dry_run)` - Validate and optionally write a full file rewrite.
- `_strip_line_numbers` (method, `meta_harness_proposer.py:283`) `def _strip_line_numbers(self, s)` - Remove leading ' 123: ' line numbers that the LLM may copy.
- `apply_line_range` (method, `meta_harness_proposer.py:287`) `def apply_line_range(self, target_path, line_start, line_end, new_string, dry_ru` - Replace a range of lines (1-indexed) with new text.
- `apply_diff_hunk` (method, `meta_harness_proposer.py:316`) `def apply_diff_hunk(self, target_path, old_string, new_string, dry_run)` - Apply a targeted string replacement after validation.
- `_norm` (method, `meta_harness_proposer.py:331`) `def _norm(s)`
- `MetaHarnessProposer` (class, `meta_harness_proposer.py:392`) `class MetaHarnessProposer` - Coding-agent proposer for harness optimisation.
- `__init__` (method, `meta_harness_proposer.py:434`) `def __init__(self, log_dir, llm_cfg, logger)`
- `propose_patch` (method, `meta_harness_proposer.py:445`) `def propose_patch(self, target_path, top_k, dry_run)` - End-to-end propose-and-apply cycle.
- `_log_proposal` (method, `meta_harness_proposer.py:538`) `def _log_proposal(self, target_path, response, applied, diag)` - Store the proposer's reasoning so future loops can evaluate it.
- `main` (method, `meta_harness_proposer.py:572`) `def main()`
- `_resolve_lazyown_dir` (function, `toposwarm_coevolve.py:63`) `def _resolve_lazyown_dir()` - Discover LazyOwn installation directory.
- `_setup_logger` (function, `toposwarm_coevolve.py:90`) `def _setup_logger(name, level)`
- `HarnessMutation` (class, `toposwarm_coevolve.py:128`) `class HarnessMutation` - Simple mutation operators over MetaHarnessConfig dicts.
- `mutate` (method, `toposwarm_coevolve.py:132`) `def mutate(cfg_dict)`
- `crossover` (method, `toposwarm_coevolve.py:167`) `def crossover(a, b)`
- `_clip` (method, `toposwarm_coevolve.py:175`) `def _clip(x, lo, hi)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 4
- Cross-boundary resolved imports (EXTRACTED): 3

## Connections

- [EXTRACTED] depends_on community 1 <-> 2 (strength 0.9): Extracted import edge crosses communities: toposwarm_coevolve.py imports toposwarm_lazyown_orchestrator.py.
- [EXTRACTED] depends_on community 1 <-> 0 (strength 0.9): Extracted import edge crosses communities: toposwarm_coevolve.py imports topo_swarm_agent.py.
- [INFERRED] bridges community 0 <-> 1 (strength 0.6): Inferred cross-community bridge: debug_routing.py reaches meta_harness_proposer.py in 4 hops.
- [INFERRED] bridges community 0 <-> 1 (strength 0.6): Inferred cross-community bridge: diagnose_accuracy.py reaches meta_harness_proposer.py in 4 hops.
- [INFERRED] bridges community 1 <-> 0 (strength 0.5): Inferred cross-community bridge: meta_harness_proposer.py reaches toposwarm_continual_trainer.py in 5 hops.
- [INFERRED] shares_context community 1 <-> 3 (strength 0.5): Inferred shared context (language py and layer utility) with no import path between community 1 (root: toposwarm_meta_harness) and community 3 (orphans).

## Risks

- [taint medium] `meta_harness_proposer.py` -> `meta_harness_proposer.py` via `compile` (0 hops)
- [taint medium] `meta_harness_proposer.py` -> `toposwarm_meta_harness.py` via `compile` (1 hops)
- [taint medium] `meta_harness_proposer.py` -> `meta_harness_proposer.py` via `urllib.request` (0 hops)
- [taint medium] `meta_harness_proposer.py` -> `toposwarm_meta_harness.py` via `urllib.request` (1 hops)
- [taint high] `toposwarm_coevolve.py` -> `toposwarm_coevolve.py` via `subprocess` (0 hops)
- [taint high] `toposwarm_coevolve.py` -> `toposwarm_meta_harness.py` via `subprocess` (1 hops)
- [taint high] `toposwarm_coevolve.py` -> `toposwarm_infer.py` via `subprocess` (1 hops)
- [taint high] `toposwarm_coevolve.py` -> `topo_swarm_agent.py` via `subprocess` (1 hops)
- [taint high] `toposwarm_coevolve.py` -> `toposwarm_lazyown_orchestrator.py` via `subprocess` (1 hops)
- [taint high] `toposwarm_coevolve.py` -> `ts_utils.py` via `subprocess` (2 hops)
- [taint medium] `toposwarm_infer.py` -> `toposwarm_infer.py` via `urllib.request` (0 hops)

## Open Questions

- Is the dangerous import `compile` in `meta_harness_proposer.py` still required, or can it be isolated?
- What would break if the most connected file in root: toposwarm_meta_harness changed?
- Should root: toposwarm_meta_harness be split, given cohesion 0.60?

## Sources

- `meta_harness_proposer.py`
- `toposwarm_coevolve.py`
- `toposwarm_infer.py`
- `toposwarm_meta_harness.py`
