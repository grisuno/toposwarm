# root: toposwarm_lazyown_orchestrator

*Community 2 | 3 files | cohesion 0.50*

## Definition

This community groups 3 file(s) rooted at `root` with dominant language py (cohesion 0.50). Central symbols: `LazyOwnOrchestrator`, `LazyOwnToolRegistry`, `SessionContext`, `TestKeywordRouter`, `TestNeuralRouter`, `TestOrchestratorRun`, `TestSessionContext`, `__init__`. Core file: `toposwarm_lazyown_orchestrator.py` (77 symbols). Documented purpose: Tests for LazyOwn orchestrator improvements..

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_orchestrator.py` | py | testing | 25 | yes |
| `toposwarm_lazyown_orchestrator.py` | py | utility | 77 | yes |
| `toposwarm_lazyown_sweep.py` | py | utility | 5 | yes |

## Key Symbols

- `TestSessionContext` (class, `tests/test_orchestrator.py:15`) `class TestSessionContext` - Unit tests for the multi-turn SessionContext.
- `_load_ctx` (method, `tests/test_orchestrator.py:18`) `def _load_ctx(self)`
- `test_empty_prefix` (method, `tests/test_orchestrator.py:23`) `def test_empty_prefix(self)`
- `test_prefix_with_target` (method, `tests/test_orchestrator.py:28`) `def test_prefix_with_target(self)`
- `test_update_extracts_ip` (method, `tests/test_orchestrator.py:35`) `def test_update_extracts_ip(self)`
- `test_phase_progression` (method, `tests/test_orchestrator.py:43`) `def test_phase_progression(self)`
- `test_findings_from_output` (method, `tests/test_orchestrator.py:49`) `def test_findings_from_output(self)`
- `TestKeywordRouter` (class, `tests/test_orchestrator.py:56`) `class TestKeywordRouter` - Tests for the deterministic keyword fallback router.
- `_load_router` (method, `tests/test_orchestrator.py:59`) `def _load_router(self)`
- `test_recon_keyword` (method, `tests/test_orchestrator.py:63`) `def test_recon_keyword(self)`
- `test_config_keyword` (method, `tests/test_orchestrator.py:69`) `def test_config_keyword(self)`
- `test_c2_keyword` (method, `tests/test_orchestrator.py:74`) `def test_c2_keyword(self)`
- `test_fallback_search` (method, `tests/test_orchestrator.py:79`) `def test_fallback_search(self)`
- `test_extract_arg_ip` (method, `tests/test_orchestrator.py:84`) `def test_extract_arg_ip(self)`
- `TestNeuralRouter` (class, `tests/test_orchestrator.py:89`) `class TestNeuralRouter` - Tests for the neural route path using mocks.
- `orchestrator` (method, `tests/test_orchestrator.py:93`) `def orchestrator(self)`
- `test_neural_route_none_when_no_engine` (method, `tests/test_orchestrator.py:120`) `def test_neural_route_none_when_no_engine(self, orchestrator)`
- `test_neural_route_with_mock_head` (method, `tests/test_orchestrator.py:123`) `def test_neural_route_with_mock_head(self, orchestrator)`
- `mock_register_forward_hook` (method, `tests/test_orchestrator.py:135`) `def mock_register_forward_hook(cb)`
- `mock_model_forward` (method, `tests/test_orchestrator.py:141`) `def mock_model_forward(ids)`
- `test_neural_route_low_confidence_fallback` (method, `tests/test_orchestrator.py:159`) `def test_neural_route_low_confidence_fallback(self, orchestrator)`
- `mock_register_forward_hook` (method, `tests/test_orchestrator.py:169`) `def mock_register_forward_hook(cb)`
- `mock_model_forward` (method, `tests/test_orchestrator.py:175`) `def mock_model_forward(ids)`
- `TestOrchestratorRun` (class, `tests/test_orchestrator.py:193`) `class TestOrchestratorRun` - Integration-level tests for the run() method.
- `test_run_updates_session` (method, `tests/test_orchestrator.py:196`) `def test_run_updates_session(self)`
- `_import_infer` (function, `toposwarm_lazyown_orchestrator.py:60`) `def _import_infer()`
- `_import_agent` (function, `toposwarm_lazyown_orchestrator.py:80`) `def _import_agent()`
- `_import_meta_harness` (function, `toposwarm_lazyown_orchestrator.py:95`) `def _import_meta_harness()`
- `_import_routing_head` (function, `toposwarm_lazyown_orchestrator.py:114`) `def _import_routing_head()`
- `_import_lazyown_bridge` (function, `toposwarm_lazyown_orchestrator.py:134`) `def _import_lazyown_bridge()`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 5
- Cross-boundary resolved imports (EXTRACTED): 3

## Connections

- [EXTRACTED] depends_on community 1 <-> 2 (strength 0.9): Extracted import edge crosses communities: toposwarm_coevolve.py imports toposwarm_lazyown_orchestrator.py.
- [EXTRACTED] depends_on community 2 <-> 0 (strength 0.9): Extracted import edge crosses communities: toposwarm_lazyown_sweep.py imports topo_swarm_agent.py.
- [INFERRED] bridges community 0 <-> 2 (strength 0.6): Inferred cross-community bridge: debug_routing.py reaches tests/test_orchestrator.py in 4 hops.
- [INFERRED] bridges community 2 <-> 0 (strength 0.5): Inferred cross-community bridge: tests/test_orchestrator.py reaches toposwarm_continual_trainer.py in 5 hops.
- [INFERRED] shares_context community 2 <-> 3 (strength 0.5): Inferred shared context (language py and layer utility) with no import path between community 2 (root: toposwarm_lazyown_orchestrator) and community 3 (orphans).

## Risks

- [taint high] `toposwarm_coevolve.py` -> `toposwarm_lazyown_orchestrator.py` via `subprocess` (1 hops)
- [taint high] `toposwarm_lazyown_orchestrator.py` -> `toposwarm_lazyown_orchestrator.py` via `subprocess` (0 hops)
- [taint high] `toposwarm_lazyown_sweep.py` -> `toposwarm_lazyown_sweep.py` via `subprocess` (0 hops)
- [dataflow UNCHECKED_ALLOC] `toposwarm_lazyown_orchestrator.py:1279` `main` `n_examples`: Result of allocator stored in `n_examples` is never checked against NULL.

## Open Questions

- Is the dangerous import `subprocess` in `toposwarm_lazyown_orchestrator.py` still required, or can it be isolated?
- What would break if the most connected file in root: toposwarm_lazyown_orchestrator changed?
- Should root: toposwarm_lazyown_orchestrator be split, given cohesion 0.50?

## Sources

- `tests/test_orchestrator.py`
- `toposwarm_lazyown_orchestrator.py`
- `toposwarm_lazyown_sweep.py`
