# Polyglot Codebase Knowledge Graph

> Generated offline by **readmenator**. Supports C, C++, Python, Go, Rust, JS/TS, Java, C#, Shell, PHP, Dart, GDScript, Nim, ASM, Ruby, Swift, Kotlin, Scala, Lua, Elixir.
> No LLMs. No tokens. Pure static analysis. See more [here](https://github.com/grisuno/ReadMenator)

**Total Files Parsed:** 17 | **Total Symbols Extracted:** 636 | **Total Imports:** 258
 | **Resolved Imports:** 16

<!-- ranking_model: v1.0 | weights: {ppr:0.45,auth:0.2,test:0.15,doc:0.1,fresh:0.1} | alpha:0.85 | commit:75d209c | date:2026-07-18 -->


## Table of Contents

1. [Statistics Dashboard](#statistics-dashboard)
2. [Architectural Layers](#architectural-layers)
3. [Ranked Context](#ranked-context)
4. [God Nodes](#god-nodes)
5. [Community Analysis](#community-analysis)
6. [Surprising Connections](#surprising-connections)
7. [Suggested Questions](#suggested-questions)
8. [Taint Propagation Map](#taint-propagation-map)
9. [Hotspot Analysis](#hotspot-analysis)
10. [Change Impact Analysis](#change-impact-analysis)
11. [Suggested Linting Rules](#suggested-linting-rules)
12. [Orphans](#orphans)
13. [Query Recipes](#query-recipes)
14. [Structural Knowledge Map](#structural-knowledge-map)
15. [UML Class Diagram](#uml-class-diagram)
16. [Code Property Graph](#code-property-graph)
17. [Architecture Reference](#architecture-reference)
    - [PY (17 files)](#py-17-files)

---

## Statistics Dashboard

| Metric | Value |
|--------|-------|
| Total Files | 17 |
| Total Symbols | 636 |
| Total Imports | 258 |
| Call Edges | 4865 |
| Inheritance Edges | 30 |
| Languages | 1 |
| Avg Symbols/File | 37.4 |
| Avg Imports/File | 15.2 |
| Resolved Imports | 16 |

### Top Files by Import Count (Fan-Out)

| File | Imports | Symbols | Language |
|------|---------|---------|----------|
| `toposwarm_lazyown_orchestrator.py` | 27 | 83 | py |
| `topo_swarm_agent.py` | 26 | 104 | py |
| `toposwarm_infer.py` | 25 | 37 | py |
| `toposwarm_meta_harness.py` | 25 | 54 | py |
| `toposwarm_hybrid.py` | 24 | 48 | py |
| `topogpt2_1.py` | 22 | 126 | py |
| `toposwarm_coevolve.py` | 20 | 33 | py |
| `toposwarm_continual_trainer.py` | 18 | 51 | py |
| `meta_harness_proposer.py` | 15 | 24 | py |
| `test_orchestrator.py` | 12 | 25 | py |

---

## Architectural Layers

Auto-detected from path patterns, naming conventions, and imported frameworks.

| Layer | Files |
|-------|-------|
| utility | 11 |
| testing | 4 |
| data_access | 2 |

### data_access

- `lazyown_dataset_enhancer.py` (py, 19 symbols)
- `lazyown_dataset_generator.py` (py, 8 symbols)

### utility

- `meta_harness_proposer.py` (py, 24 symbols)
- `topo_swarm_agent.py` (py, 104 symbols)
- `topogpt2_1.py` (py, 126 symbols)
- `toposwarm_coevolve.py` (py, 33 symbols)
- `toposwarm_continual_trainer.py` (py, 51 symbols)
- `toposwarm_hybrid.py` (py, 48 symbols)
- `toposwarm_infer.py` (py, 37 symbols)
- `toposwarm_lazyown_orchestrator.py` (py, 83 symbols)
- `toposwarm_lazyown_sweep.py` (py, 5 symbols)
- `toposwarm_meta_harness.py` (py, 54 symbols)
- `ts_utils.py` (py, 7 symbols)

### testing

- `test_dataset_enhancer.py` (py, 6 symbols)
- `test_dataset_generator.py` (py, 5 symbols)
- `test_model_config.py` (py, 1 symbols)
- `test_orchestrator.py` (py, 25 symbols)

---

## Ranked Context

Files ranked by composite score for the current query context. The ranking combines Personalized PageRank (query relevance), global authority, test coverage, documentation coverage, and code freshness. Model: v1.0.

| Rank | File | Composite | PPR | Authority | Test | Doc |
|------|------|-----------|-----|-----------|------|-----|
| 1 | `ts_utils.py` | 0.2042 | 0.2042 | 0.2042 | 0.00 | 0.71 |
| 2 | `topo_swarm_agent.py` | 0.1557 | 0.1005 | 0.1005 | 0.00 | 0.90 |
| 3 | `toposwarm_meta_harness.py` | 0.1483 | 0.1369 | 0.1369 | 0.00 | 0.59 |
| 4 | `toposwarm_infer.py` | 0.1395 | 0.0733 | 0.0733 | 0.00 | 0.92 |
| 5 | `toposwarm_lazyown_orchestrator.py` | 0.1260 | 0.1642 | 0.1642 | 0.00 | 0.19 |
| 6 | `toposwarm_lazyown_sweep.py` | 0.1017 | 0.0642 | 0.0642 | 0.00 | 0.60 |
| 7 | `meta_harness_proposer.py` | 0.0959 | 0.0642 | 0.0642 | 0.00 | 0.54 |
| 8 | `toposwarm_continual_trainer.py` | 0.0809 | 0.0642 | 0.0642 | 0.00 | 0.39 |
| 9 | `toposwarm_coevolve.py` | 0.0720 | 0.0642 | 0.0642 | 0.00 | 0.30 |
| 10 | `toposwarm_hybrid.py` | 0.0604 | 0.0000 | 0.0000 | 0.00 | 0.60 |

---

## God Nodes

Most architecturally central files ranked by combined import/export degree and symbol richness.

| File | Score | Connections | PageRank |
|------|-------|-------------|----------|
| `topo_swarm_agent.py` | 16.4 | | 0.1005 |
| `toposwarm_lazyown_orchestrator.py` | 14.3 | | 0.1642 |
| `topogpt2_1.py` | 12.6 | | 0.0000 |
| `toposwarm_coevolve.py` | 11.3 | | 0.0642 |
| `toposwarm_meta_harness.py` | 9.4 | | 0.1369 |
| `toposwarm_continual_trainer.py` | 7.1 | | 0.0642 |
| `toposwarm_infer.py` | 5.7 | | 0.0733 |
| `toposwarm_hybrid.py` | 4.8 | | 0.0000 |
| `ts_utils.py` | 4.7 | | 0.2042 |
| `test_orchestrator.py` | 4.5 | | 0.0000 |

---

## Community Analysis

Files grouped by import-based community detection. Cohesion measures how tightly connected each community is internally.

### root (Cohesion: 0.50)

**2 files** in this community:

- `meta_harness_proposer.py` (py, 24 symbols)
- `toposwarm_meta_harness.py` (py, 54 symbols)

### root (Cohesion: 0.75)

**6 files** in this community:

- `test_orchestrator.py` (py, 25 symbols)
- `topo_swarm_agent.py` (py, 104 symbols)
- `toposwarm_coevolve.py` (py, 33 symbols)
- `toposwarm_infer.py` (py, 37 symbols)
- `toposwarm_lazyown_orchestrator.py` (py, 83 symbols)
- `toposwarm_lazyown_sweep.py` (py, 5 symbols)

### root (Cohesion: 0.50)

**2 files** in this community:

- `toposwarm_continual_trainer.py` (py, 51 symbols)
- `ts_utils.py` (py, 7 symbols)

---

## Surprising Connections

Files in different communities connected through 3+ indirect hops.

- `meta_harness_proposer.py` <-> `toposwarm_continual_trainer.py` (5 hops, across 3 communities)
- `test_orchestrator.py` <-> `toposwarm_continual_trainer.py` (5 hops, across 2 communities)
- `meta_harness_proposer.py` <-> `test_orchestrator.py` (4 hops, across 2 communities)
- `meta_harness_proposer.py` <-> `toposwarm_lazyown_sweep.py` (4 hops, across 2 communities)
- `meta_harness_proposer.py` <-> `ts_utils.py` (4 hops, across 3 communities)

---

## Suggested Questions

Auto-generated exploration prompts based on graph structure:

- What does topo_swarm_agent.py depend on, and what depends on it? (3 connections)
- What does toposwarm_lazyown_orchestrator.py depend on, and what depends on it? (3 connections)
- What does topogpt2_1.py depend on, and what depends on it? (0 connections)
- How are the 6 files in 'root' related to each other?
- Why are meta_harness_proposer.py and toposwarm_continual_trainer.py connected through 5 hops across 3 communities?

---

## Taint Propagation Map

Taint analysis traces how dangerous imports propagate through the codebase via transitive dependencies. Source files import dangerous modules directly; sink files receive the danger indirectly.

**Taint Sources:** 7 | **Taint Sinks:** 9 | **Propagation Paths:** 18

- `meta_harness_proposer.py` imports `compile` (0 hop to `meta_harness_proposer.py`) [medium]
  Path: meta_harness_proposer.py
- `meta_harness_proposer.py` imports `compile` (1 hop to `toposwarm_meta_harness.py`) [medium]
  Path: meta_harness_proposer.py -> toposwarm_meta_harness.py
- `meta_harness_proposer.py` imports `urllib.request` (0 hop to `meta_harness_proposer.py`) [medium]
  Path: meta_harness_proposer.py
- `meta_harness_proposer.py` imports `urllib.request` (1 hop to `toposwarm_meta_harness.py`) [medium]
  Path: meta_harness_proposer.py -> toposwarm_meta_harness.py
- `toposwarm_coevolve.py` imports `subprocess` (0 hop to `toposwarm_coevolve.py`) [high]
  Path: toposwarm_coevolve.py
- `toposwarm_coevolve.py` imports `subprocess` (1 hop to `toposwarm_lazyown_orchestrator.py`) [high]
  Path: toposwarm_coevolve.py -> toposwarm_lazyown_orchestrator.py
- `toposwarm_coevolve.py` imports `subprocess` (1 hop to `toposwarm_infer.py`) [high]
  Path: toposwarm_coevolve.py -> toposwarm_infer.py
- `toposwarm_coevolve.py` imports `subprocess` (1 hop to `topo_swarm_agent.py`) [high]
  Path: toposwarm_coevolve.py -> topo_swarm_agent.py
- `toposwarm_coevolve.py` imports `subprocess` (1 hop to `toposwarm_meta_harness.py`) [high]
  Path: toposwarm_coevolve.py -> toposwarm_meta_harness.py
- `toposwarm_coevolve.py` imports `subprocess` (2 hops to `ts_utils.py`) [high]
  Path: toposwarm_coevolve.py -> topo_swarm_agent.py -> ts_utils.py
- `toposwarm_hybrid.py` imports `urllib.request` (0 hop to `toposwarm_hybrid.py`) [medium]
  Path: toposwarm_hybrid.py
- `toposwarm_infer.py` imports `urllib.request` (0 hop to `toposwarm_infer.py`) [medium]
  Path: toposwarm_infer.py
- `toposwarm_lazyown_orchestrator.py` imports `subprocess` (0 hop to `toposwarm_lazyown_orchestrator.py`) [high]
  Path: toposwarm_lazyown_orchestrator.py
- `toposwarm_lazyown_sweep.py` imports `subprocess` (0 hop to `toposwarm_lazyown_sweep.py`) [high]
  Path: toposwarm_lazyown_sweep.py
- `toposwarm_lazyown_sweep.py` imports `subprocess` (1 hop to `toposwarm_lazyown_orchestrator.py`) [high]
  Path: toposwarm_lazyown_sweep.py -> toposwarm_lazyown_orchestrator.py
- `toposwarm_lazyown_sweep.py` imports `subprocess` (1 hop to `topo_swarm_agent.py`) [high]
  Path: toposwarm_lazyown_sweep.py -> topo_swarm_agent.py
- `toposwarm_lazyown_sweep.py` imports `subprocess` (2 hops to `ts_utils.py`) [high]
  Path: toposwarm_lazyown_sweep.py -> topo_swarm_agent.py -> ts_utils.py
- `toposwarm_meta_harness.py` imports `subprocess` (0 hop to `toposwarm_meta_harness.py`) [high]
  Path: toposwarm_meta_harness.py

---

## Hotspot Analysis

Files ranked by combined complexity (symbol count) and centrality (connection count). High-scoring files are architecturally critical and may need refactoring attention.

| File | Complexity | Centrality | Combined | Symbols | Connections |
|------|-----------|------------|----------|---------|-------------|
| `ts_utils.py` | 0.056 | 0.324 | 0.216 | 7 | 11 |
| `topo_swarm_agent.py` | 0.825 | 0.853 | 0.842 | 104 | 29 |
| `toposwarm_meta_harness.py` | 0.429 | 0.824 | 0.665 | 54 | 28 |
| `toposwarm_infer.py` | 0.294 | 0.765 | 0.576 | 37 | 26 |
| `toposwarm_lazyown_orchestrator.py` | 0.659 | 1.000 | 0.864 | 83 | 34 |
| `toposwarm_lazyown_sweep.py` | 0.040 | 0.412 | 0.263 | 5 | 14 |
| `meta_harness_proposer.py` | 0.191 | 0.471 | 0.358 | 24 | 16 |
| `toposwarm_continual_trainer.py` | 0.405 | 0.588 | 0.515 | 51 | 20 |
| `toposwarm_coevolve.py` | 0.262 | 0.765 | 0.564 | 33 | 26 |
| `toposwarm_hybrid.py` | 0.381 | 0.706 | 0.576 | 48 | 24 |
| `topogpt2_1.py` | 1.000 | 0.647 | 0.788 | 126 | 22 |
| `test_orchestrator.py` | 0.198 | 0.471 | 0.362 | 25 | 16 |
| `lazyown_dataset_enhancer.py` | 0.151 | 0.206 | 0.184 | 19 | 7 |
| `lazyown_dataset_generator.py` | 0.064 | 0.235 | 0.167 | 8 | 8 |
| `test_dataset_enhancer.py` | 0.048 | 0.088 | 0.072 | 6 | 3 |

---

## Change Impact Analysis

Files sorted by how many other files would be affected if they changed. High-impact files should be changed with caution.

| File | Direct Dependents | Transitive Dependents | Total Impact |
|------|------------------|----------------------|--------------|
| `ts_utils.py` | 2 | 2 | 4 |
| `toposwarm_lazyown_orchestrator.py` | 3 | 0 | 3 |
| `topo_swarm_agent.py` | 2 | 0 | 2 |
| `toposwarm_meta_harness.py` | 2 | 0 | 2 |
| `toposwarm_infer.py` | 1 | 0 | 1 |
| `lazyown_dataset_enhancer.py` | 0 | 0 | 0 |
| `lazyown_dataset_generator.py` | 0 | 0 | 0 |
| `meta_harness_proposer.py` | 0 | 0 | 0 |
| `test_dataset_enhancer.py` | 0 | 0 | 0 |
| `test_dataset_generator.py` | 0 | 0 | 0 |
| `test_model_config.py` | 0 | 0 | 0 |
| `test_orchestrator.py` | 0 | 0 | 0 |
| `topogpt2_1.py` | 0 | 0 | 0 |
| `toposwarm_coevolve.py` | 0 | 0 | 0 |
| `toposwarm_continual_trainer.py` | 0 | 0 | 0 |

---

## Suggested Linting Rules

Automatically suggested linting and security rules based on patterns detected in the codebase. These can be exported as Semgrep rules using the `--export-rules` flag.

| Rule ID | Severity | Description | Language | Matches |
|---------|----------|-------------|----------|---------|
| `RM001` | info | Large number of functions in py: 541 total | py | 541 |
| `RM002` | info | Print statement found (consider logging instead) | python | 49 |

---

## Orphans

Files with no documentation or low connectivity. These are candidates for documentation investment or cleanup.

- `test_dataset_enhancer.py` (6 symbols, no doc)
- `test_dataset_generator.py` (5 symbols, no doc)
- `test_model_config.py` (1 symbols, no doc)

---

## Query Recipes

Example queries you can run against this knowledge base using the ranking engine:

```
# Find files most relevant to a concept
readmenator query "Where is the import resolver implemented?"

# Rank files by relevance to a topic
readmenator query "How does documentation generation work?"

# Explain why a file ranks highly
readmenator query "explain readmenator/_documentation.py"

# Trace dependency paths with ranked context
readmenator query "path from CLI to exporter"
```

The ranking model uses the following signals:

- **Personalized PageRank** (45% weight): query-specific relevance via seed propagation
- **Global Authority** (20% weight): structural importance via standard PageRank
- **Test Coverage** (15% weight): fraction of symbols referenced in test files
- **Doc Coverage** (10% weight): presence of docstrings and file-level docs
- **Freshness** (10% weight): recent modification activity

Results include score decomposition and justification paths for each ranked item.

---

## Structural Knowledge Map

```mermaid
graph TD
    classDef mod fill:#1e1e1e,stroke:#ff6666,stroke-width:2px,color:#fff;
    classDef cls fill:#2d2d2d,stroke:#4ec9b0,stroke-width:2px,color:#fff;
    classDef fn fill:#333,stroke:#dcdcaa,stroke-width:1px,color:#dcdcaa;
    classDef ext fill:#111,stroke:#666,stroke-dasharray:5 5,color:#aaa;
    subgraph community_1 ["root"]
    topo_swarm_agent_py["topo_swarm_agent.py (py)"]
    class topo_swarm_agent_py mod;
    topo_swarm_agent_py_SwarmConfig["SwarmConfig"]
    class topo_swarm_agent_py_SwarmConfig cls;
    topo_swarm_agent_py --> topo_swarm_agent_py_SwarmConfig
    topo_swarm_agent_py__setup_logger["_setup_logger"]
    class topo_swarm_agent_py__setup_logger fn;
    topo_swarm_agent_py --> topo_swarm_agent_py__setup_logger
    topo_swarm_agent_py__set_seed["_set_seed"]
    class topo_swarm_agent_py__set_seed fn;
    topo_swarm_agent_py --> topo_swarm_agent_py__set_seed
    topo_swarm_agent_py__param_count["_param_count"]
    class topo_swarm_agent_py__param_count fn;
    topo_swarm_agent_py --> topo_swarm_agent_py__param_count
    topo_swarm_agent_py__get_torus_positions["_get_torus_positions"]
    class topo_swarm_agent_py__get_torus_positions fn;
    topo_swarm_agent_py --> topo_swarm_agent_py__get_torus_positions
    toposwarm_lazyown_orchestrator_py["toposwarm_lazyown_orchestrator.py (py)"]
    class toposwarm_lazyown_orchestrator_py mod;
    toposwarm_coevolve_py["toposwarm_coevolve.py (py)"]
    class toposwarm_coevolve_py mod;
    end
    subgraph community_0 ["root"]
    toposwarm_meta_harness_py["toposwarm_meta_harness.py (py)"]
    class toposwarm_meta_harness_py mod;
    toposwarm_infer_py["toposwarm_infer.py (py)"]
    class toposwarm_infer_py mod;
    toposwarm_hybrid_py["toposwarm_hybrid.py (py)"]
    class toposwarm_hybrid_py mod;
    topogpt2_1_py["topogpt2_1.py (py)"]
    class topogpt2_1_py mod;
    end
    subgraph community_2 ["root"]
    toposwarm_continual_trainer_py["toposwarm_continual_trainer.py (py)"]
    class toposwarm_continual_trainer_py mod;
    tests_test_orchestrator_py["test_orchestrator.py (py)"]
    class tests_test_orchestrator_py mod;
    meta_harness_proposer_py["meta_harness_proposer.py (py)"]
    class meta_harness_proposer_py mod;
    toposwarm_lazyown_sweep_py["toposwarm_lazyown_sweep.py (py)"]
    class toposwarm_lazyown_sweep_py mod;
    lazyown_dataset_generator_py["lazyown_dataset_generator.py (py)"]
    class lazyown_dataset_generator_py mod;
    ts_utils_py["ts_utils.py (py)"]
    class ts_utils_py mod;
    lazyown_dataset_enhancer_py["lazyown_dataset_enhancer.py (py)"]
    class lazyown_dataset_enhancer_py mod;
    tests_test_dataset_enhancer_py["test_dataset_enhancer.py (py)"]
    class tests_test_dataset_enhancer_py mod;
    tests_test_dataset_generator_py["test_dataset_generator.py (py)"]
    class tests_test_dataset_generator_py mod;
    tests_test_model_config_py["test_model_config.py (py)"]
    class tests_test_model_config_py mod;
    end
    meta_harness_proposer_py -- resolved_imports --> toposwarm_meta_harness_py
    tests_test_orchestrator_py -- resolved_imports --> toposwarm_lazyown_orchestrator_py
    tests_test_orchestrator_py -- resolved_imports --> toposwarm_lazyown_orchestrator_py
    tests_test_orchestrator_py -- resolved_imports --> toposwarm_lazyown_orchestrator_py
    tests_test_orchestrator_py -- resolved_imports --> toposwarm_lazyown_orchestrator_py
    topo_swarm_agent_py -- resolved_imports --> ts_utils_py
    toposwarm_coevolve_py -- resolved_imports --> toposwarm_meta_harness_py
    toposwarm_coevolve_py -- resolved_imports --> toposwarm_lazyown_orchestrator_py
    toposwarm_coevolve_py -- resolved_imports --> toposwarm_lazyown_orchestrator_py
    toposwarm_coevolve_py -- resolved_imports --> toposwarm_infer_py
    toposwarm_coevolve_py -- resolved_imports --> topo_swarm_agent_py
    toposwarm_coevolve_py -- resolved_imports --> toposwarm_meta_harness_py
    toposwarm_continual_trainer_py -- resolved_imports --> ts_utils_py
    toposwarm_continual_trainer_py -- resolved_imports --> ts_utils_py
    toposwarm_lazyown_sweep_py -- resolved_imports --> toposwarm_lazyown_orchestrator_py
    toposwarm_lazyown_sweep_py -- resolved_imports --> topo_swarm_agent_py
    ext___future__["__future__"]
    class ext___future__ ext;
    lazyown_dataset_enhancer_py -.->|imports| ext___future__
    ext_argparse["argparse"]
    class ext_argparse ext;
    lazyown_dataset_enhancer_py -.->|imports| ext_argparse
    ext_json["json"]
    class ext_json ext;
    lazyown_dataset_enhancer_py -.->|imports| ext_json
    ext_random["random"]
    class ext_random ext;
    lazyown_dataset_enhancer_py -.->|imports| ext_random
    ext_re["re"]
    class ext_re ext;
    lazyown_dataset_enhancer_py -.->|imports| ext_re
    ext_pathlib["pathlib"]
    class ext_pathlib ext;
    lazyown_dataset_enhancer_py -.->|imports| ext_pathlib
    ext_typing["typing"]
    class ext_typing ext;
    lazyown_dataset_enhancer_py -.->|imports| ext_typing
    lazyown_dataset_generator_py -.->|imports| ext___future__
    lazyown_dataset_generator_py -.->|imports| ext_argparse
    lazyown_dataset_generator_py -.->|imports| ext_json
    lazyown_dataset_generator_py -.->|imports| ext_random
    lazyown_dataset_generator_py -.->|imports| ext_re
    lazyown_dataset_generator_py -.->|imports| ext_pathlib
    lazyown_dataset_generator_py -.->|imports| ext_typing
    ext_collections["collections"]
    class ext_collections ext;
    lazyown_dataset_generator_py -.->|imports| ext_collections
    meta_harness_proposer_py -.->|imports| ext___future__
    meta_harness_proposer_py -.->|imports| ext_argparse
    meta_harness_proposer_py -.->|imports| ext_json
    ext_logging["logging"]
    class ext_logging ext;
    meta_harness_proposer_py -.->|imports| ext_logging
    ext_os["os"]
    class ext_os ext;
    meta_harness_proposer_py -.->|imports| ext_os
    ext_py_compile["py_compile"]
    class ext_py_compile ext;
    meta_harness_proposer_py -.->|imports| ext_py_compile
    meta_harness_proposer_py -.->|imports| ext_re
    ext_sys["sys"]
    class ext_sys ext;
    meta_harness_proposer_py -.->|imports| ext_sys
    ext_tempfile["tempfile"]
    class ext_tempfile ext;
    meta_harness_proposer_py -.->|imports| ext_tempfile
    ext_time["time"]
    class ext_time ext;
    meta_harness_proposer_py -.->|imports| ext_time
    ext_urllib_request["urllib.request"]
    class ext_urllib_request ext;
    meta_harness_proposer_py -.->|imports| ext_urllib_request
    ext_dataclasses["dataclasses"]
    class ext_dataclasses ext;
    meta_harness_proposer_py -.->|imports| ext_dataclasses
    meta_harness_proposer_py -.->|imports| ext_pathlib
    meta_harness_proposer_py -.->|imports| ext_typing
    ext_toposwarm_meta_harness["toposwarm_meta_harness"]
    class ext_toposwarm_meta_harness ext;
    meta_harness_proposer_py -.->|imports| ext_toposwarm_meta_harness
    tests_test_dataset_enhancer_py -.->|imports| ext_sys
    tests_test_dataset_enhancer_py -.->|imports| ext_pathlib
    ext_importlib_util["importlib.util"]
    class ext_importlib_util ext;
    tests_test_dataset_enhancer_py -.->|imports| ext_importlib_util
    tests_test_dataset_generator_py -.->|imports| ext_sys
    tests_test_dataset_generator_py -.->|imports| ext_pathlib
    tests_test_dataset_generator_py -.->|imports| ext_importlib_util
    tests_test_model_config_py -.->|imports| ext_sys
    tests_test_model_config_py -.->|imports| ext_pathlib
    tests_test_model_config_py -.->|imports| ext_importlib_util
    tests_test_orchestrator_py -.->|imports| ext_sys
    tests_test_orchestrator_py -.->|imports| ext_pathlib
    ext_unittest_mock["unittest.mock"]
    class ext_unittest_mock ext;
    tests_test_orchestrator_py -.->|imports| ext_unittest_mock
    ext_pytest["pytest"]
    class ext_pytest ext;
    tests_test_orchestrator_py -.->|imports| ext_pytest
    ext_toposwarm_lazyown_orchestrator["toposwarm_lazyown_orchestrator"]
    class ext_toposwarm_lazyown_orchestrator ext;
    tests_test_orchestrator_py -.->|imports| ext_toposwarm_lazyown_orchestrator
    tests_test_orchestrator_py -.->|imports| ext_toposwarm_lazyown_orchestrator
    ext_importlib["importlib"]
    class ext_importlib ext;
    tests_test_orchestrator_py -.->|imports| ext_importlib
    tests_test_orchestrator_py -.->|imports| ext_toposwarm_lazyown_orchestrator
    ext_torch["torch"]
    class ext_torch ext;
    tests_test_orchestrator_py -.->|imports| ext_torch
    tests_test_orchestrator_py -.->|imports| ext_torch
    tests_test_orchestrator_py -.->|imports| ext_importlib
    tests_test_orchestrator_py -.->|imports| ext_toposwarm_lazyown_orchestrator
    topo_swarm_agent_py -.->|imports| ext___future__
    ext_contextlib["contextlib"]
    class ext_contextlib ext;
    topo_swarm_agent_py -.->|imports| ext_contextlib
    ext_hashlib["hashlib"]
    class ext_hashlib ext;
    topo_swarm_agent_py -.->|imports| ext_hashlib
    topo_swarm_agent_py -.->|imports| ext_json
    topo_swarm_agent_py -.->|imports| ext_logging
    ext_math["math"]
    class ext_math ext;
    topo_swarm_agent_py -.->|imports| ext_math
    topo_swarm_agent_py -.->|imports| ext_os
    topo_swarm_agent_py -.->|imports| ext_sys
    ext_threading["threading"]
    class ext_threading ext;
    topo_swarm_agent_py -.->|imports| ext_threading
    topo_swarm_agent_py -.->|imports| ext_time
    ext_warnings["warnings"]
    class ext_warnings ext;
    topo_swarm_agent_py -.->|imports| ext_warnings
    topo_swarm_agent_py -.->|imports| ext_collections
    topo_swarm_agent_py -.->|imports| ext_dataclasses
    topo_swarm_agent_py -.->|imports| ext_pathlib
    topo_swarm_agent_py -.->|imports| ext_typing
    ext_numpy["numpy"]
    class ext_numpy ext;
    topo_swarm_agent_py -.->|imports| ext_numpy
    topo_swarm_agent_py -.->|imports| ext_torch
    ext_torch_nn["torch.nn"]
    class ext_torch_nn ext;
    topo_swarm_agent_py -.->|imports| ext_torch_nn
    ext_torch_nn_functional["torch.nn.functional"]
    class ext_torch_nn_functional ext;
    topo_swarm_agent_py -.->|imports| ext_torch_nn_functional
    ext_safetensors_torch["safetensors.torch"]
    class ext_safetensors_torch ext;
    topo_swarm_agent_py -.->|imports| ext_safetensors_torch
    topo_swarm_agent_py -.->|imports| ext_safetensors_torch
    ext_torch_utils_checkpoint["torch.utils.checkpoint"]
    class ext_torch_utils_checkpoint ext;
    topo_swarm_agent_py -.->|imports| ext_torch_utils_checkpoint
    topo_swarm_agent_py -.->|imports| ext_argparse
    ext_ts_utils["ts_utils"]
    class ext_ts_utils ext;
    topo_swarm_agent_py -.->|imports| ext_ts_utils
    ext_tiktoken["tiktoken"]
    class ext_tiktoken ext;
    topo_swarm_agent_py -.->|imports| ext_tiktoken
    ext_datasets["datasets"]
    class ext_datasets ext;
    topo_swarm_agent_py -.->|imports| ext_datasets
    topogpt2_1_py -.->|imports| ext_torch
    topogpt2_1_py -.->|imports| ext_torch_nn
    topogpt2_1_py -.->|imports| ext_torch_nn_functional
    topogpt2_1_py -.->|imports| ext_torch_utils_checkpoint
    topogpt2_1_py -.->|imports| ext_safetensors_torch
    topogpt2_1_py -.->|imports| ext_numpy
    topogpt2_1_py -.->|imports| ext_math
    topogpt2_1_py -.->|imports| ext_os
    topogpt2_1_py -.->|imports| ext_sys
    topogpt2_1_py -.->|imports| ext_time
    topogpt2_1_py -.->|imports| ext_json
    topogpt2_1_py -.->|imports| ext_hashlib
    topogpt2_1_py -.->|imports| ext_logging
    topogpt2_1_py -.->|imports| ext_warnings
    topogpt2_1_py -.->|imports| ext_argparse
    ext_datetime["datetime"]
    class ext_datetime ext;
    topogpt2_1_py -.->|imports| ext_datetime
    topogpt2_1_py -.->|imports| ext_typing
    topogpt2_1_py -.->|imports| ext_dataclasses
    topogpt2_1_py -.->|imports| ext_collections
    topogpt2_1_py -.->|imports| ext_tiktoken
    topogpt2_1_py -.->|imports| ext_datasets
    ext_shutil["shutil"]
    class ext_shutil ext;
    topogpt2_1_py -.->|imports| ext_shutil
    toposwarm_coevolve_py -.->|imports| ext___future__
    toposwarm_coevolve_py -.->|imports| ext_argparse
    ext_copy["copy"]
    class ext_copy ext;
    toposwarm_coevolve_py -.->|imports| ext_copy
    toposwarm_coevolve_py -.->|imports| ext_importlib_util
    toposwarm_coevolve_py -.->|imports| ext_json
    toposwarm_coevolve_py -.->|imports| ext_logging
    toposwarm_coevolve_py -.->|imports| ext_os
    toposwarm_coevolve_py -.->|imports| ext_random
    ext_subprocess["subprocess"]
    class ext_subprocess ext;
    toposwarm_coevolve_py -.->|imports| ext_subprocess
    toposwarm_coevolve_py -.->|imports| ext_sys
    toposwarm_coevolve_py -.->|imports| ext_time
    toposwarm_coevolve_py -.->|imports| ext_dataclasses
    toposwarm_coevolve_py -.->|imports| ext_pathlib
    toposwarm_coevolve_py -.->|imports| ext_typing
    toposwarm_coevolve_py -.->|imports| ext_toposwarm_meta_harness
    toposwarm_coevolve_py -.->|imports| ext_toposwarm_lazyown_orchestrator
    toposwarm_coevolve_py -.->|imports| ext_toposwarm_lazyown_orchestrator
    ext_toposwarm_infer["toposwarm_infer"]
    class ext_toposwarm_infer ext;
    toposwarm_coevolve_py -.->|imports| ext_toposwarm_infer
    ext_topo_swarm_agent["topo_swarm_agent"]
    class ext_topo_swarm_agent ext;
    toposwarm_coevolve_py -.->|imports| ext_topo_swarm_agent
    toposwarm_coevolve_py -.->|imports| ext_toposwarm_meta_harness
    toposwarm_continual_trainer_py -.->|imports| ext___future__
    toposwarm_continual_trainer_py -.->|imports| ext_argparse
    toposwarm_continual_trainer_py -.->|imports| ext_importlib_util
    toposwarm_continual_trainer_py -.->|imports| ext_json
    toposwarm_continual_trainer_py -.->|imports| ext_logging
    toposwarm_continual_trainer_py -.->|imports| ext_math
    toposwarm_continual_trainer_py -.->|imports| ext_os
    toposwarm_continual_trainer_py -.->|imports| ext_random
    toposwarm_continual_trainer_py -.->|imports| ext_sys
    toposwarm_continual_trainer_py -.->|imports| ext_dataclasses
    toposwarm_continual_trainer_py -.->|imports| ext_pathlib
    toposwarm_continual_trainer_py -.->|imports| ext_typing
    toposwarm_continual_trainer_py -.->|imports| ext_torch
    toposwarm_continual_trainer_py -.->|imports| ext_torch_nn
    toposwarm_continual_trainer_py -.->|imports| ext_torch_nn_functional
    toposwarm_continual_trainer_py -.->|imports| ext_ts_utils
    toposwarm_continual_trainer_py -.->|imports| ext_ts_utils
    toposwarm_continual_trainer_py -.->|imports| ext_logging
    toposwarm_hybrid_py -.->|imports| ext___future__
    ext_ast["ast"]
    class ext_ast ext;
    toposwarm_hybrid_py -.->|imports| ext_ast
    toposwarm_hybrid_py -.->|imports| ext_json
    toposwarm_hybrid_py -.->|imports| ext_logging
    ext_operator["operator"]
    class ext_operator ext;
    toposwarm_hybrid_py -.->|imports| ext_operator
    toposwarm_hybrid_py -.->|imports| ext_os
    toposwarm_hybrid_py -.->|imports| ext_re
    toposwarm_hybrid_py -.->|imports| ext_sys
    ext_urllib_parse["urllib.parse"]
    class ext_urllib_parse ext;
    toposwarm_hybrid_py -.->|imports| ext_urllib_parse
    toposwarm_hybrid_py -.->|imports| ext_urllib_request
    toposwarm_hybrid_py -.->|imports| ext_dataclasses
    toposwarm_hybrid_py -.->|imports| ext_datetime
    toposwarm_hybrid_py -.->|imports| ext_pathlib
    toposwarm_hybrid_py -.->|imports| ext_typing
    toposwarm_hybrid_py -.->|imports| ext_torch
    toposwarm_hybrid_py -.->|imports| ext_torch_nn_functional
    toposwarm_hybrid_py -.->|imports| ext_importlib_util
    toposwarm_hybrid_py -.->|imports| ext_argparse
    toposwarm_hybrid_py -.->|imports| ext_importlib_util
    ext_transformers["transformers"]
    class ext_transformers ext;
    toposwarm_hybrid_py -.->|imports| ext_transformers
    toposwarm_hybrid_py -.->|imports| ext_safetensors_torch
    ext_inspect["inspect"]
    class ext_inspect ext;
    toposwarm_hybrid_py -.->|imports| ext_inspect
    toposwarm_hybrid_py -.->|imports| ext_dataclasses
    ext_langdetect["langdetect"]
    class ext_langdetect ext;
    toposwarm_hybrid_py -.->|imports| ext_langdetect
    toposwarm_infer_py -.->|imports| ext___future__
    toposwarm_infer_py -.->|imports| ext_ast
    toposwarm_infer_py -.->|imports| ext_json
    toposwarm_infer_py -.->|imports| ext_logging
    toposwarm_infer_py -.->|imports| ext_math
    toposwarm_infer_py -.->|imports| ext_operator
    toposwarm_infer_py -.->|imports| ext_os
    toposwarm_infer_py -.->|imports| ext_re
    toposwarm_infer_py -.->|imports| ext_sys
    ext_urllib_error["urllib.error"]
    class ext_urllib_error ext;
    toposwarm_infer_py -.->|imports| ext_urllib_error
    toposwarm_infer_py -.->|imports| ext_urllib_parse
    toposwarm_infer_py -.->|imports| ext_urllib_request
    toposwarm_infer_py -.->|imports| ext_dataclasses
    toposwarm_infer_py -.->|imports| ext_datetime
    toposwarm_infer_py -.->|imports| ext_pathlib
    toposwarm_infer_py -.->|imports| ext_typing
    toposwarm_infer_py -.->|imports| ext_torch
    toposwarm_infer_py -.->|imports| ext_importlib_util
    ext_types["types"]
    class ext_types ext;
    toposwarm_infer_py -.->|imports| ext_types
    toposwarm_infer_py -.->|imports| ext_argparse
    toposwarm_infer_py -.->|imports| ext_torch_nn_functional
    toposwarm_infer_py -.->|imports| ext_re
    toposwarm_infer_py -.->|imports| ext_re
    toposwarm_infer_py -.->|imports| ext_re
    toposwarm_infer_py -.->|imports| ext_langdetect
    toposwarm_lazyown_orchestrator_py -.->|imports| ext___future__
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_argparse
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_importlib_util
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_json
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_logging
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_os
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_re
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_subprocess
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_sys
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_time
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_dataclasses
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_pathlib
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_typing
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_random
    ext_mcp_server["mcp.server"]
    class ext_mcp_server ext;
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_mcp_server
    ext_mcp_server_stdio["mcp.server.stdio"]
    class ext_mcp_server_stdio ext;
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_mcp_server_stdio
    ext_mcp["mcp"]
    class ext_mcp ext;
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_mcp
    ext_asyncio["asyncio"]
    class ext_asyncio ext;
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_asyncio
    ext_fcntl["fcntl"]
    class ext_fcntl ext;
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_fcntl
    ext_pty["pty"]
    class ext_pty ext;
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_pty
    ext_select["select"]
    class ext_select ext;
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_select
    ext_struct["struct"]
    class ext_struct ext;
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_struct
    ext_termios["termios"]
    class ext_termios ext;
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_termios
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_torch
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_importlib_util
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_importlib_util
    toposwarm_lazyown_orchestrator_py -.->|imports| ext_json
    toposwarm_lazyown_sweep_py -.->|imports| ext___future__
    toposwarm_lazyown_sweep_py -.->|imports| ext_argparse
    toposwarm_lazyown_sweep_py -.->|imports| ext_json
    toposwarm_lazyown_sweep_py -.->|imports| ext_logging
    toposwarm_lazyown_sweep_py -.->|imports| ext_random
    toposwarm_lazyown_sweep_py -.->|imports| ext_sys
    toposwarm_lazyown_sweep_py -.->|imports| ext_time
    toposwarm_lazyown_sweep_py -.->|imports| ext_pathlib
    toposwarm_lazyown_sweep_py -.->|imports| ext_typing
    toposwarm_lazyown_sweep_py -.->|imports| ext_toposwarm_lazyown_orchestrator
    toposwarm_lazyown_sweep_py -.->|imports| ext_topo_swarm_agent
    toposwarm_lazyown_sweep_py -.->|imports| ext_subprocess
    toposwarm_meta_harness_py -.->|imports| ext___future__
    toposwarm_meta_harness_py -.->|imports| ext_hashlib
    toposwarm_meta_harness_py -.->|imports| ext_json
    toposwarm_meta_harness_py -.->|imports| ext_logging
    toposwarm_meta_harness_py -.->|imports| ext_math
    toposwarm_meta_harness_py -.->|imports| ext_os
    toposwarm_meta_harness_py -.->|imports| ext_re
    toposwarm_meta_harness_py -.->|imports| ext_sys
    toposwarm_meta_harness_py -.->|imports| ext_time
    toposwarm_meta_harness_py -.->|imports| ext_collections
    toposwarm_meta_harness_py -.->|imports| ext_dataclasses
    toposwarm_meta_harness_py -.->|imports| ext_pathlib
    toposwarm_meta_harness_py -.->|imports| ext_typing
    toposwarm_meta_harness_py -.->|imports| ext_numpy
    ext_sentence_transformers["sentence_transformers"]
    class ext_sentence_transformers ext;
    toposwarm_meta_harness_py -.->|imports| ext_sentence_transformers
    ext_sklearn_feature_extraction_text["sklearn.feature_extraction.text"]
    class ext_sklearn_feature_extraction_text ext;
    toposwarm_meta_harness_py -.->|imports| ext_sklearn_feature_extraction_text
    toposwarm_meta_harness_py -.->|imports| ext_numpy
    ext_sklearn_metrics_pairwise["sklearn.metrics.pairwise"]
    class ext_sklearn_metrics_pairwise ext;
    toposwarm_meta_harness_py -.->|imports| ext_sklearn_metrics_pairwise
    toposwarm_meta_harness_py -.->|imports| ext_numpy
    toposwarm_meta_harness_py -.->|imports| ext_subprocess
    toposwarm_meta_harness_py -.->|imports| ext_shutil
    ext_psutil["psutil"]
    class ext_psutil ext;
    toposwarm_meta_harness_py -.->|imports| ext_psutil
    toposwarm_meta_harness_py -.->|imports| ext_shutil
    toposwarm_meta_harness_py -.->|imports| ext_sklearn_feature_extraction_text
    toposwarm_meta_harness_py -.->|imports| ext_sklearn_metrics_pairwise
    ts_utils_py -.->|imports| ext___future__
    ts_utils_py -.->|imports| ext_ast
    ts_utils_py -.->|imports| ext_importlib_util
    ts_utils_py -.->|imports| ext_logging
    ts_utils_py -.->|imports| ext_sys
    ext_functools["functools"]
    class ext_functools ext;
    ts_utils_py -.->|imports| ext_functools
    ts_utils_py -.->|imports| ext_pathlib
    ts_utils_py -.->|imports| ext_typing
```

---

## UML Class Diagram

Auto-generated Mermaid class diagram from parsed class-level symbols. Shows classes, structs, interfaces, traits, and their methods with inheritance and dependency relationships.

```mermaid
classDiagram
  class lazyown_dataset_enhancer_py_ExperienceStoreReader {
    <<class>>
    +_difficulty(record)
    +_sanitize_output(text)
    +_build_toolbench_record(instruction, tool_name, arg, answer, domain)
    +print_stats(records)
    +main()
    +__init__(self, log_dir)
    +list_runs(self)
    +read_trace(self, run_dir)
    +read_score(self, run_dir)
    +read_harness(self, run_dir)
  }
  class lazyown_dataset_enhancer_py_DatasetEnhancer {
    <<class>>
    +_difficulty(record)
    +_sanitize_output(text)
    +_build_toolbench_record(instruction, tool_name, arg, answer, domain)
    +print_stats(records)
    +main()
    +__init__(self, log_dir)
    +list_runs(self)
    +read_trace(self, run_dir)
    +read_score(self, run_dir)
    +read_harness(self, run_dir)
  }
  class meta_harness_proposer_py_LLMConfig {
    <<class>>
    +_setup_logger(name, level)
    +main()
    +__init__(self, cfg, logger)
    +_try_chat(self, api_url, model, system, user)
    +chat(self, system, user)
    +__init__(self, log_dir, logger)
    +list_runs(self, n)
    +load_run(self, run_dir)
    +build_diagnostic_context(self, top_k)
    +__init__(self, logger)
  }
  class meta_harness_proposer_py_LLMClient {
    <<class>>
    +_setup_logger(name, level)
    +main()
    +__init__(self, cfg, logger)
    +_try_chat(self, api_url, model, system, user)
    +chat(self, system, user)
    +__init__(self, log_dir, logger)
    +list_runs(self, n)
    +load_run(self, run_dir)
    +build_diagnostic_context(self, top_k)
    +__init__(self, logger)
  }
  class meta_harness_proposer_py_ExperienceReader {
    <<class>>
    +_setup_logger(name, level)
    +main()
    +__init__(self, cfg, logger)
    +_try_chat(self, api_url, model, system, user)
    +chat(self, system, user)
    +__init__(self, log_dir, logger)
    +list_runs(self, n)
    +load_run(self, run_dir)
    +build_diagnostic_context(self, top_k)
    +__init__(self, logger)
  }
  class meta_harness_proposer_py_PatchEngine {
    <<class>>
    +_setup_logger(name, level)
    +main()
    +__init__(self, cfg, logger)
    +_try_chat(self, api_url, model, system, user)
    +chat(self, system, user)
    +__init__(self, log_dir, logger)
    +list_runs(self, n)
    +load_run(self, run_dir)
    +build_diagnostic_context(self, top_k)
    +__init__(self, logger)
  }
  class meta_harness_proposer_py_MetaHarnessProposer {
    <<class>>
    +_setup_logger(name, level)
    +main()
    +__init__(self, cfg, logger)
    +_try_chat(self, api_url, model, system, user)
    +chat(self, system, user)
    +__init__(self, log_dir, logger)
    +list_runs(self, n)
    +load_run(self, run_dir)
    +build_diagnostic_context(self, top_k)
    +__init__(self, logger)
  }
  class test_orchestrator_py_TestSessionContext {
    <<class>>
    +_load_ctx(self)
    +test_empty_prefix(self)
    +test_prefix_with_target(self)
    +test_update_extracts_ip(self)
    +test_phase_progression(self)
    +test_findings_from_output(self)
    +_load_router(self)
    +test_recon_keyword(self)
    +test_config_keyword(self)
    +test_c2_keyword(self)
  }
  class test_orchestrator_py_TestKeywordRouter {
    <<class>>
    +_load_ctx(self)
    +test_empty_prefix(self)
    +test_prefix_with_target(self)
    +test_update_extracts_ip(self)
    +test_phase_progression(self)
    +test_findings_from_output(self)
    +_load_router(self)
    +test_recon_keyword(self)
    +test_config_keyword(self)
    +test_c2_keyword(self)
  }
  class test_orchestrator_py_TestNeuralRouter {
    <<class>>
    +_load_ctx(self)
    +test_empty_prefix(self)
    +test_prefix_with_target(self)
    +test_update_extracts_ip(self)
    +test_phase_progression(self)
    +test_findings_from_output(self)
    +_load_router(self)
    +test_recon_keyword(self)
    +test_config_keyword(self)
    +test_c2_keyword(self)
  }
  class test_orchestrator_py_TestOrchestratorRun {
    <<class>>
    +_load_ctx(self)
    +test_empty_prefix(self)
    +test_prefix_with_target(self)
    +test_update_extracts_ip(self)
    +test_phase_progression(self)
    +test_findings_from_output(self)
    +_load_router(self)
    +test_recon_keyword(self)
    +test_config_keyword(self)
    +test_c2_keyword(self)
  }
  class topo_swarm_agent_py_SwarmConfig {
    <<class>>
    +_setup_logger(name, level)
    +_set_seed(seed, device)
    +_param_count(module)
    +_get_torus_positions(n_angular, n_radial, device)
    +inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)
    +_chunked_ce(logits, targets, chunk_size)
    +build_dataloaders(cfg, tokenizer, logger)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
  }
  class topo_swarm_agent_py_QuaternionOps {
    <<class>>
    +_setup_logger(name, level)
    +_set_seed(seed, device)
    +_param_count(module)
    +_get_torus_positions(n_angular, n_radial, device)
    +inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)
    +_chunked_ce(logits, targets, chunk_size)
    +build_dataloaders(cfg, tokenizer, logger)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
  }
  class topo_swarm_agent_py_QuaternionLinear {
    <<class>>
    +_setup_logger(name, level)
    +_set_seed(seed, device)
    +_param_count(module)
    +_get_torus_positions(n_angular, n_radial, device)
    +inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)
    +_chunked_ce(logits, targets, chunk_size)
    +build_dataloaders(cfg, tokenizer, logger)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
  }
  class topo_swarm_agent_py_SpectralBottleneck {
    <<class>>
    +_setup_logger(name, level)
    +_set_seed(seed, device)
    +_param_count(module)
    +_get_torus_positions(n_angular, n_radial, device)
    +inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)
    +_chunked_ce(logits, targets, chunk_size)
    +build_dataloaders(cfg, tokenizer, logger)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
  }
  class topo_swarm_agent_py_RMSNorm {
    <<class>>
    +_setup_logger(name, level)
    +_set_seed(seed, device)
    +_param_count(module)
    +_get_torus_positions(n_angular, n_radial, device)
    +inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)
    +_chunked_ce(logits, targets, chunk_size)
    +build_dataloaders(cfg, tokenizer, logger)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
  }
  class topo_swarm_agent_py_RotaryEmbedding {
    <<class>>
    +_setup_logger(name, level)
    +_set_seed(seed, device)
    +_param_count(module)
    +_get_torus_positions(n_angular, n_radial, device)
    +inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)
    +_chunked_ce(logits, targets, chunk_size)
    +build_dataloaders(cfg, tokenizer, logger)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
  }
  class topo_swarm_agent_py_SwiGLU {
    <<class>>
    +_setup_logger(name, level)
    +_set_seed(seed, device)
    +_param_count(module)
    +_get_torus_positions(n_angular, n_radial, device)
    +inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)
    +_chunked_ce(logits, targets, chunk_size)
    +build_dataloaders(cfg, tokenizer, logger)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
  }
  class topo_swarm_agent_py_SwarmMoEGate {
    <<class>>
    +_setup_logger(name, level)
    +_set_seed(seed, device)
    +_param_count(module)
    +_get_torus_positions(n_angular, n_radial, device)
    +inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)
    +_chunked_ce(logits, targets, chunk_size)
    +build_dataloaders(cfg, tokenizer, logger)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
  }
  class topo_swarm_agent_py_SwarmMoE {
    <<class>>
    +_setup_logger(name, level)
    +_set_seed(seed, device)
    +_param_count(module)
    +_get_torus_positions(n_angular, n_radial, device)
    +inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)
    +_chunked_ce(logits, targets, chunk_size)
    +build_dataloaders(cfg, tokenizer, logger)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
  }
  class topo_swarm_agent_py_SwarmMoEAdapter {
    <<class>>
    +_setup_logger(name, level)
    +_set_seed(seed, device)
    +_param_count(module)
    +_get_torus_positions(n_angular, n_radial, device)
    +inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)
    +_chunked_ce(logits, targets, chunk_size)
    +build_dataloaders(cfg, tokenizer, logger)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
  }
  class topo_swarm_agent_py_QuaternionTorusBrain {
    <<class>>
    +_setup_logger(name, level)
    +_set_seed(seed, device)
    +_param_count(module)
    +_get_torus_positions(n_angular, n_radial, device)
    +inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)
    +_chunked_ce(logits, targets, chunk_size)
    +build_dataloaders(cfg, tokenizer, logger)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
  }
  class topo_swarm_agent_py_QuaternionAttention {
    <<class>>
    +_setup_logger(name, level)
    +_set_seed(seed, device)
    +_param_count(module)
    +_get_torus_positions(n_angular, n_radial, device)
    +inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)
    +_chunked_ce(logits, targets, chunk_size)
    +build_dataloaders(cfg, tokenizer, logger)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
  }
  class topo_swarm_agent_py_HRMModule {
    <<class>>
    +_setup_logger(name, level)
    +_set_seed(seed, device)
    +_param_count(module)
    +_get_torus_positions(n_angular, n_radial, device)
    +inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)
    +_chunked_ce(logits, targets, chunk_size)
    +build_dataloaders(cfg, tokenizer, logger)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
  }
  class topo_swarm_agent_py_TopoSwarmLayer {
    <<class>>
    +_setup_logger(name, level)
    +_set_seed(seed, device)
    +_param_count(module)
    +_get_torus_positions(n_angular, n_radial, device)
    +inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)
    +_chunked_ce(logits, targets, chunk_size)
    +build_dataloaders(cfg, tokenizer, logger)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
  }
  class topo_swarm_agent_py_TopoSwarmModel {
    <<class>>
    +_setup_logger(name, level)
    +_set_seed(seed, device)
    +_param_count(module)
    +_get_torus_positions(n_angular, n_radial, device)
    +inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)
    +_chunked_ce(logits, targets, chunk_size)
    +build_dataloaders(cfg, tokenizer, logger)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
  }
  class topo_swarm_agent_py_EpisodicMemory {
    <<class>>
    +_setup_logger(name, level)
    +_set_seed(seed, device)
    +_param_count(module)
    +_get_torus_positions(n_angular, n_radial, device)
    +inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)
    +_chunked_ce(logits, targets, chunk_size)
    +build_dataloaders(cfg, tokenizer, logger)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
  }
  class topo_swarm_agent_py_SwarmOrchestrator {
    <<class>>
    +_setup_logger(name, level)
    +_set_seed(seed, device)
    +_param_count(module)
    +_get_torus_positions(n_angular, n_radial, device)
    +inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)
    +_chunked_ce(logits, targets, chunk_size)
    +build_dataloaders(cfg, tokenizer, logger)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
  }
  class topo_swarm_agent_py_BPETokenizer {
    <<class>>
    +_setup_logger(name, level)
    +_set_seed(seed, device)
    +_param_count(module)
    +_get_torus_positions(n_angular, n_radial, device)
    +inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)
    +_chunked_ce(logits, targets, chunk_size)
    +build_dataloaders(cfg, tokenizer, logger)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
  }
  class topo_swarm_agent_py_ToolBenchDataset {
    <<class>>
    +_setup_logger(name, level)
    +_set_seed(seed, device)
    +_param_count(module)
    +_get_torus_positions(n_angular, n_radial, device)
    +inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)
    +_chunked_ce(logits, targets, chunk_size)
    +build_dataloaders(cfg, tokenizer, logger)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
  }
  class topo_swarm_agent_py_CheckpointManager {
    <<class>>
    +_setup_logger(name, level)
    +_set_seed(seed, device)
    +_param_count(module)
    +_get_torus_positions(n_angular, n_radial, device)
    +inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)
    +_chunked_ce(logits, targets, chunk_size)
    +build_dataloaders(cfg, tokenizer, logger)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
  }
  class topo_swarm_agent_py_KappaDetector {
    <<class>>
    +_setup_logger(name, level)
    +_set_seed(seed, device)
    +_param_count(module)
    +_get_torus_positions(n_angular, n_radial, device)
    +inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)
    +_chunked_ce(logits, targets, chunk_size)
    +build_dataloaders(cfg, tokenizer, logger)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
  }
  class topo_swarm_agent_py_SwarmTrainer {
    <<class>>
    +_setup_logger(name, level)
    +_set_seed(seed, device)
    +_param_count(module)
    +_get_torus_positions(n_angular, n_radial, device)
    +inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)
    +_chunked_ce(logits, targets, chunk_size)
    +build_dataloaders(cfg, tokenizer, logger)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
  }
  class topogpt2_1_py_TopoGPT2Config {
    <<class>>
    +setup_logger(name, level)
    +set_seed(seed, device)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
    +normalize(q, eps)
    +conjugate(q)
    +rotate_vector(v, q)
    +__init__(self, in_features, out_features, bias)
    +forward(self, x)
  }
  class topogpt2_1_py_QuaternionOps {
    <<class>>
    +setup_logger(name, level)
    +set_seed(seed, device)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
    +normalize(q, eps)
    +conjugate(q)
    +rotate_vector(v, q)
    +__init__(self, in_features, out_features, bias)
    +forward(self, x)
  }
  class topogpt2_1_py_QuaternionLinear {
    <<class>>
    +setup_logger(name, level)
    +set_seed(seed, device)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
    +normalize(q, eps)
    +conjugate(q)
    +rotate_vector(v, q)
    +__init__(self, in_features, out_features, bias)
    +forward(self, x)
  }
  class topogpt2_1_py_QuaternionSpectralLayer {
    <<class>>
    +setup_logger(name, level)
    +set_seed(seed, device)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
    +normalize(q, eps)
    +conjugate(q)
    +rotate_vector(v, q)
    +__init__(self, in_features, out_features, bias)
    +forward(self, x)
  }
  class topogpt2_1_py_SpectralAutoencoder {
    <<class>>
    +setup_logger(name, level)
    +set_seed(seed, device)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
    +normalize(q, eps)
    +conjugate(q)
    +rotate_vector(v, q)
    +__init__(self, in_features, out_features, bias)
    +forward(self, x)
  }
  class topogpt2_1_py_QuaternionTorusBrain {
    <<class>>
    +setup_logger(name, level)
    +set_seed(seed, device)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
    +normalize(q, eps)
    +conjugate(q)
    +rotate_vector(v, q)
    +__init__(self, in_features, out_features, bias)
    +forward(self, x)
  }
  class topogpt2_1_py_RotaryEmbedding {
    <<class>>
    +setup_logger(name, level)
    +set_seed(seed, device)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
    +normalize(q, eps)
    +conjugate(q)
    +rotate_vector(v, q)
    +__init__(self, in_features, out_features, bias)
    +forward(self, x)
  }
  class topogpt2_1_py_RMSNorm {
    <<class>>
    +setup_logger(name, level)
    +set_seed(seed, device)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
    +normalize(q, eps)
    +conjugate(q)
    +rotate_vector(v, q)
    +__init__(self, in_features, out_features, bias)
    +forward(self, x)
  }
  class topogpt2_1_py_SwiGLU {
    <<class>>
    +setup_logger(name, level)
    +set_seed(seed, device)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
    +normalize(q, eps)
    +conjugate(q)
    +rotate_vector(v, q)
    +__init__(self, in_features, out_features, bias)
    +forward(self, x)
  }
  class topogpt2_1_py_TopoMoEBrain {
    <<class>>
    +setup_logger(name, level)
    +set_seed(seed, device)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
    +normalize(q, eps)
    +conjugate(q)
    +rotate_vector(v, q)
    +__init__(self, in_features, out_features, bias)
    +forward(self, x)
  }
  class topogpt2_1_py_MultiHeadAttention {
    <<class>>
    +setup_logger(name, level)
    +set_seed(seed, device)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
    +normalize(q, eps)
    +conjugate(q)
    +rotate_vector(v, q)
    +__init__(self, in_features, out_features, bias)
    +forward(self, x)
  }
  class topogpt2_1_py_TopoGPT2Layer {
    <<class>>
    +setup_logger(name, level)
    +set_seed(seed, device)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
    +normalize(q, eps)
    +conjugate(q)
    +rotate_vector(v, q)
    +__init__(self, in_features, out_features, bias)
    +forward(self, x)
  }
  class topogpt2_1_py_TopoGPT2 {
    <<class>>
    +setup_logger(name, level)
    +set_seed(seed, device)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
    +normalize(q, eps)
    +conjugate(q)
    +rotate_vector(v, q)
    +__init__(self, in_features, out_features, bias)
    +forward(self, x)
  }
  class topogpt2_1_py_BPETokenizer {
    <<class>>
    +setup_logger(name, level)
    +set_seed(seed, device)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
    +normalize(q, eps)
    +conjugate(q)
    +rotate_vector(v, q)
    +__init__(self, in_features, out_features, bias)
    +forward(self, x)
  }
  class topogpt2_1_py_CorpusDownloader {
    <<class>>
    +setup_logger(name, level)
    +set_seed(seed, device)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
    +normalize(q, eps)
    +conjugate(q)
    +rotate_vector(v, q)
    +__init__(self, in_features, out_features, bias)
    +forward(self, x)
  }
  class topogpt2_1_py_TokenizedDataset {
    <<class>>
    +setup_logger(name, level)
    +set_seed(seed, device)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
    +normalize(q, eps)
    +conjugate(q)
    +rotate_vector(v, q)
    +__init__(self, in_features, out_features, bias)
    +forward(self, x)
  }
  class topogpt2_1_py_CheckpointManager {
    <<class>>
    +setup_logger(name, level)
    +set_seed(seed, device)
    +main()
    +__post_init__(self)
    +hamilton_product(q1, q2)
    +normalize(q, eps)
    +conjugate(q)
    +rotate_vector(v, q)
    +__init__(self, in_features, out_features, bias)
    +forward(self, x)
  }
```

---

## Code Property Graph

Machine-readable Code Property Graph (CPG) in JSON-LD format. This block allows AI agents to parse the full structural graph without additional file reads. Compatible with GraphRAG pipelines.

```json
{"@context": "https://schema.org", "analysis": {"communities": [{"cohesion": 0.5, "id": 0, "label": "root", "size": 2}, {"cohesion": 0.75, "id": 1, "label": "root", "size": 6}, {"cohesion": 0.5, "id": 2, "label": "root", "size": 2}], "god_nodes": [{"node_id": "topo_swarm_agent.py", "score": 16.4}, {"node_id": "toposwarm_lazyown_orchestrator.py", "score": 14.3}, {"node_id": "topogpt2_1.py", "score": 12.6}, {"node_id": "toposwarm_coevolve.py", "score": 11.3}, {"node_id": "toposwarm_meta_harness.py", "score": 9.4}, {"node_id": "toposwarm_continual_trainer.py", "score": 7.1}, {"node_id": "toposwarm_infer.py", "score": 5.7}, {"node_id": "toposwarm_hybrid.py", "score": 4.8}, {"node_id": "ts_utils.py", "score": 4.7}, {"node_id": "tests/test_orchestrator.py", "score": 4.5}], "surprising_connections": [{"hops": 5, "source": "meta_harness_proposer.py", "target": "toposwarm_continual_trainer.py"}, {"hops": 5, "source": "tests/test_orchestrator.py", "target": "toposwarm_continual_trainer.py"}, {"hops": 4, "source": "meta_harness_proposer.py", "target": "tests/test_orchestrator.py"}, {"hops": 4, "source": "meta_harness_proposer.py", "target": "toposwarm_lazyown_sweep.py"}, {"hops": 4, "source": "meta_harness_proposer.py", "target": "ts_utils.py"}]}, "edges": [{"confidence": "EXTRACTED", "relation": "imports", "source": "lazyown_dataset_enhancer.py", "target": "__future__"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "lazyown_dataset_enhancer.py", "target": "argparse"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "lazyown_dataset_enhancer.py", "target": "json"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "lazyown_dataset_enhancer.py", "target": "random"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "lazyown_dataset_enhancer.py", "target": "re"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "lazyown_dataset_enhancer.py", "target": "pathlib"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "lazyown_dataset_enhancer.py", "target": "typing"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "lazyown_dataset_generator.py", "target": "__future__"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "lazyown_dataset_generator.py", "target": "argparse"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "lazyown_dataset_generator.py", "target": "json"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "lazyown_dataset_generator.py", "target": "random"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "lazyown_dataset_generator.py", "target": "re"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "lazyown_dataset_generator.py", "target": "pathlib"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "lazyown_dataset_generator.py", "target": "typing"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "lazyown_dataset_generator.py", "target": "collections"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "meta_harness_proposer.py", "target": "__future__"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "meta_harness_proposer.py", "target": "argparse"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "meta_harness_proposer.py", "target": "json"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "meta_harness_proposer.py", "target": "logging"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "meta_harness_proposer.py", "target": "os"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "meta_harness_proposer.py", "target": "py_compile"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "meta_harness_proposer.py", "target": "re"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "meta_harness_proposer.py", "target": "sys"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "meta_harness_proposer.py", "target": "tempfile"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "meta_harness_proposer.py", "target": "time"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "meta_harness_proposer.py", "target": "urllib.request"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "meta_harness_proposer.py", "target": "dataclasses"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "meta_harness_proposer.py", "target": "pathlib"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "meta_harness_proposer.py", "target": "typing"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "meta_harness_proposer.py", "target": "toposwarm_meta_harness"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "tests/test_dataset_enhancer.py", "target": "sys"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "tests/test_dataset_enhancer.py", "target": "pathlib"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "tests/test_dataset_enhancer.py", "target": "importlib.util"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "tests/test_dataset_generator.py", "target": "sys"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "tests/test_dataset_generator.py", "target": "pathlib"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "tests/test_dataset_generator.py", "target": "importlib.util"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "tests/test_model_config.py", "target": "sys"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "tests/test_model_config.py", "target": "pathlib"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "tests/test_model_config.py", "target": "importlib.util"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "tests/test_orchestrator.py", "target": "sys"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "tests/test_orchestrator.py", "target": "pathlib"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "tests/test_orchestrator.py", "target": "unittest.mock"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "tests/test_orchestrator.py", "target": "pytest"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "tests/test_orchestrator.py", "target": "toposwarm_lazyown_orchestrator"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "tests/test_orchestrator.py", "target": "toposwarm_lazyown_orchestrator"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "tests/test_orchestrator.py", "target": "importlib"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "tests/test_orchestrator.py", "target": "toposwarm_lazyown_orchestrator"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "tests/test_orchestrator.py", "target": "torch"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "tests/test_orchestrator.py", "target": "torch"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "tests/test_orchestrator.py", "target": "importlib"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "tests/test_orchestrator.py", "target": "toposwarm_lazyown_orchestrator"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "__future__"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "contextlib"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "hashlib"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "json"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "logging"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "math"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "os"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "sys"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "threading"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "time"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "warnings"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "collections"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "dataclasses"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "pathlib"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "typing"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "numpy"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "torch"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "torch.nn"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "torch.nn.functional"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "safetensors.torch"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "safetensors.torch"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "torch.utils.checkpoint"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "argparse"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "ts_utils"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "tiktoken"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topo_swarm_agent.py", "target": "datasets"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topogpt2_1.py", "target": "torch"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topogpt2_1.py", "target": "torch.nn"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topogpt2_1.py", "target": "torch.nn.functional"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topogpt2_1.py", "target": "torch.utils.checkpoint"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topogpt2_1.py", "target": "safetensors.torch"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topogpt2_1.py", "target": "numpy"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topogpt2_1.py", "target": "math"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topogpt2_1.py", "target": "os"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topogpt2_1.py", "target": "sys"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topogpt2_1.py", "target": "time"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topogpt2_1.py", "target": "json"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topogpt2_1.py", "target": "hashlib"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topogpt2_1.py", "target": "logging"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topogpt2_1.py", "target": "warnings"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topogpt2_1.py", "target": "argparse"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topogpt2_1.py", "target": "datetime"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topogpt2_1.py", "target": "typing"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topogpt2_1.py", "target": "dataclasses"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topogpt2_1.py", "target": "collections"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topogpt2_1.py", "target": "tiktoken"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topogpt2_1.py", "target": "datasets"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "topogpt2_1.py", "target": "shutil"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_coevolve.py", "target": "__future__"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_coevolve.py", "target": "argparse"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_coevolve.py", "target": "copy"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_coevolve.py", "target": "importlib.util"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_coevolve.py", "target": "json"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_coevolve.py", "target": "logging"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_coevolve.py", "target": "os"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_coevolve.py", "target": "random"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_coevolve.py", "target": "subprocess"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_coevolve.py", "target": "sys"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_coevolve.py", "target": "time"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_coevolve.py", "target": "dataclasses"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_coevolve.py", "target": "pathlib"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_coevolve.py", "target": "typing"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_coevolve.py", "target": "toposwarm_meta_harness"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_coevolve.py", "target": "toposwarm_lazyown_orchestrator"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_coevolve.py", "target": "toposwarm_lazyown_orchestrator"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_coevolve.py", "target": "toposwarm_infer"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_coevolve.py", "target": "topo_swarm_agent"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_coevolve.py", "target": "toposwarm_meta_harness"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_continual_trainer.py", "target": "__future__"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_continual_trainer.py", "target": "argparse"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_continual_trainer.py", "target": "importlib.util"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_continual_trainer.py", "target": "json"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_continual_trainer.py", "target": "logging"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_continual_trainer.py", "target": "math"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_continual_trainer.py", "target": "os"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_continual_trainer.py", "target": "random"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_continual_trainer.py", "target": "sys"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_continual_trainer.py", "target": "dataclasses"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_continual_trainer.py", "target": "pathlib"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_continual_trainer.py", "target": "typing"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_continual_trainer.py", "target": "torch"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_continual_trainer.py", "target": "torch.nn"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_continual_trainer.py", "target": "torch.nn.functional"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_continual_trainer.py", "target": "ts_utils"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_continual_trainer.py", "target": "ts_utils"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_continual_trainer.py", "target": "logging"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "__future__"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "ast"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "json"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "logging"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "operator"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "os"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "re"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "sys"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "urllib.parse"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "urllib.request"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "dataclasses"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "datetime"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "pathlib"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "typing"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "torch"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "torch.nn.functional"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "importlib.util"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "argparse"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "importlib.util"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "transformers"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "safetensors.torch"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "inspect"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "dataclasses"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_hybrid.py", "target": "langdetect"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "__future__"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "ast"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "json"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "logging"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "math"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "operator"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "os"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "re"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "sys"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "urllib.error"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "urllib.parse"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "urllib.request"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "dataclasses"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "datetime"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "pathlib"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "typing"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "torch"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "importlib.util"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "types"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "argparse"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "torch.nn.functional"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "re"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "re"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "re"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_infer.py", "target": "langdetect"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "__future__"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "argparse"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "importlib.util"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "json"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "logging"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "os"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "re"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "subprocess"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "sys"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "time"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "dataclasses"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "pathlib"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "typing"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "random"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "mcp.server"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "mcp.server.stdio"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "mcp"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "asyncio"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "fcntl"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "pty"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "select"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "struct"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "termios"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "torch"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "importlib.util"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "importlib.util"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_orchestrator.py", "target": "json"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_sweep.py", "target": "__future__"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_sweep.py", "target": "argparse"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_sweep.py", "target": "json"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_sweep.py", "target": "logging"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_sweep.py", "target": "random"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_sweep.py", "target": "sys"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_sweep.py", "target": "time"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_sweep.py", "target": "pathlib"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_sweep.py", "target": "typing"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_sweep.py", "target": "toposwarm_lazyown_orchestrator"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_sweep.py", "target": "topo_swarm_agent"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_lazyown_sweep.py", "target": "subprocess"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "__future__"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "hashlib"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "json"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "logging"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "math"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "os"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "re"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "sys"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "time"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "collections"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "dataclasses"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "pathlib"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "typing"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "numpy"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "sentence_transformers"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "sklearn.feature_extraction.text"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "numpy"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "sklearn.metrics.pairwise"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "numpy"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "subprocess"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "shutil"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "psutil"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "shutil"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "sklearn.feature_extraction.text"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "toposwarm_meta_harness.py", "target": "sklearn.metrics.pairwise"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "ts_utils.py", "target": "__future__"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "ts_utils.py", "target": "ast"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "ts_utils.py", "target": "importlib.util"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "ts_utils.py", "target": "logging"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "ts_utils.py", "target": "sys"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "ts_utils.py", "target": "functools"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "ts_utils.py", "target": "pathlib"}, {"confidence": "EXTRACTED", "relation": "imports", "source": "ts_utils.py", "target": "typing"}, {"confidence": "EXTRACTED", "relation": "resolved_imports", "source": "meta_harness_proposer.py", "target": "toposwarm_meta_harness.py"}, {"confidence": "EXTRACTED", "relation": "resolved_imports", "source": "tests/test_orchestrator.py", "target": "toposwarm_lazyown_orchestrator.py"}, {"confidence": "EXTRACTED", "relation": "resolved_imports", "source": "tests/test_orchestrator.py", "target": "toposwarm_lazyown_orchestrator.py"}, {"confidence": "EXTRACTED", "relation": "resolved_imports", "source": "tests/test_orchestrator.py", "target": "toposwarm_lazyown_orchestrator.py"}, {"confidence": "EXTRACTED", "relation": "resolved_imports", "source": "tests/test_orchestrator.py", "target": "toposwarm_lazyown_orchestrator.py"}, {"confidence": "EXTRACTED", "relation": "resolved_imports", "source": "topo_swarm_agent.py", "target": "ts_utils.py"}, {"confidence": "EXTRACTED", "relation": "resolved_imports", "source": "toposwarm_coevolve.py", "target": "toposwarm_meta_harness.py"}, {"confidence": "EXTRACTED", "relation": "resolved_imports", "source": "toposwarm_coevolve.py", "target": "toposwarm_lazyown_orchestrator.py"}, {"confidence": "EXTRACTED", "relation": "resolved_imports", "source": "toposwarm_coevolve.py", "target": "toposwarm_lazyown_orchestrator.py"}, {"confidence": "EXTRACTED", "relation": "resolved_imports", "source": "toposwarm_coevolve.py", "target": "toposwarm_infer.py"}, {"confidence": "EXTRACTED", "relation": "resolved_imports", "source": "toposwarm_coevolve.py", "target": "topo_swarm_agent.py"}, {"confidence": "EXTRACTED", "relation": "resolved_imports", "source": "toposwarm_coevolve.py", "target": "toposwarm_meta_harness.py"}, {"confidence": "EXTRACTED", "relation": "resolved_imports", "source": "toposwarm_continual_trainer.py", "target": "ts_utils.py"}, {"confidence": "EXTRACTED", "relation": "resolved_imports", "source": "toposwarm_continual_trainer.py", "target": "ts_utils.py"}, {"confidence": "EXTRACTED", "relation": "resolved_imports", "source": "toposwarm_lazyown_sweep.py", "target": "toposwarm_lazyown_orchestrator.py"}, {"confidence": "EXTRACTED", "relation": "resolved_imports", "source": "toposwarm_lazyown_sweep.py", "target": "topo_swarm_agent.py"}], "generator": "readmenator", "metadata": {"edge_count": 5169, "file_count": 17, "language_count": 1, "symbol_count": 636}, "nodes": [{"id": "lazyown_dataset_enhancer.py", "kind": "module", "label": "lazyown_dataset_enhancer.py", "language": "py", "sha256": "98f9f1179bb66369", "symbol_count": 19, "symbols": [{"doc": "Lower = easier.  Factors:\n  - prompt length (shorter = easier)\n  - number of words (fewer = easier)\n  - output length (shorter = easier)\n  - has error markers (harder)", "kind": "function", "line": 64, "name": "_difficulty", "signature": "def _difficulty(record)"}, {"kind": "class", "line": 87, "name": "ExperienceStoreReader", "signature": "class ExperienceStoreReader"}, {"doc": "Redact potential PII / sensitive data from LazyOwn output traces.", "kind": "method", "line": 136, "name": "_sanitize_output", "signature": "def _sanitize_output(text)"}, {"doc": "Standard ToolBench-format record.", "kind": "method", "line": 149, "name": "_build_toolbench_record", "signature": "def _build_toolbench_record(instruction, tool_name, arg, answer, domain)"}, {"kind": "class", "line": 165, "name": "DatasetEnhancer", "signature": "class DatasetEnhancer"}, {"kind": "method", "line": 348, "name": "print_stats", "signature": "def print_stats(records)"}, {"kind": "method", "line": 375, "name": "main", "signature": "def main()"}, {"kind": "method", "line": 88, "name": "__init__", "signature": "def __init__(self, log_dir)"}, {"kind": "method", "line": 91, "name": "list_runs", "signature": "def list_runs(self)"}, {"kind": "method", "line": 98, "name": "read_trace", "signature": "def read_trace(self, run_dir)"}, {"kind": "method", "line": 113, "name": "read_score", "signature": "def read_score(self, run_dir)"}, {"kind": "method", "line": 122, "name": "read_harness", "signature": "def read_harness(self, run_dir)"}, {"kind": "method", "line": 166, "name": "__init__", "signature": "def __init__(self, log_dir, max_runs)"}, {"kind": "method", "line": 171, "name": "enhance", "signature": "def enhance(self)"}, {"doc": "Add examples where the prompt is ambiguous and the model must NOT\npick a random tool, or where the user asks something outside LazyOwn's scope.", "kind": "method", "line": 236, "name": "add_negative_examples", "signature": "def add_negative_examples(self, records, n)"}, {"doc": "Sort by difficulty (easy → hard).", "kind": "method", "line": 261, "name": "curriculum_sort", "signature": "def curriculum_sort(self, records)"}, {"doc": "Deduplicate by instruction text only (same prompt can have different outputs).", "kind": "method", "line": 265, "name": "deduplicate", "signature": "def deduplicate(self, records)"}, {"doc": "Lightweight augmentation: replace IP addresses, hostnames, and common\nkeywords with variants to increase diversity without an LLM.", "kind": "method", "line": 276, "name": "augment_simple", "signature": "def augment_simple(self, records, multiplier)"}, {"kind": "method", "line": 301, "name": "run", "signature": "def run(self, merge_with)"}]}, {"id": "lazyown_dataset_generator.py", "kind": "module", "label": "lazyown_dataset_generator.py", "language": "py", "sha256": "44454f8ba5b145c4", "symbol_count": 8, "symbols": [{"kind": "function", "line": 3321, "name": "_make_record", "signature": "def _make_record(tool_name, desc, category, instruction, arg)"}, {"doc": "Replace common pentest terms with synonyms to increase diversity.", "kind": "function", "line": 3414, "name": "_apply_pentest_synonyms", "signature": "def _apply_pentest_synonyms(instr)"}, {"doc": "Generate additional phrasings via IP substitution, prefix injection, verb swap, and synonym replacement.", "kind": "function", "line": 3430, "name": "_expand", "signature": "def _expand(tool_name, phrasings)"}, {"doc": "Return True if the phrasing is too generic and likely to dilute training.\nCriteria:\n  - empty arg AND the instruction starts with a generic verb\n  - instruction has fewer than 4 meaningful tokens", "kind": "function", "line": 3554, "name": "_is_noisy_phrasing", "signature": "def _is_noisy_phrasing(instruction, arg)"}, {"kind": "function", "line": 3571, "name": "build_dataset", "signature": "def build_dataset()"}, {"kind": "function", "line": 3595, "name": "write_jsonl", "signature": "def write_jsonl(records, path)"}, {"kind": "function", "line": 3602, "name": "print_stats", "signature": "def print_stats(records)"}, {"kind": "function", "line": 3616, "name": "main", "signature": "def main()"}]}, {"id": "meta_harness_proposer.py", "kind": "module", "label": "meta_harness_proposer.py", "language": "py", "sha256": "ebc8e1ed5c9bd1fa", "symbol_count": 24, "symbols": [{"kind": "function", "line": 58, "name": "_setup_logger", "signature": "def _setup_logger(name, level)"}, {"kind": "class", "line": 75, "name": "LLMConfig", "signature": "class LLMConfig"}, {"doc": "Minimal OpenAI-compatible chat client using only urllib.\n\nAuto-falls back to local Ollama if the primary endpoint returns\n401/403/404 (auth or routing errors).", "kind": "class", "line": 86, "name": "LLMClient", "signature": "class LLMClient"}, {"doc": "Reads meta_harness_logs/ and builds diagnostic context.", "kind": "class", "line": 150, "name": "ExperienceReader", "signature": "class ExperienceReader"}, {"doc": "Applies code patches safely.", "kind": "class", "line": 243, "name": "PatchEngine", "signature": "class PatchEngine"}, {"doc": "Coding-agent proposer for harness optimisation.\n\nWorkflow:\n    1. Read experience store (scores + traces).\n    2. Build diagnostic context.\n    3. Read current harness source.\n    4. Prompt LLM to propose a patch.\n    5. Validate & apply patch.\n    6. Log the proposal as a new run.", "kind": "class", "line": 392, "name": "MetaHarnessProposer", "signature": "class MetaHarnessProposer"}, {"kind": "method", "line": 572, "name": "main", "signature": "def main()"}, {"kind": "method", "line": 93, "name": "__init__", "signature": "def __init__(self, cfg, logger)"}, {"kind": "method", "line": 97, "name": "_try_chat", "signature": "def _try_chat(self, api_url, model, system, user)"}, {"doc": "Send a chat request and return the assistant message content.", "kind": "method", "line": 121, "name": "chat", "signature": "def chat(self, system, user)"}, {"kind": "method", "line": 153, "name": "__init__", "signature": "def __init__(self, log_dir, logger)"}, {"kind": "method", "line": 157, "name": "list_runs", "signature": "def list_runs(self, n)"}, {"kind": "method", "line": 165, "name": "load_run", "signature": "def load_run(self, run_dir)"}, {"doc": "Build a rich diagnostic string containing:\n- failed runs with their traces\n- successful runs for contrast\n- aggregate statistics", "kind": "method", "line": 193, "name": "build_diagnostic_context", "signature": "def build_diagnostic_context(self, top_k)"}, {"kind": "method", "line": 246, "name": "__init__", "signature": "def __init__(self, logger)"}, {"doc": "Return (ok, error_message).", "kind": "method", "line": 249, "name": "validate_syntax", "signature": "def validate_syntax(self, code)"}, {"doc": "Validate and optionally write a full file rewrite.", "kind": "method", "line": 265, "name": "apply_full_rewrite", "signature": "def apply_full_rewrite(self, target_path, new_code, dry_run)"}, {"doc": "Remove leading ' 123: ' line numbers that the LLM may copy.", "kind": "method", "line": 283, "name": "_strip_line_numbers", "signature": "def _strip_line_numbers(self, s)"}, {"doc": "Replace a range of lines (1-indexed) with new text.", "kind": "method", "line": 287, "name": "apply_line_range", "signature": "def apply_line_range(self, target_path, line_start, line_end, new_string, dry_run)"}, {"doc": "Apply a targeted string replacement after validation.\n\nTries exact match first, then fuzzy match (ignoring leading/trailing\nwhitespace per line), then without line numbers.  If all fail, prints\nthe patch for manual apply.", "kind": "method", "line": 316, "name": "apply_diff_hunk", "signature": "def apply_diff_hunk(self, target_path, old_string, new_string, dry_run)"}, {"kind": "method", "line": 434, "name": "__init__", "signature": "def __init__(self, log_dir, llm_cfg, logger)"}, {"doc": "End-to-end propose-and-apply cycle.\n\nReturns True if a patch was successfully applied (or validated in dry-run).", "kind": "method", "line": 445, "name": "propose_patch", "signature": "def propose_patch(self, target_path, top_k, dry_run)"}, {"doc": "Store the proposer's reasoning so future loops can evaluate it.", "kind": "method", "line": 538, "name": "_log_proposal", "signature": "def _log_proposal(self, target_path, response, applied, diag)"}, {"kind": "method", "line": 331, "name": "_norm", "signature": "def _norm(s)"}]}, {"id": "tests/test_dataset_enhancer.py", "kind": "module", "label": "test_dataset_enhancer.py", "language": "py", "sha256": "38db7879fc24e78c", "symbol_count": 6, "symbols": [{"kind": "function", "line": 13, "name": "_load_enhancer_module", "signature": "def _load_enhancer_module()"}, {"kind": "function", "line": 24, "name": "test_sanitize_ip", "signature": "def test_sanitize_ip()"}, {"kind": "function", "line": 31, "name": "test_sanitize_password", "signature": "def test_sanitize_password()"}, {"kind": "function", "line": 38, "name": "test_sanitize_ntlm_hash", "signature": "def test_sanitize_ntlm_hash()"}, {"kind": "function", "line": 44, "name": "test_sanitize_email", "signature": "def test_sanitize_email()"}, {"kind": "function", "line": 50, "name": "test_sanitize_idempotent_on_clean_text", "signature": "def test_sanitize_idempotent_on_clean_text()"}]}, {"id": "tests/test_dataset_generator.py", "kind": "module", "label": "test_dataset_generator.py", "language": "py", "sha256": "18cb0016497dc1d1", "symbol_count": 5, "symbols": [{"kind": "function", "line": 13, "name": "_load_gen_module", "signature": "def _load_gen_module()"}, {"kind": "function", "line": 24, "name": "test_is_noisy_short_instruction", "signature": "def test_is_noisy_short_instruction()"}, {"kind": "function", "line": 30, "name": "test_is_noisy_generic_verb_empty_arg", "signature": "def test_is_noisy_generic_verb_empty_arg()"}, {"kind": "function", "line": 36, "name": "test_is_noisy_permitted_with_arg", "signature": "def test_is_noisy_permitted_with_arg()"}, {"kind": "function", "line": 42, "name": "test_build_dataset_filters_noise", "signature": "def test_build_dataset_filters_noise()"}]}, {"id": "tests/test_model_config.py", "kind": "module", "label": "test_model_config.py", "language": "py", "sha256": "60b1ec2276467b83", "symbol_count": 1, "symbols": [{"kind": "function", "line": 11, "name": "test_d_model_compatible_with_checkpoint", "signature": "def test_d_model_compatible_with_checkpoint()"}]}, {"id": "tests/test_orchestrator.py", "kind": "module", "label": "test_orchestrator.py", "language": "py", "sha256": "c630576ee71345c0", "symbol_count": 25, "symbols": [{"doc": "Unit tests for the multi-turn SessionContext.", "kind": "class", "line": 15, "name": "TestSessionContext", "signature": "class TestSessionContext"}, {"doc": "Tests for the deterministic keyword fallback router.", "kind": "class", "line": 56, "name": "TestKeywordRouter", "signature": "class TestKeywordRouter"}, {"doc": "Tests for the neural route path using mocks.", "kind": "class", "line": 89, "name": "TestNeuralRouter", "signature": "class TestNeuralRouter"}, {"doc": "Integration-level tests for the run() method.", "kind": "class", "line": 193, "name": "TestOrchestratorRun", "signature": "class TestOrchestratorRun"}, {"kind": "method", "line": 18, "name": "_load_ctx", "signature": "def _load_ctx(self)"}, {"kind": "method", "line": 23, "name": "test_empty_prefix", "signature": "def test_empty_prefix(self)"}, {"kind": "method", "line": 28, "name": "test_prefix_with_target", "signature": "def test_prefix_with_target(self)"}, {"kind": "method", "line": 35, "name": "test_update_extracts_ip", "signature": "def test_update_extracts_ip(self)"}, {"kind": "method", "line": 43, "name": "test_phase_progression", "signature": "def test_phase_progression(self)"}, {"kind": "method", "line": 49, "name": "test_findings_from_output", "signature": "def test_findings_from_output(self)"}, {"kind": "method", "line": 59, "name": "_load_router", "signature": "def _load_router(self)"}, {"kind": "method", "line": 63, "name": "test_recon_keyword", "signature": "def test_recon_keyword(self)"}, {"kind": "method", "line": 69, "name": "test_config_keyword", "signature": "def test_config_keyword(self)"}, {"kind": "method", "line": 74, "name": "test_c2_keyword", "signature": "def test_c2_keyword(self)"}, {"kind": "method", "line": 79, "name": "test_fallback_search", "signature": "def test_fallback_search(self)"}, {"kind": "method", "line": 84, "name": "test_extract_arg_ip", "signature": "def test_extract_arg_ip(self)"}, {"kind": "method", "line": 93, "name": "orchestrator", "signature": "def orchestrator(self)"}, {"kind": "method", "line": 120, "name": "test_neural_route_none_when_no_engine", "signature": "def test_neural_route_none_when_no_engine(self, orchestrator)"}, {"kind": "method", "line": 123, "name": "test_neural_route_with_mock_head", "signature": "def test_neural_route_with_mock_head(self, orchestrator)"}, {"kind": "method", "line": 159, "name": "test_neural_route_low_confidence_fallback", "signature": "def test_neural_route_low_confidence_fallback(self, orchestrator)"}, {"kind": "method", "line": 196, "name": "test_run_updates_session", "signature": "def test_run_updates_session(self)"}, {"kind": "method", "line": 135, "name": "mock_register_forward_hook", "signature": "def mock_register_forward_hook(cb)"}, {"kind": "method", "line": 141, "name": "mock_model_forward", "signature": "def mock_model_forward(ids)"}, {"kind": "method", "line": 169, "name": "mock_register_forward_hook", "signature": "def mock_register_forward_hook(cb)"}, {"kind": "method", "line": 175, "name": "mock_model_forward", "signature": "def mock_model_forward(ids)"}]}, {"id": "topo_swarm_agent.py", "kind": "module", "label": "topo_swarm_agent.py", "language": "py", "sha256": "7cf7119cd9bb3d4b", "symbol_count": 104, "symbols": [{"doc": "All architectural and training hyper-parameters in one place.\n\nScale target: fit inside 6 GB VRAM on an RTX 2060.\n- Weights: ~2 M params × 4 bytes = ~8 MB\n- Activations (B=4, S=256): ~256 MB peak with gradient checkpointing\n- Swarm overhead: N_AGENTS × D_MODEL × 4 bytes per Berry-phase tensor", "kind": "class", "line": 84, "name": "SwarmConfig", "signature": "class SwarmConfig"}, {"doc": "Return an idempotent logger. Delegates to ts_utils.setup_logger.", "kind": "method", "line": 225, "name": "_setup_logger", "signature": "def _setup_logger(name, level)"}, {"doc": "Deterministic seed across torch, numpy, and CUDA.", "kind": "method", "line": 243, "name": "_set_seed", "signature": "def _set_seed(seed, device)"}, {"doc": "Return total and trainable parameter counts.", "kind": "method", "line": 253, "name": "_param_count", "signature": "def _param_count(module)"}, {"doc": "Cached angular / radial position linspaces for soft torus assignment.", "kind": "method", "line": 264, "name": "_get_torus_positions", "signature": "def _get_torus_positions(n_angular, n_radial, device)"}, {"doc": "Pure-functional quaternion operations over arbitrary leading batch dims.\nTensors have shape [..., 4] where the last dim is [w, x, y, z].", "kind": "class", "line": 282, "name": "QuaternionOps", "signature": "class QuaternionOps"}, {"doc": "Linear map in the quaternion algebra.\n\nImplements W ⊗ x via a single batched einsum over stacked weight matrices,\nreducing CUDA kernel launches from 16 (naive 4×4 matmul loop) to 1.\n\nInput  x: [..., 4*in_q]\nOutput  : [..., 4*out_q]", "kind": "class", "line": 330, "name": "QuaternionLinear", "signature": "class QuaternionLinear(Module)"}, {"doc": "1-D spectral autoencoder acting as the function-call signal filter.\n\nCompresses the token representation via rfft → learned complex kernel →\nirfft → QuaternionLinear bottleneck → decode.  The bottleneck forces the\nmodel to route function-call intent through a harmonic low-band subspace,\nsuppressing lexical noise from the surrounding context.\n\nReturns (latent [B,S,latent_dim], recon_loss scalar).", "kind": "class", "line": 394, "name": "SpectralBottleneck", "signature": "class SpectralBottleneck(Module)"}, {"doc": "Root Mean Square Layer Normalisation (LLaMA-style, no bias).", "kind": "class", "line": 465, "name": "RMSNorm", "signature": "class RMSNorm(Module)"}, {"doc": "NTK-aware Rotary Position Embeddings.\n\nExtends the standard RoPE base frequency when the requested sequence length\nexceeds the training context, preventing aliasing in high-frequency dims.", "kind": "class", "line": 489, "name": "RotaryEmbedding", "signature": "class RotaryEmbedding(Module)"}, {"doc": "SwiGLU feed-forward: SiLU(gate(x)) * up(x) → down(...).", "kind": "class", "line": 548, "name": "SwiGLU", "signature": "class SwiGLU(Module)"}, {"doc": "Sigmoid gate: selects top-k experts per token, weights normalised.", "kind": "class", "line": 587, "name": "SwarmMoEGate", "signature": "class SwarmMoEGate(Module)"}, {"doc": "Drop-in MoE replacement for SwiGLU in TopoSwarmLayer.\n\nArchitecture: N_EXPERTS independent SwiGLU experts + sigmoid gate.\nEach token routes to top_k experts; outputs are weighted-summed.\n\nFor a 2M-param model (D=64, FFN_DIM=128):\n  - 4 experts, top-2, expert_dim=128 → same FLOP as one dense FFN\n    but 4× more representational capacity.", "kind": "class", "line": 608, "name": "SwarmMoE", "signature": "class SwarmMoE(Module)"}, {"doc": "Residual MoE adapter: output = LayerNorm(input + moe(input)).\n\nPlugs between model.norm_out and model.lm_head.  Zero-init on the output\nprojection of every expert means the adapter is an identity at init time —\nthe model starts at its existing accuracy and the adapter learns on top.\n\nExpert architecture: d_model → d_model//2 → d_model (small bottleneck)\nGate: sigmoid (MiMo V2 style) → top-k selection, normalised weights.", "kind": "class", "line": 665, "name": "SwarmMoEAdapter", "signature": "class SwarmMoEAdapter(Module)"}, {"doc": "Inject a SwarmMoEAdapter into an already-loaded TopoSwarmModel.\n\nThe backbone weights remain unchanged; only the adapter is new.\nOptionally freezes all backbone parameters so only the adapter trains.\n\nArgs:\n    model:           Loaded TopoSwarmModel instance.\n    n_experts:       Number of MoE experts in the adapter.\n    top_k:           Experts activated per token.\n    dropout:         Adapter dropout.\n    freeze_backbone: If True, freeze all non-adapter model parameters.\n    adapter_path:    If given, load adapter weights from this path instead\n                     of initialising from scratch.\n\nReturns:\n    The injected SwarmMoEAdapter (also stored as model.moe_adapter).", "kind": "method", "line": 749, "name": "inject_moe_adapter", "signature": "def inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)"}, {"doc": "Toroidal message-passing FFN replacement.\n\nPipeline per forward:\n1.  Flatten [B, S, D] → [B*S, D].\n2.  SpectralBottleneck: 1-D spectral encode → quaternion latent.\n3.  Torus projection: QuaternionLinear → 4 scalars → (phi1, phi2) angles.\n4.  Soft assignment: haversine distance to N_TORUS_NODES grid nodes.\n5.  Node grid construction: weighted blend of node embeddings + input.\n6.  Quaternion message-passing on the torus graph (vectorised scatter).\n7.  Readout: attention-weighted sum → SwiGLU projection.\n8.  Reshape [B*S, D] → [B, S, D].\n\nProcesses tokens in chunks of TORUS_TOKEN_CHUNK_SIZE to bound peak\nVRAM to O(chunk × N_NODES × D) rather than O(B*S × N_NODES × D).", "kind": "class", "line": 807, "name": "QuaternionTorusBrain", "signature": "class QuaternionTorusBrain(Module)"}, {"doc": "Grouped-query attention (GQA) with RoPE and quaternion Q/K projections.\n\nA lightweight per-head 1-D spectral filter compresses the query and key\nvectors before dot-product attention, forcing harmonic representations.", "kind": "class", "line": 998, "name": "QuaternionAttention", "signature": "class QuaternionAttention(Module)"}, {"doc": "Hierarchical Reasoning Model embedded in the torus agent.\n\nL-module (fast / action): recurrent GRU-gated unit responsible for\nthe syntax of tool calls (the \"how\").\n\nH-module (slow / strategy): a wider linear unit responsible for\ntool selection (the \"what\").\n\nThe ACT (Adaptive Computational Time) halt logit is computed from the\nHamilton-product norm of the final H-state quaternion: when the norm\nexceeds ACT_HALT_THRESHOLD the agent emits a decision; otherwise it\nre-enters the message-passing loop (the \"swarm consult\" step).", "kind": "class", "line": 1103, "name": "HRMModule", "signature": "class HRMModule(Module)"}, {"doc": "Single transformer layer: GQA attention + QuaternionTorusBrain FFN.\n\nBoth sub-layers use pre-norm (RMSNorm) and residual connections.\nGradient checkpointing is applied to the attention sub-layer.", "kind": "class", "line": 1205, "name": "TopoSwarmLayer", "signature": "class TopoSwarmLayer(Module)"}, {"doc": "Micro quaternionic toroidal transformer for tool-use reasoning.\n\nArchitecture:\n- Token embedding + learned positional bias.\n- N_LAYERS of TopoSwarmLayer (GQA + QuaternionTorusBrain).\n- HRM module on the pooled representation for ACT control.\n- Language-model head (tied weights with embedding).\n\nThe Berry-phase offset is passed through every layer to specialise each\nswarm agent slot without duplicating weight tensors.", "kind": "class", "line": 1273, "name": "TopoSwarmModel", "signature": "class TopoSwarmModel(Module)"}, {"doc": "Cross-entropy over the sequence without materialising the full [N, V] matrix.\n\nProcesses the sequence in chunks of chunk_size to bound peak memory to\nO(chunk_size × VOCAB_SIZE) instead of O(B*S × VOCAB_SIZE).\n\nArgs:\n    logits: [B, S, V] or [N, V].\n    targets: [B, S] or [N] integer targets.\n    chunk_size: Tokens per chunk.\n\nReturns:\n    Scalar mean cross-entropy.", "kind": "method", "line": 1445, "name": "_chunked_ce", "signature": "def _chunked_ce(logits, targets, chunk_size)"}, {"doc": "Three-tier episodic memory inspired by the tricameral neurology architecture.\n\nTier assignment is driven by a surprise score: cross-entropy modulated by\nthe mean ACT gate activity.  High-surprise events go to working memory\n(highest replay priority); low-surprise events to long-term if their\ncomputed importance exceeds a threshold.", "kind": "class", "line": 1487, "name": "EpisodicMemory", "signature": "class EpisodicMemory"}, {"doc": "Coordinates N_AGENTS lightweight agent slots over a shared weight tensor.\n\nEach agent slot is identified by a distinct Berry-phase offset on the\ntoroidal manifold.  The orchestrator:\n1. Dispatches the same input to all slots in parallel (or sequentially\n   if VRAM is tight).\n2. Aggregates outputs via majority vote on the halt decision and\n   mean-pooled logits.\n3. Selects the tool call proposed by the slot with the highest ACT\n   confidence (halt logit).\n\nSwarm consensus protocol:\n- If all slots halt → emit the tool call immediately.\n- If fewer than half halt → perform one extra ACT step (internal\n  torus message-passing consult) and re-evaluate.\n- Otherwise → emit the call proposed by the most confident slot.", "kind": "class", "line": 1602, "name": "SwarmOrchestrator", "signature": "class SwarmOrchestrator"}, {"doc": "Thin wrapper around tiktoken's GPT-2 BPE encoding.\n\nAdds special tool tokens by reserving a range at the top of the\nvocabulary [TOOL_TOKEN_OFFSET, TOOL_TOKEN_OFFSET + TOOL_VOCAB_SIZE).", "kind": "class", "line": 1693, "name": "BPETokenizer", "signature": "class BPETokenizer"}, {"doc": "ToolBench \"Instruction-Tool-Result\" dataset loader.\n\nAttempts to load from HuggingFace datasets first; falls back to a local\nJSONL file at cfg.DATASET_LOCAL_PATH.  Only successful traces\n(is_halt=True or equivalent) are retained.\n\nEach sample is a flat token sequence:\n    [instruction tokens] [tool token] [result tokens]\ntruncated to MAX_SEQ_LEN.  Training targets are the input shifted by 1.", "kind": "class", "line": 1811, "name": "ToolBenchDataset", "signature": "class ToolBenchDataset(Dataset)"}, {"doc": "Manages safetensors checkpoints with JSON metadata in a single directory.\n\nWrites to checkpoints_toposwarm/latest/ atomically by writing a temp\nfile and renaming it.", "kind": "class", "line": 2046, "name": "CheckpointManager", "signature": "class CheckpointManager"}, {"doc": "Tracks the kappa coherence metric over a sliding window to detect grokking.\n\nKappa is defined as the inverse of the cross-entropy loss (clipped),\nnormalised to [0, 1].  A sharp upward jump of more than KAPPA_JUMP_THRESHOLD\nwithin the window signals that the model has found the function-call\nstructure (the ToolBench grokking point).", "kind": "class", "line": 2149, "name": "KappaDetector", "signature": "class KappaDetector"}, {"doc": "Three-phase training pipeline for the TopoSwarm agent.\n\nPhase 0 (Kernel Calibration): Pre-trains only the SpectralBottleneck\nparameters on the API schema strings to seed the harmonic filter.\n\nPhase 1 (Main Training): Full model training with grokking detection\nvia the KappaDetector.\n\nPhase 2 (Annealing): Fine-tunes with a reduced learning rate and\ncosine schedule to stabilise the tool-call routing.", "kind": "class", "line": 2192, "name": "SwarmTrainer", "signature": "class SwarmTrainer"}, {"doc": "Build train and validation DataLoaders from the ToolBench dataset.\n\nArgs:\n    cfg: Swarm configuration.\n    tokenizer: BPETokenizer for encoding.\n    logger: Logger instance.\n\nReturns:\n    Tuple of (train_loader, val_loader).", "kind": "method", "line": 2509, "name": "build_dataloaders", "signature": "def build_dataloaders(cfg, tokenizer, logger)"}, {"doc": "CLI entry point.\n\nModes:\n    --train             : Run the full three-phase training pipeline.\n    --resume            : Resume training from the latest checkpoint.\n    --infer --prompt P  : Load checkpoint and run swarm inference.\n    --param-count       : Print model parameter counts and exit.", "kind": "method", "line": 2552, "name": "main", "signature": "def main()"}, {"kind": "method", "line": 202, "name": "__post_init__", "signature": "def __post_init__(self)"}, {"doc": "Hamilton (cross) product q1 ⊗ q2 for tensors of shape [..., 4].", "kind": "method", "line": 289, "name": "hamilton_product", "signature": "def hamilton_product(q1, q2)"}, {"doc": "Unit-normalise quaternion tensors.", "kind": "method", "line": 304, "name": "normalize", "signature": "def normalize(q, eps)"}, {"doc": "Apply a Berry-phase rotation around the w-axis of the quaternion manifold.\n\nMultiplies the (x, y, z) imaginary components by the complex phase\ne^{i*phase} encoded as a rotation in the yz-plane, leaving the real\ncomponent w unchanged.  Used to differentiate swarm agent slots.", "kind": "method", "line": 309, "name": "berry_phase_rotation", "signature": "def berry_phase_rotation(q, phase)"}, {"doc": "Initialise quaternion weight matrices.\n\nArgs:\n    in_features: Must be divisible by 4.\n    out_features: Must be divisible by 4.\n    bias: Whether to add a bias parameter.\n    init_std: Normal initialisation standard deviation.", "kind": "method", "line": 341, "name": "__init__", "signature": "def __init__(self, in_features, out_features, bias, init_std)"}, {"doc": "Fused Hamilton product via a single batched einsum.", "kind": "method", "line": 370, "name": "forward", "signature": "def forward(self, x)"}, {"doc": "Build encoder/decoder spectral kernels and quaternion projections.\n\nArgs:\n    cfg: Swarm configuration object.", "kind": "method", "line": 406, "name": "__init__", "signature": "def __init__(self, cfg)"}, {"doc": "Apply a learned complex spectral filter in the rfft domain.", "kind": "method", "line": 428, "name": "_filter", "signature": "def _filter(self, x, kr, ki)"}, {"doc": "Encode x through the spectral bottleneck.\n\nA single rfft of x is computed and reused by both the encode branch\nand the high-frequency penalty, avoiding a redundant FFT call.\n\nArgs:\n    x: Input tensor [..., D_MODEL].\n\nReturns:\n    Tuple of (latent [..., latent_dim], scalar auxiliary loss).", "kind": "method", "line": 436, "name": "forward", "signature": "def forward(self, x)"}, {"doc": "Args:\n    d_model: Feature dimension.\n    eps: Numerical stability epsilon.", "kind": "method", "line": 468, "name": "__init__", "signature": "def __init__(self, d_model, eps)"}, {"doc": "Normalise by the RMS of x and rescale by learned weight.", "kind": "method", "line": 478, "name": "forward", "signature": "def forward(self, x)"}, {"doc": "Args:\n    d_head: Attention head dimension.\n    max_seq_len: Maximum sequence length to pre-cache.\n    base: RoPE base frequency.\n    ntk_factor: Set to max_seq / train_seq when extrapolating.", "kind": "method", "line": 497, "name": "__init__", "signature": "def __init__(self, d_head, max_seq_len, base, ntk_factor)"}, {"doc": "Pre-compute cos/sin tables up to seq_len.", "kind": "method", "line": 522, "name": "_build_cache", "signature": "def _build_cache(self, seq_len)"}, {"kind": "method", "line": 530, "name": "_rotate_half", "signature": "def _rotate_half(self, x)"}, {"doc": "Apply rotary embedding to query or key tensor [B, H, S, d_head].", "kind": "method", "line": 534, "name": "forward", "signature": "def forward(self, x, seq_len)"}, {"doc": "Args:\n    d_model: Input and output feature dimension.\n    hidden_dim: Intermediate expansion dimension.\n    dropout: Dropout probability after the output projection.", "kind": "method", "line": 551, "name": "__init__", "signature": "def __init__(self, d_model, hidden_dim, dropout)"}, {"doc": "Gated SiLU activation with residual dropout.", "kind": "method", "line": 566, "name": "forward", "signature": "def forward(self, x)"}, {"kind": "method", "line": 590, "name": "__init__", "signature": "def __init__(self, d_model, n_experts, top_k)"}, {"doc": "x: [..., D] → (topk_idx [... K], topk_weight [..., K])", "kind": "method", "line": 597, "name": "forward", "signature": "def forward(self, x)"}, {"kind": "method", "line": 620, "name": "__init__", "signature": "def __init__(self, d_model, expert_hidden_dim, n_experts, top_k, dropout)"}, {"doc": "x: [B, S, D] → [B, S, D]  (autograd-safe, no in-place scatter)", "kind": "method", "line": 637, "name": "forward", "signature": "def forward(self, x)"}, {"kind": "method", "line": 679, "name": "__init__", "signature": "def __init__(self, d_model, n_experts, top_k, bottleneck, dropout)"}, {"doc": "x: [B, S, D] → [B, S, D]  (residual)\n\nAutograd-safe: no in-place scatter — computes all expert outputs at\nonce and weights them via a sparse weight tensor.", "kind": "method", "line": 705, "name": "forward", "signature": "def forward(self, x)"}, {"kind": "method", "line": 727, "name": "save", "signature": "def save(self, path)"}, {"kind": "method", "line": 738, "name": "load", "signature": "def load(cls, path)"}, {"doc": "Args:\n    cfg: Swarm configuration.", "kind": "method", "line": 825, "name": "__init__", "signature": "def __init__(self, cfg)"}, {"doc": "Construct the adjacency structure of the discrete torus.\n\nEach node (r, a) connects angularly to (r, a±1) and radially to\n(r±1, a).  Angular neighbours wrap around (periodic boundary).\nRadial neighbours are open (no wrap).  Edge types encode direction:\n0=ang-left, 1=ang-right, 2=rad-inner, 3=rad-outer.", "kind": "method", "line": 855, "name": "_build_torus_graph", "signature": "def _build_torus_graph(self)"}, {"doc": "Soft assignment of token coordinates to torus nodes via haversine distance.\n\nArgs:\n    phi1: Angular coordinate [-pi, pi] of shape [N].\n    phi2: Radial coordinate [-pi, pi] of shape [N].\n\nReturns:\n    Soft assignment weights [N, N_TORUS_NODES] summing to 1.", "kind": "method", "line": 887, "name": "_torus_soft_assign", "signature": "def _torus_soft_assign(self, phi1, phi2)"}, {"doc": "One round of quaternion message-passing on the torus graph.\n\nMessages are Hamilton-product-rotated by a learnable edge quaternion\nand aggregated via scatter-add to each destination node.\n\nArgs:\n    node_feat: Node feature tensor [N_chunk, N_NODES, D_MODEL].\n\nReturns:\n    Updated node features [N_chunk, N_NODES, D_MODEL].", "kind": "method", "line": 909, "name": "_message_passing", "signature": "def _message_passing(self, node_feat)"}, {"doc": "Full torus forward with optional Berry-phase offset for swarm slots.\n\nProcesses tokens in chunks to bound peak VRAM.\n\nArgs:\n    x: Input [B, S, D_MODEL].\n    berry_phase: Phase offset applied to the torus projection output\n                 for this agent slot, rotating the soft assignment\n                 and inducing specialisation.\n\nReturns:\n    Tuple of (output [B, S, D_MODEL], scalar auxiliary recon loss).", "kind": "method", "line": 940, "name": "forward", "signature": "def forward(self, x, berry_phase)"}, {"doc": "Args:\n    cfg: Swarm configuration.", "kind": "method", "line": 1006, "name": "__init__", "signature": "def __init__(self, cfg)"}, {"doc": "Apply the shared per-head spectral filter [B, H, S, d_head].", "kind": "method", "line": 1039, "name": "_head_filter", "signature": "def _head_filter(self, x)"}, {"doc": "GQA forward pass with RoPE and optional gradient checkpointing.\n\nArgs:\n    x: Input [B, S, D].\n    is_causal: Whether to apply causal masking.\n\nReturns:\n    Output [B, S, D].", "kind": "method", "line": 1045, "name": "forward", "signature": "def forward(self, x, is_causal)"}, {"doc": "Args:\n    cfg: Swarm configuration.", "kind": "method", "line": 1119, "name": "__init__", "signature": "def __init__(self, cfg)"}, {"doc": "One GRU-gated L-module step.", "kind": "method", "line": 1156, "name": "_l_step", "signature": "def _l_step(self, x, state)"}, {"doc": "One H-module strategy update.", "kind": "method", "line": 1163, "name": "_h_step", "signature": "def _h_step(self, z)"}, {"doc": "Run the HRM hierarchy and return the updated state with ACT signal.\n\nArgs:\n    x: Pooled context embedding [B, D].\n\nReturns:\n    Tuple of (h_state [B, D], halt_logit [B, 1], act_loss scalar).", "kind": "method", "line": 1167, "name": "forward", "signature": "def forward(self, x)"}, {"doc": "Args:\n    cfg: Swarm configuration.", "kind": "method", "line": 1213, "name": "__init__", "signature": "def __init__(self, cfg)"}, {"kind": "method", "line": 1237, "name": "_attn_fn", "signature": "def _attn_fn(self, x)"}, {"doc": "Pre-norm layer forward.\n\nArgs:\n    x: Input [B, S, D].\n    berry_phase: Swarm Berry-phase offset for the torus brain.\n\nReturns:\n    Tuple of (output [B, S, D], torus recon loss scalar).", "kind": "method", "line": 1240, "name": "forward", "signature": "def forward(self, x, berry_phase)"}, {"doc": "Args:\n    cfg: Swarm configuration.", "kind": "method", "line": 1287, "name": "__init__", "signature": "def __init__(self, cfg)"}, {"doc": "Full forward pass for one agent slot.\n\nArgs:\n    input_ids: Token ids [B, S].  Any id outside [0, VOCAB_SIZE) is\n               clamped before the embedding lookup so a bad upstream\n               token never triggers a CUDA device-side assert.\n    berry_phase: Slot-specific torus phase offset.\n    targets: Optional target ids [B, S] for computing the LM loss.\n\nReturns:\n    Dict with keys:\n    - \"logits\": [B, S_clip, VOCAB_SIZE]\n    - \"halt_logit\": [B, 1] ACT confidence\n    - \"loss\": scalar (only when targets is provided)\n    - \"recon_loss\": scalar torus reconstruction loss\n    - \"act_loss\": scalar ACT entropy regulariser", "kind": "method", "line": 1311, "name": "forward", "signature": "def forward(self, input_ids, berry_phase, targets)"}, {"doc": "Autoregressive generation with ACT-driven early stopping.\n\nThe model stops generating when the halt logit exceeds the threshold\nand ACT_MAX_STEPS is not yet reached, simulating the \"swarm consult\"\ninternal loop: low confidence → continue message-passing rather than\nemitting output.\n\nArgs:\n    input_ids: Prompt token ids [1, S].\n    max_new_tokens: Maximum tokens to generate.\n    temperature: Sampling temperature.\n    top_k: Top-k truncation before sampling.\n    berry_phase: Agent slot phase.\n    act_halt_threshold: Confidence threshold for early stopping.\n\nReturns:\n    Tuple of (generated ids [1, S + new_tokens], did_halt bool).", "kind": "method", "line": 1392, "name": "generate", "signature": "def generate(self, input_ids, max_new_tokens, temperature, top_k, berry_phase, act_halt_threshold)"}, {"doc": "Args:\n    cfg: Swarm configuration for capacity and threshold parameters.", "kind": "method", "line": 1497, "name": "__init__", "signature": "def __init__(self, cfg)"}, {"doc": "Surprise = cross-entropy × (1 - gate_mean), clipped to [0, 10].\n\nA high gate_mean (confident model) attenuates the surprise signal;\na low gate_mean (uncertain) amplifies it.\n\nArgs:\n    logits: Raw model logits [B, S, V] or [N, V].\n    targets: Integer targets matching logits.\n    gate_mean: Mean ACT halt probability in [0, 1].\n\nReturns:\n    Scalar surprise value.", "kind": "method", "line": 1512, "name": "compute_surprise", "signature": "def compute_surprise(logits, targets, gate_mean)"}, {"doc": "Store an episode in the appropriate memory tier.\n\nArgs:\n    episode: Dict of tensors/metadata describing the experience.\n    surprise: Scalar surprise score from compute_surprise.", "kind": "method", "line": 1537, "name": "store", "signature": "def store(self, episode, surprise)"}, {"doc": "Sample n episodes with priority proportional to surprise / importance.\n\nDraws from all three tiers; working memory contributes the most\nsamples (50 %), short-term 30 %, long-term 20 %.\n\nArgs:\n    n: Number of episodes to sample.\n\nReturns:\n    List of episode dicts.", "kind": "method", "line": 1558, "name": "sample", "signature": "def sample(self, n)"}, {"doc": "Apply exponential forgetting to the long-term memory scores.", "kind": "method", "line": 1591, "name": "_decay", "signature": "def _decay(self)"}, {"doc": "Args:\n    model: Shared TopoSwarmModel instance.\n    cfg: Swarm configuration.", "kind": "method", "line": 1622, "name": "__init__", "signature": "def __init__(self, model, cfg)"}, {"doc": "Run swarm inference and return the decoded output string.\n\nArgs:\n    input_ids: Prompt token ids [1, S].\n    tokenizer: BPETokenizer used to decode output ids.\n    max_new_tokens: Maximum tokens any slot may generate.\n    temperature: Sampling temperature.\n    top_k: Top-k sampling truncation.\n\nReturns:\n    Decoded string of the winning slot's output.", "kind": "method", "line": 1640, "name": "infer", "signature": "def infer(self, input_ids, tokenizer, max_new_tokens, temperature, top_k)"}, {"doc": "Args:\n    cfg: Swarm config (provides TOOL_TOKEN_OFFSET and TOOL_VOCAB_SIZE).", "kind": "method", "line": 1701, "name": "__init__", "signature": "def __init__(self, cfg)"}, {"doc": "Encode text to BPE token ids, clamped to the BPE vocab ceiling.\n\ntiktoken encodes exclusively within [0, bpe_vocab_size), but we clamp\ndefensively to prevent any edge-case overflow from reaching the\nembedding table lookup.", "kind": "method", "line": 1739, "name": "encode", "signature": "def encode(self, text)"}, {"doc": "Decode token ids to text, silently dropping tool tokens.", "kind": "method", "line": 1751, "name": "decode", "signature": "def decode(self, ids)"}, {"doc": "Return a stable integer token id for a named tool.\n\nAssigns a deterministic id within the tool-token range based on the\nMD5 hash of the tool name, ensuring consistent mapping across runs.\nThe result is always in [TOOL_TOKEN_OFFSET, TOOL_TOKEN_OFFSET + TOOL_VOCAB_SIZE)\nwhich is guaranteed to be < VOCAB_SIZE by the __init__ check above.\n\nArgs:\n    tool_name: Canonical tool identifier string.\n\nReturns:\n    Integer token id in [TOOL_TOKEN_OFFSET, TOOL_TOKEN_OFFSET + TOOL_VOCAB_SIZE).", "kind": "method", "line": 1756, "name": "tool_token", "signature": "def tool_token(self, tool_name)"}, {"doc": "Encode a ToolBench-style (instruction, tool, result) triple.\n\nInserts a dedicated tool token between the instruction and the result,\nso the model learns to associate the tool-token with the API semantics\nrather than carrying the full JSON in the sequence.\n\nAll returned ids are guaranteed to be in [0, VOCAB_SIZE) because:\n- BPE ids are clamped in encode() to [0, bpe_vocab_size).\n- tool_token() returns ids in [tool_offset, tool_offset + tool_vocab_size)\n  which is < VOCAB_SIZE by construction (checked in __init__).\n\nArgs:\n    instruction: Natural language instruction string.\n    tool_name: Tool / API identifier.\n    result: Observed tool output string.\n\nReturns:\n    Flat list of token ids, all in [0, VOCAB_SIZE).", "kind": "method", "line": 1778, "name": "encode_tool_trace", "signature": "def encode_tool_trace(self, instruction, tool_name, result)"}, {"doc": "Args:\n    cfg: Swarm configuration.\n    tokenizer: BPETokenizer for encoding traces.\n    split: Dataset split name.\n    logger: Optional logger instance.", "kind": "method", "line": 1824, "name": "__init__", "signature": "def __init__(self, cfg, tokenizer, split, logger)"}, {"doc": "Load and tokenise tool traces with three-level fallback.\n\nLevel 1 – Maurus/ToolBench (HuggingFace parquet, no loading script).\n    Schema: {query, api_list, domain}.  api_list is a JSON list of\n    dicts each with keys tool_name and api_name.\nLevel 2 – local JSONL at cfg.DATASET_LOCAL_PATH.\n    Accepted schemas: any dict with recognisable query/tool/result keys.\nLevel 3 – synthetic stubs of fixed length MAX_SEQ_LEN with token ids\n    inside [0, VOCAB_SIZE).  Safe dry-run fallback.", "kind": "method", "line": 1846, "name": "_load", "signature": "def _load(self, split)"}, {"doc": "Encode a tool-trace record to token ids.\n\nHandles three schemas:\n\nMaurus/ToolBench (primary):\n    query      : str  – natural language instruction\n    api_list   : list of dicts with keys tool_name, api_name,\n                 api_description (used as the \"result\" proxy)\n    domain     : str  – category label\n\nLegacy ToolBench JSONL:\n    instruction / query / input / prompt → instruction text\n    api_name / tool_name / tool          → tool identifier\n    response / result / output / answer  → observed result\n\nAll text fields are truncated to 512 characters before encoding to\nprevent single records from dominating the token budget.", "kind": "method", "line": 1927, "name": "_encode_record", "signature": "def _encode_record(self, rec)"}, {"doc": "Generate n synthetic tool-trace stubs safe for dry-run training.\n\nAll token ids produced from these stubs are guaranteed to be within\n[0, VOCAB_SIZE) because:\n- instruction and result text encode to ids within [0, bpe_vocab_size).\n- tool_token() returns ids within [TOOL_TOKEN_OFFSET, TOOL_TOKEN_OFFSET\n  + TOOL_VOCAB_SIZE) < VOCAB_SIZE (validated in BPETokenizer.__init__).", "kind": "method", "line": 1984, "name": "_synthetic_stubs", "signature": "def _synthetic_stubs(self, n)"}, {"kind": "method", "line": 2017, "name": "__len__", "signature": "def __len__(self)"}, {"doc": "Return a (input_ids, target_ids) pair of length MAX_SEQ_LEN.\n\nToken ids are clamped to [0, VOCAB_SIZE - 1] as a hard safety guard\nagainst any upstream encoding edge case that could produce an\nout-of-bounds embedding lookup on the GPU.", "kind": "method", "line": 2020, "name": "__getitem__", "signature": "def __getitem__(self, idx)"}, {"doc": "Args:\n    cfg: Swarm configuration.\n    logger: Logger instance.", "kind": "method", "line": 2054, "name": "__init__", "signature": "def __init__(self, cfg, logger)"}, {"doc": "Save model weights and metadata if the interval has elapsed.\n\nArgs:\n    model: Model to checkpoint.\n    optimizer: Optimizer state to checkpoint.\n    meta: Scalar metadata dict (epoch, step, loss, etc.).\n    force: If True, save regardless of the time interval.", "kind": "method", "line": 2066, "name": "save", "signature": "def save(self, model, optimizer, meta, force)"}, {"doc": "Load model weights and metadata from the latest checkpoint.\n\nArgs:\n    model: Target model (mutated in-place).\n    optimizer: Optional optimizer to restore state into.\n    device: Device string for weight map.\n\nReturns:\n    Metadata dict if found, None otherwise.", "kind": "method", "line": 2108, "name": "load", "signature": "def load(self, model, optimizer, device)"}, {"doc": "Args:\n    cfg: Swarm configuration (window and threshold).", "kind": "method", "line": 2159, "name": "__init__", "signature": "def __init__(self, cfg)"}, {"doc": "Update the detector with the latest loss value.\n\nArgs:\n    loss: Scalar training loss.\n\nReturns:\n    Tuple of (current_kappa, grokking_detected bool).", "kind": "method", "line": 2167, "name": "update", "signature": "def update(self, loss)"}, {"doc": "Args:\n    model: TopoSwarmModel instance.\n    cfg: Swarm configuration.\n    tokenizer: BPETokenizer.\n    logger: Logger instance.", "kind": "method", "line": 2206, "name": "__init__", "signature": "def __init__(self, model, cfg, tokenizer, logger)"}, {"doc": "Build AdamW with weight decay applied only to non-bias, non-norm params.\n\nArgs:\n    lr: Learning rate.\n\nReturns:\n    Configured AdamW optimizer.", "kind": "method", "line": 2233, "name": "_make_optimizer", "signature": "def _make_optimizer(self, lr)"}, {"doc": "Apply warmup + cosine decay learning rate schedule.", "kind": "method", "line": 2263, "name": "_warmup_cosine_lr", "signature": "def _warmup_cosine_lr(self, optimizer, step, total_steps, warmup_steps, base_lr)"}, {"doc": "Forward + backward for one micro-batch, returns detached loss.\n\nArgs:\n    optimizer: Current optimizer.\n    input_ids: [B, S] token ids.\n    targets: [B, S] target ids.\n    accum_step: Index within the gradient accumulation window.\n    berry_phase: Agent slot phase for this forward pass.\n\nReturns:\n    Scalar loss value (Python float).", "kind": "method", "line": 2280, "name": "_train_one_batch", "signature": "def _train_one_batch(self, optimizer, input_ids, targets, accum_step, berry_phase)"}, {"doc": "Phase 0: Kernel calibration on API schema tokens.\n\nFreezes all parameters except the SpectralBottleneck kernels,\ntraining only the spectral filter to recognise API intent.\n\nArgs:\n    dataloader: Training dataloader.\n    n_steps: Number of calibration gradient steps.", "kind": "method", "line": 2322, "name": "_phase0_calibrate", "signature": "def _phase0_calibrate(self, dataloader, n_steps)"}, {"doc": "Full three-phase training loop.\n\nPhase 0: Kernel calibration (50 steps, spectral params only).\nPhase 1: Main training for cfg.EPOCHS epochs with kappa detection.\nPhase 2: Cosine annealing for 1 extra epoch at half learning rate.\n\nArgs:\n    train_dl: Training DataLoader.\n    val_dl: Validation DataLoader.\n    resume: If True, attempt to restore from the latest checkpoint.", "kind": "method", "line": 2363, "name": "train", "signature": "def train(self, train_dl, val_dl, resume)"}, {"doc": "Compute mean validation loss over the first EVAL_INTERVAL_STEPS batches.\n\nArgs:\n    val_dl: Validation DataLoader.\n\nReturns:\n    Mean loss scalar.", "kind": "method", "line": 2476, "name": "_evaluate", "signature": "def _evaluate(self, val_dl)"}, {"kind": "method", "line": 1072, "name": "_manual_attn", "signature": "def _manual_attn()"}]}, {"id": "topogpt2_1.py", "kind": "module", "label": "topogpt2_1.py", "language": "py", "sha256": "28f93aa1f0651b03", "symbol_count": 126, "symbols": [{"doc": "Configuración completa para TopoGPT2.", "kind": "class", "line": 55, "name": "TopoGPT2Config", "signature": "class TopoGPT2Config"}, {"kind": "method", "line": 155, "name": "setup_logger", "signature": "def setup_logger(name, level)"}, {"kind": "method", "line": 165, "name": "set_seed", "signature": "def set_seed(seed, device)"}, {"doc": "Operaciones de cuaterniones puras en PyTorch.\nRepresentación: [..., 4]  donde last dim = [w, x, y, z]\nq = w + x*i + y*j + z*k", "kind": "class", "line": 177, "name": "QuaternionOps", "signature": "class QuaternionOps"}, {"doc": "Capa lineal con pesos cuaterniones.\n\nImplementa la multiplicación W * x en el álgebra de cuaterniones:\n- W = Ww + Wx*i + Wy*j + Wz*k  (cuaternión de pesos)\n- x = xw + xx*i + xy*j + xz*k  (cuaternión de entrada)\n- out = W * x  (producto de Hamilton extendido a vectores)\n\nParámetros: 4 matrices reales de forma [out_q, in_q]", "kind": "class", "line": 216, "name": "QuaternionLinear", "signature": "class QuaternionLinear(Module)"}, {"doc": "Convolución espectral 2D con cuaterniones y producto de Hamilton completo.\n\nOperación en dominio de frecuencia:\n    P(k) = W(k) ⊗ X(k)  (producto de Hamilton de cuaterniones complejos)\n\nDonde:\n    X(k) = FFT2(x) con 4 canales cuaterniones [Xw, Xx, Xy, Xz]\n    W(k) = kernel complejo aprendible con componentes [Ww, Wx, Wy, Wz]\n\nReglas del producto de Hamilton en dominio de frecuencia:\n    Pw = Ww·Xw - Wx·Xx - Wy·Xy - Wz·Xz\n    Px = Ww·Xx + Wx·Xw + Wy·Xz - Wz·Xy\n    Py = Ww·Xy - Wx·Xz + Wy·Xw + Wz·Xx\n    Pz = Ww·Xz + Wx·Xy - Wy·Xx + Wz·Xw\n\nCada Wc es un kernel complejo (partes real e imaginaria independientes).", "kind": "class", "line": 261, "name": "QuaternionSpectralLayer", "signature": "class QuaternionSpectralLayer(Module)"}, {"doc": "Autoencoder espectral con cuaterniones.\n\nOpera en dos niveles:\n1. Espectral 1D sobre el vector de features (FFT sobre dim D_MODEL):\n   captura la espectrografía global del embedding.\n2. Espectral 2D sobre el grid del toro (QuaternionSpectralLayer):\n   captura correlaciones espaciales en la topología.\n\nDevuelve (latent, recon_loss) para regularización.", "kind": "class", "line": 348, "name": "SpectralAutoencoder", "signature": "class SpectralAutoencoder(Module)"}, {"doc": "Reemplaza el MLP en cada capa del transformer.\n\nPipeline (completamente vectorizado sobre batch Y secuencia):\n\n1. Flatten: [B, S, D] → [B·S, D]\n2. SpectralAutoencoder: filtrado espectral 1D + compresión cuaternión\n3. Proyección al toro:\n   - Calcula 2 ángulos (phi1, phi2) ∈ [-π, π]²\n   - Asignación blanda a los 8 nodos via distancia circular en el toro\n4. Construye grid de nodos: [B·S, N_NODES=8, D_MODEL]\n5. QuaternionSpectralLayer 2D sobre el grid [B·S, 4*D_QUAT, RADIAL, ANGULAR]\n6. Message-passing con rotaciones cuaterniones sobre el grafo toro\n7. Readout: atención sobre los 8 nodos → [B·S, D_MODEL]\n8. Reshape: [B·S, D] → [B, S, D]", "kind": "class", "line": 431, "name": "QuaternionTorusBrain", "signature": "class QuaternionTorusBrain(Module)"}, {"doc": "Rotary Position Embeddings (RoPE) - Su et al., 2021.\nCodifica la posición como rotaciones del espacio de atención,\nnaturalmente relativas y sin parámetros extra.", "kind": "class", "line": 648, "name": "RotaryEmbedding", "signature": "class RotaryEmbedding(Module)"}, {"doc": "Root Mean Square Layer Normalization (sin bias). Más estable que LayerNorm.", "kind": "class", "line": 696, "name": "RMSNorm", "signature": "class RMSNorm(Module)"}, {"doc": "SwiGLU: SiLU(gate(x)) * up(x) -> down\nUsado en LLaMA 2/3, Qwen, Mistral en lugar de GELU-FFN.\nDimension interna: 8/3 * d_model (convención LLaMA, redondeada a múltiplo de 4).", "kind": "class", "line": 713, "name": "SwiGLU", "signature": "class SwiGLU(Module)"}, {"doc": "Mixture of Experts sobre la capa topologica.\n\nArquitectura (inspirada en DeepSeek-MoE / Mixtral):\n  - 1 experto compartido: QuaternionTorusBrain (siempre activo)\n  - N_EXPERTS expertos SwiGLU ligeros (activacion esparsa: Top-K por token)\n  - Router: Linear(D, N_EXPERTS) + softmax → top-K\n\nLoad-balancing loss (auxiliar): penaliza si un experto acapara todos los tokens.\nActiva MOE_TOP_K de N_EXPERTS expertos por token.\n\nSin MoE (MOE_ENABLED=False): se comporta como QuaternionTorusBrain puro.", "kind": "class", "line": 742, "name": "TopoMoEBrain", "signature": "class TopoMoEBrain(Module)"}, {"doc": "Multi-head attention con:\n- Flash Attention (scaled_dot_product_attention de PyTorch 2.0+)\n- Rotary Position Embeddings (RoPE)\n- GQA (Grouped Query Attention): N_KV_HEADS < N_HEADS, reduce VRAM de K/V\n- KV Cache para inferencia autoregresiva eficiente\n- Temperatura termodinámica aprendible", "kind": "class", "line": 847, "name": "MultiHeadAttention", "signature": "class MultiHeadAttention(Module)"}, {"doc": "Capa del transformer con TopoMoEBrain (TopoBrain + MoE SwiGLU experts).\n\nEsquema pre-norm (estilo LLaMA):\n    x = x + Attention_GQA(RMSNorm(x))\n    x = x + TopoMoEBrain(RMSNorm(x))", "kind": "class", "line": 929, "name": "TopoGPT2Layer", "signature": "class TopoGPT2Layer(Module)"}, {"doc": "TopoGPT2: Transformer de lenguaje con TopoBrain cuaternión-espectral.\n\nArquitectura:\n    Embedding de tokens + RoPE (en Attention)\n    N_LAYERS × TopoGPT2Layer (Attention + QuaternionTorusBrain)\n    RMSNorm final\n    Proyección a vocabulario (weight-tied con embeddings)", "kind": "class", "line": 976, "name": "TopoGPT2", "signature": "class TopoGPT2(Module)"}, {"doc": "Wrapper alrededor de tiktoken (GPT-2 compatible).", "kind": "class", "line": 1082, "name": "BPETokenizer", "signature": "class BPETokenizer"}, {"doc": "Descarga corpus de texto para entrenamiento.\n\nSoporta:\n- 'tinystories': ~2GB de cuentos cortos (ideal para pruebas)\n- 'wikitext103': ~500MB de Wikipedia curada\n- 'file': archivo de texto local\n\nUsa HuggingFace 'datasets' para TinyStories y WikiText.", "kind": "class", "line": 1107, "name": "CorpusDownloader", "signature": "class CorpusDownloader"}, {"doc": "Dataset de tokens para language modeling (next-token prediction).\n\nGuarda los tokens tokenizados en disco la primera vez (cache .pt)\npara evitar re-tokenizar en cada ejecucion. La clave de cache incluye\nun hash del contenido del corpus + tokenizador + max_tokens.", "kind": "class", "line": 1170, "name": "TokenizedDataset", "signature": "class TokenizedDataset(Dataset)"}, {"doc": "Gestiona checkpoints de forma acumulativa y segura.\n\nEstructura en disco:\n    checkpoints_topogpt2/\n      latest/\n        model.safetensors   <- pesos del modelo (formato seguro, sin pickle)\n        optimizer.pt        <- estado del optimizador (requiere .pt)\n        state.json          <- metadatos: epoch, step, historial, config\n      best/\n        model.safetensors\n        state.json\n      step_NNNNN/           <- snapshots periodicos (rotados)\n        model.safetensors\n        optimizer.pt\n        state.json\n\nEl historial se ACUMULA entre sesiones de entrenamiento: cada --resume\nagrega nuevas entradas a train_loss[], val_loss[], etc.", "kind": "class", "line": 1220, "name": "CheckpointManager", "signature": "class CheckpointManager"}, {"doc": "Entrenador acumulativo y resumible.\n\nCaracteristicas:\n- Checkpoint automatico en safetensors cada N minutos + cada epoch\n- Historial acumulativo entre sesiones (--resume agrega al historial existente)\n- Guarda el mejor modelo en checkpoints/best/ automaticamente\n- LR schedule: cosine con warmup relativo a los steps de ESTA sesion\n- Mixed Precision (AMP) + acumulacion de gradientes", "kind": "class", "line": 1453, "name": "TopoGPT2Trainer", "signature": "class TopoGPT2Trainer"}, {"doc": "Calcula todas las metricas del diagrama de fases de Book.md.\n\nTodas las metricas se derivan de cantidades medibles (pesos, gradientes):\n\ndelta  (δ): margen de discretizacion.  max|w - round(w)|\n            δ≈0 -> cristal;  δ≈0.49 -> vidrio frio\nkappa  (κ): numero de condicion de la covarianza del gradiente.\n            κ≈1 -> cristalino;  κ>>1 -> amorfo\nT_eff:      temperatura efectiva = (lr/2) * Var(gradiente).\n            T_eff→0 -> congelado; T_eff alto -> ruidoso\nalpha  (α): indice de pureza = -log(δ + ε).\n            α=20 -> perfecto; α<1 -> vidrio\nberry:      fase de Berry de los kernels espectrales imaginarios.\n            |berry|>π/2 con winding≠0 -> insulador topologico\nlc:         complejidad local = 1 - similitud coseno promedio entre filas.\nsp:         superposicion = correlacion promedio inter-fila de pesos.", "kind": "class", "line": 1746, "name": "MechanisticMetrics", "signature": "class MechanisticMetrics"}, {"doc": "Encuentra el ratio imaginario/real optimo para los kernels espectrales.\n\nAnalogia con main.py: evalua la transicion GOE→GUE en el espacio\nde kernels. Un ratio optimo promueve estructura topologica (insulador)\nvs estructura amorfa (vidrio).\n\nMetodo: calibra con un mini-batch y mide la varianza del gradiente\nen funcion del ratio. Ratios que minimizan la varianza de gradiente\n(maxima coherencia espectral) son preferibles.\n\nNo entrena: solo inicializa los kernels con distintos ratios y mide.\nTiempo tipico: < 30 segundos.", "kind": "class", "line": 1983, "name": "Phase0_KernelOptimizer", "signature": "class Phase0_KernelOptimizer"}, {"doc": "Encuentra el batch size optimo testando candidatos con pocos pasos.\n\nDe main.py: el batch size regula la temperatura del horno de cristalizacion.\nBatch sizes demasiado chicos -> ruido excesivo (vidrio frio).\nBatch sizes demasiado grandes -> sin presion annealing (amorfos).\nLa ventana optima empirica de main.py: [24, 128] para Strassen.\n\nPara LM, testeamos candidatos midiendo:\n- delta (δ): velocidad de descenso en prospect_steps pasos\n- T_eff: temperatura efectiva del gradiente\n\nTiempo tipico: < 2 minutos para 3 candidatos × 30 pasos.", "kind": "class", "line": 2058, "name": "Phase1_BatchProspector", "signature": "class Phase1_BatchProspector"}, {"doc": "Encuentra semillas prometedoras midiendo la trayectoria de delta.\n\nDe main.py: una semilla \"buena\" muestra delta descendente en los\nprimeros N pasos (enfriamiento). Una semilla \"mala\" se estanca en\nel plateau vidrioso (~0.49).\n\nCriterio de seleccion:\n1. Semillas con delta_velocity < 0 (enfriando) AND kappa bajo.\n2. Si no hay, semillas solo enfriando.\n3. Fallback: semilla con menor delta final.\n\nTiempo tipico: < 3 minutos para 5 semillas × 50 pasos.", "kind": "class", "line": 2141, "name": "Phase2_SeedMiner", "signature": "class Phase2_SeedMiner"}, {"doc": "Refinamiento post-entrenamiento mediante recocido simulado.\n\nDe main.py: despues de que el modelo converge, una fase de annealing\ncon criterio de aceptacion de Metropolis puede empujar los pesos\nhacia estados de menor energia libre (menor delta o mejor val_loss).\n\nAceptacion de Metropolis:\n    si Δloss < 0: siempre acepta (mejora)\n    si Δloss >= 0: acepta con prob exp(-Δloss / T)\n\nLa temperatura T decae exponencialmente: T(t) = T0 * cooling_rate^t\n\nAl rechazar: restaura el mejor estado conocido.\nSi se estanca: perturbacion termica (ruido gaussiano en pesos).\n\nTiempo: proporcional a refine_epochs (user-controlled).", "kind": "class", "line": 2223, "name": "Phase4_AnnealingRefiner", "signature": "class Phase4_AnnealingRefiner"}, {"doc": "Orquesta las 5 fases de entrenamiento segun main.py + Book.md.\n\nFases:\n  0  Kernel ratio optimization  (GOE-GUE spectral calibration)\n  1  Batch size prospecting      (temperatura del horno de cristalizacion)\n  2  Seed mining                 (seleccion de semilla enfriante)\n  3  Full training               (entrenamiento principal con metricas)\n  4  Annealing refinement        (recocido simulado post-entrenamiento)\n\nLas fases 0-2 son rapidas (prospecting). La fase 3 es el grueso.\nLa fase 4 es opcional (--refine).\n\nPara no ser prohibitivo:\n  --prospect         activa fases 0, 1, 2 antes del entrenamiento\n  --refine-epochs N  activa fase 4 con N epocas de annealing\n  Sin flags: solo fase 3 (comportamiento original, identico a antes)", "kind": "class", "line": 2384, "name": "TopoPhasePipeline", "signature": "class TopoPhasePipeline"}, {"kind": "method", "line": 2506, "name": "main", "signature": "def main()"}, {"kind": "method", "line": 124, "name": "__post_init__", "signature": "def __post_init__(self)"}, {"doc": "Producto de Hamilton q1 ⊗ q2. Ambos [..., 4].", "kind": "method", "line": 185, "name": "hamilton_product", "signature": "def hamilton_product(q1, q2)"}, {"kind": "method", "line": 197, "name": "normalize", "signature": "def normalize(q, eps)"}, {"kind": "method", "line": 201, "name": "conjugate", "signature": "def conjugate(q)"}, {"doc": "Rota vector 3D v por cuaternión unitario q. v:[...,3] q:[...,4]", "kind": "method", "line": 206, "name": "rotate_vector", "signature": "def rotate_vector(v, q)"}, {"kind": "method", "line": 228, "name": "__init__", "signature": "def __init__(self, in_features, out_features, bias)"}, {"doc": "x: [..., in_features] → [..., out_features]", "kind": "method", "line": 244, "name": "forward", "signature": "def forward(self, x)"}, {"kind": "method", "line": 281, "name": "__init__", "signature": "def __init__(self, in_q, out_q, grid_h, grid_w, init_scale)"}, {"kind": "method", "line": 300, "name": "_kernel", "signature": "def _kernel(self, c)"}, {"doc": "Suma sobre canales in_q: Y[b,o,h,w] = Σ_i W[i,o,h,w]·X[b,i,h,w]", "kind": "method", "line": 303, "name": "_contract", "signature": "def _contract(self, W, X)"}, {"doc": "x: [B, 4*in_q, H, W]  (4 canales cuaterniones sobre grid espacial)\n→ [B, 4*out_q, H, W]", "kind": "method", "line": 307, "name": "forward", "signature": "def forward(self, x)"}, {"kind": "method", "line": 361, "name": "__init__", "signature": "def __init__(self, config)"}, {"doc": "Filtro espectral 1D: x[..., D] → filtrado[..., D]", "kind": "method", "line": 393, "name": "_filter1d", "signature": "def _filter1d(self, x, kr, ki)"}, {"doc": "x: [..., D_MODEL] → latent: [..., D_LAT]", "kind": "method", "line": 399, "name": "encode", "signature": "def encode(self, x)"}, {"doc": "z: [..., D_LAT] → recon: [..., D_MODEL]", "kind": "method", "line": 404, "name": "decode", "signature": "def decode(self, z)"}, {"doc": "Devuelve (latent, recon_loss)", "kind": "method", "line": 409, "name": "forward", "signature": "def forward(self, x)"}, {"doc": "Procesa el grid del toro con QuaternionSpectralLayer.\ngrid: [B, 4*D_QUAT, RADIAL, ANGULAR]  →  [B, 4*D_QUAT, RADIAL, ANGULAR]", "kind": "method", "line": 416, "name": "process_torus_grid", "signature": "def process_torus_grid(self, grid)"}, {"kind": "method", "line": 449, "name": "__init__", "signature": "def __init__(self, d_model, config)"}, {"doc": "Construye las aristas del grafo toro 2×4.\n\nNodos indexados como: node = r * N_ANGULAR + a\n  r ∈ [0, RADIAL-1], a ∈ [0, ANGULAR-1]\n\nAristas angulares: nodo ↔ nodo a la izquierda/derecha (periódico)\nAristas radiales:  nodo ↔ nodo del anillo interior/exterior", "kind": "method", "line": 489, "name": "_build_torus_graph", "signature": "def _build_torus_graph(self)"}, {"doc": "Asignación blanda de tokens a los 8 nodos del toro via distancia circular.\n\nphi1: [BS] ángulo angular ∈ [-π, π]\nphi2: [BS] ángulo radial ∈ [-π, π]\n→ weights: [BS, N_NODES]  (suma a 1, softmax de distancias negativas)", "kind": "method", "line": 523, "name": "_torus_soft_assign", "signature": "def _torus_soft_assign(self, phi1, phi2)"}, {"doc": "Message-passing VECTORIZADO con rotaciones cuaterniones.\nSin bucles Python: todas las aristas se procesan en paralelo.\n\nnode_feat: [BS, N_NODES, D_MODEL]\n→ [BS, N_NODES, D_MODEL]", "kind": "method", "line": 550, "name": "_message_passing", "signature": "def _message_passing(self, node_feat)"}, {"doc": "x: [B, S, D_MODEL]\n→ output: [B, S, D_MODEL], recon_loss: scalar", "kind": "method", "line": 587, "name": "forward", "signature": "def forward(self, x)"}, {"kind": "method", "line": 655, "name": "__init__", "signature": "def __init__(self, d_head, max_seq_len, base)"}, {"kind": "method", "line": 661, "name": "_build_cache", "signature": "def _build_cache(self, seq_len)"}, {"kind": "method", "line": 668, "name": "_rotate_half", "signature": "def _rotate_half(self, x)"}, {"doc": "q, k: [B, n_heads, S_q/S_k, d_head]\noffset: posicion inicial (para KV cache: longitud del cache existente)\nAplica posiciones [offset .. offset+S-1] a q y k.", "kind": "method", "line": 672, "name": "forward", "signature": "def forward(self, q, k, seq_len, offset)"}, {"kind": "method", "line": 699, "name": "__init__", "signature": "def __init__(self, d_model, eps)"}, {"kind": "method", "line": 704, "name": "forward", "signature": "def forward(self, x)"}, {"kind": "method", "line": 720, "name": "__init__", "signature": "def __init__(self, d_model, expansion, dropout)"}, {"kind": "method", "line": 734, "name": "forward", "signature": "def forward(self, x)"}, {"kind": "method", "line": 757, "name": "__init__", "signature": "def __init__(self, d_model, config)"}, {"doc": "x: [N, D] donde N = B*S (tokens aplanados)\nRetorna:\nexpert_out: [N, D]  suma ponderada de top-K expertos\naux_loss:   escalar  load-balancing loss\nRouting vectorizado sin boolean indexing ni sincronizacion CUDA.\nUsa dispatch por indices agrupados (estilo Mixtral/DeepSeek) para\ncompatibilidad total con torch.utils.checkpoint.", "kind": "method", "line": 778, "name": "_route", "signature": "def _route(self, x)"}, {"doc": "x: [B, S, D]\n→ output: [B, S, D], aux_loss: escalar", "kind": "method", "line": 820, "name": "forward", "signature": "def forward(self, x)"}, {"kind": "method", "line": 857, "name": "__init__", "signature": "def __init__(self, d_model, n_heads, config)"}, {"doc": "Args:\n    x:        [B, S, D]\n    is_causal: usar mascara causal\n    past_kv:  (K_cache, V_cache) de pasos anteriores o None\nReturns:\n    out:      [B, S, D]\n    kv_cache: (K, V) completos para cachear en generate()", "kind": "method", "line": 875, "name": "forward", "signature": "def forward(self, x, is_causal, past_kv)"}, {"kind": "method", "line": 938, "name": "__init__", "signature": "def __init__(self, d_model, n_heads, config)"}, {"kind": "method", "line": 947, "name": "_forward_impl", "signature": "def _forward_impl(self, x, past_kv)"}, {"doc": "Retorna (x_out, aux_loss, kv_cache).\nCon gradient checkpointing en training (solo cuando no hay KV cache).", "kind": "method", "line": 956, "name": "forward", "signature": "def forward(self, x, past_kv)"}, {"kind": "method", "line": 987, "name": "__init__", "signature": "def __init__(self, config)"}, {"kind": "method", "line": 1006, "name": "_init_weights", "signature": "def _init_weights(self)"}, {"doc": "token_ids: [B, S]  (enteros)\npast_kvs:  lista de (K, V) por capa, o None para entrenamiento\n→ logits: [B, S, VOCAB_SIZE], aux_loss: scalar, new_kvs: list[(K,V)]", "kind": "method", "line": 1013, "name": "forward", "signature": "def forward(self, token_ids, past_kvs)"}, {"kind": "method", "line": 1036, "name": "count_params", "signature": "def count_params(self)"}, {"doc": "Generacion autoregresiva con KV cache y muestreo top-k.\nEn el primer paso procesa el prompt completo y guarda el cache.\nEn pasos siguientes solo procesa 1 token nuevo (O(n) en lugar de O(n^2)).", "kind": "method", "line": 1042, "name": "generate", "signature": "def generate(self, token_ids, max_new_tokens, temperature, top_k)"}, {"kind": "method", "line": 1085, "name": "__init__", "signature": "def __init__(self, encoding)"}, {"kind": "method", "line": 1093, "name": "encode", "signature": "def encode(self, text)"}, {"kind": "method", "line": 1096, "name": "decode", "signature": "def decode(self, tokens)"}, {"kind": "method", "line": 1099, "name": "eot_token", "signature": "def eot_token(self)"}, {"kind": "method", "line": 1119, "name": "__init__", "signature": "def __init__(self, corpus, data_dir, logger)"}, {"doc": "Devuelve el texto del corpus. Descarga si es necesario.", "kind": "method", "line": 1125, "name": "get_text", "signature": "def get_text(self, split)"}, {"kind": "method", "line": 1150, "name": "_download_hf", "signature": "def _download_hf(self, dataset_name, split, text_column, name)"}, {"kind": "method", "line": 1179, "name": "__init__", "signature": "def __init__(self, text, tokenizer, seq_len, max_tokens, cache_dir, split_tag)"}, {"kind": "method", "line": 1206, "name": "__len__", "signature": "def __len__(self)"}, {"kind": "method", "line": 1209, "name": "__getitem__", "signature": "def __getitem__(self, idx)"}, {"kind": "method", "line": 1245, "name": "__init__", "signature": "def __init__(self, config, logger)"}, {"doc": "Lee el checkpoint 'latest' y ajusta cfg.N_KV_HEADS / cfg.GQA_GROUPS\npara que coincidan con la arquitectura guardada.\nNecesario cuando el codigo cambio GQA despues de guardar el checkpoint.", "kind": "method", "line": 1255, "name": "patch_config_for_resume", "signature": "def patch_config_for_resume(self, cfg)"}, {"kind": "method", "line": 1284, "name": "_save_model", "signature": "def _save_model(self, model, directory)"}, {"kind": "method", "line": 1297, "name": "_load_model", "signature": "def _load_model(self, model, directory)"}, {"kind": "method", "line": 1328, "name": "_save_optimizer", "signature": "def _save_optimizer(self, optimizer, directory)"}, {"kind": "method", "line": 1331, "name": "_load_optimizer", "signature": "def _load_optimizer(self, optimizer, directory, device)"}, {"kind": "method", "line": 1340, "name": "_save_state", "signature": "def _save_state(self, state, directory)"}, {"kind": "method", "line": 1345, "name": "_load_state", "signature": "def _load_state(self, directory)"}, {"kind": "method", "line": 1356, "name": "should_save", "signature": "def should_save(self)"}, {"doc": "Guarda checkpoint completo.\n\nstate debe contener al menos: completed_epochs, global_step,\nbest_val_loss, history, config.", "kind": "method", "line": 1359, "name": "save", "signature": "def save(self, model, optimizer, state, is_best)"}, {"doc": "Carga el ultimo checkpoint guardado.\nDevuelve el state dict (vacio si no hay checkpoint).", "kind": "method", "line": 1404, "name": "load_latest", "signature": "def load_latest(self, model, optimizer)"}, {"doc": "Carga el mejor modelo guardado (solo pesos, sin optimizador).", "kind": "method", "line": 1431, "name": "load_best", "signature": "def load_best(self, model)"}, {"kind": "method", "line": 1443, "name": "has_checkpoint", "signature": "def has_checkpoint(self)"}, {"kind": "method", "line": 1465, "name": "__init__", "signature": "def __init__(self, model, config, tokenizer)"}, {"doc": "Carga el ultimo checkpoint disponible.\nRestaura: pesos del modelo, estado del optimizador, historial acumulado,\nepoch/step completados y mejor val_loss.\nDevuelve True si se cargo un checkpoint, False si empieza de cero.", "kind": "method", "line": 1500, "name": "resume", "signature": "def resume(self)"}, {"doc": "Construye el dict de estado para persistir en state.json.", "kind": "method", "line": 1525, "name": "_current_state", "signature": "def _current_state(self)"}, {"doc": "Cosine decay con warmup. El schedule es relativo a la sesion actual.", "kind": "method", "line": 1536, "name": "_cosine_lr", "signature": "def _cosine_lr(self, step_in_session, total_steps_session)"}, {"kind": "method", "line": 1544, "name": "_set_lr", "signature": "def _set_lr(self, lr)"}, {"doc": "Entrena cfg.EPOCHS epocas adicionales a partir de completed_epochs.\nEl historial se acumula sobre sesiones previas.", "kind": "method", "line": 1548, "name": "train", "signature": "def train(self, train_dl, val_dl)"}, {"doc": "Genera una muestra de texto al final de cada epoch para monitorear\nla calidad cualitativa del modelo (detecta degeneracion, repeticion, etc.).", "kind": "method", "line": 1684, "name": "_sample_text", "signature": "def _sample_text(self, tokenizer, prompts, max_new, temperature, top_k)"}, {"kind": "method", "line": 1716, "name": "evaluate", "signature": "def evaluate(self, dataloader)"}, {"kind": "method", "line": 1766, "name": "__init__", "signature": "def __init__(self, config)"}, {"kind": "method", "line": 1774, "name": "compute_delta", "signature": "def compute_delta(self, model)"}, {"kind": "method", "line": 1781, "name": "compute_alpha", "signature": "def compute_alpha(self, delta)"}, {"doc": "Captura gradientes de forma segura, ignorando tensores corruptos.", "kind": "method", "line": 1786, "name": "update_grad_buffer", "signature": "def update_grad_buffer(self, model)"}, {"doc": "T_eff = lr/2 * Var(gradiente). Temperatura termodinamica efectiva.", "kind": "method", "line": 1812, "name": "compute_t_eff", "signature": "def compute_t_eff(self, lr)"}, {"doc": "κ = λ_max / λ_min de la covarianza del gradiente.\nParámetro de orden para cristalización (κ≈1 = cristal).\nNota: requiere pasadas backward adicionales. Se ejecuta con protección\npara no corromper el estado AMP del trainer principal.", "kind": "method", "line": 1820, "name": "compute_kappa", "signature": "def compute_kappa(self, model, dataloader, n_batches)"}, {"doc": "Fase de Berry de los kernels espectrales imaginarios.\nSurge de los parametros ki_w, ki_x, ki_y, ki_z de QuaternionSpectralLayer.\n|berry|>pi/2 con winding!=0 indica estructura topologica.", "kind": "method", "line": 1878, "name": "compute_berry_phase", "signature": "def compute_berry_phase(self, model)"}, {"doc": "Complejidad local: 1 - similitud coseno promedio entre filas de pesos.", "kind": "method", "line": 1891, "name": "compute_lc", "signature": "def compute_lc(self, model)"}, {"doc": "Superposicion: correlacion inter-fila promedio (entrelazamiento de features).", "kind": "method", "line": 1905, "name": "compute_sp", "signature": "def compute_sp(self, model)"}, {"doc": "Clasificacion de fase segun Book.md:\n\ndiscrete_crystal:       delta<0.05, kappa<1.5\ntopological_insulator:  |berry|>pi/2, winding!=0\ncold_glass:             kappa>>1, delta>0.3\nfunctional_glass:       intermedio (lo mas comun en LM)", "kind": "method", "line": 1921, "name": "classify_phase", "signature": "def classify_phase(self, delta, kappa, berry)"}, {"doc": "Calcula todas las metricas.\ncompute_kappa=True hace pasadas backward adicionales (caro, usar cada N epochs).", "kind": "method", "line": 1940, "name": "compute_all", "signature": "def compute_all(self, model, lr, dataloader, compute_kappa)"}, {"kind": "method", "line": 1965, "name": "format_log", "signature": "def format_log(self, m)"}, {"kind": "method", "line": 2001, "name": "__init__", "signature": "def __init__(self, config, logger)"}, {"doc": "Mide la coherencia espectral para un ratio dado.\nRetorna: varianza del gradiente (menor = mas coherente = mejor).", "kind": "method", "line": 2005, "name": "_measure_ratio", "signature": "def _measure_ratio(self, ratio, sample_batch)"}, {"doc": "Retorna el mejor ratio de inicializacion de kernels espectrales.", "kind": "method", "line": 2034, "name": "optimize", "signature": "def optimize(self, dataloader)"}, {"kind": "method", "line": 2074, "name": "__init__", "signature": "def __init__(self, config, logger)"}, {"doc": "Retorna el mejor batch size segun delta y T_eff.", "kind": "method", "line": 2078, "name": "prospect", "signature": "def prospect(self, candidates, train_dataset, prospect_steps)"}, {"kind": "method", "line": 2157, "name": "__init__", "signature": "def __init__(self, config, logger)"}, {"doc": "Retorna la semilla con la mejor trayectoria de delta.", "kind": "method", "line": 2161, "name": "mine", "signature": "def mine(self, seed_start, n_seeds, train_dataset, prospect_steps)"}, {"kind": "method", "line": 2243, "name": "__init__", "signature": "def __init__(self, trainer, t0, cooling_rate, stagnation_patience)"}, {"doc": "Ejecuta refine_epochs epocas de recocido simulado.\nRetorna el historial de refinamiento.", "kind": "method", "line": 2252, "name": "refine", "signature": "def refine(self, train_dl, val_dl, refine_epochs)"}, {"kind": "method", "line": 2404, "name": "__init__", "signature": "def __init__(self, config, train_dataset, val_dataset, tokenizer, logger)"}, {"kind": "method", "line": 2414, "name": "_make_dataloaders", "signature": "def _make_dataloaders(self, batch_size)"}, {"doc": "Ejecuta el pipeline completo.\nRetorna el trainer con el modelo entrenado.", "kind": "method", "line": 2426, "name": "run", "signature": "def run(self, run_prospect, refine_epochs, resume, prospect_steps, probe_seeds, seed_start)"}, {"kind": "method", "line": 964, "name": "ckpt_fn", "signature": "def ckpt_fn(x_in)"}]}, {"id": "toposwarm_coevolve.py", "kind": "module", "label": "toposwarm_coevolve.py", "language": "py", "sha256": "58607ec4396b984f", "symbol_count": 33, "symbols": [{"doc": "Discover LazyOwn installation directory.\n\nPriority:\n  1. LAZYOWN_DIR environment variable (expanded ~).\n  2. Default relative to this script: <repo>/LazyOwn.\n  3. User home directory: ~/LazyOwn.\n  4. Return the relative default anyway (caller will see available=False).", "kind": "function", "line": 63, "name": "_resolve_lazyown_dir", "signature": "def _resolve_lazyown_dir()"}, {"kind": "function", "line": 90, "name": "_setup_logger", "signature": "def _setup_logger(name, level)"}, {"doc": "Simple mutation operators over MetaHarnessConfig dicts.", "kind": "class", "line": 128, "name": "HarnessMutation", "signature": "class HarnessMutation"}, {"kind": "method", "line": 175, "name": "_clip", "signature": "def _clip(x, lo, hi)"}, {"doc": "Deterministic mock of LazyOwnBridge for isolated harness evaluation.\nReturns canned responses so the orchestrator can be exercised even when\nLazyOwn is not present.", "kind": "class", "line": 183, "name": "MockLazyOwnBridge", "signature": "class MockLazyOwnBridge"}, {"doc": "Evaluates a harness configuration by running the LazyOwn orchestrator\non a suite of validation prompts and aggregating scores.\n\nUses in-process evaluation (no subprocess) so:\n- Meta-Harness logs are written to the same filesystem store.\n- Import errors are visible immediately.\n- Latencies are realistic.", "kind": "class", "line": 233, "name": "HarnessEvaluator", "signature": "class HarnessEvaluator"}, {"doc": "Thin wrapper around toposwarm_continual_trainer.py for inner-loop\nweight updates.", "kind": "class", "line": 391, "name": "WeightTrainer", "signature": "class WeightTrainer"}, {"doc": "Outer-loop harness evolution with optional inner-loop weight co-evolution.", "kind": "class", "line": 451, "name": "CoEvolutionEngine", "signature": "class CoEvolutionEngine"}, {"kind": "method", "line": 646, "name": "main", "signature": "def main()"}, {"kind": "method", "line": 132, "name": "mutate", "signature": "def mutate(cfg_dict)"}, {"kind": "method", "line": 167, "name": "crossover", "signature": "def crossover(a, b)"}, {"kind": "method", "line": 190, "name": "__init__", "signature": "def __init__(self)"}, {"kind": "method", "line": 196, "name": "available", "signature": "def available(self)"}, {"kind": "method", "line": 199, "name": "run", "signature": "def run(self, command, timeout)"}, {"kind": "method", "line": 222, "name": "get_config", "signature": "def get_config(self)"}, {"kind": "method", "line": 225, "name": "set_config", "signature": "def set_config(self, key, value)"}, {"kind": "method", "line": 244, "name": "__init__", "signature": "def __init__(self, prompts, lazyown_dir, logger, use_mock_bridge)"}, {"doc": "Run each prompt through the orchestrator and collect metrics.\n\nAlso logs every evaluation to the Meta-Harness experience store so the\nproposer has data to diagnose.", "kind": "method", "line": 256, "name": "evaluate", "signature": "def evaluate(self, cfg_dict)"}, {"doc": "Build a LazyOwnOrchestrator with the given MetaHarnessConfig.", "kind": "method", "line": 313, "name": "_build_orchestrator", "signature": "def _build_orchestrator(self, cfg_dict)"}, {"doc": "Write one evaluation to the Meta-Harness experience store.", "kind": "method", "line": 343, "name": "_log_run", "signature": "def _log_run(self, orch, prompt, result, latency_ms, ctx_len, ok, cfg_dict)"}, {"kind": "method", "line": 397, "name": "__init__", "signature": "def __init__(self, logger)"}, {"kind": "method", "line": 402, "name": "_load", "signature": "def _load(self)"}, {"kind": "method", "line": 415, "name": "is_available", "signature": "def is_available(self)"}, {"doc": "Run a short fine-tuning burst and return metrics.", "kind": "method", "line": 418, "name": "fine_tune", "signature": "def fine_tune(self, dataset_path, steps, learning_rate)"}, {"kind": "method", "line": 456, "name": "__init__", "signature": "def __init__(self, generations, population_size, train_steps_per_gen, proposer_interval, lazyown_dir, logger)"}, {"kind": "method", "line": 490, "name": "run", "signature": "def run(self)"}, {"kind": "method", "line": 550, "name": "_next_generation", "signature": "def _next_generation(self, scores)"}, {"kind": "method", "line": 567, "name": "_tournament_select", "signature": "def _tournament_select(sorted_scores, k)"}, {"kind": "method", "line": 575, "name": "_is_on_frontier", "signature": "def _is_on_frontier(self, cfg, metrics)"}, {"kind": "method", "line": 596, "name": "_run_proposer", "signature": "def _run_proposer(self)"}, {"kind": "method", "line": 619, "name": "_save_state", "signature": "def _save_state(self, generation)"}, {"kind": "method", "line": 628, "name": "load_state", "signature": "def load_state(self, path)"}, {"kind": "method", "line": 635, "name": "_report_frontier", "signature": "def _report_frontier(self)"}]}, {"id": "toposwarm_continual_trainer.py", "kind": "module", "label": "toposwarm_continual_trainer.py", "language": "py", "sha256": "3409a8a2120846de", "symbol_count": 51, "symbols": [{"kind": "function", "line": 91, "name": "_import", "signature": "def _import(name, filename)"}, {"doc": "All hyper-parameters for the continual learning run.", "kind": "class", "line": 111, "name": "ContinualConfig", "signature": "class ContinualConfig"}, {"kind": "method", "line": 158, "name": "_setup_logger", "signature": "def _setup_logger(level)"}, {"doc": "Tracks per-example surprise scores and returns a priority-weighted\nreplay sample so the trainer oversamples examples the model is failing on.\n\nSurprise (from NeuroLogos tricameral):\n    surprise = CE_loss × (1 − confidence)\nwhere confidence = softmax_max of the LM-head logits at the routing position.\n\nHigh surprise = model is wrong AND was overconfident → hardest to learn.\nThese examples are stored and mixed into subsequent mini-batches at a\nconfigurable ratio (default 25 % of each batch).", "kind": "class", "line": 166, "name": "SurpriseBuffer", "signature": "class SurpriseBuffer"}, {"kind": "method", "line": 232, "name": "_load_jsonl", "signature": "def _load_jsonl(path)"}, {"doc": "Encode a ToolBench-format record into (input_ids, target_ids).\n\nUses the same compact format as topo_swarm_agent.ToolBenchDataset._encode_record:\n    [instruction BPE tokens]  [tool token]  [compact result BPE tokens]\n\nThis matches the pretraining distribution exactly, keeping cross-entropy in\nthe same range as the original training (1-2 nats) rather than the full\nvocabulary baseline (~10.8 nats for random predictions over 50k+ tokens).", "kind": "method", "line": 247, "name": "_encode_record", "signature": "def _encode_record(record, tok, cfg)"}, {"kind": "class", "line": 300, "name": "ToolBenchDataset", "signature": "class ToolBenchDataset(Dataset)"}, {"kind": "method", "line": 319, "name": "_collate", "signature": "def _collate(batch)"}, {"doc": "Circular buffer of ToolBench examples.\n\nRandomly selects REPLAY_RATIO * batch_size samples to mix into every\nfine-tuning batch, ensuring the model continuously sees original-task\nexamples during LazyOwn training.", "kind": "class", "line": 334, "name": "ReplayBuffer", "signature": "class ReplayBuffer"}, {"doc": "Elastic Weight Consolidation.\n\nComputes the diagonal of the Fisher Information Matrix on a sample of\nToolBench data, then adds the quadratic penalty to the loss at every\nfine-tuning step.\n\nThe penalty is:\n    L_ewc = λ/2 · Σ_i  F_i · (θ_i − θ*_i)²\n\nwhere θ* is the snapshot of parameters BEFORE fine-tuning begins, and\nF_i is the empirical Fisher diagonal (mean squared gradient of log-prob).", "kind": "class", "line": 365, "name": "EWC", "signature": "class EWC"}, {"doc": "Liquid neuron for routing: slow proj (gradient) + fast Hebbian weights.\n\nArchitecture:\n    slow_out  = W_slow(x)            # [B, n_tools], gradient path\n    fast_out  = x @ W_fast.T         # [B, n_tools], Hebbian path, no grad\n    output    = LayerNorm(slow_out + fast_scale * fast_out)\n\nW_fast is updated after each training step via:\n    ΔW_fast = lr_hebb × (post.T @ pre) / B   (clamped ±0.3)\nwhere pre = hidden states, post = one-hot tool labels.\n\nHomeostasis clips output norm to [0.5, 2.0] to prevent explosion.", "kind": "class", "line": 514, "name": "SwarmLiquidNeuron", "signature": "class SwarmLiquidNeuron(Module)"}, {"doc": "Thin linear probe: d_model → n_tools.\n\nTrained on top of the frozen (or lightly-tuned) backbone with standard\ncross-entropy over the N LazyOwn tools.  Bypasses the 50k-token LM head\nso 100% of the gradient goes to the routing decision.\n\nTool-to-index mapping is deterministic (sorted tool name list), so the\nhead can be saved/loaded independently of the backbone checkpoint.", "kind": "class", "line": 600, "name": "RoutingHead", "signature": "class RoutingHead(Module)"}, {"doc": "Fine-tuning loop with EWC + Replay.\n\nEach training step:\n    1. Sample a mini-batch from LazyOwn dataset.\n    2. Sample REPLAY_RATIO fraction from ToolBench replay buffer.\n    3. Concatenate → mixed batch.\n    4. Compute task loss on mixed batch.\n    5. Add EWC penalty.\n    6. Backward + gradient clip + optimizer step.\n\nThe combined loss is:\n    L = L_task(mixed_batch) + EWC.penalty()", "kind": "class", "line": 730, "name": "ContinualTrainer", "signature": "class ContinualTrainer"}, {"doc": "Measure routing accuracy on a held-out subset of both datasets.\n\nRouting accuracy = fraction of examples where the highest-probability\ntool token matches the ground-truth tool in the api_list.", "kind": "method", "line": 1137, "name": "evaluate_routing", "signature": "def evaluate_routing(model, cfg, tok, lazyown_records, toolbench_records, logger)"}, {"kind": "method", "line": 1195, "name": "build_model_and_tok", "signature": "def build_model_and_tok(cl_cfg, logger)"}, {"doc": "Generate dataset → compute Fisher → fine-tune → evaluate.", "kind": "method", "line": 1217, "name": "run_full_pipeline", "signature": "def run_full_pipeline(cl_cfg, logger)"}, {"kind": "method", "line": 1384, "name": "main", "signature": "def main()"}, {"kind": "method", "line": 180, "name": "__init__", "signature": "def __init__(self, maxsize, replay_ratio)"}, {"doc": "Add batch examples to buffer, keyed by surprise score.", "kind": "method", "line": 186, "name": "update", "signature": "def update(self, records, task_losses, logits)"}, {"doc": "Return a priority-weighted sample of hard examples.", "kind": "method", "line": 213, "name": "sample", "signature": "def sample(self, batch_size)"}, {"kind": "method", "line": 223, "name": "__len__", "signature": "def __len__(self)"}, {"kind": "method", "line": 301, "name": "__init__", "signature": "def __init__(self, records, tok, cfg)"}, {"kind": "method", "line": 312, "name": "__len__", "signature": "def __len__(self)"}, {"kind": "method", "line": 315, "name": "__getitem__", "signature": "def __getitem__(self, idx)"}, {"kind": "method", "line": 343, "name": "__init__", "signature": "def __init__(self, records, max_size, tok, cfg)"}, {"kind": "method", "line": 351, "name": "sample", "signature": "def sample(self, n)"}, {"kind": "method", "line": 356, "name": "__len__", "signature": "def __len__(self)"}, {"kind": "method", "line": 380, "name": "__init__", "signature": "def __init__(self, model, cfg, cl_cfg, tok, logger)"}, {"doc": "Compute Fisher diagonal on a sample of ToolBench records and snapshot θ*.\n\nUses label log-prob gradients (empirical Fisher):\n    F_i = (1/N) Σ_n  (∂ log p(y_n|x_n, θ) / ∂ θ_i)²", "kind": "method", "line": 401, "name": "compute", "signature": "def compute(self, toolbench_records)"}, {"kind": "method", "line": 465, "name": "save", "signature": "def save(self, path)"}, {"kind": "method", "line": 470, "name": "load", "signature": "def load(self, path)"}, {"doc": "Returns the EWC penalty term to add to the task loss.\n\nComplexity: O(params) per step — negligible for a 2M-param model.", "kind": "method", "line": 481, "name": "penalty", "signature": "def penalty(self)"}, {"kind": "method", "line": 534, "name": "__init__", "signature": "def __init__(self, d_model, n_tools)"}, {"doc": "x: [B, d_model] → logits [B, n_tools]", "kind": "method", "line": 551, "name": "forward", "signature": "def forward(self, x)"}, {"doc": "Strengthen W_fast associations after correct predictions.\n\npre:    [B, d_model] — hidden states (instruction-end position)\nlabels: [B]          — true tool class indices", "kind": "method", "line": 570, "name": "hebbian_update", "signature": "def hebbian_update(self, pre, labels)"}, {"kind": "method", "line": 614, "name": "__init__", "signature": "def __init__(self, d_model, tool_names, n_experts, top_k, hidden_dim)"}, {"kind": "method", "line": 651, "name": "n_tools", "signature": "def n_tools(self)"}, {"doc": "hidden: [B, d_model] → logits [B, n_tools]\n\nPipeline:\n  0. Pre-MLP: enrich representation capacity\n  1. LiquidNeuron: slow grad + fast Hebbian → base logits [B, n_tools]\n  2. MoE gate: select top-k specialty expert refinements\n  3. Weighted sum of expert-refined logits", "kind": "method", "line": 654, "name": "forward", "signature": "def forward(self, hidden)"}, {"kind": "method", "line": 685, "name": "label", "signature": "def label(self, tool_name)"}, {"doc": "hidden: [B, d_model] → list of predicted tool name strings", "kind": "method", "line": 688, "name": "predict", "signature": "def predict(self, hidden)"}, {"kind": "method", "line": 695, "name": "save", "signature": "def save(self, path)"}, {"kind": "method", "line": 706, "name": "load", "signature": "def load(cls, d_model, path)"}, {"kind": "method", "line": 746, "name": "__init__", "signature": "def __init__(self, model, cfg, cl_cfg, tok, ewc, replay, logger, routing_head)"}, {"kind": "method", "line": 782, "name": "_make_optimizer", "signature": "def _make_optimizer(self)"}, {"kind": "method", "line": 821, "name": "_lr_schedule", "signature": "def _lr_schedule(optimizer, step, total, warmup, base_lr)"}, {"doc": "Append replay samples to the LazyOwn batch.", "kind": "method", "line": 830, "name": "_merge_with_replay", "signature": "def _merge_with_replay(self, ids, tgt)"}, {"doc": "Routing accuracy using the LM head (primary) and routing head (secondary).\n\nFeeds only instruction tokens; evaluates the last-position logits.\nUses cached encode for speed.  Always returns LM-head accuracy (which\nmatches the training objective) so the metric is honest.", "kind": "method", "line": 863, "name": "_routing_accuracy", "signature": "def _routing_accuracy(self, records)"}, {"kind": "method", "line": 923, "name": "train", "signature": "def train(self, lazyown_dataset, train_records, val_records)"}, {"kind": "method", "line": 1153, "name": "_accuracy", "signature": "def _accuracy(records, label)"}, {"kind": "method", "line": 887, "name": "_hook", "signature": "def _hook(m, i, o)"}, {"kind": "method", "line": 995, "name": "_capture", "signature": "def _capture(module, inp, out_h)"}]}, {"id": "toposwarm_hybrid.py", "kind": "module", "label": "toposwarm_hybrid.py", "language": "py", "sha256": "d105e9c5ade780c3", "symbol_count": 48, "symbols": [{"doc": "Import topo_swarm_agent, searching script dir then cwd.", "kind": "function", "line": 85, "name": "_import_agent", "signature": "def _import_agent()"}, {"doc": "All hyper-parameters for the hybrid system — zero magic numbers.", "kind": "class", "line": 115, "name": "HybridConfig", "signature": "class HybridConfig"}, {"doc": "Idempotent logger with a single StreamHandler.", "kind": "method", "line": 164, "name": "_setup_logger", "signature": "def _setup_logger(name, level)"}, {"doc": "Evaluate a math expression safely via AST — no eval().", "kind": "method", "line": 182, "name": "_safe_eval", "signature": "def _safe_eval(expr)"}, {"doc": "Structured result from a tool call.", "kind": "class", "line": 218, "name": "ToolResult", "signature": "class ToolResult"}, {"doc": "Registry of executable tools with keyword-based routing.", "kind": "class", "line": 231, "name": "ToolRegistry", "signature": "class ToolRegistry"}, {"doc": "Thin wrapper around TopoSwarmModel that performs only tool routing.\n\nThe router uses keyword-based routing (deterministic, no model inference\nneeded for the routing decision) combined with the crystallised model for\nswarm-consensus confidence scoring.\n\nBecause the model's Pass 2 output is always noisy, we bypass it entirely\nand return only the (tool_name, tool_arg) pair.  The LanguageBackend\nhandles all text generation.", "kind": "class", "line": 396, "name": "TopoSwarmRouter", "signature": "class TopoSwarmRouter"}, {"doc": "Language generation backend.\n\nSupports three modes:\n- tinystories: HuggingFace GPT-2-style model loaded via transformers.\n- checkpoint:  Raw PyTorch state_dict for your own 25M model.\n- none:        Returns empty string; caller uses deterministic template.", "kind": "class", "line": 465, "name": "LanguageBackend", "signature": "class LanguageBackend"}, {"doc": "Build a clean deterministic answer from the tool result.\n\nUsed when the language backend is disabled or produces output below\nBACKEND_MIN_OUTPUT_CHARS.\n\nArgs:\n    tool_name: Canonical tool name.\n    tool_arg: Argument passed to the tool.\n    tool_result: ToolResult instance.\n\nReturns:\n    Human-readable answer string.", "kind": "method", "line": 887, "name": "_template_answer", "signature": "def _template_answer(tool_name, tool_arg, tool_result)"}, {"doc": "Return True if the backend output is genuinely informative.\n\nChecks length and absence of common TinyStories non-answer patterns\n(story openers, repetition, incomplete sentences starting with\nconjunctions).", "kind": "method", "line": 918, "name": "_is_useful_output", "signature": "def _is_useful_output(text, min_chars)"}, {"doc": "All intermediate and final outputs of one hybrid inference run.", "kind": "class", "line": 946, "name": "HybridResult", "signature": "class HybridResult"}, {"doc": "Combines TopoSwarmRouter + LanguageBackend into a single inference call.\n\nPipeline:\n1. Router.route(prompt)        → (tool_name, tool_arg)\n2. Registry.execute(...)       → ToolResult\n3. Backend.generate(...)       → raw natural-language answer\n4. Quality check               → use backend output or template fallback", "kind": "class", "line": 977, "name": "HybridOrchestrator", "signature": "class HybridOrchestrator"}, {"doc": "CLI entry point.\n\nFlags\n-----\n--prompt TEXT              : User request.\n--backend-type STR         : tinystories | checkpoint | none\n--backend-model STR        : HuggingFace model ID or local path\n--backend-checkpoint PATH  : Path to raw .pt checkpoint (checkpoint mode)\n--router-checkpoint DIR    : Path to checkpoints_toposwarm directory\n--list-tools               : Print registered tools and exit\n--dry-run                  : Test tool execution only (no models loaded)\n--temperature F            : Router sampling temperature\n--device STR               : Force cpu or cuda", "kind": "method", "line": 1051, "name": "main", "signature": "def main()"}, {"kind": "method", "line": 192, "name": "_eval", "signature": "def _eval(node)"}, {"kind": "method", "line": 221, "name": "__init__", "signature": "def __init__(self, tool_name, arg, output, ok)"}, {"kind": "method", "line": 227, "name": "__str__", "signature": "def __str__(self)"}, {"kind": "method", "line": 234, "name": "__init__", "signature": "def __init__(self, cfg)"}, {"kind": "method", "line": 240, "name": "_register", "signature": "def _register(self)"}, {"doc": "Resolve tool name to canonical key via exact match, alias, or substring.", "kind": "method", "line": 249, "name": "resolve", "signature": "def resolve(self, raw)"}, {"doc": "Infer tool name and argument from prompt keywords.\n\nReturns (tool_name, tool_arg) where tool_arg is the most specific\nsub-string of the prompt relevant to the tool (e.g. city name for\nweather, expression for calc_expr).", "kind": "method", "line": 261, "name": "route", "signature": "def route(self, prompt)"}, {"doc": "Execute a tool by canonical name.", "kind": "method", "line": 287, "name": "execute", "signature": "def execute(self, tool_name, arg)"}, {"kind": "method", "line": 299, "name": "_http_get", "signature": "def _http_get(self, url)"}, {"doc": "Register all built-in tools.", "kind": "method", "line": 304, "name": "_register_all", "signature": "def _register_all(self)"}, {"kind": "method", "line": 387, "name": "tool_names", "signature": "def tool_names(self)"}, {"doc": "Args:\n    cfg: Hybrid configuration.\n    registry: ToolRegistry used for routing via registry.route().\n    logger: Logger instance.", "kind": "method", "line": 409, "name": "__init__", "signature": "def __init__(self, cfg, registry, logger)"}, {"doc": "Load checkpoint weights.", "kind": "method", "line": 428, "name": "_load", "signature": "def _load(self)"}, {"doc": "Determine the tool and argument for a prompt.\n\nUses keyword-based routing (deterministic) — the crystallised model\nweights already encoded this perfectly, so we replicate the same logic\nwithout running the full forward pass for routing.\n\nArgs:\n    prompt: Natural language user prompt.\n\nReturns:\n    Tuple of (tool_name, tool_arg).", "kind": "method", "line": 441, "name": "route", "signature": "def route(self, prompt)"}, {"doc": "Args:\n    cfg: Hybrid configuration (BACKEND_TYPE, BACKEND_MODEL_ID, etc.).\n    logger: Logger instance.", "kind": "method", "line": 475, "name": "__init__", "signature": "def __init__(self, cfg, logger)"}, {"doc": "Load the language model according to BACKEND_TYPE.", "kind": "method", "line": 486, "name": "_load", "signature": "def _load(self)"}, {"doc": "Load a GPT-2-style HuggingFace model (TinyStories or compatible).\n\nThe model is loaded in half-precision on CUDA if available to minimise\nVRAM usage alongside the TopoSwarm router.  On CPU it uses full\nprecision.", "kind": "method", "line": 507, "name": "_load_tinystories", "signature": "def _load_tinystories(self)"}, {"doc": "Import topogpt2_1.py from the same directory as the checkpoint or\nthe script directory.  Returns the module or None if not found.", "kind": "method", "line": 563, "name": "_import_topogpt", "signature": "def _import_topogpt(self)"}, {"doc": "Load a safetensors or pickle checkpoint for the language backend.\n\nStrategy\n--------\n1. Try to import topogpt2_1.py from dirs near the checkpoint and\n   instantiate its model class directly — exact architecture match.\n2. Fall back to loading via topo_swarm_agent.TopoSwarmModel with\n   architecture inferred from weight shapes (strict=False, skipping\n   mismatched buffers like rope caches which are recomputed).", "kind": "method", "line": 588, "name": "_load_checkpoint", "signature": "def _load_checkpoint(self)"}, {"doc": "Generate a natural-language answer from the prompt and tool result.\n\nArgs:\n    prompt: Original user question.\n    tool_result: Raw string output from the executed tool.\n\nReturns:\n    Generated answer string, or empty string if backend is None.", "kind": "method", "line": 859, "name": "generate", "signature": "def generate(self, prompt, tool_result)"}, {"doc": "Render a human-readable summary.", "kind": "method", "line": 958, "name": "pretty", "signature": "def pretty(self)"}, {"doc": "Args:\n    cfg: Hybrid configuration.\n    logger: Logger instance.", "kind": "method", "line": 988, "name": "__init__", "signature": "def __init__(self, cfg, logger)"}, {"doc": "Execute the full hybrid pipeline for one user prompt.\n\nArgs:\n    prompt: Natural language user request.\n\nReturns:\n    HybridResult with all steps populated.", "kind": "method", "line": 1000, "name": "run", "signature": "def run(self, prompt)"}, {"kind": "method", "line": 241, "name": "decorator", "signature": "def decorator(fn)"}, {"kind": "method", "line": 308, "name": "get_weather", "signature": "def get_weather(city)"}, {"kind": "method", "line": 319, "name": "search_web", "signature": "def search_web(query)"}, {"kind": "method", "line": 331, "name": "calc_expr", "signature": "def calc_expr(expr)"}, {"kind": "method", "line": 335, "name": "get_datetime", "signature": "def get_datetime(tz_hint)"}, {"kind": "method", "line": 341, "name": "translate", "signature": "def translate(text)"}, {"kind": "method", "line": 373, "name": "get_news", "signature": "def get_news(topic)"}, {"kind": "method", "line": 383, "name": "echo", "signature": "def echo(text)"}, {"kind": "method", "line": 540, "name": "_generate", "signature": "def _generate(prompt_text)"}, {"kind": "method", "line": 703, "name": "_cfg_score", "signature": "def _cfg_score(cls)"}, {"kind": "method", "line": 812, "name": "_generate", "signature": "def _generate(prompt_text)"}, {"kind": "method", "line": 835, "name": "_generate", "signature": "def _generate(prompt_text)"}]}, {"id": "toposwarm_infer.py", "kind": "module", "label": "toposwarm_infer.py", "language": "py", "sha256": "01bbffd6980ec5bf", "symbol_count": 37, "symbols": [{"doc": "Import topo_swarm_agent, searching the script dir and cwd.", "kind": "function", "line": 51, "name": "_import_agent", "signature": "def _import_agent()"}, {"doc": "All inference-time hyper-parameters — zero magic numbers.", "kind": "class", "line": 84, "name": "InferenceConfig", "signature": "class InferenceConfig"}, {"doc": "Evaluate a mathematical expression without using eval() on arbitrary code.\n\nSupports: +, -, *, /, //, %, **, unary minus, parentheses, int and float\nliterals.  Raises ValueError on any disallowed construct.", "kind": "method", "line": 138, "name": "_safe_eval", "signature": "def _safe_eval(expr)"}, {"doc": "Structured result returned by every tool executor.", "kind": "class", "line": 189, "name": "ToolResult", "signature": "class ToolResult"}, {"doc": "Registry of executable tools.\n\nEach tool is a callable(arg: str) -> str.  Registration is done via the\n@register decorator.  Tool names are matched case-insensitively and with\ncommon aliases (e.g. \"weather\" matches \"get_weather\", \"weather_now\").", "kind": "class", "line": 210, "name": "ToolRegistry", "signature": "class ToolRegistry"}, {"doc": "Extract tool calls from model-generated text.\n\nThe model may emit tool calls in several formats; this parser tries all\nof them in priority order and returns the first match.", "kind": "class", "line": 438, "name": "ToolCallParser", "signature": "class ToolCallParser"}, {"doc": "Full agentic inference loop:\n\n1. Encode prompt.\n2. First-pass generation via SwarmOrchestrator.\n3. Parse any tool call from the generated text.\n4. Execute the tool.\n5. Second-pass generation conditioned on prompt + tool result.\n6. Return structured InferenceResult.", "kind": "class", "line": 483, "name": "InferenceEngine", "signature": "class InferenceEngine"}, {"doc": "All intermediate and final outputs of one inference run.", "kind": "class", "line": 883, "name": "InferenceResult", "signature": "class InferenceResult"}, {"doc": "Idempotent logger with a single StreamHandler.", "kind": "method", "line": 920, "name": "_setup_logger", "signature": "def _setup_logger(name, level)"}, {"doc": "CLI entry point.\n\nFlags\n-----\n--prompt TEXT        : Natural language request to the agent.\n--checkpoint DIR     : Path to checkpoints_toposwarm directory.\n--max-tokens N       : Maximum new tokens for pass 1.\n--temperature F      : Sampling temperature (0 = greedy).\n--top-k N            : Top-k truncation.\n--list-tools         : Print all registered tool names and exit.\n--dry-run            : Skip model load; test tool execution only.\n--device STR         : Force cpu or cuda.", "kind": "method", "line": 938, "name": "main", "signature": "def main()"}, {"kind": "method", "line": 157, "name": "_eval", "signature": "def _eval(node)"}, {"doc": "Args:\n    tool_name: Name of the tool that was called.\n    arg: Raw argument string passed to the tool.\n    output: Human-readable result string.\n    ok: Whether the tool call succeeded.", "kind": "method", "line": 192, "name": "__init__", "signature": "def __init__(self, tool_name, arg, output, ok)"}, {"kind": "method", "line": 205, "name": "__str__", "signature": "def __str__(self)"}, {"doc": "Args:\n    cfg: Inference configuration (provides timeout and result limits).", "kind": "method", "line": 219, "name": "__init__", "signature": "def __init__(self, cfg)"}, {"doc": "Decorator that registers a function under one or more tool names.", "kind": "method", "line": 229, "name": "register", "signature": "def register(self)"}, {"doc": "Resolve a raw tool name to its canonical registry key.\n\nPerforms exact match, then alias lookup, then prefix/substring search.\n\nArgs:\n    raw_name: Tool name as emitted by the model.\n\nReturns:\n    Canonical tool name string, or None if not found.", "kind": "method", "line": 239, "name": "resolve", "signature": "def resolve(self, raw_name)"}, {"doc": "Execute a tool by name with the given argument string.\n\nArgs:\n    raw_name: Tool name as emitted by the model.\n    arg: Argument string (stripped of surrounding whitespace/quotes).\n\nReturns:\n    ToolResult with the output or an error message.", "kind": "method", "line": 262, "name": "execute", "signature": "def execute(self, raw_name, arg)"}, {"doc": "Minimal HTTP GET with timeout, returns response body as string.", "kind": "method", "line": 292, "name": "_http_get", "signature": "def _http_get(self, url)"}, {"doc": "Register all built-in tools onto self._tools / self._aliases.", "kind": "method", "line": 301, "name": "_register_builtin_tools", "signature": "def _register_builtin_tools(self)"}, {"doc": "Args:\n    cfg: Inference config (provides TOOL_TAG_RE pattern).", "kind": "method", "line": 446, "name": "__init__", "signature": "def __init__(self, cfg)"}, {"doc": "Extract the first tool call from text.\n\nArgs:\n    text: Raw model output string.\n\nReturns:\n    Tuple of (tool_name, arg) or None if no tool call found.", "kind": "method", "line": 453, "name": "parse", "signature": "def parse(self, text)"}, {"doc": "Args:\n    cfg: Inference configuration.\n    agent_cfg: SwarmConfig used to instantiate the model.\n    logger: Logger instance.", "kind": "method", "line": 495, "name": "__init__", "signature": "def __init__(self, cfg, agent_cfg, logger)"}, {"doc": "Load weights from the latest checkpoint directory.", "kind": "method", "line": 521, "name": "_load_checkpoint", "signature": "def _load_checkpoint(self)"}, {"doc": "Encode a prompt string to a [1, S] token id tensor on the model device.\n\nWraps the raw text in the ToolBench training format so the model\nreceives input that matches its training distribution:\n\n    query: <text>\n    api_list: [{\"tool_name\": \"<inferred>\", ...}]\n    domain: General\n    <tool_token>\n\nThe tool name is inferred from keyword signals so the tool token sits\nat the correct position — matching encode_tool_trace() used at training.\nToken ids are clamped to [0, VOCAB_SIZE-1] to prevent embedding crashes.", "kind": "method", "line": 538, "name": "_encode_prompt", "signature": "def _encode_prompt(self, text)"}, {"doc": "Custom autoregressive generation loop with three inference-time fixes.\n\nFix 1 — Repetition penalty: divides logits of already-seen tokens by\nREPETITION_PENALTY, preventing the single-token collapse (. / is / :).\n\nFix 2 — ACT-driven temperature: when the halt_prob exceeds\nACT_TEMPERATURE_TRIGGER the temperature is boosted by\nACT_TEMPERATURE_BOOST, forcing lexical diversity at high-confidence\nsteps rather than collapsing to the mode token.\n\nFix 3 — MIN_ANSWER_TOKENS guard: the ACT halt signal is ignored for\nthe first MIN_ANSWER_TOKENS newly generated tokens, guaranteeing at\nleast that many tokens of output regardless of halt confidence.\n\nAll three fixes operate purely on logits/probabilities at decode time\nwith no weight updates — no retraining required.", "kind": "method", "line": 586, "name": "_generate", "signature": "def _generate(self, prompt_ids, max_new_tokens, temperature)"}, {"doc": "Full agentic inference loop for one user prompt.\n\nProtocol (matches the training distribution exactly):\n\nPass 1 — The prompt is encoded in ToolBench format:\n    [instruction_tokens][tool_token]\nThe model generates a completion of the result side.\nThis raw completion is stored as first_output.\n\nTool execution — The tool inferred at encoding time is executed\nwith the prompt as its argument.  This gives a real, live result\nindependent of what the model generated.\n\nPass 2 — The full sequence:\n    [instruction_tokens][tool_token][real_result_tokens]\nis fed to the model, which generates the final natural-language\nanswer conditioned on the ground-truth tool output.\n\nArgs:\n    prompt: Natural language user request.\n\nReturns:\n    InferenceResult with all intermediate steps populated.", "kind": "method", "line": 679, "name": "run", "signature": "def run(self, prompt)"}, {"doc": "Build a deterministic natural-language answer from the tool result.\n\nUsed when the model Pass 2 output is too short to be useful.  Each\ntool has a dedicated template that formats the raw result string into\na readable sentence.  No model weights involved — pure string\nformatting.", "kind": "method", "line": 818, "name": "_template_answer", "signature": "def _template_answer(self, tool_name, tool_arg, tool_result)"}, {"doc": "Infer the tool name and argument from the prompt text.\n\nReturns the same (tool_name, arg) pair that _encode_prompt uses,\nso both are guaranteed to be consistent.  The argument is the\nfull prompt text — each tool executor extracts what it needs.", "kind": "method", "line": 844, "name": "_infer_tool_and_arg", "signature": "def _infer_tool_and_arg(self, prompt)"}, {"doc": "Render a human-readable summary of the inference run.", "kind": "method", "line": 895, "name": "pretty", "signature": "def pretty(self)"}, {"kind": "method", "line": 231, "name": "decorator", "signature": "def decorator(fn)"}, {"doc": "Fetch current weather from wttr.in (no API key required).", "kind": "method", "line": 305, "name": "get_weather", "signature": "def get_weather(city)"}, {"doc": "Instant-answer search via DuckDuckGo JSON API (no API key).", "kind": "method", "line": 323, "name": "search_web", "signature": "def search_web(query)"}, {"doc": "Evaluate a mathematical expression safely.", "kind": "method", "line": 340, "name": "calc_expr", "signature": "def calc_expr(expr)"}, {"doc": "Return the current UTC datetime (tz_hint is informational only).", "kind": "method", "line": 345, "name": "get_datetime", "signature": "def get_datetime(tz_hint)"}, {"doc": "Translate text using MyMemory free API (no key, 5k chars/day limit).\n\nAccepted formats:\n  \"translate <text> to <lang>\"\n  \"<text> to <lang>\"\n  \"<text>\"  (defaults to English)\n\nStrips the \"translate\" verb and detects source language via\nlangdetect so MyMemory receives a valid langpair (e.g. es|en).\nFalls back to es|en when detection fails.", "kind": "method", "line": 351, "name": "translate", "signature": "def translate(text)"}, {"doc": "Fetch recent news headlines via DuckDuckGo news search.\nReturns up to 3 snippet summaries.", "kind": "method", "line": 409, "name": "get_news", "signature": "def get_news(topic)"}, {"doc": "Return the input unchanged. Used for model self-testing.", "kind": "method", "line": 428, "name": "echo", "signature": "def echo(text)"}]}, {"id": "toposwarm_lazyown_orchestrator.py", "kind": "module", "label": "toposwarm_lazyown_orchestrator.py", "language": "py", "sha256": "25112bb0995248c9", "symbol_count": 83, "symbols": [{"doc": "Discover LazyOwn installation directory.\n\nPriority:\n  1. LAZYOWN_DIR environment variable (expanded ~).\n  2. Default relative to this script: <repo>/LazyOwn.\n  3. User home directory: ~/LazyOwn.\n  4. Return the relative default anyway (caller will see available=False).", "kind": "function", "line": 56, "name": "_resolve_lazyown_dir", "signature": "def _resolve_lazyown_dir()"}, {"kind": "function", "line": 93, "name": "_import_infer", "signature": "def _import_infer()"}, {"kind": "function", "line": 113, "name": "_import_agent", "signature": "def _import_agent()"}, {"kind": "function", "line": 128, "name": "_import_meta_harness", "signature": "def _import_meta_harness()"}, {"kind": "function", "line": 147, "name": "_import_routing_head", "signature": "def _import_routing_head()"}, {"doc": "Persistent session state across multiple prompts.", "kind": "class", "line": 170, "name": "SessionContext", "signature": "class SessionContext"}, {"doc": "Thin wrapper around LazyOwn's _run_lazyown_command logic.\n\nCalls LazyOwn non-interactively via a PTY subprocess so the terminal-size\nioctl does not crash.  Strips ANSI codes from output.\n\nAll heavy imports (pty, fcntl, termios, select, struct) are lazy so the\nbridge can be imported on non-Linux systems for dataset generation.", "kind": "class", "line": 227, "name": "LazyOwnBridge", "signature": "class LazyOwnBridge"}, {"doc": "Extends TopoSwarm's ToolRegistry with all LazyOwn MCP tools.\n\nEach tool is a thin wrapper that calls LazyOwnBridge.run() with the\nappropriate LazyOwn shell command or payload manipulation.\n\nTools are grouped by category so keyword routing maps naturally.", "kind": "class", "line": 372, "name": "LazyOwnToolRegistry", "signature": "class LazyOwnToolRegistry(ToolRegistry)"}, {"doc": "Map a natural-language security prompt to a (tool_name, tool_arg) pair.\n\nPriority: explicit LazyOwn keywords → security domain keywords → fallback.\nThe returned tool_arg is the most useful sub-string to pass to that tool.", "kind": "method", "line": 691, "name": "infer_lazyown_tool", "signature": "def infer_lazyown_tool(prompt)"}, {"doc": "Extract the most useful argument string for each tool category.", "kind": "method", "line": 716, "name": "_extract_arg", "signature": "def _extract_arg(prompt, tool_name)"}, {"doc": "Combines TopoSwarm router with LazyOwn tool execution.\n\nInferenceEngine is loaded only when needed (lazy) so the orchestrator\ncan be used for dataset generation without a GPU.\n\nMeta-Harness integration (2026-05):\n- Filesystem experience store: every execution is logged with code,\n  traces, and scores for future proposer diagnosis.\n- Environment bootstrap: gathers a LazyOwn sandbox snapshot before the\n  first turn to eliminate wasted exploratory commands.\n- Draft-verification routing: retrieves confirmers/challengers from\n  prior episodes to verify or revise the keyword router's draft.", "kind": "class", "line": 764, "name": "LazyOwnOrchestrator", "signature": "class LazyOwnOrchestrator"}, {"doc": "Generate a rich ToolBench-format JSONL for fine-tuning the TopoSwarm router.\n\nUses lazyown_dataset_generator.py (80 tools × 5-10 phrasings + chain examples)\nfor ~420 high-quality training examples covering every LazyOwn MCP tool.\nIf LazyOwn is live, a random sample of tools are actually executed and their\nreal output replaces the placeholder in the `answer` field.\n\nReturns the number of examples written.", "kind": "method", "line": 1092, "name": "generate_dataset", "signature": "def generate_dataset(output_path, bridge)"}, {"doc": "Fine-tune the TopoSwarm router on the full LazyOwn tool dataset using\nEWC + Experience Replay to prevent catastrophic forgetting.\n\nPipeline (delegated to toposwarm_continual_trainer.py):\n  1. Load the 420-example lazyown_full.jsonl.\n  2. Compute / load Fisher Information diagonal on any available ToolBench\n     data (anchors critical weights so general routing is preserved).\n  3. Build a ToolBench replay buffer (20 % of every mini-batch).\n  4. Fine-tune with combined loss: L_task + λ/2 · Σ F_i(θ_i − θ*_i)²\n  5. Evaluate routing accuracy on held-out LazyOwn + ToolBench samples.\n  6. Print final checkpoint stats (epoch, step, task_loss, ewc_lambda).", "kind": "method", "line": 1173, "name": "finetune_on_lazyown", "signature": "def finetune_on_lazyown(dataset_path, agent_cfg, logger)"}, {"doc": "Expose the TopoSwarm→LazyOwn orchestrator as an MCP stdio server.\n\nTools exposed:\n  toposwarm_query   — NL prompt → routed LazyOwn tool → answer\n  lazyown_*         — direct passthrough to every registered tool", "kind": "method", "line": 1250, "name": "run_mcp_server", "signature": "def run_mcp_server(orchestrator)"}, {"kind": "method", "line": 1329, "name": "_setup_logger", "signature": "def _setup_logger(level)"}, {"kind": "method", "line": 1346, "name": "main", "signature": "def main()"}, {"doc": "Compact context block injected before the user prompt.", "kind": "method", "line": 181, "name": "to_prompt_prefix", "signature": "def to_prompt_prefix(self)"}, {"kind": "method", "line": 195, "name": "update", "signature": "def update(self, tool_name, arg, output, ok)"}, {"kind": "method", "line": 251, "name": "__init__", "signature": "def __init__(self, lazyown_dir, default_timeout)"}, {"kind": "method", "line": 257, "name": "available", "signature": "def available(self)"}, {"doc": "Execute a LazyOwn shell command and return cleaned output.", "kind": "method", "line": 265, "name": "run", "signature": "def run(self, command, timeout)"}, {"kind": "method", "line": 344, "name": "get_config", "signature": "def get_config(self)"}, {"kind": "method", "line": 353, "name": "set_config", "signature": "def set_config(self, key, value)"}, {"kind": "method", "line": 455, "name": "__init__", "signature": "def __init__(self, cfg, bridge)"}, {"doc": "Register every LazyOwn MCP tool as a ToolRegistry callable.", "kind": "method", "line": 460, "name": "_register_lazyown_tools", "signature": "def _register_lazyown_tools(self)"}, {"kind": "method", "line": 780, "name": "__init__", "signature": "def __init__(self, cfg, agent_cfg, bridge, logger, load_model, meta_cfg)"}, {"doc": "Load the trained RoutingHead if a checkpoint exists.", "kind": "method", "line": 825, "name": "_load_routing_head", "signature": "def _load_routing_head(self)"}, {"doc": "Use the TopoSwarm model + RoutingHead to predict the LazyOwn tool.\nReturns (tool_name, tool_arg) or None if unavailable / uncertain.", "kind": "method", "line": 847, "name": "_neural_route", "signature": "def _neural_route(self, prompt)"}, {"doc": "Route prompt → LazyOwn tool → answer.", "kind": "method", "line": 887, "name": "run", "signature": "def run(self, prompt)"}, {"kind": "method", "line": 1273, "name": "list_tools", "signature": "def list_tools()"}, {"kind": "method", "line": 1307, "name": "call_tool", "signature": "def call_tool(name, arguments)"}, {"kind": "method", "line": 1317, "name": "_serve", "signature": "def _serve()"}, {"kind": "method", "line": 466, "name": "run_command", "signature": "def run_command(arg)"}, {"kind": "method", "line": 470, "name": "get_config", "signature": "def get_config(_)"}, {"kind": "method", "line": 475, "name": "set_config", "signature": "def set_config(arg)"}, {"kind": "method", "line": 483, "name": "list_modules", "signature": "def list_modules(_)"}, {"kind": "method", "line": 487, "name": "get_beacons", "signature": "def get_beacons(_)"}, {"kind": "method", "line": 491, "name": "c2_command", "signature": "def c2_command(arg)"}, {"kind": "method", "line": 495, "name": "run_api", "signature": "def run_api(arg)"}, {"kind": "method", "line": 499, "name": "list_sessions", "signature": "def list_sessions(_)"}, {"kind": "method", "line": 507, "name": "read_session_file", "signature": "def read_session_file(arg)"}, {"kind": "method", "line": 514, "name": "c2_status", "signature": "def c2_status(_)"}, {"kind": "method", "line": 518, "name": "create_addon", "signature": "def create_addon(arg)"}, {"kind": "method", "line": 522, "name": "list_addons", "signature": "def list_addons(_)"}, {"kind": "method", "line": 529, "name": "list_plugins", "signature": "def list_plugins(_)"}, {"kind": "method", "line": 536, "name": "poll_events", "signature": "def poll_events(_)"}, {"kind": "method", "line": 540, "name": "ack_event", "signature": "def ack_event(arg)"}, {"kind": "method", "line": 544, "name": "add_rule", "signature": "def add_rule(arg)"}, {"kind": "method", "line": 548, "name": "list_event_rules", "signature": "def list_event_rules(_)"}, {"kind": "method", "line": 552, "name": "heartbeat_status", "signature": "def heartbeat_status(_)"}, {"kind": "method", "line": 556, "name": "session_init", "signature": "def session_init(arg)"}, {"kind": "method", "line": 560, "name": "discover_commands", "signature": "def discover_commands(arg)"}, {"kind": "method", "line": 564, "name": "phase_guide", "signature": "def phase_guide(arg)"}, {"kind": "method", "line": 568, "name": "command_help", "signature": "def command_help(arg)"}, {"kind": "method", "line": 572, "name": "add_target", "signature": "def add_target(arg)"}, {"kind": "method", "line": 578, "name": "list_targets", "signature": "def list_targets(_)"}, {"kind": "method", "line": 582, "name": "run_agent", "signature": "def run_agent(arg)"}, {"kind": "method", "line": 586, "name": "agent_status", "signature": "def agent_status(arg)"}, {"kind": "method", "line": 590, "name": "agent_result", "signature": "def agent_result(arg)"}, {"kind": "method", "line": 594, "name": "list_agents", "signature": "def list_agents(_)"}, {"kind": "method", "line": 598, "name": "set_active_target", "signature": "def set_active_target(arg)"}, {"kind": "method", "line": 602, "name": "campaign_sitrep", "signature": "def campaign_sitrep(_)"}, {"kind": "method", "line": 606, "name": "c2_notes", "signature": "def c2_notes(arg)"}, {"kind": "method", "line": 610, "name": "credentials", "signature": "def credentials(_)"}, {"kind": "method", "line": 614, "name": "report_update", "signature": "def report_update(arg)"}, {"kind": "method", "line": 618, "name": "campaign_lessons", "signature": "def campaign_lessons(_)"}, {"kind": "method", "line": 622, "name": "auto_populate", "signature": "def auto_populate(_)"}, {"kind": "method", "line": 626, "name": "session_state", "signature": "def session_state(_)"}, {"kind": "method", "line": 630, "name": "recommend_next", "signature": "def recommend_next(_)"}, {"kind": "method", "line": 634, "name": "timeline", "signature": "def timeline(_)"}, {"kind": "method", "line": 638, "name": "c2_vuln_analysis", "signature": "def c2_vuln_analysis(arg)"}, {"kind": "method", "line": 642, "name": "c2_redop", "signature": "def c2_redop(arg)"}, {"kind": "method", "line": 646, "name": "c2_search_agent", "signature": "def c2_search_agent(arg)"}, {"kind": "method", "line": 650, "name": "c2_script", "signature": "def c2_script(arg)"}, {"kind": "method", "line": 654, "name": "c2_adversary", "signature": "def c2_adversary(arg)"}, {"kind": "method", "line": 658, "name": "policy_status", "signature": "def policy_status(_)"}, {"kind": "method", "line": 662, "name": "auto_loop", "signature": "def auto_loop(arg)"}, {"kind": "method", "line": 666, "name": "create_tool", "signature": "def create_tool(arg)"}, {"kind": "method", "line": 670, "name": "llm_ask", "signature": "def llm_ask(arg)"}, {"kind": "method", "line": 674, "name": "inject_objective", "signature": "def inject_objective(arg)"}, {"kind": "method", "line": 678, "name": "next_objective", "signature": "def next_objective(_)"}, {"kind": "method", "line": 682, "name": "read_prompt", "signature": "def read_prompt(arg)"}, {"kind": "method", "line": 863, "name": "_hook", "signature": "def _hook(module, inp, out)"}]}, {"id": "toposwarm_lazyown_sweep.py", "kind": "module", "label": "toposwarm_lazyown_sweep.py", "language": "py", "sha256": "39ee4e38b067ad9d", "symbol_count": 5, "symbols": [{"doc": "Generate N diverse pentesting prompts.", "kind": "function", "line": 130, "name": "generate_prompts", "signature": "def generate_prompts(n)"}, {"kind": "function", "line": 145, "name": "setup_logger", "signature": "def setup_logger()"}, {"doc": "Execute prompts against LazyOwn and collect results.", "kind": "function", "line": 155, "name": "run_sweep", "signature": "def run_sweep(prompts, bridge, logger)"}, {"doc": "Write results as JSONL for continual trainer.\n\nMatches the format of lazyown_dataset_generator.py:\n- instruction: the prompt\n- api_list: minimal tool metadata\n- answer: [TOOL_CALL: tool_name(arg)]\n- domain: Security/RealSuccess or Security/RealFailure", "kind": "function", "line": 189, "name": "write_results", "signature": "def write_results(results, out_path)"}, {"kind": "function", "line": 223, "name": "main", "signature": "def main()"}]}, {"id": "toposwarm_meta_harness.py", "kind": "module", "label": "toposwarm_meta_harness.py", "language": "py", "sha256": "c6bdbc88ece8f514", "symbol_count": 54, "symbols": [{"doc": "All Meta-Harness hyper-parameters in one place.", "kind": "class", "line": 60, "name": "MetaHarnessConfig", "signature": "class MetaHarnessConfig"}, {"kind": "method", "line": 95, "name": "_setup_logger", "signature": "def _setup_logger(name, level)"}, {"doc": "Short stable hash for naming log directories.", "kind": "method", "line": 107, "name": "_stable_id", "signature": "def _stable_id(text)"}, {"kind": "method", "line": 112, "name": "_now_iso", "signature": "def _now_iso()"}, {"doc": "Append-only filesystem store for harness code, execution traces, and scores.\n\nEach evaluated harness run gets its own directory:\n\n    meta_harness_logs/\n      run_0001_<hash>/\n        harness.json   – config / code snapshot\n        trace.jsonl    – step-by-step execution trace\n        score.json     – metrics (success, latency, token count, ...)\n        reasoning.txt  – optional proposer reasoning\n\nThe store is intentionally plain-text / JSON so a coding-agent proposer can\nnavigate it with standard tools (`grep`, `cat`, `ls`) without bespoke APIs.", "kind": "class", "line": 121, "name": "MetaHarnessLogger", "signature": "class MetaHarnessLogger"}, {"doc": "Semantic episodic retrieval with graceful degradation.\n\nPriority:\n    1. sentence-transformers dense embeddings (best quality).\n    2. sklearn TF-IDF + cosine similarity (no GPU, good quality).\n    3. Return None so caller falls back to Jaccard token overlap.\n\nThe retriever is rebuildable incrementally: call `add()` for each new\nepisode, then `search()` for retrieval.", "kind": "class", "line": 322, "name": "DenseMemoryRetriever", "signature": "class DenseMemoryRetriever"}, {"doc": "Persistent episodic memory backed by the filesystem log store.\n\nUnlike the in-RAM EpisodicMemory in topo_swarm_agent.py, this memory:\n- Survives process restarts.\n- Can be queried by keyword overlap, tool name, or simple TF-IDF cosine.\n- Returns raw execution traces (not compressed summaries) so a proposer can\n  perform causal diagnosis.", "kind": "class", "line": 430, "name": "MetaHarnessMemory", "signature": "class MetaHarnessMemory"}, {"doc": "Gathers a sandbox snapshot *before* the first router/tool turn and formats\nit as a compact [Environment Snapshot] block.\n\nThis eliminates the 2-4 exploratory turns that the LazyOwn agent typically\nspends discovering what targets, sessions, and modules are available.", "kind": "class", "line": 583, "name": "EnvironmentBootstrapper", "signature": "class EnvironmentBootstrapper"}, {"doc": "Two-stage routing inspired by Meta-Harness's text-classification harness.\n\nStage 1 (Draft):  Produce an initial tool proposal using fast keyword\n                  heuristics (same as the existing infer_lazyown_tool).\n\nStage 2 (Verify): Retrieve confirmers (same tool, past successes) and\n                  challengers (different tool / failures) from the\n                  MetaHarnessMemory, then decide whether to keep or revise\n                  the draft.\n\nThis is lightweight — no LLM call — but gives the harness a structured\nway to learn from prior executions without retraining model weights.", "kind": "class", "line": 738, "name": "DraftVerifier", "signature": "class DraftVerifier"}, {"doc": "Maintain a population of harness configurations and their evaluation scores.\n\nThe frontier is updated after every evaluation so the orchestrator can\ndynamically switch to the best harness variant for the current task context\n(accuracy vs. latency vs. context-cost trade-offs).", "kind": "class", "line": 837, "name": "ParetoFrontier", "signature": "class ParetoFrontier"}, {"doc": "Single entry-point that wires together Logger, Memory, Bootstrapper,\nDraftVerifier, and ParetoFrontier.\n\nUsage inside LazyOwnOrchestrator:\n\n    mh = MetaHarnessOptimizer(MetaHarnessConfig())\n    snapshot = mh.bootstrap.gather_snapshot(bridge)\n    snapshot_text = mh.bootstrap.format_snapshot(snapshot)\n    tool, arg, conf = mh.draft_verifier.route(prompt, snapshot_text)\n    ... execute tool ...\n    mh.log_run(harness_cfg, trace_steps, score)\n    mh.memory.store(score, trace_steps)\n    mh.frontier.add(harness_cfg, score)", "kind": "class", "line": 948, "name": "MetaHarnessOptimizer", "signature": "class MetaHarnessOptimizer"}, {"kind": "method", "line": 1013, "name": "_demo", "signature": "def _demo()"}, {"kind": "method", "line": 138, "name": "__init__", "signature": "def __init__(self, cfg, logger)"}, {"kind": "method", "line": 149, "name": "_count_existing_runs", "signature": "def _count_existing_runs(self)"}, {"kind": "method", "line": 152, "name": "_next_run_dir", "signature": "def _next_run_dir(self, hint)"}, {"doc": "Keep only the most recent MAX_LOGGED_RUNS directories.", "kind": "method", "line": 158, "name": "_prune_old", "signature": "def _prune_old(self)"}, {"doc": "Persist one complete harness evaluation.\n\nArgs:\n    harness_snapshot: JSON-serialisable dict describing the harness\n        config / code (e.g. {\"orchestrator_version\": \"2.1\", ...}).\n    trace_steps: List of step dicts, each with keys like\n        { \"step\": int, \"prompt\": str, \"tool\": str, \"output\": str, \"t_ms\": float }.\n    score: Dict of metrics, e.g.\n        { \"success\": true, \"latency_ms\": 120, \"context_chars\": 450 }.\n    reasoning: Optional free-text proposer reasoning.\n\nReturns:\n    Path to the newly created run directory.", "kind": "method", "line": 176, "name": "log_run", "signature": "def log_run(self, harness_snapshot, trace_steps, score, reasoning)"}, {"doc": "Return run directories newest-first.", "kind": "method", "line": 229, "name": "list_runs", "signature": "def list_runs(self, n)"}, {"doc": "Simple regex search across all trace.jsonl files.\nReturns list of (run_dir, line_no, matched_line).", "kind": "method", "line": 238, "name": "grep_traces", "signature": "def grep_traces(self, pattern, max_results)"}, {"doc": "Load every score.json into a list.", "kind": "method", "line": 257, "name": "get_scores", "signature": "def get_scores(self)"}, {"doc": "Return run directories that are on the Pareto frontier.\n\nBy default maximises success_rate and minimises latency_ms + context_chars.", "kind": "method", "line": 269, "name": "get_pareto_runs", "signature": "def get_pareto_runs(self, metrics)"}, {"kind": "method", "line": 335, "name": "__init__", "signature": "def __init__(self, logger)"}, {"kind": "method", "line": 362, "name": "add", "signature": "def add(self, text, episode)"}, {"kind": "method", "line": 368, "name": "_rebuild_tfidf", "signature": "def _rebuild_tfidf(self)"}, {"kind": "method", "line": 376, "name": "bulk_index", "signature": "def bulk_index(self, texts, episodes)"}, {"kind": "method", "line": 392, "name": "search", "signature": "def search(self, query, top_k)"}, {"kind": "method", "line": 401, "name": "_search_st", "signature": "def _search_st(self, query, top_k)"}, {"kind": "method", "line": 412, "name": "_search_tfidf", "signature": "def _search_tfidf(self, query, top_k)"}, {"kind": "method", "line": 441, "name": "__init__", "signature": "def __init__(self, logger, capacity, dense)"}, {"kind": "method", "line": 453, "name": "_build_index", "signature": "def _build_index(self)"}, {"kind": "method", "line": 464, "name": "_load_episode", "signature": "def _load_episode(self, run_dir)"}, {"kind": "method", "line": 482, "name": "_episode_text", "signature": "def _episode_text(score, traces)"}, {"doc": "Index a newly logged episode.", "kind": "method", "line": 493, "name": "store", "signature": "def store(self, score, traces)"}, {"doc": "Retrieve the top-k most similar prior episodes.\n\nUses dense semantic retrieval when available (sentence-transformers or\nsklearn TF-IDF), then falls back to token-overlap Jaccard for anything\nnot covered by the dense index.  Results are fused by max-of-scores.", "kind": "method", "line": 505, "name": "retrieve_similar", "signature": "def retrieve_similar(self, prompt, tool_hint, top_k, min_score)"}, {"doc": "Split retrieved episodes into confirmers (same tool, success) and\nchallengers (different tool or failure).", "kind": "method", "line": 549, "name": "retrieve_confirmers_and_challengers", "signature": "def retrieve_confirmers_and_challengers(self, draft_tool, prompt, top_k)"}, {"doc": "Very simple whitespace + punctuation tokeniser.", "kind": "method", "line": 573, "name": "_tokenise", "signature": "def _tokenise(text)"}, {"kind": "method", "line": 592, "name": "__init__", "signature": "def __init__(self, cfg, logger)"}, {"doc": "Collect environment state via the LazyOwnBridge.\n\nReturns a dict with keys:\n    working_dir, lazyown_dir, config, targets, sessions,\n    modules_available, beacons, languages, memory_estimate.", "kind": "method", "line": 596, "name": "gather_snapshot", "signature": "def gather_snapshot(self, bridge)"}, {"doc": "Best-effort parse of newline / comma list output.", "kind": "method", "line": 680, "name": "_parse_list", "signature": "def _parse_list(raw)"}, {"doc": "Render the snapshot as a compact [Environment Snapshot] block suitable\nfor injection into a prompt.", "kind": "method", "line": 687, "name": "format_snapshot", "signature": "def format_snapshot(self, snapshot, max_chars)"}, {"kind": "method", "line": 754, "name": "__init__", "signature": "def __init__(self, cfg, memory, keyword_router, logger)"}, {"doc": "Draft-verify routing.\n\nReturns:\n    Tuple of (tool_name, tool_arg, confidence).", "kind": "method", "line": 766, "name": "route", "signature": "def route(self, prompt, snapshot_text)"}, {"doc": "Best-effort arg re-extraction when the tool changes.", "kind": "method", "line": 820, "name": "_reextract_arg", "signature": "def _reextract_arg(prompt, tool_name, fallback)"}, {"kind": "method", "line": 846, "name": "__init__", "signature": "def __init__(self, cfg, logger)"}, {"doc": "Add a candidate to the population and return True if it lies on the\ncurrent Pareto frontier.", "kind": "method", "line": 855, "name": "add", "signature": "def add(self, config, metrics)"}, {"doc": "Select the best harness config according to a scalarised preference.\n\npreference maps metric name → weight (positive = maximise, negative = minimise).\nDefault: maximise success_rate, minimise latency_ms and context_chars.", "kind": "method", "line": 875, "name": "select_best", "signature": "def select_best(self, preference)"}, {"doc": "Return all configs currently on the Pareto frontier.", "kind": "method", "line": 907, "name": "frontier_configs", "signature": "def frontier_configs(self)"}, {"kind": "method", "line": 911, "name": "_is_on_frontier", "signature": "def _is_on_frontier(self, candidate)"}, {"doc": "Remove oldest non-frontier entries when population grows too large.", "kind": "method", "line": 933, "name": "_prune", "signature": "def _prune(self)"}, {"kind": "method", "line": 965, "name": "__init__", "signature": "def __init__(self, cfg)"}, {"doc": "Bind the draft verifier to the existing keyword router.", "kind": "method", "line": 980, "name": "set_router", "signature": "def set_router(self, keyword_router)"}, {"doc": "Persist one run and update in-memory indexes.", "kind": "method", "line": 986, "name": "log_run", "signature": "def log_run(self, harness_snapshot, trace_steps, score, reasoning)"}, {"doc": "Return the current Pareto-best harness configuration.", "kind": "method", "line": 999, "name": "get_best_harness_config", "signature": "def get_best_harness_config(self)"}, {"doc": "Ad-hoc retrieval of prior episodes for prompt engineering.", "kind": "method", "line": 1003, "name": "query_experience", "signature": "def query_experience(self, prompt, tool_hint, top_k)"}]}, {"id": "ts_utils.py", "kind": "module", "label": "ts_utils.py", "language": "py", "sha256": "16dd7219300f2699", "symbol_count": 7, "symbols": [{"doc": "Return an idempotent logger with a single StreamHandler.", "kind": "function", "line": 25, "name": "setup_logger", "signature": "def setup_logger(name, level)"}, {"doc": "Evaluate a numeric expression via AST — never calls eval() on arbitrary code.", "kind": "function", "line": 42, "name": "safe_eval", "signature": "def safe_eval(expr)"}, {"doc": "Load a Python file as a named module.\n\nTries each candidate path in order; raises FileNotFoundError if none found.\nPre-registers the module in sys.modules before exec so that @dataclass\nintrospection works correctly on Python 3.13+.", "kind": "function", "line": 62, "name": "import_module", "signature": "def import_module(name)"}, {"doc": "Return a cached version of tokenizer.encode().\n\n@lru_cache requires hashable args; str instructions are fine.\nCache survives the lifetime of the tokenizer object.", "kind": "function", "line": 86, "name": "make_cached_encode", "signature": "def make_cached_encode(tokenizer)"}, {"doc": "Return a cached version of tokenizer.tool_token().", "kind": "function", "line": 100, "name": "make_cached_tool_token", "signature": "def make_cached_tool_token(tokenizer)"}, {"kind": "function", "line": 94, "name": "_cached_encode", "signature": "def _cached_encode(text)"}, {"kind": "function", "line": 103, "name": "_cached_tool_token", "signature": "def _cached_tool_token(tool_name)"}]}], "type": "CodePropertyGraph", "version": "1.0"}
```

---

## Architecture Reference

### PY (17 files)

#### `lazyown_dataset_enhancer.py`
**Path:** `lazyown_dataset_enhancer.py`

**Classes:**
- `ExperienceStoreReader` (line 87) `class ExperienceStoreReader`
- `DatasetEnhancer` (line 165) `class DatasetEnhancer`

**Functions:**
- `_difficulty` (line 64) `def _difficulty(record)` - *Lower = easier.  Factors:
  - prompt length (shorter = easier)
  - number of words (fewer = easier)
  - output length (shorter = easier)
  - has error markers (harder)*

**Methods:**
- `_sanitize_output` (line 136) `def _sanitize_output(text)` - *Redact potential PII / sensitive data from LazyOwn output traces.*
- `_build_toolbench_record` (line 149) `def _build_toolbench_record(instruction, tool_name, arg, answer, domain)` - *Standard ToolBench-format record.*
- `print_stats` (line 348) `def print_stats(records)`
- `main` (line 375) `def main()`
- `__init__` (line 88) `def __init__(self, log_dir)`
- `list_runs` (line 91) `def list_runs(self)`
- `read_trace` (line 98) `def read_trace(self, run_dir)`
- `read_score` (line 113) `def read_score(self, run_dir)`
- `read_harness` (line 122) `def read_harness(self, run_dir)`
- `__init__` (line 166) `def __init__(self, log_dir, max_runs)`
- `enhance` (line 171) `def enhance(self)`
- `add_negative_examples` (line 236) `def add_negative_examples(self, records, n)` - *Add examples where the prompt is ambiguous and the model must NOT
pick a random tool, or where the user asks something outside LazyOwn's scope.*
- `curriculum_sort` (line 261) `def curriculum_sort(self, records)` - *Sort by difficulty (easy → hard).*
- `deduplicate` (line 265) `def deduplicate(self, records)` - *Deduplicate by instruction text only (same prompt can have different outputs).*
- `augment_simple` (line 276) `def augment_simple(self, records, multiplier)` - *Lightweight augmentation: replace IP addresses, hostnames, and common
keywords with variants to increase diversity without an LLM.*
- `run` (line 301) `def run(self, merge_with)`

#### `lazyown_dataset_generator.py`
**Path:** `lazyown_dataset_generator.py`

**Functions:**
- `_make_record` (line 3321) `def _make_record(tool_name, desc, category, instruction, arg)`
- `_apply_pentest_synonyms` (line 3414) `def _apply_pentest_synonyms(instr)` - *Replace common pentest terms with synonyms to increase diversity.*
- `_expand` (line 3430) `def _expand(tool_name, phrasings)` - *Generate additional phrasings via IP substitution, prefix injection, verb swap, and synonym replacement.*
- `_is_noisy_phrasing` (line 3554) `def _is_noisy_phrasing(instruction, arg)` - *Return True if the phrasing is too generic and likely to dilute training.
Criteria:
  - empty arg AND the instruction starts with a generic verb
  - instruction has fewer than 4 meaningful tokens*
- `build_dataset` (line 3571) `def build_dataset()`
- `write_jsonl` (line 3595) `def write_jsonl(records, path)`
- `print_stats` (line 3602) `def print_stats(records)`
- `main` (line 3616) `def main()`

#### `meta_harness_proposer.py`
**Path:** `meta_harness_proposer.py`

**Classes:**
- `LLMConfig` (line 75) `class LLMConfig`
- `LLMClient` (line 86) `class LLMClient` - *Minimal OpenAI-compatible chat client using only urllib.

Auto-falls back to local Ollama if the primary endpoint returns
401/403/404 (auth or routing errors).*
- `ExperienceReader` (line 150) `class ExperienceReader` - *Reads meta_harness_logs/ and builds diagnostic context.*
- `PatchEngine` (line 243) `class PatchEngine` - *Applies code patches safely.*
- `MetaHarnessProposer` (line 392) `class MetaHarnessProposer` - *Coding-agent proposer for harness optimisation.

Workflow:
    1. Read experience store (scores + traces).
    2. Build diagnostic context.
    3. Read current harness source.
    4. Prompt LLM to propose a patch.
    5. Validate & apply patch.
    6. Log the proposal as a new run.*

**Functions:**
- `_setup_logger` (line 58) `def _setup_logger(name, level)`

**Methods:**
- `main` (line 572) `def main()`
- `__init__` (line 93) `def __init__(self, cfg, logger)`
- `_try_chat` (line 97) `def _try_chat(self, api_url, model, system, user)`
- `chat` (line 121) `def chat(self, system, user)` - *Send a chat request and return the assistant message content.*
- `__init__` (line 153) `def __init__(self, log_dir, logger)`
- `list_runs` (line 157) `def list_runs(self, n)`
- `load_run` (line 165) `def load_run(self, run_dir)`
- `build_diagnostic_context` (line 193) `def build_diagnostic_context(self, top_k)` - *Build a rich diagnostic string containing:
- failed runs with their traces
- successful runs for contrast
- aggregate statistics*
- `__init__` (line 246) `def __init__(self, logger)`
- `validate_syntax` (line 249) `def validate_syntax(self, code)` - *Return (ok, error_message).*
- `apply_full_rewrite` (line 265) `def apply_full_rewrite(self, target_path, new_code, dry_run)` - *Validate and optionally write a full file rewrite.*
- `_strip_line_numbers` (line 283) `def _strip_line_numbers(self, s)` - *Remove leading ' 123: ' line numbers that the LLM may copy.*
- `apply_line_range` (line 287) `def apply_line_range(self, target_path, line_start, line_end, new_string, dry_run)` - *Replace a range of lines (1-indexed) with new text.*
- `apply_diff_hunk` (line 316) `def apply_diff_hunk(self, target_path, old_string, new_string, dry_run)` - *Apply a targeted string replacement after validation.

Tries exact match first, then fuzzy match (ignoring leading/trailing
whitespace per line), then without line numbers.  If all fail, prints
the patch for manual apply.*
- `__init__` (line 434) `def __init__(self, log_dir, llm_cfg, logger)`
- `propose_patch` (line 445) `def propose_patch(self, target_path, top_k, dry_run)` - *End-to-end propose-and-apply cycle.

Returns True if a patch was successfully applied (or validated in dry-run).*
- `_log_proposal` (line 538) `def _log_proposal(self, target_path, response, applied, diag)` - *Store the proposer's reasoning so future loops can evaluate it.*
- `_norm` (line 331) `def _norm(s)`

#### `test_dataset_enhancer.py`
**Path:** `tests/test_dataset_enhancer.py`

**Functions:**
- `_load_enhancer_module` (line 13) `def _load_enhancer_module()`
- `test_sanitize_ip` (line 24) `def test_sanitize_ip()`
- `test_sanitize_password` (line 31) `def test_sanitize_password()`
- `test_sanitize_ntlm_hash` (line 38) `def test_sanitize_ntlm_hash()`
- `test_sanitize_email` (line 44) `def test_sanitize_email()`
- `test_sanitize_idempotent_on_clean_text` (line 50) `def test_sanitize_idempotent_on_clean_text()`

#### `test_dataset_generator.py`
**Path:** `tests/test_dataset_generator.py`

**Functions:**
- `_load_gen_module` (line 13) `def _load_gen_module()`
- `test_is_noisy_short_instruction` (line 24) `def test_is_noisy_short_instruction()`
- `test_is_noisy_generic_verb_empty_arg` (line 30) `def test_is_noisy_generic_verb_empty_arg()`
- `test_is_noisy_permitted_with_arg` (line 36) `def test_is_noisy_permitted_with_arg()`
- `test_build_dataset_filters_noise` (line 42) `def test_build_dataset_filters_noise()`

#### `test_model_config.py`
**Path:** `tests/test_model_config.py`

**Functions:**
- `test_d_model_compatible_with_checkpoint` (line 11) `def test_d_model_compatible_with_checkpoint()`

#### `test_orchestrator.py`
**Path:** `tests/test_orchestrator.py`

**Classes:**
- `TestSessionContext` (line 15) `class TestSessionContext` - *Unit tests for the multi-turn SessionContext.*
- `TestKeywordRouter` (line 56) `class TestKeywordRouter` - *Tests for the deterministic keyword fallback router.*
- `TestNeuralRouter` (line 89) `class TestNeuralRouter` - *Tests for the neural route path using mocks.*
- `TestOrchestratorRun` (line 193) `class TestOrchestratorRun` - *Integration-level tests for the run() method.*

**Methods:**
- `_load_ctx` (line 18) `def _load_ctx(self)`
- `test_empty_prefix` (line 23) `def test_empty_prefix(self)`
- `test_prefix_with_target` (line 28) `def test_prefix_with_target(self)`
- `test_update_extracts_ip` (line 35) `def test_update_extracts_ip(self)`
- `test_phase_progression` (line 43) `def test_phase_progression(self)`
- `test_findings_from_output` (line 49) `def test_findings_from_output(self)`
- `_load_router` (line 59) `def _load_router(self)`
- `test_recon_keyword` (line 63) `def test_recon_keyword(self)`
- `test_config_keyword` (line 69) `def test_config_keyword(self)`
- `test_c2_keyword` (line 74) `def test_c2_keyword(self)`
- `test_fallback_search` (line 79) `def test_fallback_search(self)`
- `test_extract_arg_ip` (line 84) `def test_extract_arg_ip(self)`
- `orchestrator` (line 93) `def orchestrator(self)`
- `test_neural_route_none_when_no_engine` (line 120) `def test_neural_route_none_when_no_engine(self, orchestrator)`
- `test_neural_route_with_mock_head` (line 123) `def test_neural_route_with_mock_head(self, orchestrator)`
- `test_neural_route_low_confidence_fallback` (line 159) `def test_neural_route_low_confidence_fallback(self, orchestrator)`
- `test_run_updates_session` (line 196) `def test_run_updates_session(self)`
- `mock_register_forward_hook` (line 135) `def mock_register_forward_hook(cb)`
- `mock_model_forward` (line 141) `def mock_model_forward(ids)`
- `mock_register_forward_hook` (line 169) `def mock_register_forward_hook(cb)`
- `mock_model_forward` (line 175) `def mock_model_forward(ids)`

#### `topo_swarm_agent.py`
**Path:** `topo_swarm_agent.py`

**Classes:**
- `SwarmConfig` (line 84) `class SwarmConfig` - *All architectural and training hyper-parameters in one place.

Scale target: fit inside 6 GB VRAM on an RTX 2060.
- Weights: ~2 M params × 4 bytes = ~8 MB
- Activations (B=4, S=256): ~256 MB peak with gradient checkpointing
- Swarm overhead: N_AGENTS × D_MODEL × 4 bytes per Berry-phase tensor*
- `QuaternionOps` (line 282) `class QuaternionOps` - *Pure-functional quaternion operations over arbitrary leading batch dims.
Tensors have shape [..., 4] where the last dim is [w, x, y, z].*
- `QuaternionLinear` (line 330) `class QuaternionLinear(Module)` - *Linear map in the quaternion algebra.

Implements W ⊗ x via a single batched einsum over stacked weight matrices,
reducing CUDA kernel launches from 16 (naive 4×4 matmul loop) to 1.

Input  x: [..., 4*in_q]
Output  : [..., 4*out_q]*
- `SpectralBottleneck` (line 394) `class SpectralBottleneck(Module)` - *1-D spectral autoencoder acting as the function-call signal filter.

Compresses the token representation via rfft → learned complex kernel →
irfft → QuaternionLinear bottleneck → decode.  The bottleneck forces the
model to route function-call intent through a harmonic low-band subspace,
suppressing lexical noise from the surrounding context.

Returns (latent [B,S,latent_dim], recon_loss scalar).*
- `RMSNorm` (line 465) `class RMSNorm(Module)` - *Root Mean Square Layer Normalisation (LLaMA-style, no bias).*
- `RotaryEmbedding` (line 489) `class RotaryEmbedding(Module)` - *NTK-aware Rotary Position Embeddings.

Extends the standard RoPE base frequency when the requested sequence length
exceeds the training context, preventing aliasing in high-frequency dims.*
- `SwiGLU` (line 548) `class SwiGLU(Module)` - *SwiGLU feed-forward: SiLU(gate(x)) * up(x) → down(...).*
- `SwarmMoEGate` (line 587) `class SwarmMoEGate(Module)` - *Sigmoid gate: selects top-k experts per token, weights normalised.*
- `SwarmMoE` (line 608) `class SwarmMoE(Module)` - *Drop-in MoE replacement for SwiGLU in TopoSwarmLayer.

Architecture: N_EXPERTS independent SwiGLU experts + sigmoid gate.
Each token routes to top_k experts; outputs are weighted-summed.

For a 2M-param model (D=64, FFN_DIM=128):
  - 4 experts, top-2, expert_dim=128 → same FLOP as one dense FFN
    but 4× more representational capacity.*
- `SwarmMoEAdapter` (line 665) `class SwarmMoEAdapter(Module)` - *Residual MoE adapter: output = LayerNorm(input + moe(input)).

Plugs between model.norm_out and model.lm_head.  Zero-init on the output
projection of every expert means the adapter is an identity at init time —
the model starts at its existing accuracy and the adapter learns on top.

Expert architecture: d_model → d_model//2 → d_model (small bottleneck)
Gate: sigmoid (MiMo V2 style) → top-k selection, normalised weights.*
- `QuaternionTorusBrain` (line 807) `class QuaternionTorusBrain(Module)` - *Toroidal message-passing FFN replacement.

Pipeline per forward:
1.  Flatten [B, S, D] → [B*S, D].
2.  SpectralBottleneck: 1-D spectral encode → quaternion latent.
3.  Torus projection: QuaternionLinear → 4 scalars → (phi1, phi2) angles.
4.  Soft assignment: haversine distance to N_TORUS_NODES grid nodes.
5.  Node grid construction: weighted blend of node embeddings + input.
6.  Quaternion message-passing on the torus graph (vectorised scatter).
7.  Readout: attention-weighted sum → SwiGLU projection.
8.  Reshape [B*S, D] → [B, S, D].

Processes tokens in chunks of TORUS_TOKEN_CHUNK_SIZE to bound peak
VRAM to O(chunk × N_NODES × D) rather than O(B*S × N_NODES × D).*
- `QuaternionAttention` (line 998) `class QuaternionAttention(Module)` - *Grouped-query attention (GQA) with RoPE and quaternion Q/K projections.

A lightweight per-head 1-D spectral filter compresses the query and key
vectors before dot-product attention, forcing harmonic representations.*
- `HRMModule` (line 1103) `class HRMModule(Module)` - *Hierarchical Reasoning Model embedded in the torus agent.

L-module (fast / action): recurrent GRU-gated unit responsible for
the syntax of tool calls (the "how").

H-module (slow / strategy): a wider linear unit responsible for
tool selection (the "what").

The ACT (Adaptive Computational Time) halt logit is computed from the
Hamilton-product norm of the final H-state quaternion: when the norm
exceeds ACT_HALT_THRESHOLD the agent emits a decision; otherwise it
re-enters the message-passing loop (the "swarm consult" step).*
- `TopoSwarmLayer` (line 1205) `class TopoSwarmLayer(Module)` - *Single transformer layer: GQA attention + QuaternionTorusBrain FFN.

Both sub-layers use pre-norm (RMSNorm) and residual connections.
Gradient checkpointing is applied to the attention sub-layer.*
- `TopoSwarmModel` (line 1273) `class TopoSwarmModel(Module)` - *Micro quaternionic toroidal transformer for tool-use reasoning.

Architecture:
- Token embedding + learned positional bias.
- N_LAYERS of TopoSwarmLayer (GQA + QuaternionTorusBrain).
- HRM module on the pooled representation for ACT control.
- Language-model head (tied weights with embedding).

The Berry-phase offset is passed through every layer to specialise each
swarm agent slot without duplicating weight tensors.*
- `EpisodicMemory` (line 1487) `class EpisodicMemory` - *Three-tier episodic memory inspired by the tricameral neurology architecture.

Tier assignment is driven by a surprise score: cross-entropy modulated by
the mean ACT gate activity.  High-surprise events go to working memory
(highest replay priority); low-surprise events to long-term if their
computed importance exceeds a threshold.*
- `SwarmOrchestrator` (line 1602) `class SwarmOrchestrator` - *Coordinates N_AGENTS lightweight agent slots over a shared weight tensor.

Each agent slot is identified by a distinct Berry-phase offset on the
toroidal manifold.  The orchestrator:
1. Dispatches the same input to all slots in parallel (or sequentially
   if VRAM is tight).
2. Aggregates outputs via majority vote on the halt decision and
   mean-pooled logits.
3. Selects the tool call proposed by the slot with the highest ACT
   confidence (halt logit).

Swarm consensus protocol:
- If all slots halt → emit the tool call immediately.
- If fewer than half halt → perform one extra ACT step (internal
  torus message-passing consult) and re-evaluate.
- Otherwise → emit the call proposed by the most confident slot.*
- `BPETokenizer` (line 1693) `class BPETokenizer` - *Thin wrapper around tiktoken's GPT-2 BPE encoding.

Adds special tool tokens by reserving a range at the top of the
vocabulary [TOOL_TOKEN_OFFSET, TOOL_TOKEN_OFFSET + TOOL_VOCAB_SIZE).*
- `ToolBenchDataset` (line 1811) `class ToolBenchDataset(Dataset)` - *ToolBench "Instruction-Tool-Result" dataset loader.

Attempts to load from HuggingFace datasets first; falls back to a local
JSONL file at cfg.DATASET_LOCAL_PATH.  Only successful traces
(is_halt=True or equivalent) are retained.

Each sample is a flat token sequence:
    [instruction tokens] [tool token] [result tokens]
truncated to MAX_SEQ_LEN.  Training targets are the input shifted by 1.*
- `CheckpointManager` (line 2046) `class CheckpointManager` - *Manages safetensors checkpoints with JSON metadata in a single directory.

Writes to checkpoints_toposwarm/latest/ atomically by writing a temp
file and renaming it.*
- `KappaDetector` (line 2149) `class KappaDetector` - *Tracks the kappa coherence metric over a sliding window to detect grokking.

Kappa is defined as the inverse of the cross-entropy loss (clipped),
normalised to [0, 1].  A sharp upward jump of more than KAPPA_JUMP_THRESHOLD
within the window signals that the model has found the function-call
structure (the ToolBench grokking point).*
- `SwarmTrainer` (line 2192) `class SwarmTrainer` - *Three-phase training pipeline for the TopoSwarm agent.

Phase 0 (Kernel Calibration): Pre-trains only the SpectralBottleneck
parameters on the API schema strings to seed the harmonic filter.

Phase 1 (Main Training): Full model training with grokking detection
via the KappaDetector.

Phase 2 (Annealing): Fine-tunes with a reduced learning rate and
cosine schedule to stabilise the tool-call routing.*

**Methods:**
- `_setup_logger` (line 225) `def _setup_logger(name, level)` - *Return an idempotent logger. Delegates to ts_utils.setup_logger.*
- `_set_seed` (line 243) `def _set_seed(seed, device)` - *Deterministic seed across torch, numpy, and CUDA.*
- `_param_count` (line 253) `def _param_count(module)` - *Return total and trainable parameter counts.*
- `_get_torus_positions` (line 264) `def _get_torus_positions(n_angular, n_radial, device)` - *Cached angular / radial position linspaces for soft torus assignment.*
- `inject_moe_adapter` (line 749) `def inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)` - *Inject a SwarmMoEAdapter into an already-loaded TopoSwarmModel.

The backbone weights remain unchanged; only the adapter is new.
Optionally freezes all backbone parameters so only the adapter trains.

Args:
    model:           Loaded TopoSwarmModel instance.
    n_experts:       Number of MoE experts in the adapter.
    top_k:           Experts activated per token.
    dropout:         Adapter dropout.
    freeze_backbone: If True, freeze all non-adapter model parameters.
    adapter_path:    If given, load adapter weights from this path instead
                     of initialising from scratch.

Returns:
    The injected SwarmMoEAdapter (also stored as model.moe_adapter).*
- `_chunked_ce` (line 1445) `def _chunked_ce(logits, targets, chunk_size)` - *Cross-entropy over the sequence without materialising the full [N, V] matrix.

Processes the sequence in chunks of chunk_size to bound peak memory to
O(chunk_size × VOCAB_SIZE) instead of O(B*S × VOCAB_SIZE).

Args:
    logits: [B, S, V] or [N, V].
    targets: [B, S] or [N] integer targets.
    chunk_size: Tokens per chunk.

Returns:
    Scalar mean cross-entropy.*
- `build_dataloaders` (line 2509) `def build_dataloaders(cfg, tokenizer, logger)` - *Build train and validation DataLoaders from the ToolBench dataset.

Args:
    cfg: Swarm configuration.
    tokenizer: BPETokenizer for encoding.
    logger: Logger instance.

Returns:
    Tuple of (train_loader, val_loader).*
- `main` (line 2552) `def main()` - *CLI entry point.

Modes:
    --train             : Run the full three-phase training pipeline.
    --resume            : Resume training from the latest checkpoint.
    --infer --prompt P  : Load checkpoint and run swarm inference.
    --param-count       : Print model parameter counts and exit.*
- `__post_init__` (line 202) `def __post_init__(self)`
- `hamilton_product` (line 289) `def hamilton_product(q1, q2)` - *Hamilton (cross) product q1 ⊗ q2 for tensors of shape [..., 4].*
- `normalize` (line 304) `def normalize(q, eps)` - *Unit-normalise quaternion tensors.*
- `berry_phase_rotation` (line 309) `def berry_phase_rotation(q, phase)` - *Apply a Berry-phase rotation around the w-axis of the quaternion manifold.

Multiplies the (x, y, z) imaginary components by the complex phase
e^{i*phase} encoded as a rotation in the yz-plane, leaving the real
component w unchanged.  Used to differentiate swarm agent slots.*
- `__init__` (line 341) `def __init__(self, in_features, out_features, bias, init_std)` - *Initialise quaternion weight matrices.

Args:
    in_features: Must be divisible by 4.
    out_features: Must be divisible by 4.
    bias: Whether to add a bias parameter.
    init_std: Normal initialisation standard deviation.*
- `forward` (line 370) `def forward(self, x)` - *Fused Hamilton product via a single batched einsum.*
- `__init__` (line 406) `def __init__(self, cfg)` - *Build encoder/decoder spectral kernels and quaternion projections.

Args:
    cfg: Swarm configuration object.*
- `_filter` (line 428) `def _filter(self, x, kr, ki)` - *Apply a learned complex spectral filter in the rfft domain.*
- `forward` (line 436) `def forward(self, x)` - *Encode x through the spectral bottleneck.

A single rfft of x is computed and reused by both the encode branch
and the high-frequency penalty, avoiding a redundant FFT call.

Args:
    x: Input tensor [..., D_MODEL].

Returns:
    Tuple of (latent [..., latent_dim], scalar auxiliary loss).*
- `__init__` (line 468) `def __init__(self, d_model, eps)` - *Args:
    d_model: Feature dimension.
    eps: Numerical stability epsilon.*
- `forward` (line 478) `def forward(self, x)` - *Normalise by the RMS of x and rescale by learned weight.*
- `__init__` (line 497) `def __init__(self, d_head, max_seq_len, base, ntk_factor)` - *Args:
    d_head: Attention head dimension.
    max_seq_len: Maximum sequence length to pre-cache.
    base: RoPE base frequency.
    ntk_factor: Set to max_seq / train_seq when extrapolating.*
- `_build_cache` (line 522) `def _build_cache(self, seq_len)` - *Pre-compute cos/sin tables up to seq_len.*
- `_rotate_half` (line 530) `def _rotate_half(self, x)`
- `forward` (line 534) `def forward(self, x, seq_len)` - *Apply rotary embedding to query or key tensor [B, H, S, d_head].*
- `__init__` (line 551) `def __init__(self, d_model, hidden_dim, dropout)` - *Args:
    d_model: Input and output feature dimension.
    hidden_dim: Intermediate expansion dimension.
    dropout: Dropout probability after the output projection.*
- `forward` (line 566) `def forward(self, x)` - *Gated SiLU activation with residual dropout.*
- `__init__` (line 590) `def __init__(self, d_model, n_experts, top_k)`
- `forward` (line 597) `def forward(self, x)` - *x: [..., D] → (topk_idx [... K], topk_weight [..., K])*
- `__init__` (line 620) `def __init__(self, d_model, expert_hidden_dim, n_experts, top_k, dropout)`
- `forward` (line 637) `def forward(self, x)` - *x: [B, S, D] → [B, S, D]  (autograd-safe, no in-place scatter)*
- `__init__` (line 679) `def __init__(self, d_model, n_experts, top_k, bottleneck, dropout)`
- `forward` (line 705) `def forward(self, x)` - *x: [B, S, D] → [B, S, D]  (residual)

Autograd-safe: no in-place scatter — computes all expert outputs at
once and weights them via a sparse weight tensor.*
- `save` (line 727) `def save(self, path)`
- `load` (line 738) `def load(cls, path)`
- `__init__` (line 825) `def __init__(self, cfg)` - *Args:
    cfg: Swarm configuration.*
- `_build_torus_graph` (line 855) `def _build_torus_graph(self)` - *Construct the adjacency structure of the discrete torus.

Each node (r, a) connects angularly to (r, a±1) and radially to
(r±1, a).  Angular neighbours wrap around (periodic boundary).
Radial neighbours are open (no wrap).  Edge types encode direction:
0=ang-left, 1=ang-right, 2=rad-inner, 3=rad-outer.*
- `_torus_soft_assign` (line 887) `def _torus_soft_assign(self, phi1, phi2)` - *Soft assignment of token coordinates to torus nodes via haversine distance.

Args:
    phi1: Angular coordinate [-pi, pi] of shape [N].
    phi2: Radial coordinate [-pi, pi] of shape [N].

Returns:
    Soft assignment weights [N, N_TORUS_NODES] summing to 1.*
- `_message_passing` (line 909) `def _message_passing(self, node_feat)` - *One round of quaternion message-passing on the torus graph.

Messages are Hamilton-product-rotated by a learnable edge quaternion
and aggregated via scatter-add to each destination node.

Args:
    node_feat: Node feature tensor [N_chunk, N_NODES, D_MODEL].

Returns:
    Updated node features [N_chunk, N_NODES, D_MODEL].*
- `forward` (line 940) `def forward(self, x, berry_phase)` - *Full torus forward with optional Berry-phase offset for swarm slots.

Processes tokens in chunks to bound peak VRAM.

Args:
    x: Input [B, S, D_MODEL].
    berry_phase: Phase offset applied to the torus projection output
                 for this agent slot, rotating the soft assignment
                 and inducing specialisation.

Returns:
    Tuple of (output [B, S, D_MODEL], scalar auxiliary recon loss).*
- `__init__` (line 1006) `def __init__(self, cfg)` - *Args:
    cfg: Swarm configuration.*
- `_head_filter` (line 1039) `def _head_filter(self, x)` - *Apply the shared per-head spectral filter [B, H, S, d_head].*
- `forward` (line 1045) `def forward(self, x, is_causal)` - *GQA forward pass with RoPE and optional gradient checkpointing.

Args:
    x: Input [B, S, D].
    is_causal: Whether to apply causal masking.

Returns:
    Output [B, S, D].*
- `__init__` (line 1119) `def __init__(self, cfg)` - *Args:
    cfg: Swarm configuration.*
- `_l_step` (line 1156) `def _l_step(self, x, state)` - *One GRU-gated L-module step.*
- `_h_step` (line 1163) `def _h_step(self, z)` - *One H-module strategy update.*
- `forward` (line 1167) `def forward(self, x)` - *Run the HRM hierarchy and return the updated state with ACT signal.

Args:
    x: Pooled context embedding [B, D].

Returns:
    Tuple of (h_state [B, D], halt_logit [B, 1], act_loss scalar).*
- `__init__` (line 1213) `def __init__(self, cfg)` - *Args:
    cfg: Swarm configuration.*
- `_attn_fn` (line 1237) `def _attn_fn(self, x)`
- `forward` (line 1240) `def forward(self, x, berry_phase)` - *Pre-norm layer forward.

Args:
    x: Input [B, S, D].
    berry_phase: Swarm Berry-phase offset for the torus brain.

Returns:
    Tuple of (output [B, S, D], torus recon loss scalar).*
- `__init__` (line 1287) `def __init__(self, cfg)` - *Args:
    cfg: Swarm configuration.*
- `forward` (line 1311) `def forward(self, input_ids, berry_phase, targets)` - *Full forward pass for one agent slot.

Args:
    input_ids: Token ids [B, S].  Any id outside [0, VOCAB_SIZE) is
               clamped before the embedding lookup so a bad upstream
               token never triggers a CUDA device-side assert.
    berry_phase: Slot-specific torus phase offset.
    targets: Optional target ids [B, S] for computing the LM loss.

Returns:
    Dict with keys:
    - "logits": [B, S_clip, VOCAB_SIZE]
    - "halt_logit": [B, 1] ACT confidence
    - "loss": scalar (only when targets is provided)
    - "recon_loss": scalar torus reconstruction loss
    - "act_loss": scalar ACT entropy regulariser*
- `generate` (line 1392) `def generate(self, input_ids, max_new_tokens, temperature, top_k, berry_phase, act_halt_threshold)` - *Autoregressive generation with ACT-driven early stopping.

The model stops generating when the halt logit exceeds the threshold
and ACT_MAX_STEPS is not yet reached, simulating the "swarm consult"
internal loop: low confidence → continue message-passing rather than
emitting output.

Args:
    input_ids: Prompt token ids [1, S].
    max_new_tokens: Maximum tokens to generate.
    temperature: Sampling temperature.
    top_k: Top-k truncation before sampling.
    berry_phase: Agent slot phase.
    act_halt_threshold: Confidence threshold for early stopping.

Returns:
    Tuple of (generated ids [1, S + new_tokens], did_halt bool).*
- `__init__` (line 1497) `def __init__(self, cfg)` - *Args:
    cfg: Swarm configuration for capacity and threshold parameters.*
- `compute_surprise` (line 1512) `def compute_surprise(logits, targets, gate_mean)` - *Surprise = cross-entropy × (1 - gate_mean), clipped to [0, 10].

A high gate_mean (confident model) attenuates the surprise signal;
a low gate_mean (uncertain) amplifies it.

Args:
    logits: Raw model logits [B, S, V] or [N, V].
    targets: Integer targets matching logits.
    gate_mean: Mean ACT halt probability in [0, 1].

Returns:
    Scalar surprise value.*
- `store` (line 1537) `def store(self, episode, surprise)` - *Store an episode in the appropriate memory tier.

Args:
    episode: Dict of tensors/metadata describing the experience.
    surprise: Scalar surprise score from compute_surprise.*
- `sample` (line 1558) `def sample(self, n)` - *Sample n episodes with priority proportional to surprise / importance.

Draws from all three tiers; working memory contributes the most
samples (50 %), short-term 30 %, long-term 20 %.

Args:
    n: Number of episodes to sample.

Returns:
    List of episode dicts.*
- `_decay` (line 1591) `def _decay(self)` - *Apply exponential forgetting to the long-term memory scores.*
- `__init__` (line 1622) `def __init__(self, model, cfg)` - *Args:
    model: Shared TopoSwarmModel instance.
    cfg: Swarm configuration.*
- `infer` (line 1640) `def infer(self, input_ids, tokenizer, max_new_tokens, temperature, top_k)` - *Run swarm inference and return the decoded output string.

Args:
    input_ids: Prompt token ids [1, S].
    tokenizer: BPETokenizer used to decode output ids.
    max_new_tokens: Maximum tokens any slot may generate.
    temperature: Sampling temperature.
    top_k: Top-k sampling truncation.

Returns:
    Decoded string of the winning slot's output.*
- `__init__` (line 1701) `def __init__(self, cfg)` - *Args:
    cfg: Swarm config (provides TOOL_TOKEN_OFFSET and TOOL_VOCAB_SIZE).*
- `encode` (line 1739) `def encode(self, text)` - *Encode text to BPE token ids, clamped to the BPE vocab ceiling.

tiktoken encodes exclusively within [0, bpe_vocab_size), but we clamp
defensively to prevent any edge-case overflow from reaching the
embedding table lookup.*
- `decode` (line 1751) `def decode(self, ids)` - *Decode token ids to text, silently dropping tool tokens.*
- `tool_token` (line 1756) `def tool_token(self, tool_name)` - *Return a stable integer token id for a named tool.

Assigns a deterministic id within the tool-token range based on the
MD5 hash of the tool name, ensuring consistent mapping across runs.
The result is always in [TOOL_TOKEN_OFFSET, TOOL_TOKEN_OFFSET + TOOL_VOCAB_SIZE)
which is guaranteed to be < VOCAB_SIZE by the __init__ check above.

Args:
    tool_name: Canonical tool identifier string.

Returns:
    Integer token id in [TOOL_TOKEN_OFFSET, TOOL_TOKEN_OFFSET + TOOL_VOCAB_SIZE).*
- `encode_tool_trace` (line 1778) `def encode_tool_trace(self, instruction, tool_name, result)` - *Encode a ToolBench-style (instruction, tool, result) triple.

Inserts a dedicated tool token between the instruction and the result,
so the model learns to associate the tool-token with the API semantics
rather than carrying the full JSON in the sequence.

All returned ids are guaranteed to be in [0, VOCAB_SIZE) because:
- BPE ids are clamped in encode() to [0, bpe_vocab_size).
- tool_token() returns ids in [tool_offset, tool_offset + tool_vocab_size)
  which is < VOCAB_SIZE by construction (checked in __init__).

Args:
    instruction: Natural language instruction string.
    tool_name: Tool / API identifier.
    result: Observed tool output string.

Returns:
    Flat list of token ids, all in [0, VOCAB_SIZE).*
- `__init__` (line 1824) `def __init__(self, cfg, tokenizer, split, logger)` - *Args:
    cfg: Swarm configuration.
    tokenizer: BPETokenizer for encoding traces.
    split: Dataset split name.
    logger: Optional logger instance.*
- `_load` (line 1846) `def _load(self, split)` - *Load and tokenise tool traces with three-level fallback.

Level 1 – Maurus/ToolBench (HuggingFace parquet, no loading script).
    Schema: {query, api_list, domain}.  api_list is a JSON list of
    dicts each with keys tool_name and api_name.
Level 2 – local JSONL at cfg.DATASET_LOCAL_PATH.
    Accepted schemas: any dict with recognisable query/tool/result keys.
Level 3 – synthetic stubs of fixed length MAX_SEQ_LEN with token ids
    inside [0, VOCAB_SIZE).  Safe dry-run fallback.*
- `_encode_record` (line 1927) `def _encode_record(self, rec)` - *Encode a tool-trace record to token ids.

Handles three schemas:

Maurus/ToolBench (primary):
    query      : str  – natural language instruction
    api_list   : list of dicts with keys tool_name, api_name,
                 api_description (used as the "result" proxy)
    domain     : str  – category label

Legacy ToolBench JSONL:
    instruction / query / input / prompt → instruction text
    api_name / tool_name / tool          → tool identifier
    response / result / output / answer  → observed result

All text fields are truncated to 512 characters before encoding to
prevent single records from dominating the token budget.*
- `_synthetic_stubs` (line 1984) `def _synthetic_stubs(self, n)` - *Generate n synthetic tool-trace stubs safe for dry-run training.

All token ids produced from these stubs are guaranteed to be within
[0, VOCAB_SIZE) because:
- instruction and result text encode to ids within [0, bpe_vocab_size).
- tool_token() returns ids within [TOOL_TOKEN_OFFSET, TOOL_TOKEN_OFFSET
  + TOOL_VOCAB_SIZE) < VOCAB_SIZE (validated in BPETokenizer.__init__).*
- `__len__` (line 2017) `def __len__(self)`
- `__getitem__` (line 2020) `def __getitem__(self, idx)` - *Return a (input_ids, target_ids) pair of length MAX_SEQ_LEN.

Token ids are clamped to [0, VOCAB_SIZE - 1] as a hard safety guard
against any upstream encoding edge case that could produce an
out-of-bounds embedding lookup on the GPU.*
- `__init__` (line 2054) `def __init__(self, cfg, logger)` - *Args:
    cfg: Swarm configuration.
    logger: Logger instance.*
- `save` (line 2066) `def save(self, model, optimizer, meta, force)` - *Save model weights and metadata if the interval has elapsed.

Args:
    model: Model to checkpoint.
    optimizer: Optimizer state to checkpoint.
    meta: Scalar metadata dict (epoch, step, loss, etc.).
    force: If True, save regardless of the time interval.*
- `load` (line 2108) `def load(self, model, optimizer, device)` - *Load model weights and metadata from the latest checkpoint.

Args:
    model: Target model (mutated in-place).
    optimizer: Optional optimizer to restore state into.
    device: Device string for weight map.

Returns:
    Metadata dict if found, None otherwise.*
- `__init__` (line 2159) `def __init__(self, cfg)` - *Args:
    cfg: Swarm configuration (window and threshold).*
- `update` (line 2167) `def update(self, loss)` - *Update the detector with the latest loss value.

Args:
    loss: Scalar training loss.

Returns:
    Tuple of (current_kappa, grokking_detected bool).*
- `__init__` (line 2206) `def __init__(self, model, cfg, tokenizer, logger)` - *Args:
    model: TopoSwarmModel instance.
    cfg: Swarm configuration.
    tokenizer: BPETokenizer.
    logger: Logger instance.*
- `_make_optimizer` (line 2233) `def _make_optimizer(self, lr)` - *Build AdamW with weight decay applied only to non-bias, non-norm params.

Args:
    lr: Learning rate.

Returns:
    Configured AdamW optimizer.*
- `_warmup_cosine_lr` (line 2263) `def _warmup_cosine_lr(self, optimizer, step, total_steps, warmup_steps, base_lr)` - *Apply warmup + cosine decay learning rate schedule.*
- `_train_one_batch` (line 2280) `def _train_one_batch(self, optimizer, input_ids, targets, accum_step, berry_phase)` - *Forward + backward for one micro-batch, returns detached loss.

Args:
    optimizer: Current optimizer.
    input_ids: [B, S] token ids.
    targets: [B, S] target ids.
    accum_step: Index within the gradient accumulation window.
    berry_phase: Agent slot phase for this forward pass.

Returns:
    Scalar loss value (Python float).*
- `_phase0_calibrate` (line 2322) `def _phase0_calibrate(self, dataloader, n_steps)` - *Phase 0: Kernel calibration on API schema tokens.

Freezes all parameters except the SpectralBottleneck kernels,
training only the spectral filter to recognise API intent.

Args:
    dataloader: Training dataloader.
    n_steps: Number of calibration gradient steps.*
- `train` (line 2363) `def train(self, train_dl, val_dl, resume)` - *Full three-phase training loop.

Phase 0: Kernel calibration (50 steps, spectral params only).
Phase 1: Main training for cfg.EPOCHS epochs with kappa detection.
Phase 2: Cosine annealing for 1 extra epoch at half learning rate.

Args:
    train_dl: Training DataLoader.
    val_dl: Validation DataLoader.
    resume: If True, attempt to restore from the latest checkpoint.*
- `_evaluate` (line 2476) `def _evaluate(self, val_dl)` - *Compute mean validation loss over the first EVAL_INTERVAL_STEPS batches.

Args:
    val_dl: Validation DataLoader.

Returns:
    Mean loss scalar.*
- `_manual_attn` (line 1072) `def _manual_attn()`

#### `topogpt2_1.py`
**Path:** `topogpt2_1.py`

**Classes:**
- `TopoGPT2Config` (line 55) `class TopoGPT2Config` - *Configuración completa para TopoGPT2.*
- `QuaternionOps` (line 177) `class QuaternionOps` - *Operaciones de cuaterniones puras en PyTorch.
Representación: [..., 4]  donde last dim = [w, x, y, z]
q = w + x*i + y*j + z*k*
- `QuaternionLinear` (line 216) `class QuaternionLinear(Module)` - *Capa lineal con pesos cuaterniones.

Implementa la multiplicación W * x en el álgebra de cuaterniones:
- W = Ww + Wx*i + Wy*j + Wz*k  (cuaternión de pesos)
- x = xw + xx*i + xy*j + xz*k  (cuaternión de entrada)
- out = W * x  (producto de Hamilton extendido a vectores)

Parámetros: 4 matrices reales de forma [out_q, in_q]*
- `QuaternionSpectralLayer` (line 261) `class QuaternionSpectralLayer(Module)` - *Convolución espectral 2D con cuaterniones y producto de Hamilton completo.

Operación en dominio de frecuencia:
    P(k) = W(k) ⊗ X(k)  (producto de Hamilton de cuaterniones complejos)

Donde:
    X(k) = FFT2(x) con 4 canales cuaterniones [Xw, Xx, Xy, Xz]
    W(k) = kernel complejo aprendible con componentes [Ww, Wx, Wy, Wz]

Reglas del producto de Hamilton en dominio de frecuencia:
    Pw = Ww·Xw - Wx·Xx - Wy·Xy - Wz·Xz
    Px = Ww·Xx + Wx·Xw + Wy·Xz - Wz·Xy
    Py = Ww·Xy - Wx·Xz + Wy·Xw + Wz·Xx
    Pz = Ww·Xz + Wx·Xy - Wy·Xx + Wz·Xw

Cada Wc es un kernel complejo (partes real e imaginaria independientes).*
- `SpectralAutoencoder` (line 348) `class SpectralAutoencoder(Module)` - *Autoencoder espectral con cuaterniones.

Opera en dos niveles:
1. Espectral 1D sobre el vector de features (FFT sobre dim D_MODEL):
   captura la espectrografía global del embedding.
2. Espectral 2D sobre el grid del toro (QuaternionSpectralLayer):
   captura correlaciones espaciales en la topología.

Devuelve (latent, recon_loss) para regularización.*
- `QuaternionTorusBrain` (line 431) `class QuaternionTorusBrain(Module)` - *Reemplaza el MLP en cada capa del transformer.

Pipeline (completamente vectorizado sobre batch Y secuencia):

1. Flatten: [B, S, D] → [B·S, D]
2. SpectralAutoencoder: filtrado espectral 1D + compresión cuaternión
3. Proyección al toro:
   - Calcula 2 ángulos (phi1, phi2) ∈ [-π, π]²
   - Asignación blanda a los 8 nodos via distancia circular en el toro
4. Construye grid de nodos: [B·S, N_NODES=8, D_MODEL]
5. QuaternionSpectralLayer 2D sobre el grid [B·S, 4*D_QUAT, RADIAL, ANGULAR]
6. Message-passing con rotaciones cuaterniones sobre el grafo toro
7. Readout: atención sobre los 8 nodos → [B·S, D_MODEL]
8. Reshape: [B·S, D] → [B, S, D]*
- `RotaryEmbedding` (line 648) `class RotaryEmbedding(Module)` - *Rotary Position Embeddings (RoPE) - Su et al., 2021.
Codifica la posición como rotaciones del espacio de atención,
naturalmente relativas y sin parámetros extra.*
- `RMSNorm` (line 696) `class RMSNorm(Module)` - *Root Mean Square Layer Normalization (sin bias). Más estable que LayerNorm.*
- `SwiGLU` (line 713) `class SwiGLU(Module)` - *SwiGLU: SiLU(gate(x)) * up(x) -> down
Usado en LLaMA 2/3, Qwen, Mistral en lugar de GELU-FFN.
Dimension interna: 8/3 * d_model (convención LLaMA, redondeada a múltiplo de 4).*
- `TopoMoEBrain` (line 742) `class TopoMoEBrain(Module)` - *Mixture of Experts sobre la capa topologica.

Arquitectura (inspirada en DeepSeek-MoE / Mixtral):
  - 1 experto compartido: QuaternionTorusBrain (siempre activo)
  - N_EXPERTS expertos SwiGLU ligeros (activacion esparsa: Top-K por token)
  - Router: Linear(D, N_EXPERTS) + softmax → top-K

Load-balancing loss (auxiliar): penaliza si un experto acapara todos los tokens.
Activa MOE_TOP_K de N_EXPERTS expertos por token.

Sin MoE (MOE_ENABLED=False): se comporta como QuaternionTorusBrain puro.*
- `MultiHeadAttention` (line 847) `class MultiHeadAttention(Module)` - *Multi-head attention con:
- Flash Attention (scaled_dot_product_attention de PyTorch 2.0+)
- Rotary Position Embeddings (RoPE)
- GQA (Grouped Query Attention): N_KV_HEADS < N_HEADS, reduce VRAM de K/V
- KV Cache para inferencia autoregresiva eficiente
- Temperatura termodinámica aprendible*
- `TopoGPT2Layer` (line 929) `class TopoGPT2Layer(Module)` - *Capa del transformer con TopoMoEBrain (TopoBrain + MoE SwiGLU experts).

Esquema pre-norm (estilo LLaMA):
    x = x + Attention_GQA(RMSNorm(x))
    x = x + TopoMoEBrain(RMSNorm(x))*
- `TopoGPT2` (line 976) `class TopoGPT2(Module)` - *TopoGPT2: Transformer de lenguaje con TopoBrain cuaternión-espectral.

Arquitectura:
    Embedding de tokens + RoPE (en Attention)
    N_LAYERS × TopoGPT2Layer (Attention + QuaternionTorusBrain)
    RMSNorm final
    Proyección a vocabulario (weight-tied con embeddings)*
- `BPETokenizer` (line 1082) `class BPETokenizer` - *Wrapper alrededor de tiktoken (GPT-2 compatible).*
- `CorpusDownloader` (line 1107) `class CorpusDownloader` - *Descarga corpus de texto para entrenamiento.

Soporta:
- 'tinystories': ~2GB de cuentos cortos (ideal para pruebas)
- 'wikitext103': ~500MB de Wikipedia curada
- 'file': archivo de texto local

Usa HuggingFace 'datasets' para TinyStories y WikiText.*
- `TokenizedDataset` (line 1170) `class TokenizedDataset(Dataset)` - *Dataset de tokens para language modeling (next-token prediction).

Guarda los tokens tokenizados en disco la primera vez (cache .pt)
para evitar re-tokenizar en cada ejecucion. La clave de cache incluye
un hash del contenido del corpus + tokenizador + max_tokens.*
- `CheckpointManager` (line 1220) `class CheckpointManager` - *Gestiona checkpoints de forma acumulativa y segura.

Estructura en disco:
    checkpoints_topogpt2/
      latest/
        model.safetensors   <- pesos del modelo (formato seguro, sin pickle)
        optimizer.pt        <- estado del optimizador (requiere .pt)
        state.json          <- metadatos: epoch, step, historial, config
      best/
        model.safetensors
        state.json
      step_NNNNN/           <- snapshots periodicos (rotados)
        model.safetensors
        optimizer.pt
        state.json

El historial se ACUMULA entre sesiones de entrenamiento: cada --resume
agrega nuevas entradas a train_loss[], val_loss[], etc.*
- `TopoGPT2Trainer` (line 1453) `class TopoGPT2Trainer` - *Entrenador acumulativo y resumible.

Caracteristicas:
- Checkpoint automatico en safetensors cada N minutos + cada epoch
- Historial acumulativo entre sesiones (--resume agrega al historial existente)
- Guarda el mejor modelo en checkpoints/best/ automaticamente
- LR schedule: cosine con warmup relativo a los steps de ESTA sesion
- Mixed Precision (AMP) + acumulacion de gradientes*
- `MechanisticMetrics` (line 1746) `class MechanisticMetrics` - *Calcula todas las metricas del diagrama de fases de Book.md.

Todas las metricas se derivan de cantidades medibles (pesos, gradientes):

delta  (δ): margen de discretizacion.  max|w - round(w)|
            δ≈0 -> cristal;  δ≈0.49 -> vidrio frio
kappa  (κ): numero de condicion de la covarianza del gradiente.
            κ≈1 -> cristalino;  κ>>1 -> amorfo
T_eff:      temperatura efectiva = (lr/2) * Var(gradiente).
            T_eff→0 -> congelado; T_eff alto -> ruidoso
alpha  (α): indice de pureza = -log(δ + ε).
            α=20 -> perfecto; α<1 -> vidrio
berry:      fase de Berry de los kernels espectrales imaginarios.
            |berry|>π/2 con winding≠0 -> insulador topologico
lc:         complejidad local = 1 - similitud coseno promedio entre filas.
sp:         superposicion = correlacion promedio inter-fila de pesos.*
- `Phase0_KernelOptimizer` (line 1983) `class Phase0_KernelOptimizer` - *Encuentra el ratio imaginario/real optimo para los kernels espectrales.

Analogia con main.py: evalua la transicion GOE→GUE en el espacio
de kernels. Un ratio optimo promueve estructura topologica (insulador)
vs estructura amorfa (vidrio).

Metodo: calibra con un mini-batch y mide la varianza del gradiente
en funcion del ratio. Ratios que minimizan la varianza de gradiente
(maxima coherencia espectral) son preferibles.

No entrena: solo inicializa los kernels con distintos ratios y mide.
Tiempo tipico: < 30 segundos.*
- `Phase1_BatchProspector` (line 2058) `class Phase1_BatchProspector` - *Encuentra el batch size optimo testando candidatos con pocos pasos.

De main.py: el batch size regula la temperatura del horno de cristalizacion.
Batch sizes demasiado chicos -> ruido excesivo (vidrio frio).
Batch sizes demasiado grandes -> sin presion annealing (amorfos).
La ventana optima empirica de main.py: [24, 128] para Strassen.

Para LM, testeamos candidatos midiendo:
- delta (δ): velocidad de descenso en prospect_steps pasos
- T_eff: temperatura efectiva del gradiente

Tiempo tipico: < 2 minutos para 3 candidatos × 30 pasos.*
- `Phase2_SeedMiner` (line 2141) `class Phase2_SeedMiner` - *Encuentra semillas prometedoras midiendo la trayectoria de delta.

De main.py: una semilla "buena" muestra delta descendente en los
primeros N pasos (enfriamiento). Una semilla "mala" se estanca en
el plateau vidrioso (~0.49).

Criterio de seleccion:
1. Semillas con delta_velocity < 0 (enfriando) AND kappa bajo.
2. Si no hay, semillas solo enfriando.
3. Fallback: semilla con menor delta final.

Tiempo tipico: < 3 minutos para 5 semillas × 50 pasos.*
- `Phase4_AnnealingRefiner` (line 2223) `class Phase4_AnnealingRefiner` - *Refinamiento post-entrenamiento mediante recocido simulado.

De main.py: despues de que el modelo converge, una fase de annealing
con criterio de aceptacion de Metropolis puede empujar los pesos
hacia estados de menor energia libre (menor delta o mejor val_loss).

Aceptacion de Metropolis:
    si Δloss < 0: siempre acepta (mejora)
    si Δloss >= 0: acepta con prob exp(-Δloss / T)

La temperatura T decae exponencialmente: T(t) = T0 * cooling_rate^t

Al rechazar: restaura el mejor estado conocido.
Si se estanca: perturbacion termica (ruido gaussiano en pesos).

Tiempo: proporcional a refine_epochs (user-controlled).*
- `TopoPhasePipeline` (line 2384) `class TopoPhasePipeline` - *Orquesta las 5 fases de entrenamiento segun main.py + Book.md.

Fases:
  0  Kernel ratio optimization  (GOE-GUE spectral calibration)
  1  Batch size prospecting      (temperatura del horno de cristalizacion)
  2  Seed mining                 (seleccion de semilla enfriante)
  3  Full training               (entrenamiento principal con metricas)
  4  Annealing refinement        (recocido simulado post-entrenamiento)

Las fases 0-2 son rapidas (prospecting). La fase 3 es el grueso.
La fase 4 es opcional (--refine).

Para no ser prohibitivo:
  --prospect         activa fases 0, 1, 2 antes del entrenamiento
  --refine-epochs N  activa fase 4 con N epocas de annealing
  Sin flags: solo fase 3 (comportamiento original, identico a antes)*

**Methods:**
- `setup_logger` (line 155) `def setup_logger(name, level)`
- `set_seed` (line 165) `def set_seed(seed, device)`
- `main` (line 2506) `def main()`
- `__post_init__` (line 124) `def __post_init__(self)`
- `hamilton_product` (line 185) `def hamilton_product(q1, q2)` - *Producto de Hamilton q1 ⊗ q2. Ambos [..., 4].*
- `normalize` (line 197) `def normalize(q, eps)`
- `conjugate` (line 201) `def conjugate(q)`
- `rotate_vector` (line 206) `def rotate_vector(v, q)` - *Rota vector 3D v por cuaternión unitario q. v:[...,3] q:[...,4]*
- `__init__` (line 228) `def __init__(self, in_features, out_features, bias)`
- `forward` (line 244) `def forward(self, x)` - *x: [..., in_features] → [..., out_features]*
- `__init__` (line 281) `def __init__(self, in_q, out_q, grid_h, grid_w, init_scale)`
- `_kernel` (line 300) `def _kernel(self, c)`
- `_contract` (line 303) `def _contract(self, W, X)` - *Suma sobre canales in_q: Y[b,o,h,w] = Σ_i W[i,o,h,w]·X[b,i,h,w]*
- `forward` (line 307) `def forward(self, x)` - *x: [B, 4*in_q, H, W]  (4 canales cuaterniones sobre grid espacial)
→ [B, 4*out_q, H, W]*
- `__init__` (line 361) `def __init__(self, config)`
- `_filter1d` (line 393) `def _filter1d(self, x, kr, ki)` - *Filtro espectral 1D: x[..., D] → filtrado[..., D]*
- `encode` (line 399) `def encode(self, x)` - *x: [..., D_MODEL] → latent: [..., D_LAT]*
- `decode` (line 404) `def decode(self, z)` - *z: [..., D_LAT] → recon: [..., D_MODEL]*
- `forward` (line 409) `def forward(self, x)` - *Devuelve (latent, recon_loss)*
- `process_torus_grid` (line 416) `def process_torus_grid(self, grid)` - *Procesa el grid del toro con QuaternionSpectralLayer.
grid: [B, 4*D_QUAT, RADIAL, ANGULAR]  →  [B, 4*D_QUAT, RADIAL, ANGULAR]*
- `__init__` (line 449) `def __init__(self, d_model, config)`
- `_build_torus_graph` (line 489) `def _build_torus_graph(self)` - *Construye las aristas del grafo toro 2×4.

Nodos indexados como: node = r * N_ANGULAR + a
  r ∈ [0, RADIAL-1], a ∈ [0, ANGULAR-1]

Aristas angulares: nodo ↔ nodo a la izquierda/derecha (periódico)
Aristas radiales:  nodo ↔ nodo del anillo interior/exterior*
- `_torus_soft_assign` (line 523) `def _torus_soft_assign(self, phi1, phi2)` - *Asignación blanda de tokens a los 8 nodos del toro via distancia circular.

phi1: [BS] ángulo angular ∈ [-π, π]
phi2: [BS] ángulo radial ∈ [-π, π]
→ weights: [BS, N_NODES]  (suma a 1, softmax de distancias negativas)*
- `_message_passing` (line 550) `def _message_passing(self, node_feat)` - *Message-passing VECTORIZADO con rotaciones cuaterniones.
Sin bucles Python: todas las aristas se procesan en paralelo.

node_feat: [BS, N_NODES, D_MODEL]
→ [BS, N_NODES, D_MODEL]*
- `forward` (line 587) `def forward(self, x)` - *x: [B, S, D_MODEL]
→ output: [B, S, D_MODEL], recon_loss: scalar*
- `__init__` (line 655) `def __init__(self, d_head, max_seq_len, base)`
- `_build_cache` (line 661) `def _build_cache(self, seq_len)`
- `_rotate_half` (line 668) `def _rotate_half(self, x)`
- `forward` (line 672) `def forward(self, q, k, seq_len, offset)` - *q, k: [B, n_heads, S_q/S_k, d_head]
offset: posicion inicial (para KV cache: longitud del cache existente)
Aplica posiciones [offset .. offset+S-1] a q y k.*
- `__init__` (line 699) `def __init__(self, d_model, eps)`
- `forward` (line 704) `def forward(self, x)`
- `__init__` (line 720) `def __init__(self, d_model, expansion, dropout)`
- `forward` (line 734) `def forward(self, x)`
- `__init__` (line 757) `def __init__(self, d_model, config)`
- `_route` (line 778) `def _route(self, x)` - *x: [N, D] donde N = B*S (tokens aplanados)
Retorna:
expert_out: [N, D]  suma ponderada de top-K expertos
aux_loss:   escalar  load-balancing loss
Routing vectorizado sin boolean indexing ni sincronizacion CUDA.
Usa dispatch por indices agrupados (estilo Mixtral/DeepSeek) para
compatibilidad total con torch.utils.checkpoint.*
- `forward` (line 820) `def forward(self, x)` - *x: [B, S, D]
→ output: [B, S, D], aux_loss: escalar*
- `__init__` (line 857) `def __init__(self, d_model, n_heads, config)`
- `forward` (line 875) `def forward(self, x, is_causal, past_kv)` - *Args:
    x:        [B, S, D]
    is_causal: usar mascara causal
    past_kv:  (K_cache, V_cache) de pasos anteriores o None
Returns:
    out:      [B, S, D]
    kv_cache: (K, V) completos para cachear en generate()*
- `__init__` (line 938) `def __init__(self, d_model, n_heads, config)`
- `_forward_impl` (line 947) `def _forward_impl(self, x, past_kv)`
- `forward` (line 956) `def forward(self, x, past_kv)` - *Retorna (x_out, aux_loss, kv_cache).
Con gradient checkpointing en training (solo cuando no hay KV cache).*
- `__init__` (line 987) `def __init__(self, config)`
- `_init_weights` (line 1006) `def _init_weights(self)`
- `forward` (line 1013) `def forward(self, token_ids, past_kvs)` - *token_ids: [B, S]  (enteros)
past_kvs:  lista de (K, V) por capa, o None para entrenamiento
→ logits: [B, S, VOCAB_SIZE], aux_loss: scalar, new_kvs: list[(K,V)]*
- `count_params` (line 1036) `def count_params(self)`
- `generate` (line 1042) `def generate(self, token_ids, max_new_tokens, temperature, top_k)` - *Generacion autoregresiva con KV cache y muestreo top-k.
En el primer paso procesa el prompt completo y guarda el cache.
En pasos siguientes solo procesa 1 token nuevo (O(n) en lugar de O(n^2)).*
- `__init__` (line 1085) `def __init__(self, encoding)`
- `encode` (line 1093) `def encode(self, text)`
- `decode` (line 1096) `def decode(self, tokens)`
- `eot_token` (line 1099) `def eot_token(self)`
- `__init__` (line 1119) `def __init__(self, corpus, data_dir, logger)`
- `get_text` (line 1125) `def get_text(self, split)` - *Devuelve el texto del corpus. Descarga si es necesario.*
- `_download_hf` (line 1150) `def _download_hf(self, dataset_name, split, text_column, name)`
- `__init__` (line 1179) `def __init__(self, text, tokenizer, seq_len, max_tokens, cache_dir, split_tag)`
- `__len__` (line 1206) `def __len__(self)`
- `__getitem__` (line 1209) `def __getitem__(self, idx)`
- `__init__` (line 1245) `def __init__(self, config, logger)`
- `patch_config_for_resume` (line 1255) `def patch_config_for_resume(self, cfg)` - *Lee el checkpoint 'latest' y ajusta cfg.N_KV_HEADS / cfg.GQA_GROUPS
para que coincidan con la arquitectura guardada.
Necesario cuando el codigo cambio GQA despues de guardar el checkpoint.*
- `_save_model` (line 1284) `def _save_model(self, model, directory)`
- `_load_model` (line 1297) `def _load_model(self, model, directory)`
- `_save_optimizer` (line 1328) `def _save_optimizer(self, optimizer, directory)`
- `_load_optimizer` (line 1331) `def _load_optimizer(self, optimizer, directory, device)`
- `_save_state` (line 1340) `def _save_state(self, state, directory)`
- `_load_state` (line 1345) `def _load_state(self, directory)`
- `should_save` (line 1356) `def should_save(self)`
- `save` (line 1359) `def save(self, model, optimizer, state, is_best)` - *Guarda checkpoint completo.

state debe contener al menos: completed_epochs, global_step,
best_val_loss, history, config.*
- `load_latest` (line 1404) `def load_latest(self, model, optimizer)` - *Carga el ultimo checkpoint guardado.
Devuelve el state dict (vacio si no hay checkpoint).*
- `load_best` (line 1431) `def load_best(self, model)` - *Carga el mejor modelo guardado (solo pesos, sin optimizador).*
- `has_checkpoint` (line 1443) `def has_checkpoint(self)`
- `__init__` (line 1465) `def __init__(self, model, config, tokenizer)`
- `resume` (line 1500) `def resume(self)` - *Carga el ultimo checkpoint disponible.
Restaura: pesos del modelo, estado del optimizador, historial acumulado,
epoch/step completados y mejor val_loss.
Devuelve True si se cargo un checkpoint, False si empieza de cero.*
- `_current_state` (line 1525) `def _current_state(self)` - *Construye el dict de estado para persistir en state.json.*
- `_cosine_lr` (line 1536) `def _cosine_lr(self, step_in_session, total_steps_session)` - *Cosine decay con warmup. El schedule es relativo a la sesion actual.*
- `_set_lr` (line 1544) `def _set_lr(self, lr)`
- `train` (line 1548) `def train(self, train_dl, val_dl)` - *Entrena cfg.EPOCHS epocas adicionales a partir de completed_epochs.
El historial se acumula sobre sesiones previas.*
- `_sample_text` (line 1684) `def _sample_text(self, tokenizer, prompts, max_new, temperature, top_k)` - *Genera una muestra de texto al final de cada epoch para monitorear
la calidad cualitativa del modelo (detecta degeneracion, repeticion, etc.).*
- `evaluate` (line 1716) `def evaluate(self, dataloader)`
- `__init__` (line 1766) `def __init__(self, config)`
- `compute_delta` (line 1774) `def compute_delta(self, model)`
- `compute_alpha` (line 1781) `def compute_alpha(self, delta)`
- `update_grad_buffer` (line 1786) `def update_grad_buffer(self, model)` - *Captura gradientes de forma segura, ignorando tensores corruptos.*
- `compute_t_eff` (line 1812) `def compute_t_eff(self, lr)` - *T_eff = lr/2 * Var(gradiente). Temperatura termodinamica efectiva.*
- `compute_kappa` (line 1820) `def compute_kappa(self, model, dataloader, n_batches)` - *κ = λ_max / λ_min de la covarianza del gradiente.
Parámetro de orden para cristalización (κ≈1 = cristal).
Nota: requiere pasadas backward adicionales. Se ejecuta con protección
para no corromper el estado AMP del trainer principal.*
- `compute_berry_phase` (line 1878) `def compute_berry_phase(self, model)` - *Fase de Berry de los kernels espectrales imaginarios.
Surge de los parametros ki_w, ki_x, ki_y, ki_z de QuaternionSpectralLayer.
|berry|>pi/2 con winding!=0 indica estructura topologica.*
- `compute_lc` (line 1891) `def compute_lc(self, model)` - *Complejidad local: 1 - similitud coseno promedio entre filas de pesos.*
- `compute_sp` (line 1905) `def compute_sp(self, model)` - *Superposicion: correlacion inter-fila promedio (entrelazamiento de features).*
- `classify_phase` (line 1921) `def classify_phase(self, delta, kappa, berry)` - *Clasificacion de fase segun Book.md:

discrete_crystal:       delta<0.05, kappa<1.5
topological_insulator:  |berry|>pi/2, winding!=0
cold_glass:             kappa>>1, delta>0.3
functional_glass:       intermedio (lo mas comun en LM)*
- `compute_all` (line 1940) `def compute_all(self, model, lr, dataloader, compute_kappa)` - *Calcula todas las metricas.
compute_kappa=True hace pasadas backward adicionales (caro, usar cada N epochs).*
- `format_log` (line 1965) `def format_log(self, m)`
- `__init__` (line 2001) `def __init__(self, config, logger)`
- `_measure_ratio` (line 2005) `def _measure_ratio(self, ratio, sample_batch)` - *Mide la coherencia espectral para un ratio dado.
Retorna: varianza del gradiente (menor = mas coherente = mejor).*
- `optimize` (line 2034) `def optimize(self, dataloader)` - *Retorna el mejor ratio de inicializacion de kernels espectrales.*
- `__init__` (line 2074) `def __init__(self, config, logger)`
- `prospect` (line 2078) `def prospect(self, candidates, train_dataset, prospect_steps)` - *Retorna el mejor batch size segun delta y T_eff.*
- `__init__` (line 2157) `def __init__(self, config, logger)`
- `mine` (line 2161) `def mine(self, seed_start, n_seeds, train_dataset, prospect_steps)` - *Retorna la semilla con la mejor trayectoria de delta.*
- `__init__` (line 2243) `def __init__(self, trainer, t0, cooling_rate, stagnation_patience)`
- `refine` (line 2252) `def refine(self, train_dl, val_dl, refine_epochs)` - *Ejecuta refine_epochs epocas de recocido simulado.
Retorna el historial de refinamiento.*
- `__init__` (line 2404) `def __init__(self, config, train_dataset, val_dataset, tokenizer, logger)`
- `_make_dataloaders` (line 2414) `def _make_dataloaders(self, batch_size)`
- `run` (line 2426) `def run(self, run_prospect, refine_epochs, resume, prospect_steps, probe_seeds, seed_start)` - *Ejecuta el pipeline completo.
Retorna el trainer con el modelo entrenado.*
- `ckpt_fn` (line 964) `def ckpt_fn(x_in)`

#### `toposwarm_coevolve.py`
**Path:** `toposwarm_coevolve.py`

**Classes:**
- `HarnessMutation` (line 128) `class HarnessMutation` - *Simple mutation operators over MetaHarnessConfig dicts.*
- `MockLazyOwnBridge` (line 183) `class MockLazyOwnBridge` - *Deterministic mock of LazyOwnBridge for isolated harness evaluation.
Returns canned responses so the orchestrator can be exercised even when
LazyOwn is not present.*
- `HarnessEvaluator` (line 233) `class HarnessEvaluator` - *Evaluates a harness configuration by running the LazyOwn orchestrator
on a suite of validation prompts and aggregating scores.

Uses in-process evaluation (no subprocess) so:
- Meta-Harness logs are written to the same filesystem store.
- Import errors are visible immediately.
- Latencies are realistic.*
- `WeightTrainer` (line 391) `class WeightTrainer` - *Thin wrapper around toposwarm_continual_trainer.py for inner-loop
weight updates.*
- `CoEvolutionEngine` (line 451) `class CoEvolutionEngine` - *Outer-loop harness evolution with optional inner-loop weight co-evolution.*

**Functions:**
- `_resolve_lazyown_dir` (line 63) `def _resolve_lazyown_dir()` - *Discover LazyOwn installation directory.

Priority:
  1. LAZYOWN_DIR environment variable (expanded ~).
  2. Default relative to this script: <repo>/LazyOwn.
  3. User home directory: ~/LazyOwn.
  4. Return the relative default anyway (caller will see available=False).*
- `_setup_logger` (line 90) `def _setup_logger(name, level)`

**Methods:**
- `_clip` (line 175) `def _clip(x, lo, hi)`
- `main` (line 646) `def main()`
- `mutate` (line 132) `def mutate(cfg_dict)`
- `crossover` (line 167) `def crossover(a, b)`
- `__init__` (line 190) `def __init__(self)`
- `available` (line 196) `def available(self)`
- `run` (line 199) `def run(self, command, timeout)`
- `get_config` (line 222) `def get_config(self)`
- `set_config` (line 225) `def set_config(self, key, value)`
- `__init__` (line 244) `def __init__(self, prompts, lazyown_dir, logger, use_mock_bridge)`
- `evaluate` (line 256) `def evaluate(self, cfg_dict)` - *Run each prompt through the orchestrator and collect metrics.

Also logs every evaluation to the Meta-Harness experience store so the
proposer has data to diagnose.*
- `_build_orchestrator` (line 313) `def _build_orchestrator(self, cfg_dict)` - *Build a LazyOwnOrchestrator with the given MetaHarnessConfig.*
- `_log_run` (line 343) `def _log_run(self, orch, prompt, result, latency_ms, ctx_len, ok, cfg_dict)` - *Write one evaluation to the Meta-Harness experience store.*
- `__init__` (line 397) `def __init__(self, logger)`
- `_load` (line 402) `def _load(self)`
- `is_available` (line 415) `def is_available(self)`
- `fine_tune` (line 418) `def fine_tune(self, dataset_path, steps, learning_rate)` - *Run a short fine-tuning burst and return metrics.*
- `__init__` (line 456) `def __init__(self, generations, population_size, train_steps_per_gen, proposer_interval, lazyown_dir, logger)`
- `run` (line 490) `def run(self)`
- `_next_generation` (line 550) `def _next_generation(self, scores)`
- `_tournament_select` (line 567) `def _tournament_select(sorted_scores, k)`
- `_is_on_frontier` (line 575) `def _is_on_frontier(self, cfg, metrics)`
- `_run_proposer` (line 596) `def _run_proposer(self)`
- `_save_state` (line 619) `def _save_state(self, generation)`
- `load_state` (line 628) `def load_state(self, path)`
- `_report_frontier` (line 635) `def _report_frontier(self)`

#### `toposwarm_continual_trainer.py`
**Path:** `toposwarm_continual_trainer.py`

**Classes:**
- `ContinualConfig` (line 111) `class ContinualConfig` - *All hyper-parameters for the continual learning run.*
- `SurpriseBuffer` (line 166) `class SurpriseBuffer` - *Tracks per-example surprise scores and returns a priority-weighted
replay sample so the trainer oversamples examples the model is failing on.

Surprise (from NeuroLogos tricameral):
    surprise = CE_loss × (1 − confidence)
where confidence = softmax_max of the LM-head logits at the routing position.

High surprise = model is wrong AND was overconfident → hardest to learn.
These examples are stored and mixed into subsequent mini-batches at a
configurable ratio (default 25 % of each batch).*
- `ToolBenchDataset` (line 300) `class ToolBenchDataset(Dataset)`
- `ReplayBuffer` (line 334) `class ReplayBuffer` - *Circular buffer of ToolBench examples.

Randomly selects REPLAY_RATIO * batch_size samples to mix into every
fine-tuning batch, ensuring the model continuously sees original-task
examples during LazyOwn training.*
- `EWC` (line 365) `class EWC` - *Elastic Weight Consolidation.

Computes the diagonal of the Fisher Information Matrix on a sample of
ToolBench data, then adds the quadratic penalty to the loss at every
fine-tuning step.

The penalty is:
    L_ewc = λ/2 · Σ_i  F_i · (θ_i − θ*_i)²

where θ* is the snapshot of parameters BEFORE fine-tuning begins, and
F_i is the empirical Fisher diagonal (mean squared gradient of log-prob).*
- `SwarmLiquidNeuron` (line 514) `class SwarmLiquidNeuron(Module)` - *Liquid neuron for routing: slow proj (gradient) + fast Hebbian weights.

Architecture:
    slow_out  = W_slow(x)            # [B, n_tools], gradient path
    fast_out  = x @ W_fast.T         # [B, n_tools], Hebbian path, no grad
    output    = LayerNorm(slow_out + fast_scale * fast_out)

W_fast is updated after each training step via:
    ΔW_fast = lr_hebb × (post.T @ pre) / B   (clamped ±0.3)
where pre = hidden states, post = one-hot tool labels.

Homeostasis clips output norm to [0.5, 2.0] to prevent explosion.*
- `RoutingHead` (line 600) `class RoutingHead(Module)` - *Thin linear probe: d_model → n_tools.

Trained on top of the frozen (or lightly-tuned) backbone with standard
cross-entropy over the N LazyOwn tools.  Bypasses the 50k-token LM head
so 100% of the gradient goes to the routing decision.

Tool-to-index mapping is deterministic (sorted tool name list), so the
head can be saved/loaded independently of the backbone checkpoint.*
- `ContinualTrainer` (line 730) `class ContinualTrainer` - *Fine-tuning loop with EWC + Replay.

Each training step:
    1. Sample a mini-batch from LazyOwn dataset.
    2. Sample REPLAY_RATIO fraction from ToolBench replay buffer.
    3. Concatenate → mixed batch.
    4. Compute task loss on mixed batch.
    5. Add EWC penalty.
    6. Backward + gradient clip + optimizer step.

The combined loss is:
    L = L_task(mixed_batch) + EWC.penalty()*

**Functions:**
- `_import` (line 91) `def _import(name, filename)`

**Methods:**
- `_setup_logger` (line 158) `def _setup_logger(level)`
- `_load_jsonl` (line 232) `def _load_jsonl(path)`
- `_encode_record` (line 247) `def _encode_record(record, tok, cfg)` - *Encode a ToolBench-format record into (input_ids, target_ids).

Uses the same compact format as topo_swarm_agent.ToolBenchDataset._encode_record:
    [instruction BPE tokens]  [tool token]  [compact result BPE tokens]

This matches the pretraining distribution exactly, keeping cross-entropy in
the same range as the original training (1-2 nats) rather than the full
vocabulary baseline (~10.8 nats for random predictions over 50k+ tokens).*
- `_collate` (line 319) `def _collate(batch)`
- `evaluate_routing` (line 1137) `def evaluate_routing(model, cfg, tok, lazyown_records, toolbench_records, logger)` - *Measure routing accuracy on a held-out subset of both datasets.

Routing accuracy = fraction of examples where the highest-probability
tool token matches the ground-truth tool in the api_list.*
- `build_model_and_tok` (line 1195) `def build_model_and_tok(cl_cfg, logger)`
- `run_full_pipeline` (line 1217) `def run_full_pipeline(cl_cfg, logger)` - *Generate dataset → compute Fisher → fine-tune → evaluate.*
- `main` (line 1384) `def main()`
- `__init__` (line 180) `def __init__(self, maxsize, replay_ratio)`
- `update` (line 186) `def update(self, records, task_losses, logits)` - *Add batch examples to buffer, keyed by surprise score.*
- `sample` (line 213) `def sample(self, batch_size)` - *Return a priority-weighted sample of hard examples.*
- `__len__` (line 223) `def __len__(self)`
- `__init__` (line 301) `def __init__(self, records, tok, cfg)`
- `__len__` (line 312) `def __len__(self)`
- `__getitem__` (line 315) `def __getitem__(self, idx)`
- `__init__` (line 343) `def __init__(self, records, max_size, tok, cfg)`
- `sample` (line 351) `def sample(self, n)`
- `__len__` (line 356) `def __len__(self)`
- `__init__` (line 380) `def __init__(self, model, cfg, cl_cfg, tok, logger)`
- `compute` (line 401) `def compute(self, toolbench_records)` - *Compute Fisher diagonal on a sample of ToolBench records and snapshot θ*.

Uses label log-prob gradients (empirical Fisher):
    F_i = (1/N) Σ_n  (∂ log p(y_n|x_n, θ) / ∂ θ_i)²*
- `save` (line 465) `def save(self, path)`
- `load` (line 470) `def load(self, path)`
- `penalty` (line 481) `def penalty(self)` - *Returns the EWC penalty term to add to the task loss.

Complexity: O(params) per step — negligible for a 2M-param model.*
- `__init__` (line 534) `def __init__(self, d_model, n_tools)`
- `forward` (line 551) `def forward(self, x)` - *x: [B, d_model] → logits [B, n_tools]*
- `hebbian_update` (line 570) `def hebbian_update(self, pre, labels)` - *Strengthen W_fast associations after correct predictions.

pre:    [B, d_model] — hidden states (instruction-end position)
labels: [B]          — true tool class indices*
- `__init__` (line 614) `def __init__(self, d_model, tool_names, n_experts, top_k, hidden_dim)`
- `n_tools` (line 651) `def n_tools(self)`
- `forward` (line 654) `def forward(self, hidden)` - *hidden: [B, d_model] → logits [B, n_tools]

Pipeline:
  0. Pre-MLP: enrich representation capacity
  1. LiquidNeuron: slow grad + fast Hebbian → base logits [B, n_tools]
  2. MoE gate: select top-k specialty expert refinements
  3. Weighted sum of expert-refined logits*
- `label` (line 685) `def label(self, tool_name)`
- `predict` (line 688) `def predict(self, hidden)` - *hidden: [B, d_model] → list of predicted tool name strings*
- `save` (line 695) `def save(self, path)`
- `load` (line 706) `def load(cls, d_model, path)`
- `__init__` (line 746) `def __init__(self, model, cfg, cl_cfg, tok, ewc, replay, logger, routing_head)`
- `_make_optimizer` (line 782) `def _make_optimizer(self)`
- `_lr_schedule` (line 821) `def _lr_schedule(optimizer, step, total, warmup, base_lr)`
- `_merge_with_replay` (line 830) `def _merge_with_replay(self, ids, tgt)` - *Append replay samples to the LazyOwn batch.*
- `_routing_accuracy` (line 863) `def _routing_accuracy(self, records)` - *Routing accuracy using the LM head (primary) and routing head (secondary).

Feeds only instruction tokens; evaluates the last-position logits.
Uses cached encode for speed.  Always returns LM-head accuracy (which
matches the training objective) so the metric is honest.*
- `train` (line 923) `def train(self, lazyown_dataset, train_records, val_records)`
- `_accuracy` (line 1153) `def _accuracy(records, label)`
- `_hook` (line 887) `def _hook(m, i, o)`
- `_capture` (line 995) `def _capture(module, inp, out_h)`

#### `toposwarm_hybrid.py`
**Path:** `toposwarm_hybrid.py`

**Classes:**
- `HybridConfig` (line 115) `class HybridConfig` - *All hyper-parameters for the hybrid system — zero magic numbers.*
- `ToolResult` (line 218) `class ToolResult` - *Structured result from a tool call.*
- `ToolRegistry` (line 231) `class ToolRegistry` - *Registry of executable tools with keyword-based routing.*
- `TopoSwarmRouter` (line 396) `class TopoSwarmRouter` - *Thin wrapper around TopoSwarmModel that performs only tool routing.

The router uses keyword-based routing (deterministic, no model inference
needed for the routing decision) combined with the crystallised model for
swarm-consensus confidence scoring.

Because the model's Pass 2 output is always noisy, we bypass it entirely
and return only the (tool_name, tool_arg) pair.  The LanguageBackend
handles all text generation.*
- `LanguageBackend` (line 465) `class LanguageBackend` - *Language generation backend.

Supports three modes:
- tinystories: HuggingFace GPT-2-style model loaded via transformers.
- checkpoint:  Raw PyTorch state_dict for your own 25M model.
- none:        Returns empty string; caller uses deterministic template.*
- `HybridResult` (line 946) `class HybridResult` - *All intermediate and final outputs of one hybrid inference run.*
- `HybridOrchestrator` (line 977) `class HybridOrchestrator` - *Combines TopoSwarmRouter + LanguageBackend into a single inference call.

Pipeline:
1. Router.route(prompt)        → (tool_name, tool_arg)
2. Registry.execute(...)       → ToolResult
3. Backend.generate(...)       → raw natural-language answer
4. Quality check               → use backend output or template fallback*

**Functions:**
- `_import_agent` (line 85) `def _import_agent()` - *Import topo_swarm_agent, searching script dir then cwd.*

**Methods:**
- `_setup_logger` (line 164) `def _setup_logger(name, level)` - *Idempotent logger with a single StreamHandler.*
- `_safe_eval` (line 182) `def _safe_eval(expr)` - *Evaluate a math expression safely via AST — no eval().*
- `_template_answer` (line 887) `def _template_answer(tool_name, tool_arg, tool_result)` - *Build a clean deterministic answer from the tool result.

Used when the language backend is disabled or produces output below
BACKEND_MIN_OUTPUT_CHARS.

Args:
    tool_name: Canonical tool name.
    tool_arg: Argument passed to the tool.
    tool_result: ToolResult instance.

Returns:
    Human-readable answer string.*
- `_is_useful_output` (line 918) `def _is_useful_output(text, min_chars)` - *Return True if the backend output is genuinely informative.

Checks length and absence of common TinyStories non-answer patterns
(story openers, repetition, incomplete sentences starting with
conjunctions).*
- `main` (line 1051) `def main()` - *CLI entry point.

Flags
-----
--prompt TEXT              : User request.
--backend-type STR         : tinystories | checkpoint | none
--backend-model STR        : HuggingFace model ID or local path
--backend-checkpoint PATH  : Path to raw .pt checkpoint (checkpoint mode)
--router-checkpoint DIR    : Path to checkpoints_toposwarm directory
--list-tools               : Print registered tools and exit
--dry-run                  : Test tool execution only (no models loaded)
--temperature F            : Router sampling temperature
--device STR               : Force cpu or cuda*
- `_eval` (line 192) `def _eval(node)`
- `__init__` (line 221) `def __init__(self, tool_name, arg, output, ok)`
- `__str__` (line 227) `def __str__(self)`
- `__init__` (line 234) `def __init__(self, cfg)`
- `_register` (line 240) `def _register(self)`
- `resolve` (line 249) `def resolve(self, raw)` - *Resolve tool name to canonical key via exact match, alias, or substring.*
- `route` (line 261) `def route(self, prompt)` - *Infer tool name and argument from prompt keywords.

Returns (tool_name, tool_arg) where tool_arg is the most specific
sub-string of the prompt relevant to the tool (e.g. city name for
weather, expression for calc_expr).*
- `execute` (line 287) `def execute(self, tool_name, arg)` - *Execute a tool by canonical name.*
- `_http_get` (line 299) `def _http_get(self, url)`
- `_register_all` (line 304) `def _register_all(self)` - *Register all built-in tools.*
- `tool_names` (line 387) `def tool_names(self)`
- `__init__` (line 409) `def __init__(self, cfg, registry, logger)` - *Args:
    cfg: Hybrid configuration.
    registry: ToolRegistry used for routing via registry.route().
    logger: Logger instance.*
- `_load` (line 428) `def _load(self)` - *Load checkpoint weights.*
- `route` (line 441) `def route(self, prompt)` - *Determine the tool and argument for a prompt.

Uses keyword-based routing (deterministic) — the crystallised model
weights already encoded this perfectly, so we replicate the same logic
without running the full forward pass for routing.

Args:
    prompt: Natural language user prompt.

Returns:
    Tuple of (tool_name, tool_arg).*
- `__init__` (line 475) `def __init__(self, cfg, logger)` - *Args:
    cfg: Hybrid configuration (BACKEND_TYPE, BACKEND_MODEL_ID, etc.).
    logger: Logger instance.*
- `_load` (line 486) `def _load(self)` - *Load the language model according to BACKEND_TYPE.*
- `_load_tinystories` (line 507) `def _load_tinystories(self)` - *Load a GPT-2-style HuggingFace model (TinyStories or compatible).

The model is loaded in half-precision on CUDA if available to minimise
VRAM usage alongside the TopoSwarm router.  On CPU it uses full
precision.*
- `_import_topogpt` (line 563) `def _import_topogpt(self)` - *Import topogpt2_1.py from the same directory as the checkpoint or
the script directory.  Returns the module or None if not found.*
- `_load_checkpoint` (line 588) `def _load_checkpoint(self)` - *Load a safetensors or pickle checkpoint for the language backend.

Strategy
--------
1. Try to import topogpt2_1.py from dirs near the checkpoint and
   instantiate its model class directly — exact architecture match.
2. Fall back to loading via topo_swarm_agent.TopoSwarmModel with
   architecture inferred from weight shapes (strict=False, skipping
   mismatched buffers like rope caches which are recomputed).*
- `generate` (line 859) `def generate(self, prompt, tool_result)` - *Generate a natural-language answer from the prompt and tool result.

Args:
    prompt: Original user question.
    tool_result: Raw string output from the executed tool.

Returns:
    Generated answer string, or empty string if backend is None.*
- `pretty` (line 958) `def pretty(self)` - *Render a human-readable summary.*
- `__init__` (line 988) `def __init__(self, cfg, logger)` - *Args:
    cfg: Hybrid configuration.
    logger: Logger instance.*
- `run` (line 1000) `def run(self, prompt)` - *Execute the full hybrid pipeline for one user prompt.

Args:
    prompt: Natural language user request.

Returns:
    HybridResult with all steps populated.*
- `decorator` (line 241) `def decorator(fn)`
- `get_weather` (line 308) `def get_weather(city)`
- `search_web` (line 319) `def search_web(query)`
- `calc_expr` (line 331) `def calc_expr(expr)`
- `get_datetime` (line 335) `def get_datetime(tz_hint)`
- `translate` (line 341) `def translate(text)`
- `get_news` (line 373) `def get_news(topic)`
- `echo` (line 383) `def echo(text)`
- `_generate` (line 540) `def _generate(prompt_text)`
- `_cfg_score` (line 703) `def _cfg_score(cls)`
- `_generate` (line 812) `def _generate(prompt_text)`
- `_generate` (line 835) `def _generate(prompt_text)`

#### `toposwarm_infer.py`
**Path:** `toposwarm_infer.py`

**Classes:**
- `InferenceConfig` (line 84) `class InferenceConfig` - *All inference-time hyper-parameters — zero magic numbers.*
- `ToolResult` (line 189) `class ToolResult` - *Structured result returned by every tool executor.*
- `ToolRegistry` (line 210) `class ToolRegistry` - *Registry of executable tools.

Each tool is a callable(arg: str) -> str.  Registration is done via the
@register decorator.  Tool names are matched case-insensitively and with
common aliases (e.g. "weather" matches "get_weather", "weather_now").*
- `ToolCallParser` (line 438) `class ToolCallParser` - *Extract tool calls from model-generated text.

The model may emit tool calls in several formats; this parser tries all
of them in priority order and returns the first match.*
- `InferenceEngine` (line 483) `class InferenceEngine` - *Full agentic inference loop:

1. Encode prompt.
2. First-pass generation via SwarmOrchestrator.
3. Parse any tool call from the generated text.
4. Execute the tool.
5. Second-pass generation conditioned on prompt + tool result.
6. Return structured InferenceResult.*
- `InferenceResult` (line 883) `class InferenceResult` - *All intermediate and final outputs of one inference run.*

**Functions:**
- `_import_agent` (line 51) `def _import_agent()` - *Import topo_swarm_agent, searching the script dir and cwd.*

**Methods:**
- `_safe_eval` (line 138) `def _safe_eval(expr)` - *Evaluate a mathematical expression without using eval() on arbitrary code.

Supports: +, -, *, /, //, %, **, unary minus, parentheses, int and float
literals.  Raises ValueError on any disallowed construct.*
- `_setup_logger` (line 920) `def _setup_logger(name, level)` - *Idempotent logger with a single StreamHandler.*
- `main` (line 938) `def main()` - *CLI entry point.

Flags
-----
--prompt TEXT        : Natural language request to the agent.
--checkpoint DIR     : Path to checkpoints_toposwarm directory.
--max-tokens N       : Maximum new tokens for pass 1.
--temperature F      : Sampling temperature (0 = greedy).
--top-k N            : Top-k truncation.
--list-tools         : Print all registered tool names and exit.
--dry-run            : Skip model load; test tool execution only.
--device STR         : Force cpu or cuda.*
- `_eval` (line 157) `def _eval(node)`
- `__init__` (line 192) `def __init__(self, tool_name, arg, output, ok)` - *Args:
    tool_name: Name of the tool that was called.
    arg: Raw argument string passed to the tool.
    output: Human-readable result string.
    ok: Whether the tool call succeeded.*
- `__str__` (line 205) `def __str__(self)`
- `__init__` (line 219) `def __init__(self, cfg)` - *Args:
    cfg: Inference configuration (provides timeout and result limits).*
- `register` (line 229) `def register(self)` - *Decorator that registers a function under one or more tool names.*
- `resolve` (line 239) `def resolve(self, raw_name)` - *Resolve a raw tool name to its canonical registry key.

Performs exact match, then alias lookup, then prefix/substring search.

Args:
    raw_name: Tool name as emitted by the model.

Returns:
    Canonical tool name string, or None if not found.*
- `execute` (line 262) `def execute(self, raw_name, arg)` - *Execute a tool by name with the given argument string.

Args:
    raw_name: Tool name as emitted by the model.
    arg: Argument string (stripped of surrounding whitespace/quotes).

Returns:
    ToolResult with the output or an error message.*
- `_http_get` (line 292) `def _http_get(self, url)` - *Minimal HTTP GET with timeout, returns response body as string.*
- `_register_builtin_tools` (line 301) `def _register_builtin_tools(self)` - *Register all built-in tools onto self._tools / self._aliases.*
- `__init__` (line 446) `def __init__(self, cfg)` - *Args:
    cfg: Inference config (provides TOOL_TAG_RE pattern).*
- `parse` (line 453) `def parse(self, text)` - *Extract the first tool call from text.

Args:
    text: Raw model output string.

Returns:
    Tuple of (tool_name, arg) or None if no tool call found.*
- `__init__` (line 495) `def __init__(self, cfg, agent_cfg, logger)` - *Args:
    cfg: Inference configuration.
    agent_cfg: SwarmConfig used to instantiate the model.
    logger: Logger instance.*
- `_load_checkpoint` (line 521) `def _load_checkpoint(self)` - *Load weights from the latest checkpoint directory.*
- `_encode_prompt` (line 538) `def _encode_prompt(self, text)` - *Encode a prompt string to a [1, S] token id tensor on the model device.

Wraps the raw text in the ToolBench training format so the model
receives input that matches its training distribution:

    query: <text>
    api_list: [{"tool_name": "<inferred>", ...}]
    domain: General
    <tool_token>

The tool name is inferred from keyword signals so the tool token sits
at the correct position — matching encode_tool_trace() used at training.
Token ids are clamped to [0, VOCAB_SIZE-1] to prevent embedding crashes.*
- `_generate` (line 586) `def _generate(self, prompt_ids, max_new_tokens, temperature)` - *Custom autoregressive generation loop with three inference-time fixes.

Fix 1 — Repetition penalty: divides logits of already-seen tokens by
REPETITION_PENALTY, preventing the single-token collapse (. / is / :).

Fix 2 — ACT-driven temperature: when the halt_prob exceeds
ACT_TEMPERATURE_TRIGGER the temperature is boosted by
ACT_TEMPERATURE_BOOST, forcing lexical diversity at high-confidence
steps rather than collapsing to the mode token.

Fix 3 — MIN_ANSWER_TOKENS guard: the ACT halt signal is ignored for
the first MIN_ANSWER_TOKENS newly generated tokens, guaranteeing at
least that many tokens of output regardless of halt confidence.

All three fixes operate purely on logits/probabilities at decode time
with no weight updates — no retraining required.*
- `run` (line 679) `def run(self, prompt)` - *Full agentic inference loop for one user prompt.

Protocol (matches the training distribution exactly):

Pass 1 — The prompt is encoded in ToolBench format:
    [instruction_tokens][tool_token]
The model generates a completion of the result side.
This raw completion is stored as first_output.

Tool execution — The tool inferred at encoding time is executed
with the prompt as its argument.  This gives a real, live result
independent of what the model generated.

Pass 2 — The full sequence:
    [instruction_tokens][tool_token][real_result_tokens]
is fed to the model, which generates the final natural-language
answer conditioned on the ground-truth tool output.

Args:
    prompt: Natural language user request.

Returns:
    InferenceResult with all intermediate steps populated.*
- `_template_answer` (line 818) `def _template_answer(self, tool_name, tool_arg, tool_result)` - *Build a deterministic natural-language answer from the tool result.

Used when the model Pass 2 output is too short to be useful.  Each
tool has a dedicated template that formats the raw result string into
a readable sentence.  No model weights involved — pure string
formatting.*
- `_infer_tool_and_arg` (line 844) `def _infer_tool_and_arg(self, prompt)` - *Infer the tool name and argument from the prompt text.

Returns the same (tool_name, arg) pair that _encode_prompt uses,
so both are guaranteed to be consistent.  The argument is the
full prompt text — each tool executor extracts what it needs.*
- `pretty` (line 895) `def pretty(self)` - *Render a human-readable summary of the inference run.*
- `decorator` (line 231) `def decorator(fn)`
- `get_weather` (line 305) `def get_weather(city)` - *Fetch current weather from wttr.in (no API key required).*
- `search_web` (line 323) `def search_web(query)` - *Instant-answer search via DuckDuckGo JSON API (no API key).*
- `calc_expr` (line 340) `def calc_expr(expr)` - *Evaluate a mathematical expression safely.*
- `get_datetime` (line 345) `def get_datetime(tz_hint)` - *Return the current UTC datetime (tz_hint is informational only).*
- `translate` (line 351) `def translate(text)` - *Translate text using MyMemory free API (no key, 5k chars/day limit).

Accepted formats:
  "translate <text> to <lang>"
  "<text> to <lang>"
  "<text>"  (defaults to English)

Strips the "translate" verb and detects source language via
langdetect so MyMemory receives a valid langpair (e.g. es|en).
Falls back to es|en when detection fails.*
- `get_news` (line 409) `def get_news(topic)` - *Fetch recent news headlines via DuckDuckGo news search.
Returns up to 3 snippet summaries.*
- `echo` (line 428) `def echo(text)` - *Return the input unchanged. Used for model self-testing.*

#### `toposwarm_lazyown_orchestrator.py`
**Path:** `toposwarm_lazyown_orchestrator.py`

**Classes:**
- `SessionContext` (line 170) `class SessionContext` - *Persistent session state across multiple prompts.*
- `LazyOwnBridge` (line 227) `class LazyOwnBridge` - *Thin wrapper around LazyOwn's _run_lazyown_command logic.

Calls LazyOwn non-interactively via a PTY subprocess so the terminal-size
ioctl does not crash.  Strips ANSI codes from output.

All heavy imports (pty, fcntl, termios, select, struct) are lazy so the
bridge can be imported on non-Linux systems for dataset generation.*
- `LazyOwnToolRegistry` (line 372) `class LazyOwnToolRegistry(ToolRegistry)` - *Extends TopoSwarm's ToolRegistry with all LazyOwn MCP tools.

Each tool is a thin wrapper that calls LazyOwnBridge.run() with the
appropriate LazyOwn shell command or payload manipulation.

Tools are grouped by category so keyword routing maps naturally.*
- `LazyOwnOrchestrator` (line 764) `class LazyOwnOrchestrator` - *Combines TopoSwarm router with LazyOwn tool execution.

InferenceEngine is loaded only when needed (lazy) so the orchestrator
can be used for dataset generation without a GPU.

Meta-Harness integration (2026-05):
- Filesystem experience store: every execution is logged with code,
  traces, and scores for future proposer diagnosis.
- Environment bootstrap: gathers a LazyOwn sandbox snapshot before the
  first turn to eliminate wasted exploratory commands.
- Draft-verification routing: retrieves confirmers/challengers from
  prior episodes to verify or revise the keyword router's draft.*

**Functions:**
- `_resolve_lazyown_dir` (line 56) `def _resolve_lazyown_dir()` - *Discover LazyOwn installation directory.

Priority:
  1. LAZYOWN_DIR environment variable (expanded ~).
  2. Default relative to this script: <repo>/LazyOwn.
  3. User home directory: ~/LazyOwn.
  4. Return the relative default anyway (caller will see available=False).*
- `_import_infer` (line 93) `def _import_infer()`
- `_import_agent` (line 113) `def _import_agent()`
- `_import_meta_harness` (line 128) `def _import_meta_harness()`
- `_import_routing_head` (line 147) `def _import_routing_head()`

**Methods:**
- `infer_lazyown_tool` (line 691) `def infer_lazyown_tool(prompt)` - *Map a natural-language security prompt to a (tool_name, tool_arg) pair.

Priority: explicit LazyOwn keywords → security domain keywords → fallback.
The returned tool_arg is the most useful sub-string to pass to that tool.*
- `_extract_arg` (line 716) `def _extract_arg(prompt, tool_name)` - *Extract the most useful argument string for each tool category.*
- `generate_dataset` (line 1092) `def generate_dataset(output_path, bridge)` - *Generate a rich ToolBench-format JSONL for fine-tuning the TopoSwarm router.

Uses lazyown_dataset_generator.py (80 tools × 5-10 phrasings + chain examples)
for ~420 high-quality training examples covering every LazyOwn MCP tool.
If LazyOwn is live, a random sample of tools are actually executed and their
real output replaces the placeholder in the `answer` field.

Returns the number of examples written.*
- `finetune_on_lazyown` (line 1173) `def finetune_on_lazyown(dataset_path, agent_cfg, logger)` - *Fine-tune the TopoSwarm router on the full LazyOwn tool dataset using
EWC + Experience Replay to prevent catastrophic forgetting.

Pipeline (delegated to toposwarm_continual_trainer.py):
  1. Load the 420-example lazyown_full.jsonl.
  2. Compute / load Fisher Information diagonal on any available ToolBench
     data (anchors critical weights so general routing is preserved).
  3. Build a ToolBench replay buffer (20 % of every mini-batch).
  4. Fine-tune with combined loss: L_task + λ/2 · Σ F_i(θ_i − θ*_i)²
  5. Evaluate routing accuracy on held-out LazyOwn + ToolBench samples.
  6. Print final checkpoint stats (epoch, step, task_loss, ewc_lambda).*
- `run_mcp_server` (line 1250) `def run_mcp_server(orchestrator)` - *Expose the TopoSwarm→LazyOwn orchestrator as an MCP stdio server.

Tools exposed:
  toposwarm_query   — NL prompt → routed LazyOwn tool → answer
  lazyown_*         — direct passthrough to every registered tool*
- `_setup_logger` (line 1329) `def _setup_logger(level)`
- `main` (line 1346) `def main()`
- `to_prompt_prefix` (line 181) `def to_prompt_prefix(self)` - *Compact context block injected before the user prompt.*
- `update` (line 195) `def update(self, tool_name, arg, output, ok)`
- `__init__` (line 251) `def __init__(self, lazyown_dir, default_timeout)`
- `available` (line 257) `def available(self)`
- `run` (line 265) `def run(self, command, timeout)` - *Execute a LazyOwn shell command and return cleaned output.*
- `get_config` (line 344) `def get_config(self)`
- `set_config` (line 353) `def set_config(self, key, value)`
- `__init__` (line 455) `def __init__(self, cfg, bridge)`
- `_register_lazyown_tools` (line 460) `def _register_lazyown_tools(self)` - *Register every LazyOwn MCP tool as a ToolRegistry callable.*
- `__init__` (line 780) `def __init__(self, cfg, agent_cfg, bridge, logger, load_model, meta_cfg)`
- `_load_routing_head` (line 825) `def _load_routing_head(self)` - *Load the trained RoutingHead if a checkpoint exists.*
- `_neural_route` (line 847) `def _neural_route(self, prompt)` - *Use the TopoSwarm model + RoutingHead to predict the LazyOwn tool.
Returns (tool_name, tool_arg) or None if unavailable / uncertain.*
- `run` (line 887) `def run(self, prompt)` - *Route prompt → LazyOwn tool → answer.*
- `list_tools` (line 1273) `def list_tools()`
- `call_tool` (line 1307) `def call_tool(name, arguments)`
- `_serve` (line 1317) `def _serve()`
- `run_command` (line 466) `def run_command(arg)`
- `get_config` (line 470) `def get_config(_)`
- `set_config` (line 475) `def set_config(arg)`
- `list_modules` (line 483) `def list_modules(_)`
- `get_beacons` (line 487) `def get_beacons(_)`
- `c2_command` (line 491) `def c2_command(arg)`
- `run_api` (line 495) `def run_api(arg)`
- `list_sessions` (line 499) `def list_sessions(_)`
- `read_session_file` (line 507) `def read_session_file(arg)`
- `c2_status` (line 514) `def c2_status(_)`
- `create_addon` (line 518) `def create_addon(arg)`
- `list_addons` (line 522) `def list_addons(_)`
- `list_plugins` (line 529) `def list_plugins(_)`
- `poll_events` (line 536) `def poll_events(_)`
- `ack_event` (line 540) `def ack_event(arg)`
- `add_rule` (line 544) `def add_rule(arg)`
- `list_event_rules` (line 548) `def list_event_rules(_)`
- `heartbeat_status` (line 552) `def heartbeat_status(_)`
- `session_init` (line 556) `def session_init(arg)`
- `discover_commands` (line 560) `def discover_commands(arg)`
- `phase_guide` (line 564) `def phase_guide(arg)`
- `command_help` (line 568) `def command_help(arg)`
- `add_target` (line 572) `def add_target(arg)`
- `list_targets` (line 578) `def list_targets(_)`
- `run_agent` (line 582) `def run_agent(arg)`
- `agent_status` (line 586) `def agent_status(arg)`
- `agent_result` (line 590) `def agent_result(arg)`
- `list_agents` (line 594) `def list_agents(_)`
- `set_active_target` (line 598) `def set_active_target(arg)`
- `campaign_sitrep` (line 602) `def campaign_sitrep(_)`
- `c2_notes` (line 606) `def c2_notes(arg)`
- `credentials` (line 610) `def credentials(_)`
- `report_update` (line 614) `def report_update(arg)`
- `campaign_lessons` (line 618) `def campaign_lessons(_)`
- `auto_populate` (line 622) `def auto_populate(_)`
- `session_state` (line 626) `def session_state(_)`
- `recommend_next` (line 630) `def recommend_next(_)`
- `timeline` (line 634) `def timeline(_)`
- `c2_vuln_analysis` (line 638) `def c2_vuln_analysis(arg)`
- `c2_redop` (line 642) `def c2_redop(arg)`
- `c2_search_agent` (line 646) `def c2_search_agent(arg)`
- `c2_script` (line 650) `def c2_script(arg)`
- `c2_adversary` (line 654) `def c2_adversary(arg)`
- `policy_status` (line 658) `def policy_status(_)`
- `auto_loop` (line 662) `def auto_loop(arg)`
- `create_tool` (line 666) `def create_tool(arg)`
- `llm_ask` (line 670) `def llm_ask(arg)`
- `inject_objective` (line 674) `def inject_objective(arg)`
- `next_objective` (line 678) `def next_objective(_)`
- `read_prompt` (line 682) `def read_prompt(arg)`
- `_hook` (line 863) `def _hook(module, inp, out)`

#### `toposwarm_lazyown_sweep.py`
**Path:** `toposwarm_lazyown_sweep.py`

**Functions:**
- `generate_prompts` (line 130) `def generate_prompts(n)` - *Generate N diverse pentesting prompts.*
- `setup_logger` (line 145) `def setup_logger()`
- `run_sweep` (line 155) `def run_sweep(prompts, bridge, logger)` - *Execute prompts against LazyOwn and collect results.*
- `write_results` (line 189) `def write_results(results, out_path)` - *Write results as JSONL for continual trainer.

Matches the format of lazyown_dataset_generator.py:
- instruction: the prompt
- api_list: minimal tool metadata
- answer: [TOOL_CALL: tool_name(arg)]
- domain: Security/RealSuccess or Security/RealFailure*
- `main` (line 223) `def main()`

#### `toposwarm_meta_harness.py`
**Path:** `toposwarm_meta_harness.py`

**Classes:**
- `MetaHarnessConfig` (line 60) `class MetaHarnessConfig` - *All Meta-Harness hyper-parameters in one place.*
- `MetaHarnessLogger` (line 121) `class MetaHarnessLogger` - *Append-only filesystem store for harness code, execution traces, and scores.

Each evaluated harness run gets its own directory:

    meta_harness_logs/
      run_0001_<hash>/
        harness.json   – config / code snapshot
        trace.jsonl    – step-by-step execution trace
        score.json     – metrics (success, latency, token count, ...)
        reasoning.txt  – optional proposer reasoning

The store is intentionally plain-text / JSON so a coding-agent proposer can
navigate it with standard tools (`grep`, `cat`, `ls`) without bespoke APIs.*
- `DenseMemoryRetriever` (line 322) `class DenseMemoryRetriever` - *Semantic episodic retrieval with graceful degradation.

Priority:
    1. sentence-transformers dense embeddings (best quality).
    2. sklearn TF-IDF + cosine similarity (no GPU, good quality).
    3. Return None so caller falls back to Jaccard token overlap.

The retriever is rebuildable incrementally: call `add()` for each new
episode, then `search()` for retrieval.*
- `MetaHarnessMemory` (line 430) `class MetaHarnessMemory` - *Persistent episodic memory backed by the filesystem log store.

Unlike the in-RAM EpisodicMemory in topo_swarm_agent.py, this memory:
- Survives process restarts.
- Can be queried by keyword overlap, tool name, or simple TF-IDF cosine.
- Returns raw execution traces (not compressed summaries) so a proposer can
  perform causal diagnosis.*
- `EnvironmentBootstrapper` (line 583) `class EnvironmentBootstrapper` - *Gathers a sandbox snapshot *before* the first router/tool turn and formats
it as a compact [Environment Snapshot] block.

This eliminates the 2-4 exploratory turns that the LazyOwn agent typically
spends discovering what targets, sessions, and modules are available.*
- `DraftVerifier` (line 738) `class DraftVerifier` - *Two-stage routing inspired by Meta-Harness's text-classification harness.

Stage 1 (Draft):  Produce an initial tool proposal using fast keyword
                  heuristics (same as the existing infer_lazyown_tool).

Stage 2 (Verify): Retrieve confirmers (same tool, past successes) and
                  challengers (different tool / failures) from the
                  MetaHarnessMemory, then decide whether to keep or revise
                  the draft.

This is lightweight — no LLM call — but gives the harness a structured
way to learn from prior executions without retraining model weights.*
- `ParetoFrontier` (line 837) `class ParetoFrontier` - *Maintain a population of harness configurations and their evaluation scores.

The frontier is updated after every evaluation so the orchestrator can
dynamically switch to the best harness variant for the current task context
(accuracy vs. latency vs. context-cost trade-offs).*
- `MetaHarnessOptimizer` (line 948) `class MetaHarnessOptimizer` - *Single entry-point that wires together Logger, Memory, Bootstrapper,
DraftVerifier, and ParetoFrontier.

Usage inside LazyOwnOrchestrator:

    mh = MetaHarnessOptimizer(MetaHarnessConfig())
    snapshot = mh.bootstrap.gather_snapshot(bridge)
    snapshot_text = mh.bootstrap.format_snapshot(snapshot)
    tool, arg, conf = mh.draft_verifier.route(prompt, snapshot_text)
    ... execute tool ...
    mh.log_run(harness_cfg, trace_steps, score)
    mh.memory.store(score, trace_steps)
    mh.frontier.add(harness_cfg, score)*

**Methods:**
- `_setup_logger` (line 95) `def _setup_logger(name, level)`
- `_stable_id` (line 107) `def _stable_id(text)` - *Short stable hash for naming log directories.*
- `_now_iso` (line 112) `def _now_iso()`
- `_demo` (line 1013) `def _demo()`
- `__init__` (line 138) `def __init__(self, cfg, logger)`
- `_count_existing_runs` (line 149) `def _count_existing_runs(self)`
- `_next_run_dir` (line 152) `def _next_run_dir(self, hint)`
- `_prune_old` (line 158) `def _prune_old(self)` - *Keep only the most recent MAX_LOGGED_RUNS directories.*
- `log_run` (line 176) `def log_run(self, harness_snapshot, trace_steps, score, reasoning)` - *Persist one complete harness evaluation.

Args:
    harness_snapshot: JSON-serialisable dict describing the harness
        config / code (e.g. {"orchestrator_version": "2.1", ...}).
    trace_steps: List of step dicts, each with keys like
        { "step": int, "prompt": str, "tool": str, "output": str, "t_ms": float }.
    score: Dict of metrics, e.g.
        { "success": true, "latency_ms": 120, "context_chars": 450 }.
    reasoning: Optional free-text proposer reasoning.

Returns:
    Path to the newly created run directory.*
- `list_runs` (line 229) `def list_runs(self, n)` - *Return run directories newest-first.*
- `grep_traces` (line 238) `def grep_traces(self, pattern, max_results)` - *Simple regex search across all trace.jsonl files.
Returns list of (run_dir, line_no, matched_line).*
- `get_scores` (line 257) `def get_scores(self)` - *Load every score.json into a list.*
- `get_pareto_runs` (line 269) `def get_pareto_runs(self, metrics)` - *Return run directories that are on the Pareto frontier.

By default maximises success_rate and minimises latency_ms + context_chars.*
- `__init__` (line 335) `def __init__(self, logger)`
- `add` (line 362) `def add(self, text, episode)`
- `_rebuild_tfidf` (line 368) `def _rebuild_tfidf(self)`
- `bulk_index` (line 376) `def bulk_index(self, texts, episodes)`
- `search` (line 392) `def search(self, query, top_k)`
- `_search_st` (line 401) `def _search_st(self, query, top_k)`
- `_search_tfidf` (line 412) `def _search_tfidf(self, query, top_k)`
- `__init__` (line 441) `def __init__(self, logger, capacity, dense)`
- `_build_index` (line 453) `def _build_index(self)`
- `_load_episode` (line 464) `def _load_episode(self, run_dir)`
- `_episode_text` (line 482) `def _episode_text(score, traces)`
- `store` (line 493) `def store(self, score, traces)` - *Index a newly logged episode.*
- `retrieve_similar` (line 505) `def retrieve_similar(self, prompt, tool_hint, top_k, min_score)` - *Retrieve the top-k most similar prior episodes.

Uses dense semantic retrieval when available (sentence-transformers or
sklearn TF-IDF), then falls back to token-overlap Jaccard for anything
not covered by the dense index.  Results are fused by max-of-scores.*
- `retrieve_confirmers_and_challengers` (line 549) `def retrieve_confirmers_and_challengers(self, draft_tool, prompt, top_k)` - *Split retrieved episodes into confirmers (same tool, success) and
challengers (different tool or failure).*
- `_tokenise` (line 573) `def _tokenise(text)` - *Very simple whitespace + punctuation tokeniser.*
- `__init__` (line 592) `def __init__(self, cfg, logger)`
- `gather_snapshot` (line 596) `def gather_snapshot(self, bridge)` - *Collect environment state via the LazyOwnBridge.

Returns a dict with keys:
    working_dir, lazyown_dir, config, targets, sessions,
    modules_available, beacons, languages, memory_estimate.*
- `_parse_list` (line 680) `def _parse_list(raw)` - *Best-effort parse of newline / comma list output.*
- `format_snapshot` (line 687) `def format_snapshot(self, snapshot, max_chars)` - *Render the snapshot as a compact [Environment Snapshot] block suitable
for injection into a prompt.*
- `__init__` (line 754) `def __init__(self, cfg, memory, keyword_router, logger)`
- `route` (line 766) `def route(self, prompt, snapshot_text)` - *Draft-verify routing.

Returns:
    Tuple of (tool_name, tool_arg, confidence).*
- `_reextract_arg` (line 820) `def _reextract_arg(prompt, tool_name, fallback)` - *Best-effort arg re-extraction when the tool changes.*
- `__init__` (line 846) `def __init__(self, cfg, logger)`
- `add` (line 855) `def add(self, config, metrics)` - *Add a candidate to the population and return True if it lies on the
current Pareto frontier.*
- `select_best` (line 875) `def select_best(self, preference)` - *Select the best harness config according to a scalarised preference.

preference maps metric name → weight (positive = maximise, negative = minimise).
Default: maximise success_rate, minimise latency_ms and context_chars.*
- `frontier_configs` (line 907) `def frontier_configs(self)` - *Return all configs currently on the Pareto frontier.*
- `_is_on_frontier` (line 911) `def _is_on_frontier(self, candidate)`
- `_prune` (line 933) `def _prune(self)` - *Remove oldest non-frontier entries when population grows too large.*
- `__init__` (line 965) `def __init__(self, cfg)`
- `set_router` (line 980) `def set_router(self, keyword_router)` - *Bind the draft verifier to the existing keyword router.*
- `log_run` (line 986) `def log_run(self, harness_snapshot, trace_steps, score, reasoning)` - *Persist one run and update in-memory indexes.*
- `get_best_harness_config` (line 999) `def get_best_harness_config(self)` - *Return the current Pareto-best harness configuration.*
- `query_experience` (line 1003) `def query_experience(self, prompt, tool_hint, top_k)` - *Ad-hoc retrieval of prior episodes for prompt engineering.*

#### `ts_utils.py`
**Path:** `ts_utils.py`

**Functions:**
- `setup_logger` (line 25) `def setup_logger(name, level)` - *Return an idempotent logger with a single StreamHandler.*
- `safe_eval` (line 42) `def safe_eval(expr)` - *Evaluate a numeric expression via AST — never calls eval() on arbitrary code.*
- `import_module` (line 62) `def import_module(name)` - *Load a Python file as a named module.

Tries each candidate path in order; raises FileNotFoundError if none found.
Pre-registers the module in sys.modules before exec so that @dataclass
introspection works correctly on Python 3.13+.*
- `make_cached_encode` (line 86) `def make_cached_encode(tokenizer)` - *Return a cached version of tokenizer.encode().

@lru_cache requires hashable args; str instructions are fine.
Cache survives the lifetime of the tokenizer object.*
- `make_cached_tool_token` (line 100) `def make_cached_tool_token(tokenizer)` - *Return a cached version of tokenizer.tool_token().*
- `_cached_encode` (line 94) `def _cached_encode(text)`
- `_cached_tool_token` (line 103) `def _cached_tool_token(tool_name)`
