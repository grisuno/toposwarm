# orphans

*Community 3 | 11 files | cohesion 0.00*

## Definition

This community groups 11 file(s) rooted at `root` with dominant language py (cohesion 0.00). Central symbols: `AudioEncoder`, `BPETokenizer`, `CausalReasoningEngine`, `CheckpointManager`, `CorpusCallosumTrimodal`, `CorpusDownloader`, `DatasetEnhancer`, `EnhancedDiagnosticsTricameral`. Core file: `topogpt2_1.py` (126 symbols). Documented purpose: Convert existing sweep data to correct training format..

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `fix_sweep_format.py` | py | utility | 0 | yes |
| `lazyown_bridge.py` | py | utility | 46 | yes |
| `lazyown_dataset_enhancer.py` | py | data_access | 21 | yes |
| `lazyown_dataset_generator.py` | py | data_access | 8 | yes |
| `neurologos_tricameral_loss2.7.py` | py | utility | 100 | yes |
| `test_full_pipeline.py` | py | testing | 8 | yes |
| `tests/test_dataset_enhancer.py` | py | testing | 6 | yes |
| `tests/test_dataset_generator.py` | py | testing | 5 | yes |
| `tests/test_model_config.py` | py | testing | 3 | yes |
| `topogpt2_1.py` | py | utility | 126 | yes |
| `toposwarm_hybrid.py` | py | utility | 48 | yes |

## Key Symbols

- `_EnvKey` (class, `lazyown_bridge.py:41`) `class _EnvKey(str, Enum)` - Environment variable names used for configuration.
- `_FileName` (class, `lazyown_bridge.py:47`) `class _FileName(str, Enum)` - File names expected inside the LazyOwn directory.
- `_Defaults` (class, `lazyown_bridge.py:56`) `class _Defaults` - Default operational parameters.
- `ExecutionResult` (class, `lazyown_bridge.py:74`) `class ExecutionResult` - Immutable result of a LazyOwn command execution.
- `LazyOwnPathResolver` (class, `lazyown_bridge.py:90`) `class LazyOwnPathResolver` - Discovers the LazyOwn installation directory without hard-coded paths.
- `__init__` (method, `lazyown_bridge.py:104`) `def __init__(self)`
- `resolve` (method, `lazyown_bridge.py:107`) `def resolve(self)` - Return the discovered LazyOwn directory.
- `_from_env` (method, `lazyown_bridge.py:133`) `def _from_env(self)`
- `_from_repo_sibling` (method, `lazyown_bridge.py:140`) `def _from_repo_sibling(self)`
- `_from_home` (method, `lazyown_bridge.py:148`) `def _from_home(self)`
- `_from_cwd` (method, `lazyown_bridge.py:152`) `def _from_cwd(self)`
- `LazyOwnPayloadManager` (class, `lazyown_bridge.py:162`) `class LazyOwnPayloadManager` - Reads and writes LazyOwn configuration via payload.json.
- `__init__` (method, `lazyown_bridge.py:171`) `def __init__(self, lazyown_dir)`
- `payload_path` (method, `lazyown_bridge.py:176`) `def payload_path(self)`
- `read` (method, `lazyown_bridge.py:179`) `def read(self)` - Return the current payload.json as a dictionary.
- `write` (method, `lazyown_bridge.py:189`) `def write(self, data)` - Atomically overwrite payload.json with the provided dictionary.
- `get` (method, `lazyown_bridge.py:198`) `def get(self, key, default)` - Read a single key from payload.json.
- `set` (method, `lazyown_bridge.py:202`) `def set(self, key, value)` - Update a single key in payload.json without overwriting other keys.
- `update` (method, `lazyown_bridge.py:208`) `def update(self, mapping)` - Merge a dictionary into payload.json.
- `LazyOwnCommandBuilder` (class, `lazyown_bridge.py:220`) `class LazyOwnCommandBuilder` - Builds safe, validated command sequences for LazyOwn execution.
- `__init__` (method, `lazyown_bridge.py:237`) `def __init__(self, lazyown_dir)`
- `build_argv` (method, `lazyown_bridge.py:242`) `def build_argv(self, command)` - Return the subprocess argv and the stdin payload.
- `_validate_command` (method, `lazyown_bridge.py:276`) `def _validate_command(command)` - Sanitize a command string to prevent injection.
- `LazyOwnProcessExecutor` (class, `lazyown_bridge.py:294`) `class LazyOwnProcessExecutor` - Executes LazyOwn commands as subprocesses with timeout and cleanup.
- `__init__` (method, `lazyown_bridge.py:331`) `def __init__(self, lazyown_dir)`
- `execute` (method, `lazyown_bridge.py:343`) `def execute(self, argv, stdin_payload, timeout)` - Run a command and return (raw_stdout, returncode, latency_ms).
- `_resolve_timeout` (method, `lazyown_bridge.py:375`) `def _resolve_timeout(self, argv, override)`
- `_execute_with_pty` (method, `lazyown_bridge.py:387`) `def _execute_with_pty(self, argv, stdin_payload, timeout, env)`
- `_drain_pty` (method, `lazyown_bridge.py:451`) `def _drain_pty(self, master_fd, chunks)`
- `_execute_with_pipe` (method, `lazyown_bridge.py:464`) `def _execute_with_pipe(self, argv, stdin_payload, timeout, env)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 0
- Cross-boundary resolved imports (EXTRACTED): 0

## Connections

- [INFERRED] shares_context community 0 <-> 3 (strength 0.5): Inferred shared context (language py and layer utility) with no import path between community 0 (root: topo_swarm_agent) and community 3 (orphans).
- [INFERRED] shares_context community 1 <-> 3 (strength 0.5): Inferred shared context (language py and layer utility) with no import path between community 1 (root: toposwarm_meta_harness) and community 3 (orphans).
- [INFERRED] shares_context community 2 <-> 3 (strength 0.5): Inferred shared context (language py and layer utility) with no import path between community 2 (root: toposwarm_lazyown_orchestrator) and community 3 (orphans).

## Risks

- [taint high] `lazyown_bridge.py` -> `lazyown_bridge.py` via `subprocess` (0 hops)
- [taint high] `neurologos_tricameral_loss2.7.py` -> `neurologos_tricameral_loss2.7.py` via `subprocess` (0 hops)
- [taint medium] `neurologos_tricameral_loss2.7.py` -> `neurologos_tricameral_loss2.7.py` via `urllib.request` (0 hops)
- [taint medium] `neurologos_tricameral_loss2.7.py` -> `neurologos_tricameral_loss2.7.py` via `urllib.request` (0 hops)
- [taint medium] `neurologos_tricameral_loss2.7.py` -> `neurologos_tricameral_loss2.7.py` via `urllib.request` (0 hops)
- [taint high] `test_full_pipeline.py` -> `test_full_pipeline.py` via `subprocess` (0 hops)
- [taint medium] `toposwarm_hybrid.py` -> `toposwarm_hybrid.py` via `urllib.request` (0 hops)
- [dataflow UNCHECKED_ALLOC] `neurologos_tricameral_loss2.7.py:2308` `__getitem__` `image`: Result of allocator stored in `image` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `test_full_pipeline.py:79` `step1_regenerate_dataset` `lines`: Result of allocator stored in `lines` is never checked against NULL.

## Open Questions

- Is the dangerous import `subprocess` in `lazyown_bridge.py` still required, or can it be isolated?
- What would break if the most connected file in orphans changed?
- Should orphans be split, given cohesion 0.00?

## Sources

- `fix_sweep_format.py`
- `lazyown_bridge.py`
- `lazyown_dataset_enhancer.py`
- `lazyown_dataset_generator.py`
- `neurologos_tricameral_loss2.7.py`
- `test_full_pipeline.py`
- `tests/test_dataset_enhancer.py`
- `tests/test_dataset_generator.py`
- `tests/test_model_config.py`
- `topogpt2_1.py`
- `toposwarm_hybrid.py`
