# API

## lazyown_dataset_enhancer.py

### _difficulty `def _difficulty(record)`
- Defined: `lazyown_dataset_enhancer.py:64`
- Doc: Lower = easier.  Factors:

### _sanitize_output `def _sanitize_output(text)`
- Defined: `lazyown_dataset_enhancer.py:136`
- Doc: Redact potential PII / sensitive data from LazyOwn output traces.

### _build_toolbench_record `def _build_toolbench_record(instruction, tool_name, arg, answer, domain)`
- Defined: `lazyown_dataset_enhancer.py:149`
- Doc: Standard ToolBench-format record.

### print_stats `def print_stats(records)`
- Defined: `lazyown_dataset_enhancer.py:348`

### main `def main()`
- Defined: `lazyown_dataset_enhancer.py:375`

### __init__ `def __init__(self, log_dir)`
- Defined: `lazyown_dataset_enhancer.py:88`

### list_runs `def list_runs(self)`
- Defined: `lazyown_dataset_enhancer.py:91`

### read_trace `def read_trace(self, run_dir)`
- Defined: `lazyown_dataset_enhancer.py:98`

### read_score `def read_score(self, run_dir)`
- Defined: `lazyown_dataset_enhancer.py:113`

### read_harness `def read_harness(self, run_dir)`
- Defined: `lazyown_dataset_enhancer.py:122`

### __init__ `def __init__(self, log_dir, max_runs)`
- Defined: `lazyown_dataset_enhancer.py:166`

### enhance `def enhance(self)`
- Defined: `lazyown_dataset_enhancer.py:171`

### add_negative_examples `def add_negative_examples(self, records, n)`
- Defined: `lazyown_dataset_enhancer.py:236`
- Doc: Add examples where the prompt is ambiguous and the model must NOT

### curriculum_sort `def curriculum_sort(self, records)`
- Defined: `lazyown_dataset_enhancer.py:261`
- Doc: Sort by difficulty (easy → hard).

### deduplicate `def deduplicate(self, records)`
- Defined: `lazyown_dataset_enhancer.py:265`
- Doc: Deduplicate by instruction text only (same prompt can have different outputs).

### augment_simple `def augment_simple(self, records, multiplier)`
- Defined: `lazyown_dataset_enhancer.py:276`
- Doc: Lightweight augmentation: replace IP addresses, hostnames, and common

### run `def run(self, merge_with)`
- Defined: `lazyown_dataset_enhancer.py:301`

## lazyown_dataset_generator.py

### _make_record `def _make_record(tool_name, desc, category, instruction, arg)`
- Defined: `lazyown_dataset_generator.py:3321`

### _apply_pentest_synonyms `def _apply_pentest_synonyms(instr)`
- Defined: `lazyown_dataset_generator.py:3414`
- Doc: Replace common pentest terms with synonyms to increase diversity.

### _expand `def _expand(tool_name, phrasings)`
- Defined: `lazyown_dataset_generator.py:3430`
- Doc: Generate additional phrasings via IP substitution, prefix injection, verb swap, and synonym replacement.

### _is_noisy_phrasing `def _is_noisy_phrasing(instruction, arg)`
- Defined: `lazyown_dataset_generator.py:3554`
- Doc: Return True if the phrasing is too generic and likely to dilute training.

### build_dataset `def build_dataset()`
- Defined: `lazyown_dataset_generator.py:3571`

### write_jsonl `def write_jsonl(records, path)`
- Defined: `lazyown_dataset_generator.py:3595`

### print_stats `def print_stats(records)`
- Defined: `lazyown_dataset_generator.py:3602`

### main `def main()`
- Defined: `lazyown_dataset_generator.py:3616`

## meta_harness_proposer.py

### _setup_logger `def _setup_logger(name, level)`
- Defined: `meta_harness_proposer.py:58`
- Depends on: `toposwarm_meta_harness.py`

### main `def main()`
- Defined: `meta_harness_proposer.py:572`
- Depends on: `toposwarm_meta_harness.py`

### __init__ `def __init__(self, cfg, logger)`
- Defined: `meta_harness_proposer.py:93`
- Depends on: `toposwarm_meta_harness.py`

### _try_chat `def _try_chat(self, api_url, model, system, user)`
- Defined: `meta_harness_proposer.py:97`
- Depends on: `toposwarm_meta_harness.py`

### chat `def chat(self, system, user)`
- Defined: `meta_harness_proposer.py:121`
- Doc: Send a chat request and return the assistant message content.
- Depends on: `toposwarm_meta_harness.py`

### __init__ `def __init__(self, log_dir, logger)`
- Defined: `meta_harness_proposer.py:153`
- Depends on: `toposwarm_meta_harness.py`

### list_runs `def list_runs(self, n)`
- Defined: `meta_harness_proposer.py:157`
- Depends on: `toposwarm_meta_harness.py`

### load_run `def load_run(self, run_dir)`
- Defined: `meta_harness_proposer.py:165`
- Depends on: `toposwarm_meta_harness.py`

### build_diagnostic_context `def build_diagnostic_context(self, top_k)`
- Defined: `meta_harness_proposer.py:193`
- Doc: Build a rich diagnostic string containing:
- Depends on: `toposwarm_meta_harness.py`

### __init__ `def __init__(self, logger)`
- Defined: `meta_harness_proposer.py:246`
- Depends on: `toposwarm_meta_harness.py`

### validate_syntax `def validate_syntax(self, code)`
- Defined: `meta_harness_proposer.py:249`
- Doc: Return (ok, error_message).
- Depends on: `toposwarm_meta_harness.py`

### apply_full_rewrite `def apply_full_rewrite(self, target_path, new_code, dry_run)`
- Defined: `meta_harness_proposer.py:265`
- Doc: Validate and optionally write a full file rewrite.
- Depends on: `toposwarm_meta_harness.py`

### _strip_line_numbers `def _strip_line_numbers(self, s)`
- Defined: `meta_harness_proposer.py:283`
- Doc: Remove leading ' 123: ' line numbers that the LLM may copy.
- Depends on: `toposwarm_meta_harness.py`

### apply_line_range `def apply_line_range(self, target_path, line_start, line_end, new_string, dry_run)`
- Defined: `meta_harness_proposer.py:287`
- Doc: Replace a range of lines (1-indexed) with new text.
- Depends on: `toposwarm_meta_harness.py`

### apply_diff_hunk `def apply_diff_hunk(self, target_path, old_string, new_string, dry_run)`
- Defined: `meta_harness_proposer.py:316`
- Doc: Apply a targeted string replacement after validation.
- Depends on: `toposwarm_meta_harness.py`

### __init__ `def __init__(self, log_dir, llm_cfg, logger)`
- Defined: `meta_harness_proposer.py:434`
- Depends on: `toposwarm_meta_harness.py`

### propose_patch `def propose_patch(self, target_path, top_k, dry_run)`
- Defined: `meta_harness_proposer.py:445`
- Doc: End-to-end propose-and-apply cycle.
- Depends on: `toposwarm_meta_harness.py`

### _log_proposal `def _log_proposal(self, target_path, response, applied, diag)`
- Defined: `meta_harness_proposer.py:538`
- Doc: Store the proposer's reasoning so future loops can evaluate it.
- Depends on: `toposwarm_meta_harness.py`

### _norm `def _norm(s)`
- Defined: `meta_harness_proposer.py:331`
- Depends on: `toposwarm_meta_harness.py`

## tests/test_dataset_enhancer.py

### _load_enhancer_module `def _load_enhancer_module()`
- Defined: `tests/test_dataset_enhancer.py:13`

### test_sanitize_ip `def test_sanitize_ip()`
- Defined: `tests/test_dataset_enhancer.py:24`

### test_sanitize_password `def test_sanitize_password()`
- Defined: `tests/test_dataset_enhancer.py:31`

### test_sanitize_ntlm_hash `def test_sanitize_ntlm_hash()`
- Defined: `tests/test_dataset_enhancer.py:38`

### test_sanitize_email `def test_sanitize_email()`
- Defined: `tests/test_dataset_enhancer.py:44`

### test_sanitize_idempotent_on_clean_text `def test_sanitize_idempotent_on_clean_text()`
- Defined: `tests/test_dataset_enhancer.py:50`

## tests/test_dataset_generator.py

### _load_gen_module `def _load_gen_module()`
- Defined: `tests/test_dataset_generator.py:13`

### test_is_noisy_short_instruction `def test_is_noisy_short_instruction()`
- Defined: `tests/test_dataset_generator.py:24`

### test_is_noisy_generic_verb_empty_arg `def test_is_noisy_generic_verb_empty_arg()`
- Defined: `tests/test_dataset_generator.py:30`

### test_is_noisy_permitted_with_arg `def test_is_noisy_permitted_with_arg()`
- Defined: `tests/test_dataset_generator.py:36`

### test_build_dataset_filters_noise `def test_build_dataset_filters_noise()`
- Defined: `tests/test_dataset_generator.py:42`

## tests/test_model_config.py

### test_d_model_compatible_with_checkpoint `def test_d_model_compatible_with_checkpoint()`
- Defined: `tests/test_model_config.py:11`

## tests/test_orchestrator.py

### _load_ctx `def _load_ctx(self)`
- Defined: `tests/test_orchestrator.py:18`
- Depends on: `toposwarm_lazyown_orchestrator.py`

### test_empty_prefix `def test_empty_prefix(self)`
- Defined: `tests/test_orchestrator.py:23`
- Depends on: `toposwarm_lazyown_orchestrator.py`

### test_prefix_with_target `def test_prefix_with_target(self)`
- Defined: `tests/test_orchestrator.py:28`
- Depends on: `toposwarm_lazyown_orchestrator.py`

### test_update_extracts_ip `def test_update_extracts_ip(self)`
- Defined: `tests/test_orchestrator.py:35`
- Depends on: `toposwarm_lazyown_orchestrator.py`

### test_phase_progression `def test_phase_progression(self)`
- Defined: `tests/test_orchestrator.py:43`
- Depends on: `toposwarm_lazyown_orchestrator.py`

### test_findings_from_output `def test_findings_from_output(self)`
- Defined: `tests/test_orchestrator.py:49`
- Depends on: `toposwarm_lazyown_orchestrator.py`

### _load_router `def _load_router(self)`
- Defined: `tests/test_orchestrator.py:59`
- Depends on: `toposwarm_lazyown_orchestrator.py`

### test_recon_keyword `def test_recon_keyword(self)`
- Defined: `tests/test_orchestrator.py:63`
- Depends on: `toposwarm_lazyown_orchestrator.py`

### test_config_keyword `def test_config_keyword(self)`
- Defined: `tests/test_orchestrator.py:69`
- Depends on: `toposwarm_lazyown_orchestrator.py`

### test_c2_keyword `def test_c2_keyword(self)`
- Defined: `tests/test_orchestrator.py:74`
- Depends on: `toposwarm_lazyown_orchestrator.py`

### test_fallback_search `def test_fallback_search(self)`
- Defined: `tests/test_orchestrator.py:79`
- Depends on: `toposwarm_lazyown_orchestrator.py`

### test_extract_arg_ip `def test_extract_arg_ip(self)`
- Defined: `tests/test_orchestrator.py:84`
- Depends on: `toposwarm_lazyown_orchestrator.py`

### orchestrator `def orchestrator(self)`
- Defined: `tests/test_orchestrator.py:93`
- Depends on: `toposwarm_lazyown_orchestrator.py`

### test_neural_route_none_when_no_engine `def test_neural_route_none_when_no_engine(self, orchestrator)`
- Defined: `tests/test_orchestrator.py:120`
- Depends on: `toposwarm_lazyown_orchestrator.py`

### test_neural_route_with_mock_head `def test_neural_route_with_mock_head(self, orchestrator)`
- Defined: `tests/test_orchestrator.py:123`
- Depends on: `toposwarm_lazyown_orchestrator.py`

### test_neural_route_low_confidence_fallback `def test_neural_route_low_confidence_fallback(self, orchestrator)`
- Defined: `tests/test_orchestrator.py:159`
- Depends on: `toposwarm_lazyown_orchestrator.py`

### test_run_updates_session `def test_run_updates_session(self)`
- Defined: `tests/test_orchestrator.py:196`
- Depends on: `toposwarm_lazyown_orchestrator.py`

### mock_register_forward_hook `def mock_register_forward_hook(cb)`
- Defined: `tests/test_orchestrator.py:135`
- Depends on: `toposwarm_lazyown_orchestrator.py`

### mock_model_forward `def mock_model_forward(ids)`
- Defined: `tests/test_orchestrator.py:141`
- Depends on: `toposwarm_lazyown_orchestrator.py`

### mock_register_forward_hook `def mock_register_forward_hook(cb)`
- Defined: `tests/test_orchestrator.py:169`
- Depends on: `toposwarm_lazyown_orchestrator.py`

### mock_model_forward `def mock_model_forward(ids)`
- Defined: `tests/test_orchestrator.py:175`
- Depends on: `toposwarm_lazyown_orchestrator.py`

## topo_swarm_agent.py

### _setup_logger `def _setup_logger(name, level)`
- Defined: `topo_swarm_agent.py:225`
- Doc: Return an idempotent logger. Delegates to ts_utils.setup_logger.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _set_seed `def _set_seed(seed, device)`
- Defined: `topo_swarm_agent.py:243`
- Doc: Deterministic seed across torch, numpy, and CUDA.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _param_count `def _param_count(module)`
- Defined: `topo_swarm_agent.py:253`
- Doc: Return total and trainable parameter counts.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _get_torus_positions `def _get_torus_positions(n_angular, n_radial, device)`
- Defined: `topo_swarm_agent.py:264`
- Doc: Cached angular / radial position linspaces for soft torus assignment.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### inject_moe_adapter `def inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)`
- Defined: `topo_swarm_agent.py:749`
- Doc: Inject a SwarmMoEAdapter into an already-loaded TopoSwarmModel.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _chunked_ce `def _chunked_ce(logits, targets, chunk_size)`
- Defined: `topo_swarm_agent.py:1445`
- Doc: Cross-entropy over the sequence without materialising the full [N, V] matrix.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### build_dataloaders `def build_dataloaders(cfg, tokenizer, logger)`
- Defined: `topo_swarm_agent.py:2509`
- Doc: Build train and validation DataLoaders from the ToolBench dataset.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### main `def main()`
- Defined: `topo_swarm_agent.py:2552`
- Doc: CLI entry point.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __post_init__ `def __post_init__(self)`
- Defined: `topo_swarm_agent.py:202`
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### hamilton_product `def hamilton_product(q1, q2)`
- Defined: `topo_swarm_agent.py:289`
- Doc: Hamilton (cross) product q1 ⊗ q2 for tensors of shape [..., 4].
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### normalize `def normalize(q, eps)`
- Defined: `topo_swarm_agent.py:304`
- Doc: Unit-normalise quaternion tensors.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### berry_phase_rotation `def berry_phase_rotation(q, phase)`
- Defined: `topo_swarm_agent.py:309`
- Doc: Apply a Berry-phase rotation around the w-axis of the quaternion manifold.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __init__ `def __init__(self, in_features, out_features, bias, init_std)`
- Defined: `topo_swarm_agent.py:341`
- Doc: Initialise quaternion weight matrices.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### forward `def forward(self, x)`
- Defined: `topo_swarm_agent.py:370`
- Doc: Fused Hamilton product via a single batched einsum.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __init__ `def __init__(self, cfg)`
- Defined: `topo_swarm_agent.py:406`
- Doc: Build encoder/decoder spectral kernels and quaternion projections.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _filter `def _filter(self, x, kr, ki)`
- Defined: `topo_swarm_agent.py:428`
- Doc: Apply a learned complex spectral filter in the rfft domain.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### forward `def forward(self, x)`
- Defined: `topo_swarm_agent.py:436`
- Doc: Encode x through the spectral bottleneck.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __init__ `def __init__(self, d_model, eps)`
- Defined: `topo_swarm_agent.py:468`
- Doc: Args:
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### forward `def forward(self, x)`
- Defined: `topo_swarm_agent.py:478`
- Doc: Normalise by the RMS of x and rescale by learned weight.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __init__ `def __init__(self, d_head, max_seq_len, base, ntk_factor)`
- Defined: `topo_swarm_agent.py:497`
- Doc: Args:
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _build_cache `def _build_cache(self, seq_len)`
- Defined: `topo_swarm_agent.py:522`
- Doc: Pre-compute cos/sin tables up to seq_len.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _rotate_half `def _rotate_half(self, x)`
- Defined: `topo_swarm_agent.py:530`
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### forward `def forward(self, x, seq_len)`
- Defined: `topo_swarm_agent.py:534`
- Doc: Apply rotary embedding to query or key tensor [B, H, S, d_head].
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __init__ `def __init__(self, d_model, hidden_dim, dropout)`
- Defined: `topo_swarm_agent.py:551`
- Doc: Args:
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### forward `def forward(self, x)`
- Defined: `topo_swarm_agent.py:566`
- Doc: Gated SiLU activation with residual dropout.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __init__ `def __init__(self, d_model, n_experts, top_k)`
- Defined: `topo_swarm_agent.py:590`
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### forward `def forward(self, x)`
- Defined: `topo_swarm_agent.py:597`
- Doc: x: [..., D] → (topk_idx [... K], topk_weight [..., K])
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __init__ `def __init__(self, d_model, expert_hidden_dim, n_experts, top_k, dropout)`
- Defined: `topo_swarm_agent.py:620`
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### forward `def forward(self, x)`
- Defined: `topo_swarm_agent.py:637`
- Doc: x: [B, S, D] → [B, S, D]  (autograd-safe, no in-place scatter)
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __init__ `def __init__(self, d_model, n_experts, top_k, bottleneck, dropout)`
- Defined: `topo_swarm_agent.py:679`
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### forward `def forward(self, x)`
- Defined: `topo_swarm_agent.py:705`
- Doc: x: [B, S, D] → [B, S, D]  (residual)
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### save `def save(self, path)`
- Defined: `topo_swarm_agent.py:727`
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### load `def load(cls, path)`
- Defined: `topo_swarm_agent.py:738`
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __init__ `def __init__(self, cfg)`
- Defined: `topo_swarm_agent.py:825`
- Doc: Args:
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _build_torus_graph `def _build_torus_graph(self)`
- Defined: `topo_swarm_agent.py:855`
- Doc: Construct the adjacency structure of the discrete torus.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _torus_soft_assign `def _torus_soft_assign(self, phi1, phi2)`
- Defined: `topo_swarm_agent.py:887`
- Doc: Soft assignment of token coordinates to torus nodes via haversine distance.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _message_passing `def _message_passing(self, node_feat)`
- Defined: `topo_swarm_agent.py:909`
- Doc: One round of quaternion message-passing on the torus graph.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### forward `def forward(self, x, berry_phase)`
- Defined: `topo_swarm_agent.py:940`
- Doc: Full torus forward with optional Berry-phase offset for swarm slots.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __init__ `def __init__(self, cfg)`
- Defined: `topo_swarm_agent.py:1006`
- Doc: Args:
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _head_filter `def _head_filter(self, x)`
- Defined: `topo_swarm_agent.py:1039`
- Doc: Apply the shared per-head spectral filter [B, H, S, d_head].
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### forward `def forward(self, x, is_causal)`
- Defined: `topo_swarm_agent.py:1045`
- Doc: GQA forward pass with RoPE and optional gradient checkpointing.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __init__ `def __init__(self, cfg)`
- Defined: `topo_swarm_agent.py:1119`
- Doc: Args:
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _l_step `def _l_step(self, x, state)`
- Defined: `topo_swarm_agent.py:1156`
- Doc: One GRU-gated L-module step.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _h_step `def _h_step(self, z)`
- Defined: `topo_swarm_agent.py:1163`
- Doc: One H-module strategy update.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### forward `def forward(self, x)`
- Defined: `topo_swarm_agent.py:1167`
- Doc: Run the HRM hierarchy and return the updated state with ACT signal.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __init__ `def __init__(self, cfg)`
- Defined: `topo_swarm_agent.py:1213`
- Doc: Args:
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _attn_fn `def _attn_fn(self, x)`
- Defined: `topo_swarm_agent.py:1237`
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### forward `def forward(self, x, berry_phase)`
- Defined: `topo_swarm_agent.py:1240`
- Doc: Pre-norm layer forward.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __init__ `def __init__(self, cfg)`
- Defined: `topo_swarm_agent.py:1287`
- Doc: Args:
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### forward `def forward(self, input_ids, berry_phase, targets)`
- Defined: `topo_swarm_agent.py:1311`
- Doc: Full forward pass for one agent slot.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### generate `def generate(self, input_ids, max_new_tokens, temperature, top_k, berry_phase, act_halt_threshold)`
- Defined: `topo_swarm_agent.py:1392`
- Doc: Autoregressive generation with ACT-driven early stopping.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __init__ `def __init__(self, cfg)`
- Defined: `topo_swarm_agent.py:1497`
- Doc: Args:
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### compute_surprise `def compute_surprise(logits, targets, gate_mean)`
- Defined: `topo_swarm_agent.py:1512`
- Doc: Surprise = cross-entropy × (1 - gate_mean), clipped to [0, 10].
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### store `def store(self, episode, surprise)`
- Defined: `topo_swarm_agent.py:1537`
- Doc: Store an episode in the appropriate memory tier.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### sample `def sample(self, n)`
- Defined: `topo_swarm_agent.py:1558`
- Doc: Sample n episodes with priority proportional to surprise / importance.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _decay `def _decay(self)`
- Defined: `topo_swarm_agent.py:1591`
- Doc: Apply exponential forgetting to the long-term memory scores.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __init__ `def __init__(self, model, cfg)`
- Defined: `topo_swarm_agent.py:1622`
- Doc: Args:
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### infer `def infer(self, input_ids, tokenizer, max_new_tokens, temperature, top_k)`
- Defined: `topo_swarm_agent.py:1640`
- Doc: Run swarm inference and return the decoded output string.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __init__ `def __init__(self, cfg)`
- Defined: `topo_swarm_agent.py:1701`
- Doc: Args:
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### encode `def encode(self, text)`
- Defined: `topo_swarm_agent.py:1739`
- Doc: Encode text to BPE token ids, clamped to the BPE vocab ceiling.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### decode `def decode(self, ids)`
- Defined: `topo_swarm_agent.py:1751`
- Doc: Decode token ids to text, silently dropping tool tokens.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### tool_token `def tool_token(self, tool_name)`
- Defined: `topo_swarm_agent.py:1756`
- Doc: Return a stable integer token id for a named tool.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### encode_tool_trace `def encode_tool_trace(self, instruction, tool_name, result)`
- Defined: `topo_swarm_agent.py:1778`
- Doc: Encode a ToolBench-style (instruction, tool, result) triple.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __init__ `def __init__(self, cfg, tokenizer, split, logger)`
- Defined: `topo_swarm_agent.py:1824`
- Doc: Args:
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _load `def _load(self, split)`
- Defined: `topo_swarm_agent.py:1846`
- Doc: Load and tokenise tool traces with three-level fallback.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _encode_record `def _encode_record(self, rec)`
- Defined: `topo_swarm_agent.py:1927`
- Doc: Encode a tool-trace record to token ids.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _synthetic_stubs `def _synthetic_stubs(self, n)`
- Defined: `topo_swarm_agent.py:1984`
- Doc: Generate n synthetic tool-trace stubs safe for dry-run training.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __len__ `def __len__(self)`
- Defined: `topo_swarm_agent.py:2017`
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __getitem__ `def __getitem__(self, idx)`
- Defined: `topo_swarm_agent.py:2020`
- Doc: Return a (input_ids, target_ids) pair of length MAX_SEQ_LEN.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __init__ `def __init__(self, cfg, logger)`
- Defined: `topo_swarm_agent.py:2054`
- Doc: Args:
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### save `def save(self, model, optimizer, meta, force)`
- Defined: `topo_swarm_agent.py:2066`
- Doc: Save model weights and metadata if the interval has elapsed.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### load `def load(self, model, optimizer, device)`
- Defined: `topo_swarm_agent.py:2108`
- Doc: Load model weights and metadata from the latest checkpoint.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __init__ `def __init__(self, cfg)`
- Defined: `topo_swarm_agent.py:2159`
- Doc: Args:
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### update `def update(self, loss)`
- Defined: `topo_swarm_agent.py:2167`
- Doc: Update the detector with the latest loss value.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __init__ `def __init__(self, model, cfg, tokenizer, logger)`
- Defined: `topo_swarm_agent.py:2206`
- Doc: Args:
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _make_optimizer `def _make_optimizer(self, lr)`
- Defined: `topo_swarm_agent.py:2233`
- Doc: Build AdamW with weight decay applied only to non-bias, non-norm params.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _warmup_cosine_lr `def _warmup_cosine_lr(self, optimizer, step, total_steps, warmup_steps, base_lr)`
- Defined: `topo_swarm_agent.py:2263`
- Doc: Apply warmup + cosine decay learning rate schedule.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _train_one_batch `def _train_one_batch(self, optimizer, input_ids, targets, accum_step, berry_phase)`
- Defined: `topo_swarm_agent.py:2280`
- Doc: Forward + backward for one micro-batch, returns detached loss.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _phase0_calibrate `def _phase0_calibrate(self, dataloader, n_steps)`
- Defined: `topo_swarm_agent.py:2322`
- Doc: Phase 0: Kernel calibration on API schema tokens.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### train `def train(self, train_dl, val_dl, resume)`
- Defined: `topo_swarm_agent.py:2363`
- Doc: Full three-phase training loop.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _evaluate `def _evaluate(self, val_dl)`
- Defined: `topo_swarm_agent.py:2476`
- Doc: Compute mean validation loss over the first EVAL_INTERVAL_STEPS batches.
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _manual_attn `def _manual_attn()`
- Defined: `topo_swarm_agent.py:1072`
- Depends on: `ts_utils.py`
- Imported by: `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

## topogpt2_1.py

### setup_logger `def setup_logger(name, level)`
- Defined: `topogpt2_1.py:155`

### set_seed `def set_seed(seed, device)`
- Defined: `topogpt2_1.py:165`

### main `def main()`
- Defined: `topogpt2_1.py:2506`

### __post_init__ `def __post_init__(self)`
- Defined: `topogpt2_1.py:124`

### hamilton_product `def hamilton_product(q1, q2)`
- Defined: `topogpt2_1.py:185`
- Doc: Producto de Hamilton q1 ⊗ q2. Ambos [..., 4].

### normalize `def normalize(q, eps)`
- Defined: `topogpt2_1.py:197`

### conjugate `def conjugate(q)`
- Defined: `topogpt2_1.py:201`

### rotate_vector `def rotate_vector(v, q)`
- Defined: `topogpt2_1.py:206`
- Doc: Rota vector 3D v por cuaternión unitario q. v:[...,3] q:[...,4]

### __init__ `def __init__(self, in_features, out_features, bias)`
- Defined: `topogpt2_1.py:228`

### forward `def forward(self, x)`
- Defined: `topogpt2_1.py:244`
- Doc: x: [..., in_features] → [..., out_features]

### __init__ `def __init__(self, in_q, out_q, grid_h, grid_w, init_scale)`
- Defined: `topogpt2_1.py:281`

### _kernel `def _kernel(self, c)`
- Defined: `topogpt2_1.py:300`

### _contract `def _contract(self, W, X)`
- Defined: `topogpt2_1.py:303`
- Doc: Suma sobre canales in_q: Y[b,o,h,w] = Σ_i W[i,o,h,w]·X[b,i,h,w]

### forward `def forward(self, x)`
- Defined: `topogpt2_1.py:307`
- Doc: x: [B, 4*in_q, H, W]  (4 canales cuaterniones sobre grid espacial)

### __init__ `def __init__(self, config)`
- Defined: `topogpt2_1.py:361`

### _filter1d `def _filter1d(self, x, kr, ki)`
- Defined: `topogpt2_1.py:393`
- Doc: Filtro espectral 1D: x[..., D] → filtrado[..., D]

### encode `def encode(self, x)`
- Defined: `topogpt2_1.py:399`
- Doc: x: [..., D_MODEL] → latent: [..., D_LAT]

### decode `def decode(self, z)`
- Defined: `topogpt2_1.py:404`
- Doc: z: [..., D_LAT] → recon: [..., D_MODEL]

### forward `def forward(self, x)`
- Defined: `topogpt2_1.py:409`
- Doc: Devuelve (latent, recon_loss)

### process_torus_grid `def process_torus_grid(self, grid)`
- Defined: `topogpt2_1.py:416`
- Doc: Procesa el grid del toro con QuaternionSpectralLayer.

### __init__ `def __init__(self, d_model, config)`
- Defined: `topogpt2_1.py:449`

### _build_torus_graph `def _build_torus_graph(self)`
- Defined: `topogpt2_1.py:489`
- Doc: Construye las aristas del grafo toro 2×4.

### _torus_soft_assign `def _torus_soft_assign(self, phi1, phi2)`
- Defined: `topogpt2_1.py:523`
- Doc: Asignación blanda de tokens a los 8 nodos del toro via distancia circular.

### _message_passing `def _message_passing(self, node_feat)`
- Defined: `topogpt2_1.py:550`
- Doc: Message-passing VECTORIZADO con rotaciones cuaterniones.

### forward `def forward(self, x)`
- Defined: `topogpt2_1.py:587`
- Doc: x: [B, S, D_MODEL]

### __init__ `def __init__(self, d_head, max_seq_len, base)`
- Defined: `topogpt2_1.py:655`

### _build_cache `def _build_cache(self, seq_len)`
- Defined: `topogpt2_1.py:661`

### _rotate_half `def _rotate_half(self, x)`
- Defined: `topogpt2_1.py:668`

### forward `def forward(self, q, k, seq_len, offset)`
- Defined: `topogpt2_1.py:672`
- Doc: q, k: [B, n_heads, S_q/S_k, d_head]

### __init__ `def __init__(self, d_model, eps)`
- Defined: `topogpt2_1.py:699`

### forward `def forward(self, x)`
- Defined: `topogpt2_1.py:704`

### __init__ `def __init__(self, d_model, expansion, dropout)`
- Defined: `topogpt2_1.py:720`

### forward `def forward(self, x)`
- Defined: `topogpt2_1.py:734`

### __init__ `def __init__(self, d_model, config)`
- Defined: `topogpt2_1.py:757`

### _route `def _route(self, x)`
- Defined: `topogpt2_1.py:778`
- Doc: x: [N, D] donde N = B*S (tokens aplanados)

### forward `def forward(self, x)`
- Defined: `topogpt2_1.py:820`
- Doc: x: [B, S, D]

### __init__ `def __init__(self, d_model, n_heads, config)`
- Defined: `topogpt2_1.py:857`

### forward `def forward(self, x, is_causal, past_kv)`
- Defined: `topogpt2_1.py:875`
- Doc: Args:

### __init__ `def __init__(self, d_model, n_heads, config)`
- Defined: `topogpt2_1.py:938`

### _forward_impl `def _forward_impl(self, x, past_kv)`
- Defined: `topogpt2_1.py:947`

### forward `def forward(self, x, past_kv)`
- Defined: `topogpt2_1.py:956`
- Doc: Retorna (x_out, aux_loss, kv_cache).

### __init__ `def __init__(self, config)`
- Defined: `topogpt2_1.py:987`

### _init_weights `def _init_weights(self)`
- Defined: `topogpt2_1.py:1006`

### forward `def forward(self, token_ids, past_kvs)`
- Defined: `topogpt2_1.py:1013`
- Doc: token_ids: [B, S]  (enteros)

### count_params `def count_params(self)`
- Defined: `topogpt2_1.py:1036`

### generate `def generate(self, token_ids, max_new_tokens, temperature, top_k)`
- Defined: `topogpt2_1.py:1042`
- Doc: Generacion autoregresiva con KV cache y muestreo top-k.

### __init__ `def __init__(self, encoding)`
- Defined: `topogpt2_1.py:1085`

### encode `def encode(self, text)`
- Defined: `topogpt2_1.py:1093`

### decode `def decode(self, tokens)`
- Defined: `topogpt2_1.py:1096`

### eot_token `def eot_token(self)`
- Defined: `topogpt2_1.py:1099`

### __init__ `def __init__(self, corpus, data_dir, logger)`
- Defined: `topogpt2_1.py:1119`

### get_text `def get_text(self, split)`
- Defined: `topogpt2_1.py:1125`
- Doc: Devuelve el texto del corpus. Descarga si es necesario.

### _download_hf `def _download_hf(self, dataset_name, split, text_column, name)`
- Defined: `topogpt2_1.py:1150`

### __init__ `def __init__(self, text, tokenizer, seq_len, max_tokens, cache_dir, split_tag)`
- Defined: `topogpt2_1.py:1179`

### __len__ `def __len__(self)`
- Defined: `topogpt2_1.py:1206`

### __getitem__ `def __getitem__(self, idx)`
- Defined: `topogpt2_1.py:1209`

### __init__ `def __init__(self, config, logger)`
- Defined: `topogpt2_1.py:1245`

### patch_config_for_resume `def patch_config_for_resume(self, cfg)`
- Defined: `topogpt2_1.py:1255`
- Doc: Lee el checkpoint 'latest' y ajusta cfg.N_KV_HEADS / cfg.GQA_GROUPS

### _save_model `def _save_model(self, model, directory)`
- Defined: `topogpt2_1.py:1284`

### _load_model `def _load_model(self, model, directory)`
- Defined: `topogpt2_1.py:1297`

### _save_optimizer `def _save_optimizer(self, optimizer, directory)`
- Defined: `topogpt2_1.py:1328`

### _load_optimizer `def _load_optimizer(self, optimizer, directory, device)`
- Defined: `topogpt2_1.py:1331`

### _save_state `def _save_state(self, state, directory)`
- Defined: `topogpt2_1.py:1340`

### _load_state `def _load_state(self, directory)`
- Defined: `topogpt2_1.py:1345`

### should_save `def should_save(self)`
- Defined: `topogpt2_1.py:1356`

### save `def save(self, model, optimizer, state, is_best)`
- Defined: `topogpt2_1.py:1359`
- Doc: Guarda checkpoint completo.

### load_latest `def load_latest(self, model, optimizer)`
- Defined: `topogpt2_1.py:1404`
- Doc: Carga el ultimo checkpoint guardado.

### load_best `def load_best(self, model)`
- Defined: `topogpt2_1.py:1431`
- Doc: Carga el mejor modelo guardado (solo pesos, sin optimizador).

### has_checkpoint `def has_checkpoint(self)`
- Defined: `topogpt2_1.py:1443`

### __init__ `def __init__(self, model, config, tokenizer)`
- Defined: `topogpt2_1.py:1465`

### resume `def resume(self)`
- Defined: `topogpt2_1.py:1500`
- Doc: Carga el ultimo checkpoint disponible.

### _current_state `def _current_state(self)`
- Defined: `topogpt2_1.py:1525`
- Doc: Construye el dict de estado para persistir en state.json.

### _cosine_lr `def _cosine_lr(self, step_in_session, total_steps_session)`
- Defined: `topogpt2_1.py:1536`
- Doc: Cosine decay con warmup. El schedule es relativo a la sesion actual.

### _set_lr `def _set_lr(self, lr)`
- Defined: `topogpt2_1.py:1544`

### train `def train(self, train_dl, val_dl)`
- Defined: `topogpt2_1.py:1548`
- Doc: Entrena cfg.EPOCHS epocas adicionales a partir de completed_epochs.

### _sample_text `def _sample_text(self, tokenizer, prompts, max_new, temperature, top_k)`
- Defined: `topogpt2_1.py:1684`
- Doc: Genera una muestra de texto al final de cada epoch para monitorear

### evaluate `def evaluate(self, dataloader)`
- Defined: `topogpt2_1.py:1716`

### __init__ `def __init__(self, config)`
- Defined: `topogpt2_1.py:1766`

### compute_delta `def compute_delta(self, model)`
- Defined: `topogpt2_1.py:1774`

### compute_alpha `def compute_alpha(self, delta)`
- Defined: `topogpt2_1.py:1781`

### update_grad_buffer `def update_grad_buffer(self, model)`
- Defined: `topogpt2_1.py:1786`
- Doc: Captura gradientes de forma segura, ignorando tensores corruptos.

### compute_t_eff `def compute_t_eff(self, lr)`
- Defined: `topogpt2_1.py:1812`
- Doc: T_eff = lr/2 * Var(gradiente). Temperatura termodinamica efectiva.

### compute_kappa `def compute_kappa(self, model, dataloader, n_batches)`
- Defined: `topogpt2_1.py:1820`
- Doc: κ = λ_max / λ_min de la covarianza del gradiente.

### compute_berry_phase `def compute_berry_phase(self, model)`
- Defined: `topogpt2_1.py:1878`
- Doc: Fase de Berry de los kernels espectrales imaginarios.

### compute_lc `def compute_lc(self, model)`
- Defined: `topogpt2_1.py:1891`
- Doc: Complejidad local: 1 - similitud coseno promedio entre filas de pesos.

### compute_sp `def compute_sp(self, model)`
- Defined: `topogpt2_1.py:1905`
- Doc: Superposicion: correlacion inter-fila promedio (entrelazamiento de features).

### classify_phase `def classify_phase(self, delta, kappa, berry)`
- Defined: `topogpt2_1.py:1921`
- Doc: Clasificacion de fase segun Book.md:

### compute_all `def compute_all(self, model, lr, dataloader, compute_kappa)`
- Defined: `topogpt2_1.py:1940`
- Doc: Calcula todas las metricas.

### format_log `def format_log(self, m)`
- Defined: `topogpt2_1.py:1965`

### __init__ `def __init__(self, config, logger)`
- Defined: `topogpt2_1.py:2001`

### _measure_ratio `def _measure_ratio(self, ratio, sample_batch)`
- Defined: `topogpt2_1.py:2005`
- Doc: Mide la coherencia espectral para un ratio dado.

### optimize `def optimize(self, dataloader)`
- Defined: `topogpt2_1.py:2034`
- Doc: Retorna el mejor ratio de inicializacion de kernels espectrales.

### __init__ `def __init__(self, config, logger)`
- Defined: `topogpt2_1.py:2074`

### prospect `def prospect(self, candidates, train_dataset, prospect_steps)`
- Defined: `topogpt2_1.py:2078`
- Doc: Retorna el mejor batch size segun delta y T_eff.

### __init__ `def __init__(self, config, logger)`
- Defined: `topogpt2_1.py:2157`

### mine `def mine(self, seed_start, n_seeds, train_dataset, prospect_steps)`
- Defined: `topogpt2_1.py:2161`
- Doc: Retorna la semilla con la mejor trayectoria de delta.

### __init__ `def __init__(self, trainer, t0, cooling_rate, stagnation_patience)`
- Defined: `topogpt2_1.py:2243`

### refine `def refine(self, train_dl, val_dl, refine_epochs)`
- Defined: `topogpt2_1.py:2252`
- Doc: Ejecuta refine_epochs epocas de recocido simulado.

### __init__ `def __init__(self, config, train_dataset, val_dataset, tokenizer, logger)`
- Defined: `topogpt2_1.py:2404`

### _make_dataloaders `def _make_dataloaders(self, batch_size)`
- Defined: `topogpt2_1.py:2414`

### run `def run(self, run_prospect, refine_epochs, resume, prospect_steps, probe_seeds, seed_start)`
- Defined: `topogpt2_1.py:2426`
- Doc: Ejecuta el pipeline completo.

### ckpt_fn `def ckpt_fn(x_in)`
- Defined: `topogpt2_1.py:964`

## toposwarm_coevolve.py

### _resolve_lazyown_dir `def _resolve_lazyown_dir()`
- Defined: `toposwarm_coevolve.py:63`
- Doc: Discover LazyOwn installation directory.
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### _setup_logger `def _setup_logger(name, level)`
- Defined: `toposwarm_coevolve.py:90`
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### _clip `def _clip(x, lo, hi)`
- Defined: `toposwarm_coevolve.py:175`
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### main `def main()`
- Defined: `toposwarm_coevolve.py:646`
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### mutate `def mutate(cfg_dict)`
- Defined: `toposwarm_coevolve.py:132`
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### crossover `def crossover(a, b)`
- Defined: `toposwarm_coevolve.py:167`
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### __init__ `def __init__(self)`
- Defined: `toposwarm_coevolve.py:190`
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### available `def available(self)`
- Defined: `toposwarm_coevolve.py:196`
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### run `def run(self, command, timeout)`
- Defined: `toposwarm_coevolve.py:199`
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### get_config `def get_config(self)`
- Defined: `toposwarm_coevolve.py:222`
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### set_config `def set_config(self, key, value)`
- Defined: `toposwarm_coevolve.py:225`
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### __init__ `def __init__(self, prompts, lazyown_dir, logger, use_mock_bridge)`
- Defined: `toposwarm_coevolve.py:244`
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### evaluate `def evaluate(self, cfg_dict)`
- Defined: `toposwarm_coevolve.py:256`
- Doc: Run each prompt through the orchestrator and collect metrics.
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### _build_orchestrator `def _build_orchestrator(self, cfg_dict)`
- Defined: `toposwarm_coevolve.py:313`
- Doc: Build a LazyOwnOrchestrator with the given MetaHarnessConfig.
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### _log_run `def _log_run(self, orch, prompt, result, latency_ms, ctx_len, ok, cfg_dict)`
- Defined: `toposwarm_coevolve.py:343`
- Doc: Write one evaluation to the Meta-Harness experience store.
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### __init__ `def __init__(self, logger)`
- Defined: `toposwarm_coevolve.py:397`
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### _load `def _load(self)`
- Defined: `toposwarm_coevolve.py:402`
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### is_available `def is_available(self)`
- Defined: `toposwarm_coevolve.py:415`
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### fine_tune `def fine_tune(self, dataset_path, steps, learning_rate)`
- Defined: `toposwarm_coevolve.py:418`
- Doc: Run a short fine-tuning burst and return metrics.
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### __init__ `def __init__(self, generations, population_size, train_steps_per_gen, proposer_interval, lazyown_dir, logger)`
- Defined: `toposwarm_coevolve.py:456`
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### run `def run(self)`
- Defined: `toposwarm_coevolve.py:490`
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### _next_generation `def _next_generation(self, scores)`
- Defined: `toposwarm_coevolve.py:550`
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### _tournament_select `def _tournament_select(sorted_scores, k)`
- Defined: `toposwarm_coevolve.py:567`
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### _is_on_frontier `def _is_on_frontier(self, cfg, metrics)`
- Defined: `toposwarm_coevolve.py:575`
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### _run_proposer `def _run_proposer(self)`
- Defined: `toposwarm_coevolve.py:596`
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### _save_state `def _save_state(self, generation)`
- Defined: `toposwarm_coevolve.py:619`
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### load_state `def load_state(self, path)`
- Defined: `toposwarm_coevolve.py:628`
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

### _report_frontier `def _report_frontier(self)`
- Defined: `toposwarm_coevolve.py:635`
- Depends on: `topo_swarm_agent.py`, `toposwarm_infer.py`, `toposwarm_lazyown_orchestrator.py`, `toposwarm_meta_harness.py`

## toposwarm_continual_trainer.py

### _import `def _import(name, filename)`
- Defined: `toposwarm_continual_trainer.py:91`
- Depends on: `ts_utils.py`

### _setup_logger `def _setup_logger(level)`
- Defined: `toposwarm_continual_trainer.py:158`
- Depends on: `ts_utils.py`

### _load_jsonl `def _load_jsonl(path)`
- Defined: `toposwarm_continual_trainer.py:232`
- Depends on: `ts_utils.py`

### _encode_record `def _encode_record(record, tok, cfg)`
- Defined: `toposwarm_continual_trainer.py:247`
- Doc: Encode a ToolBench-format record into (input_ids, target_ids).
- Depends on: `ts_utils.py`

### _collate `def _collate(batch)`
- Defined: `toposwarm_continual_trainer.py:319`
- Depends on: `ts_utils.py`

### evaluate_routing `def evaluate_routing(model, cfg, tok, lazyown_records, toolbench_records, logger)`
- Defined: `toposwarm_continual_trainer.py:1137`
- Doc: Measure routing accuracy on a held-out subset of both datasets.
- Depends on: `ts_utils.py`

### build_model_and_tok `def build_model_and_tok(cl_cfg, logger)`
- Defined: `toposwarm_continual_trainer.py:1195`
- Depends on: `ts_utils.py`

### run_full_pipeline `def run_full_pipeline(cl_cfg, logger)`
- Defined: `toposwarm_continual_trainer.py:1217`
- Doc: Generate dataset → compute Fisher → fine-tune → evaluate.
- Depends on: `ts_utils.py`

### main `def main()`
- Defined: `toposwarm_continual_trainer.py:1384`
- Depends on: `ts_utils.py`

### __init__ `def __init__(self, maxsize, replay_ratio)`
- Defined: `toposwarm_continual_trainer.py:180`
- Depends on: `ts_utils.py`

### update `def update(self, records, task_losses, logits)`
- Defined: `toposwarm_continual_trainer.py:186`
- Doc: Add batch examples to buffer, keyed by surprise score.
- Depends on: `ts_utils.py`

### sample `def sample(self, batch_size)`
- Defined: `toposwarm_continual_trainer.py:213`
- Doc: Return a priority-weighted sample of hard examples.
- Depends on: `ts_utils.py`

### __len__ `def __len__(self)`
- Defined: `toposwarm_continual_trainer.py:223`
- Depends on: `ts_utils.py`

### __init__ `def __init__(self, records, tok, cfg)`
- Defined: `toposwarm_continual_trainer.py:301`
- Depends on: `ts_utils.py`

### __len__ `def __len__(self)`
- Defined: `toposwarm_continual_trainer.py:312`
- Depends on: `ts_utils.py`

### __getitem__ `def __getitem__(self, idx)`
- Defined: `toposwarm_continual_trainer.py:315`
- Depends on: `ts_utils.py`

### __init__ `def __init__(self, records, max_size, tok, cfg)`
- Defined: `toposwarm_continual_trainer.py:343`
- Depends on: `ts_utils.py`

### sample `def sample(self, n)`
- Defined: `toposwarm_continual_trainer.py:351`
- Depends on: `ts_utils.py`

### __len__ `def __len__(self)`
- Defined: `toposwarm_continual_trainer.py:356`
- Depends on: `ts_utils.py`

### __init__ `def __init__(self, model, cfg, cl_cfg, tok, logger)`
- Defined: `toposwarm_continual_trainer.py:380`
- Depends on: `ts_utils.py`

### compute `def compute(self, toolbench_records)`
- Defined: `toposwarm_continual_trainer.py:401`
- Doc: Compute Fisher diagonal on a sample of ToolBench records and snapshot θ*.
- Depends on: `ts_utils.py`

### save `def save(self, path)`
- Defined: `toposwarm_continual_trainer.py:465`
- Depends on: `ts_utils.py`

### load `def load(self, path)`
- Defined: `toposwarm_continual_trainer.py:470`
- Depends on: `ts_utils.py`

### penalty `def penalty(self)`
- Defined: `toposwarm_continual_trainer.py:481`
- Doc: Returns the EWC penalty term to add to the task loss.
- Depends on: `ts_utils.py`

### __init__ `def __init__(self, d_model, n_tools)`
- Defined: `toposwarm_continual_trainer.py:534`
- Depends on: `ts_utils.py`

### forward `def forward(self, x)`
- Defined: `toposwarm_continual_trainer.py:551`
- Doc: x: [B, d_model] → logits [B, n_tools]
- Depends on: `ts_utils.py`

### hebbian_update `def hebbian_update(self, pre, labels)`
- Defined: `toposwarm_continual_trainer.py:570`
- Doc: Strengthen W_fast associations after correct predictions.
- Depends on: `ts_utils.py`

### __init__ `def __init__(self, d_model, tool_names, n_experts, top_k, hidden_dim)`
- Defined: `toposwarm_continual_trainer.py:614`
- Depends on: `ts_utils.py`

### n_tools `def n_tools(self)`
- Defined: `toposwarm_continual_trainer.py:651`
- Depends on: `ts_utils.py`

### forward `def forward(self, hidden)`
- Defined: `toposwarm_continual_trainer.py:654`
- Doc: hidden: [B, d_model] → logits [B, n_tools]
- Depends on: `ts_utils.py`

### label `def label(self, tool_name)`
- Defined: `toposwarm_continual_trainer.py:685`
- Depends on: `ts_utils.py`

### predict `def predict(self, hidden)`
- Defined: `toposwarm_continual_trainer.py:688`
- Doc: hidden: [B, d_model] → list of predicted tool name strings
- Depends on: `ts_utils.py`

### save `def save(self, path)`
- Defined: `toposwarm_continual_trainer.py:695`
- Depends on: `ts_utils.py`

### load `def load(cls, d_model, path)`
- Defined: `toposwarm_continual_trainer.py:706`
- Depends on: `ts_utils.py`

### __init__ `def __init__(self, model, cfg, cl_cfg, tok, ewc, replay, logger, routing_head)`
- Defined: `toposwarm_continual_trainer.py:746`
- Depends on: `ts_utils.py`

### _make_optimizer `def _make_optimizer(self)`
- Defined: `toposwarm_continual_trainer.py:782`
- Depends on: `ts_utils.py`

### _lr_schedule `def _lr_schedule(optimizer, step, total, warmup, base_lr)`
- Defined: `toposwarm_continual_trainer.py:821`
- Depends on: `ts_utils.py`

### _merge_with_replay `def _merge_with_replay(self, ids, tgt)`
- Defined: `toposwarm_continual_trainer.py:830`
- Doc: Append replay samples to the LazyOwn batch.
- Depends on: `ts_utils.py`

### _routing_accuracy `def _routing_accuracy(self, records)`
- Defined: `toposwarm_continual_trainer.py:863`
- Doc: Routing accuracy using the LM head (primary) and routing head (secondary).
- Depends on: `ts_utils.py`

### train `def train(self, lazyown_dataset, train_records, val_records)`
- Defined: `toposwarm_continual_trainer.py:923`
- Depends on: `ts_utils.py`

### _accuracy `def _accuracy(records, label)`
- Defined: `toposwarm_continual_trainer.py:1153`
- Depends on: `ts_utils.py`

### _hook `def _hook(m, i, o)`
- Defined: `toposwarm_continual_trainer.py:887`
- Depends on: `ts_utils.py`

### _capture `def _capture(module, inp, out_h)`
- Defined: `toposwarm_continual_trainer.py:995`
- Depends on: `ts_utils.py`

## toposwarm_hybrid.py

### _import_agent `def _import_agent()`
- Defined: `toposwarm_hybrid.py:85`
- Doc: Import topo_swarm_agent, searching script dir then cwd.

### _setup_logger `def _setup_logger(name, level)`
- Defined: `toposwarm_hybrid.py:164`
- Doc: Idempotent logger with a single StreamHandler.

### _safe_eval `def _safe_eval(expr)`
- Defined: `toposwarm_hybrid.py:182`
- Doc: Evaluate a math expression safely via AST — no eval().

### _template_answer `def _template_answer(tool_name, tool_arg, tool_result)`
- Defined: `toposwarm_hybrid.py:887`
- Doc: Build a clean deterministic answer from the tool result.

### _is_useful_output `def _is_useful_output(text, min_chars)`
- Defined: `toposwarm_hybrid.py:918`
- Doc: Return True if the backend output is genuinely informative.

### main `def main()`
- Defined: `toposwarm_hybrid.py:1051`
- Doc: CLI entry point.

### _eval `def _eval(node)`
- Defined: `toposwarm_hybrid.py:192`

### __init__ `def __init__(self, tool_name, arg, output, ok)`
- Defined: `toposwarm_hybrid.py:221`

### __str__ `def __str__(self)`
- Defined: `toposwarm_hybrid.py:227`

### __init__ `def __init__(self, cfg)`
- Defined: `toposwarm_hybrid.py:234`

### _register `def _register(self)`
- Defined: `toposwarm_hybrid.py:240`

### resolve `def resolve(self, raw)`
- Defined: `toposwarm_hybrid.py:249`
- Doc: Resolve tool name to canonical key via exact match, alias, or substring.

### route `def route(self, prompt)`
- Defined: `toposwarm_hybrid.py:261`
- Doc: Infer tool name and argument from prompt keywords.

### execute `def execute(self, tool_name, arg)`
- Defined: `toposwarm_hybrid.py:287`
- Doc: Execute a tool by canonical name.

### _http_get `def _http_get(self, url)`
- Defined: `toposwarm_hybrid.py:299`

### _register_all `def _register_all(self)`
- Defined: `toposwarm_hybrid.py:304`
- Doc: Register all built-in tools.

### tool_names `def tool_names(self)`
- Defined: `toposwarm_hybrid.py:387`

### __init__ `def __init__(self, cfg, registry, logger)`
- Defined: `toposwarm_hybrid.py:409`
- Doc: Args:

### _load `def _load(self)`
- Defined: `toposwarm_hybrid.py:428`
- Doc: Load checkpoint weights.

### route `def route(self, prompt)`
- Defined: `toposwarm_hybrid.py:441`
- Doc: Determine the tool and argument for a prompt.

### __init__ `def __init__(self, cfg, logger)`
- Defined: `toposwarm_hybrid.py:475`
- Doc: Args:

### _load `def _load(self)`
- Defined: `toposwarm_hybrid.py:486`
- Doc: Load the language model according to BACKEND_TYPE.

### _load_tinystories `def _load_tinystories(self)`
- Defined: `toposwarm_hybrid.py:507`
- Doc: Load a GPT-2-style HuggingFace model (TinyStories or compatible).

### _import_topogpt `def _import_topogpt(self)`
- Defined: `toposwarm_hybrid.py:563`
- Doc: Import topogpt2_1.py from the same directory as the checkpoint or

### _load_checkpoint `def _load_checkpoint(self)`
- Defined: `toposwarm_hybrid.py:588`
- Doc: Load a safetensors or pickle checkpoint for the language backend.

### generate `def generate(self, prompt, tool_result)`
- Defined: `toposwarm_hybrid.py:859`
- Doc: Generate a natural-language answer from the prompt and tool result.

### pretty `def pretty(self)`
- Defined: `toposwarm_hybrid.py:958`
- Doc: Render a human-readable summary.

### __init__ `def __init__(self, cfg, logger)`
- Defined: `toposwarm_hybrid.py:988`
- Doc: Args:

### run `def run(self, prompt)`
- Defined: `toposwarm_hybrid.py:1000`
- Doc: Execute the full hybrid pipeline for one user prompt.

### decorator `def decorator(fn)`
- Defined: `toposwarm_hybrid.py:241`

### get_weather `def get_weather(city)`
- Defined: `toposwarm_hybrid.py:308`

### search_web `def search_web(query)`
- Defined: `toposwarm_hybrid.py:319`

### calc_expr `def calc_expr(expr)`
- Defined: `toposwarm_hybrid.py:331`

### get_datetime `def get_datetime(tz_hint)`
- Defined: `toposwarm_hybrid.py:335`

### translate `def translate(text)`
- Defined: `toposwarm_hybrid.py:341`

### get_news `def get_news(topic)`
- Defined: `toposwarm_hybrid.py:373`

### echo `def echo(text)`
- Defined: `toposwarm_hybrid.py:383`

### _generate `def _generate(prompt_text)`
- Defined: `toposwarm_hybrid.py:540`

### _cfg_score `def _cfg_score(cls)`
- Defined: `toposwarm_hybrid.py:703`

### _generate `def _generate(prompt_text)`
- Defined: `toposwarm_hybrid.py:812`

### _generate `def _generate(prompt_text)`
- Defined: `toposwarm_hybrid.py:835`

## toposwarm_infer.py

### _import_agent `def _import_agent()`
- Defined: `toposwarm_infer.py:51`
- Doc: Import topo_swarm_agent, searching the script dir and cwd.
- Imported by: `toposwarm_coevolve.py`

### _safe_eval `def _safe_eval(expr)`
- Defined: `toposwarm_infer.py:138`
- Doc: Evaluate a mathematical expression without using eval() on arbitrary code.
- Imported by: `toposwarm_coevolve.py`

### _setup_logger `def _setup_logger(name, level)`
- Defined: `toposwarm_infer.py:920`
- Doc: Idempotent logger with a single StreamHandler.
- Imported by: `toposwarm_coevolve.py`

### main `def main()`
- Defined: `toposwarm_infer.py:938`
- Doc: CLI entry point.
- Imported by: `toposwarm_coevolve.py`

### _eval `def _eval(node)`
- Defined: `toposwarm_infer.py:157`
- Imported by: `toposwarm_coevolve.py`

### __init__ `def __init__(self, tool_name, arg, output, ok)`
- Defined: `toposwarm_infer.py:192`
- Doc: Args:
- Imported by: `toposwarm_coevolve.py`

### __str__ `def __str__(self)`
- Defined: `toposwarm_infer.py:205`
- Imported by: `toposwarm_coevolve.py`

### __init__ `def __init__(self, cfg)`
- Defined: `toposwarm_infer.py:219`
- Doc: Args:
- Imported by: `toposwarm_coevolve.py`

### register `def register(self)`
- Defined: `toposwarm_infer.py:229`
- Doc: Decorator that registers a function under one or more tool names.
- Imported by: `toposwarm_coevolve.py`

### resolve `def resolve(self, raw_name)`
- Defined: `toposwarm_infer.py:239`
- Doc: Resolve a raw tool name to its canonical registry key.
- Imported by: `toposwarm_coevolve.py`

### execute `def execute(self, raw_name, arg)`
- Defined: `toposwarm_infer.py:262`
- Doc: Execute a tool by name with the given argument string.
- Imported by: `toposwarm_coevolve.py`

### _http_get `def _http_get(self, url)`
- Defined: `toposwarm_infer.py:292`
- Doc: Minimal HTTP GET with timeout, returns response body as string.
- Imported by: `toposwarm_coevolve.py`

### _register_builtin_tools `def _register_builtin_tools(self)`
- Defined: `toposwarm_infer.py:301`
- Doc: Register all built-in tools onto self._tools / self._aliases.
- Imported by: `toposwarm_coevolve.py`

### __init__ `def __init__(self, cfg)`
- Defined: `toposwarm_infer.py:446`
- Doc: Args:
- Imported by: `toposwarm_coevolve.py`

### parse `def parse(self, text)`
- Defined: `toposwarm_infer.py:453`
- Doc: Extract the first tool call from text.
- Imported by: `toposwarm_coevolve.py`

### __init__ `def __init__(self, cfg, agent_cfg, logger)`
- Defined: `toposwarm_infer.py:495`
- Doc: Args:
- Imported by: `toposwarm_coevolve.py`

### _load_checkpoint `def _load_checkpoint(self)`
- Defined: `toposwarm_infer.py:521`
- Doc: Load weights from the latest checkpoint directory.
- Imported by: `toposwarm_coevolve.py`

### _encode_prompt `def _encode_prompt(self, text)`
- Defined: `toposwarm_infer.py:538`
- Doc: Encode a prompt string to a [1, S] token id tensor on the model device.
- Imported by: `toposwarm_coevolve.py`

### _generate `def _generate(self, prompt_ids, max_new_tokens, temperature)`
- Defined: `toposwarm_infer.py:586`
- Doc: Custom autoregressive generation loop with three inference-time fixes.
- Imported by: `toposwarm_coevolve.py`

### run `def run(self, prompt)`
- Defined: `toposwarm_infer.py:679`
- Doc: Full agentic inference loop for one user prompt.
- Imported by: `toposwarm_coevolve.py`

### _template_answer `def _template_answer(self, tool_name, tool_arg, tool_result)`
- Defined: `toposwarm_infer.py:818`
- Doc: Build a deterministic natural-language answer from the tool result.
- Imported by: `toposwarm_coevolve.py`

### _infer_tool_and_arg `def _infer_tool_and_arg(self, prompt)`
- Defined: `toposwarm_infer.py:844`
- Doc: Infer the tool name and argument from the prompt text.
- Imported by: `toposwarm_coevolve.py`

### pretty `def pretty(self)`
- Defined: `toposwarm_infer.py:895`
- Doc: Render a human-readable summary of the inference run.
- Imported by: `toposwarm_coevolve.py`

### decorator `def decorator(fn)`
- Defined: `toposwarm_infer.py:231`
- Imported by: `toposwarm_coevolve.py`

### get_weather `def get_weather(city)`
- Defined: `toposwarm_infer.py:305`
- Doc: Fetch current weather from wttr.in (no API key required).
- Imported by: `toposwarm_coevolve.py`

### search_web `def search_web(query)`
- Defined: `toposwarm_infer.py:323`
- Doc: Instant-answer search via DuckDuckGo JSON API (no API key).
- Imported by: `toposwarm_coevolve.py`

### calc_expr `def calc_expr(expr)`
- Defined: `toposwarm_infer.py:340`
- Doc: Evaluate a mathematical expression safely.
- Imported by: `toposwarm_coevolve.py`

### get_datetime `def get_datetime(tz_hint)`
- Defined: `toposwarm_infer.py:345`
- Doc: Return the current UTC datetime (tz_hint is informational only).
- Imported by: `toposwarm_coevolve.py`

### translate `def translate(text)`
- Defined: `toposwarm_infer.py:351`
- Doc: Translate text using MyMemory free API (no key, 5k chars/day limit).
- Imported by: `toposwarm_coevolve.py`

### get_news `def get_news(topic)`
- Defined: `toposwarm_infer.py:409`
- Doc: Fetch recent news headlines via DuckDuckGo news search.
- Imported by: `toposwarm_coevolve.py`

### echo `def echo(text)`
- Defined: `toposwarm_infer.py:428`
- Doc: Return the input unchanged. Used for model self-testing.
- Imported by: `toposwarm_coevolve.py`

## toposwarm_lazyown_orchestrator.py

### _resolve_lazyown_dir `def _resolve_lazyown_dir()`
- Defined: `toposwarm_lazyown_orchestrator.py:56`
- Doc: Discover LazyOwn installation directory.
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _import_infer `def _import_infer()`
- Defined: `toposwarm_lazyown_orchestrator.py:93`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _import_agent `def _import_agent()`
- Defined: `toposwarm_lazyown_orchestrator.py:113`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _import_meta_harness `def _import_meta_harness()`
- Defined: `toposwarm_lazyown_orchestrator.py:128`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _import_routing_head `def _import_routing_head()`
- Defined: `toposwarm_lazyown_orchestrator.py:147`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### infer_lazyown_tool `def infer_lazyown_tool(prompt)`
- Defined: `toposwarm_lazyown_orchestrator.py:691`
- Doc: Map a natural-language security prompt to a (tool_name, tool_arg) pair.
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _extract_arg `def _extract_arg(prompt, tool_name)`
- Defined: `toposwarm_lazyown_orchestrator.py:716`
- Doc: Extract the most useful argument string for each tool category.
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### generate_dataset `def generate_dataset(output_path, bridge)`
- Defined: `toposwarm_lazyown_orchestrator.py:1092`
- Doc: Generate a rich ToolBench-format JSONL for fine-tuning the TopoSwarm router.
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### finetune_on_lazyown `def finetune_on_lazyown(dataset_path, agent_cfg, logger)`
- Defined: `toposwarm_lazyown_orchestrator.py:1173`
- Doc: Fine-tune the TopoSwarm router on the full LazyOwn tool dataset using
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### run_mcp_server `def run_mcp_server(orchestrator)`
- Defined: `toposwarm_lazyown_orchestrator.py:1250`
- Doc: Expose the TopoSwarm→LazyOwn orchestrator as an MCP stdio server.
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _setup_logger `def _setup_logger(level)`
- Defined: `toposwarm_lazyown_orchestrator.py:1329`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### main `def main()`
- Defined: `toposwarm_lazyown_orchestrator.py:1346`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### to_prompt_prefix `def to_prompt_prefix(self)`
- Defined: `toposwarm_lazyown_orchestrator.py:181`
- Doc: Compact context block injected before the user prompt.
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### update `def update(self, tool_name, arg, output, ok)`
- Defined: `toposwarm_lazyown_orchestrator.py:195`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __init__ `def __init__(self, lazyown_dir, default_timeout)`
- Defined: `toposwarm_lazyown_orchestrator.py:251`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### available `def available(self)`
- Defined: `toposwarm_lazyown_orchestrator.py:257`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### run `def run(self, command, timeout)`
- Defined: `toposwarm_lazyown_orchestrator.py:265`
- Doc: Execute a LazyOwn shell command and return cleaned output.
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### get_config `def get_config(self)`
- Defined: `toposwarm_lazyown_orchestrator.py:344`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### set_config `def set_config(self, key, value)`
- Defined: `toposwarm_lazyown_orchestrator.py:353`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __init__ `def __init__(self, cfg, bridge)`
- Defined: `toposwarm_lazyown_orchestrator.py:455`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _register_lazyown_tools `def _register_lazyown_tools(self)`
- Defined: `toposwarm_lazyown_orchestrator.py:460`
- Doc: Register every LazyOwn MCP tool as a ToolRegistry callable.
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### __init__ `def __init__(self, cfg, agent_cfg, bridge, logger, load_model, meta_cfg)`
- Defined: `toposwarm_lazyown_orchestrator.py:780`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _load_routing_head `def _load_routing_head(self)`
- Defined: `toposwarm_lazyown_orchestrator.py:825`
- Doc: Load the trained RoutingHead if a checkpoint exists.
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _neural_route `def _neural_route(self, prompt)`
- Defined: `toposwarm_lazyown_orchestrator.py:847`
- Doc: Use the TopoSwarm model + RoutingHead to predict the LazyOwn tool.
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### run `def run(self, prompt)`
- Defined: `toposwarm_lazyown_orchestrator.py:887`
- Doc: Route prompt → LazyOwn tool → answer.
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### list_tools `def list_tools()`
- Defined: `toposwarm_lazyown_orchestrator.py:1273`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### call_tool `def call_tool(name, arguments)`
- Defined: `toposwarm_lazyown_orchestrator.py:1307`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _serve `def _serve()`
- Defined: `toposwarm_lazyown_orchestrator.py:1317`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### run_command `def run_command(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:466`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### get_config `def get_config(_)`
- Defined: `toposwarm_lazyown_orchestrator.py:470`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### set_config `def set_config(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:475`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### list_modules `def list_modules(_)`
- Defined: `toposwarm_lazyown_orchestrator.py:483`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### get_beacons `def get_beacons(_)`
- Defined: `toposwarm_lazyown_orchestrator.py:487`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### c2_command `def c2_command(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:491`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### run_api `def run_api(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:495`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### list_sessions `def list_sessions(_)`
- Defined: `toposwarm_lazyown_orchestrator.py:499`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### read_session_file `def read_session_file(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:507`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### c2_status `def c2_status(_)`
- Defined: `toposwarm_lazyown_orchestrator.py:514`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### create_addon `def create_addon(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:518`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### list_addons `def list_addons(_)`
- Defined: `toposwarm_lazyown_orchestrator.py:522`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### list_plugins `def list_plugins(_)`
- Defined: `toposwarm_lazyown_orchestrator.py:529`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### poll_events `def poll_events(_)`
- Defined: `toposwarm_lazyown_orchestrator.py:536`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### ack_event `def ack_event(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:540`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### add_rule `def add_rule(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:544`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### list_event_rules `def list_event_rules(_)`
- Defined: `toposwarm_lazyown_orchestrator.py:548`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### heartbeat_status `def heartbeat_status(_)`
- Defined: `toposwarm_lazyown_orchestrator.py:552`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### session_init `def session_init(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:556`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### discover_commands `def discover_commands(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:560`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### phase_guide `def phase_guide(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:564`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### command_help `def command_help(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:568`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### add_target `def add_target(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:572`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### list_targets `def list_targets(_)`
- Defined: `toposwarm_lazyown_orchestrator.py:578`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### run_agent `def run_agent(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:582`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### agent_status `def agent_status(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:586`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### agent_result `def agent_result(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:590`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### list_agents `def list_agents(_)`
- Defined: `toposwarm_lazyown_orchestrator.py:594`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### set_active_target `def set_active_target(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:598`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### campaign_sitrep `def campaign_sitrep(_)`
- Defined: `toposwarm_lazyown_orchestrator.py:602`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### c2_notes `def c2_notes(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:606`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### credentials `def credentials(_)`
- Defined: `toposwarm_lazyown_orchestrator.py:610`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### report_update `def report_update(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:614`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### campaign_lessons `def campaign_lessons(_)`
- Defined: `toposwarm_lazyown_orchestrator.py:618`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### auto_populate `def auto_populate(_)`
- Defined: `toposwarm_lazyown_orchestrator.py:622`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### session_state `def session_state(_)`
- Defined: `toposwarm_lazyown_orchestrator.py:626`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### recommend_next `def recommend_next(_)`
- Defined: `toposwarm_lazyown_orchestrator.py:630`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### timeline `def timeline(_)`
- Defined: `toposwarm_lazyown_orchestrator.py:634`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### c2_vuln_analysis `def c2_vuln_analysis(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:638`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### c2_redop `def c2_redop(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:642`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### c2_search_agent `def c2_search_agent(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:646`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### c2_script `def c2_script(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:650`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### c2_adversary `def c2_adversary(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:654`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### policy_status `def policy_status(_)`
- Defined: `toposwarm_lazyown_orchestrator.py:658`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### auto_loop `def auto_loop(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:662`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### create_tool `def create_tool(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:666`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### llm_ask `def llm_ask(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:670`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### inject_objective `def inject_objective(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:674`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### next_objective `def next_objective(_)`
- Defined: `toposwarm_lazyown_orchestrator.py:678`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### read_prompt `def read_prompt(arg)`
- Defined: `toposwarm_lazyown_orchestrator.py:682`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

### _hook `def _hook(module, inp, out)`
- Defined: `toposwarm_lazyown_orchestrator.py:863`
- Imported by: `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `tests/test_orchestrator.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`, `toposwarm_lazyown_sweep.py`

## toposwarm_lazyown_sweep.py

### generate_prompts `def generate_prompts(n)`
- Defined: `toposwarm_lazyown_sweep.py:130`
- Doc: Generate N diverse pentesting prompts.
- Depends on: `topo_swarm_agent.py`, `toposwarm_lazyown_orchestrator.py`

### setup_logger `def setup_logger()`
- Defined: `toposwarm_lazyown_sweep.py:145`
- Depends on: `topo_swarm_agent.py`, `toposwarm_lazyown_orchestrator.py`

### run_sweep `def run_sweep(prompts, bridge, logger)`
- Defined: `toposwarm_lazyown_sweep.py:155`
- Doc: Execute prompts against LazyOwn and collect results.
- Depends on: `topo_swarm_agent.py`, `toposwarm_lazyown_orchestrator.py`

### write_results `def write_results(results, out_path)`
- Defined: `toposwarm_lazyown_sweep.py:189`
- Doc: Write results as JSONL for continual trainer.
- Depends on: `topo_swarm_agent.py`, `toposwarm_lazyown_orchestrator.py`

### main `def main()`
- Defined: `toposwarm_lazyown_sweep.py:223`
- Depends on: `topo_swarm_agent.py`, `toposwarm_lazyown_orchestrator.py`

## toposwarm_meta_harness.py

### _setup_logger `def _setup_logger(name, level)`
- Defined: `toposwarm_meta_harness.py:95`
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### _stable_id `def _stable_id(text)`
- Defined: `toposwarm_meta_harness.py:107`
- Doc: Short stable hash for naming log directories.
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### _now_iso `def _now_iso()`
- Defined: `toposwarm_meta_harness.py:112`
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### _demo `def _demo()`
- Defined: `toposwarm_meta_harness.py:1013`
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### __init__ `def __init__(self, cfg, logger)`
- Defined: `toposwarm_meta_harness.py:138`
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### _count_existing_runs `def _count_existing_runs(self)`
- Defined: `toposwarm_meta_harness.py:149`
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### _next_run_dir `def _next_run_dir(self, hint)`
- Defined: `toposwarm_meta_harness.py:152`
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### _prune_old `def _prune_old(self)`
- Defined: `toposwarm_meta_harness.py:158`
- Doc: Keep only the most recent MAX_LOGGED_RUNS directories.
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### log_run `def log_run(self, harness_snapshot, trace_steps, score, reasoning)`
- Defined: `toposwarm_meta_harness.py:176`
- Doc: Persist one complete harness evaluation.
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### list_runs `def list_runs(self, n)`
- Defined: `toposwarm_meta_harness.py:229`
- Doc: Return run directories newest-first.
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### grep_traces `def grep_traces(self, pattern, max_results)`
- Defined: `toposwarm_meta_harness.py:238`
- Doc: Simple regex search across all trace.jsonl files.
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### get_scores `def get_scores(self)`
- Defined: `toposwarm_meta_harness.py:257`
- Doc: Load every score.json into a list.
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### get_pareto_runs `def get_pareto_runs(self, metrics)`
- Defined: `toposwarm_meta_harness.py:269`
- Doc: Return run directories that are on the Pareto frontier.
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### __init__ `def __init__(self, logger)`
- Defined: `toposwarm_meta_harness.py:335`
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### add `def add(self, text, episode)`
- Defined: `toposwarm_meta_harness.py:362`
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### _rebuild_tfidf `def _rebuild_tfidf(self)`
- Defined: `toposwarm_meta_harness.py:368`
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### bulk_index `def bulk_index(self, texts, episodes)`
- Defined: `toposwarm_meta_harness.py:376`
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### search `def search(self, query, top_k)`
- Defined: `toposwarm_meta_harness.py:392`
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### _search_st `def _search_st(self, query, top_k)`
- Defined: `toposwarm_meta_harness.py:401`
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### _search_tfidf `def _search_tfidf(self, query, top_k)`
- Defined: `toposwarm_meta_harness.py:412`
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### __init__ `def __init__(self, logger, capacity, dense)`
- Defined: `toposwarm_meta_harness.py:441`
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### _build_index `def _build_index(self)`
- Defined: `toposwarm_meta_harness.py:453`
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### _load_episode `def _load_episode(self, run_dir)`
- Defined: `toposwarm_meta_harness.py:464`
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### _episode_text `def _episode_text(score, traces)`
- Defined: `toposwarm_meta_harness.py:482`
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### store `def store(self, score, traces)`
- Defined: `toposwarm_meta_harness.py:493`
- Doc: Index a newly logged episode.
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### retrieve_similar `def retrieve_similar(self, prompt, tool_hint, top_k, min_score)`
- Defined: `toposwarm_meta_harness.py:505`
- Doc: Retrieve the top-k most similar prior episodes.
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### retrieve_confirmers_and_challengers `def retrieve_confirmers_and_challengers(self, draft_tool, prompt, top_k)`
- Defined: `toposwarm_meta_harness.py:549`
- Doc: Split retrieved episodes into confirmers (same tool, success) and
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### _tokenise `def _tokenise(text)`
- Defined: `toposwarm_meta_harness.py:573`
- Doc: Very simple whitespace + punctuation tokeniser.
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### __init__ `def __init__(self, cfg, logger)`
- Defined: `toposwarm_meta_harness.py:592`
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### gather_snapshot `def gather_snapshot(self, bridge)`
- Defined: `toposwarm_meta_harness.py:596`
- Doc: Collect environment state via the LazyOwnBridge.
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### _parse_list `def _parse_list(raw)`
- Defined: `toposwarm_meta_harness.py:680`
- Doc: Best-effort parse of newline / comma list output.
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### format_snapshot `def format_snapshot(self, snapshot, max_chars)`
- Defined: `toposwarm_meta_harness.py:687`
- Doc: Render the snapshot as a compact [Environment Snapshot] block suitable
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### __init__ `def __init__(self, cfg, memory, keyword_router, logger)`
- Defined: `toposwarm_meta_harness.py:754`
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### route `def route(self, prompt, snapshot_text)`
- Defined: `toposwarm_meta_harness.py:766`
- Doc: Draft-verify routing.
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### _reextract_arg `def _reextract_arg(prompt, tool_name, fallback)`
- Defined: `toposwarm_meta_harness.py:820`
- Doc: Best-effort arg re-extraction when the tool changes.
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### __init__ `def __init__(self, cfg, logger)`
- Defined: `toposwarm_meta_harness.py:846`
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### add `def add(self, config, metrics)`
- Defined: `toposwarm_meta_harness.py:855`
- Doc: Add a candidate to the population and return True if it lies on the
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### select_best `def select_best(self, preference)`
- Defined: `toposwarm_meta_harness.py:875`
- Doc: Select the best harness config according to a scalarised preference.
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### frontier_configs `def frontier_configs(self)`
- Defined: `toposwarm_meta_harness.py:907`
- Doc: Return all configs currently on the Pareto frontier.
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### _is_on_frontier `def _is_on_frontier(self, candidate)`
- Defined: `toposwarm_meta_harness.py:911`
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### _prune `def _prune(self)`
- Defined: `toposwarm_meta_harness.py:933`
- Doc: Remove oldest non-frontier entries when population grows too large.
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### __init__ `def __init__(self, cfg)`
- Defined: `toposwarm_meta_harness.py:965`
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### set_router `def set_router(self, keyword_router)`
- Defined: `toposwarm_meta_harness.py:980`
- Doc: Bind the draft verifier to the existing keyword router.
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### log_run `def log_run(self, harness_snapshot, trace_steps, score, reasoning)`
- Defined: `toposwarm_meta_harness.py:986`
- Doc: Persist one run and update in-memory indexes.
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### get_best_harness_config `def get_best_harness_config(self)`
- Defined: `toposwarm_meta_harness.py:999`
- Doc: Return the current Pareto-best harness configuration.
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

### query_experience `def query_experience(self, prompt, tool_hint, top_k)`
- Defined: `toposwarm_meta_harness.py:1003`
- Doc: Ad-hoc retrieval of prior episodes for prompt engineering.
- Imported by: `meta_harness_proposer.py`, `toposwarm_coevolve.py`, `toposwarm_coevolve.py`

## ts_utils.py

### setup_logger `def setup_logger(name, level)`
- Defined: `ts_utils.py:25`
- Doc: Return an idempotent logger with a single StreamHandler.
- Imported by: `topo_swarm_agent.py`, `toposwarm_continual_trainer.py`, `toposwarm_continual_trainer.py`

### safe_eval `def safe_eval(expr)`
- Defined: `ts_utils.py:42`
- Doc: Evaluate a numeric expression via AST — never calls eval() on arbitrary code.
- Imported by: `topo_swarm_agent.py`, `toposwarm_continual_trainer.py`, `toposwarm_continual_trainer.py`

### import_module `def import_module(name)`
- Defined: `ts_utils.py:62`
- Doc: Load a Python file as a named module.
- Imported by: `topo_swarm_agent.py`, `toposwarm_continual_trainer.py`, `toposwarm_continual_trainer.py`

### make_cached_encode `def make_cached_encode(tokenizer)`
- Defined: `ts_utils.py:86`
- Doc: Return a cached version of tokenizer.encode().
- Imported by: `topo_swarm_agent.py`, `toposwarm_continual_trainer.py`, `toposwarm_continual_trainer.py`

### make_cached_tool_token `def make_cached_tool_token(tokenizer)`
- Defined: `ts_utils.py:100`
- Doc: Return a cached version of tokenizer.tool_token().
- Imported by: `topo_swarm_agent.py`, `toposwarm_continual_trainer.py`, `toposwarm_continual_trainer.py`

### _cached_encode `def _cached_encode(text)`
- Defined: `ts_utils.py:94`
- Imported by: `topo_swarm_agent.py`, `toposwarm_continual_trainer.py`, `toposwarm_continual_trainer.py`

### _cached_tool_token `def _cached_tool_token(tool_name)`
- Defined: `ts_utils.py:103`
- Imported by: `topo_swarm_agent.py`, `toposwarm_continual_trainer.py`, `toposwarm_continual_trainer.py`
