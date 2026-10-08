# Second Brain

*Last synthesized: 2026-10-07 | 23 files | 4 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `topo_swarm_agent.py`, `toposwarm_lazyown_orchestrator.py`, `topogpt2_1.py`. Architecturally it is 3 layers, dominant utility (16 files) across 4 import-based communities. Recorded risk surface: 0 security findings and 0 dependency cycles.

Surprising tissue lives between root: topo_swarm_agent, root: toposwarm_meta_harness, root: toposwarm_lazyown_orchestrator: 3 extracted cross-community imports and 8 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (100% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 23 |
| Symbols | 793 |
| Resolved imports | 20 |
| Languages | py |
| Communities | 4 |
| Doc coverage | 100% (23/23 files) |
| Security findings | 0 |
| Estimated read cost | ~24727 tokens (chars/4, offline so $0) |

## Reading Order

1. Skim Stats and God Nodes below for blast radius.
2. Open the largest community page first, then follow Connections.
3. Use `queries.md` for the next question; log the answer there.

```
grep -rn '<keyword>' index.md community_*.md
readmenator query "<question>" --target readmenator_toposwarm_e1vkmkeq
```

## Concept Wiki

- [root: topo_swarm_agent (5 files, cohesion 0.75)](./community_0_root_topo_swarm_agent.md)
- [root: toposwarm_meta_harness (4 files, cohesion 0.60)](./community_1_root_toposwarm_meta_harness.md)
- [root: toposwarm_lazyown_orchestrator (3 files, cohesion 0.50)](./community_2_root_toposwarm_lazyown_orchestrator.md)
- [orphans (11 files, cohesion 0.00)](./community_3_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `topo_swarm_agent.py` | 20.4 |
| `toposwarm_lazyown_orchestrator.py` | 13.7 |
| `topogpt2_1.py` | 12.6 |
| `toposwarm_coevolve.py` | 11.3 |
| `neurologos_tricameral_loss2.7.py` | 10.0 |

## Strongest Connections

- 1 -> 2: depends_on (strength 0.9, EXTRACTED)
- 1 -> 0: depends_on (strength 0.9, EXTRACTED)
- 2 -> 0: depends_on (strength 0.9, EXTRACTED)
- 0 -> 1: bridges (strength 0.6, INFERRED)
- 0 -> 2: bridges (strength 0.6, INFERRED)
- 0 -> 1: bridges (strength 0.6, INFERRED)
- 1 -> 0: bridges (strength 0.5, INFERRED)
- 2 -> 0: bridges (strength 0.5, INFERRED)
- 0 -> 3: shares_context (strength 0.5, INFERRED)
- 1 -> 3: shares_context (strength 0.5, INFERRED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
