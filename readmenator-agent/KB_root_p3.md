# Subsystem: root (page 3 of 3)
Previous: [KB_root_p2.md](KB_root_p2.md)

## ts_utils.py
- Doc: — Shared utilities for the TopoSwarm project.
- Layer: utility
- Language: py
- Symbols:
  - `setup_logger` (function, line 25) `def setup_logger(name, level)`
  - `safe_eval` (function, line 42) `def safe_eval(expr)`
  - `import_module` (function, line 62) `def import_module(name)`
  - `make_cached_encode` (function, line 86) `def make_cached_encode(tokenizer)`
  - `make_cached_tool_token` (function, line 100) `def make_cached_tool_token(tokenizer)`
  - `_cached_encode` (function, line 94) `def _cached_encode(text)`
  - `_cached_tool_token` (function, line 103) `def _cached_tool_token(tool_name)`
- Imported by: `debug_routing.py`, `diagnose_accuracy.py`, `topo_swarm_agent.py`, `toposwarm_continual_trainer.py`

