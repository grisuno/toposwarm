# Gotchas

## God Nodes (high connectivity)

These files have the most connections. Changes here have high blast radius.

- `topo_swarm_agent.py` (score: 20.40, imported by 4 files)
- `toposwarm_lazyown_orchestrator.py` (score: 13.70, imported by 3 files)
- `topogpt2_1.py` (score: 12.60)
- `toposwarm_coevolve.py` (score: 11.30)
- `neurologos_tricameral_loss2.7.py` (score: 10.00)
- `toposwarm_meta_harness.py` (score: 9.60, imported by 2 files)
- `ts_utils.py` (score: 8.70, imported by 4 files)
- `toposwarm_continual_trainer.py` (score: 7.10)
- `toposwarm_infer.py` (score: 5.70, imported by 1 files)
- `toposwarm_hybrid.py` (score: 4.80)

## Blast Radius (change impact)

Editing these files can break the listed number of dependents. Run their tests after any change.

- `ts_utils.py` -- 4 direct, 6 total dependents
- `topo_swarm_agent.py` -- 4 direct, 4 total dependents
- `toposwarm_lazyown_orchestrator.py` -- 3 direct, 3 total dependents
- `toposwarm_meta_harness.py` -- 2 direct, 2 total dependents
- `toposwarm_infer.py` -- 1 direct, 1 total dependents

## Hotspots (complexity + centrality)

- `topo_swarm_agent.py` -- complexity: 0.8, centrality: 1.0, combined: 0.9
- `neurologos_tricameral_loss2.7.py` -- complexity: 0.8, centrality: 1.0, combined: 0.9
- `topogpt2_1.py` -- complexity: 1.0, centrality: 0.7, combined: 0.8
- `toposwarm_lazyown_orchestrator.py` -- complexity: 0.6, centrality: 0.9, combined: 0.8
- `toposwarm_meta_harness.py` -- complexity: 0.4, centrality: 0.9, combined: 0.7
- `toposwarm_coevolve.py` -- complexity: 0.3, centrality: 0.9, combined: 0.6
- `toposwarm_infer.py` -- complexity: 0.3, centrality: 0.8, combined: 0.6
- `toposwarm_hybrid.py` -- complexity: 0.4, centrality: 0.8, combined: 0.6
- `toposwarm_continual_trainer.py` -- complexity: 0.4, centrality: 0.6, combined: 0.5
- `lazyown_bridge.py` -- complexity: 0.4, centrality: 0.5, combined: 0.5

## Dataflow Issues (INFERRED, review each lead)

- `neurologos_tricameral_loss2.7.py:2308` `__getitem__` [UNCHECKED_ALLOC] `image`: Result of allocator stored in `image` is never checked against NULL.
- `test_full_pipeline.py:79` `step1_regenerate_dataset` [UNCHECKED_ALLOC] `lines`: Result of allocator stored in `lines` is never checked against NULL.
- `toposwarm_lazyown_orchestrator.py:1279` `main` [UNCHECKED_ALLOC] `n_examples`: Result of allocator stored in `n_examples` is never checked against NULL.
