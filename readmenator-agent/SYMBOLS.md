# Symbols

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `DatasetEnhancer` | class | `lazyown_dataset_enhancer.py:165` | `class DatasetEnhancer` |
| `ExperienceStoreReader` | class | `lazyown_dataset_enhancer.py:87` | `class ExperienceStoreReader` |
| `__init__` | method | `lazyown_dataset_enhancer.py:88` | `def __init__(self, log_dir)` |
| `__init__` | method | `lazyown_dataset_enhancer.py:166` | `def __init__(self, log_dir, max_runs)` |
| `_build_toolbench_record` | method | `lazyown_dataset_enhancer.py:149` | `def _build_toolbench_record(instruction, tool_name, arg, answer, domain)` |
| `_difficulty` | function | `lazyown_dataset_enhancer.py:64` | `def _difficulty(record)` |
| `_sanitize_output` | method | `lazyown_dataset_enhancer.py:136` | `def _sanitize_output(text)` |
| `add_negative_examples` | method | `lazyown_dataset_enhancer.py:236` | `def add_negative_examples(self, records, n)` |
| `augment_simple` | method | `lazyown_dataset_enhancer.py:276` | `def augment_simple(self, records, multiplier)` |
| `curriculum_sort` | method | `lazyown_dataset_enhancer.py:261` | `def curriculum_sort(self, records)` |
| `deduplicate` | method | `lazyown_dataset_enhancer.py:265` | `def deduplicate(self, records)` |
| `enhance` | method | `lazyown_dataset_enhancer.py:171` | `def enhance(self)` |
| `list_runs` | method | `lazyown_dataset_enhancer.py:91` | `def list_runs(self)` |
| `main` | method | `lazyown_dataset_enhancer.py:375` | `def main()` |
| `print_stats` | method | `lazyown_dataset_enhancer.py:348` | `def print_stats(records)` |
| `read_harness` | method | `lazyown_dataset_enhancer.py:122` | `def read_harness(self, run_dir)` |
| `read_score` | method | `lazyown_dataset_enhancer.py:113` | `def read_score(self, run_dir)` |
| `read_trace` | method | `lazyown_dataset_enhancer.py:98` | `def read_trace(self, run_dir)` |
| `run` | method | `lazyown_dataset_enhancer.py:301` | `def run(self, merge_with)` |
| `_apply_pentest_synonyms` | function | `lazyown_dataset_generator.py:3414` | `def _apply_pentest_synonyms(instr)` |
| `_expand` | function | `lazyown_dataset_generator.py:3430` | `def _expand(tool_name, phrasings)` |
| `_is_noisy_phrasing` | function | `lazyown_dataset_generator.py:3554` | `def _is_noisy_phrasing(instruction, arg)` |
| `_make_record` | function | `lazyown_dataset_generator.py:3321` | `def _make_record(tool_name, desc, category, instruction, arg)` |
| `build_dataset` | function | `lazyown_dataset_generator.py:3571` | `def build_dataset()` |
| `main` | function | `lazyown_dataset_generator.py:3616` | `def main()` |
| `print_stats` | function | `lazyown_dataset_generator.py:3602` | `def print_stats(records)` |
| `write_jsonl` | function | `lazyown_dataset_generator.py:3595` | `def write_jsonl(records, path)` |
| `ExperienceReader` | class | `meta_harness_proposer.py:150` | `class ExperienceReader` |
| `LLMClient` | class | `meta_harness_proposer.py:86` | `class LLMClient` |
| `LLMConfig` | class | `meta_harness_proposer.py:75` | `class LLMConfig` |
| `MetaHarnessProposer` | class | `meta_harness_proposer.py:392` | `class MetaHarnessProposer` |
| `PatchEngine` | class | `meta_harness_proposer.py:243` | `class PatchEngine` |
| `__init__` | method | `meta_harness_proposer.py:93` | `def __init__(self, cfg, logger)` |
| `__init__` | method | `meta_harness_proposer.py:153` | `def __init__(self, log_dir, logger)` |
| `__init__` | method | `meta_harness_proposer.py:246` | `def __init__(self, logger)` |
| `__init__` | method | `meta_harness_proposer.py:434` | `def __init__(self, log_dir, llm_cfg, logger)` |
| `_log_proposal` | method | `meta_harness_proposer.py:538` | `def _log_proposal(self, target_path, response, applied, diag)` |
| `_norm` | method | `meta_harness_proposer.py:331` | `def _norm(s)` |
| `_setup_logger` | function | `meta_harness_proposer.py:58` | `def _setup_logger(name, level)` |
| `_strip_line_numbers` | method | `meta_harness_proposer.py:283` | `def _strip_line_numbers(self, s)` |
| `_try_chat` | method | `meta_harness_proposer.py:97` | `def _try_chat(self, api_url, model, system, user)` |
| `apply_diff_hunk` | method | `meta_harness_proposer.py:316` | `def apply_diff_hunk(self, target_path, old_string, new_string, dry_run)` |
| `apply_full_rewrite` | method | `meta_harness_proposer.py:265` | `def apply_full_rewrite(self, target_path, new_code, dry_run)` |
| `apply_line_range` | method | `meta_harness_proposer.py:287` | `def apply_line_range(self, target_path, line_start, line_end, new_string, dry_run)` |
| `build_diagnostic_context` | method | `meta_harness_proposer.py:193` | `def build_diagnostic_context(self, top_k)` |
| `chat` | method | `meta_harness_proposer.py:121` | `def chat(self, system, user)` |
| `list_runs` | method | `meta_harness_proposer.py:157` | `def list_runs(self, n)` |
| `load_run` | method | `meta_harness_proposer.py:165` | `def load_run(self, run_dir)` |
| `main` | method | `meta_harness_proposer.py:572` | `def main()` |
| `propose_patch` | method | `meta_harness_proposer.py:445` | `def propose_patch(self, target_path, top_k, dry_run)` |
| `validate_syntax` | method | `meta_harness_proposer.py:249` | `def validate_syntax(self, code)` |
| `_load_enhancer_module` | function | `tests/test_dataset_enhancer.py:13` | `def _load_enhancer_module()` |
| `test_sanitize_email` | function | `tests/test_dataset_enhancer.py:44` | `def test_sanitize_email()` |
| `test_sanitize_idempotent_on_clean_text` | function | `tests/test_dataset_enhancer.py:50` | `def test_sanitize_idempotent_on_clean_text()` |
| `test_sanitize_ip` | function | `tests/test_dataset_enhancer.py:24` | `def test_sanitize_ip()` |
| `test_sanitize_ntlm_hash` | function | `tests/test_dataset_enhancer.py:38` | `def test_sanitize_ntlm_hash()` |
| `test_sanitize_password` | function | `tests/test_dataset_enhancer.py:31` | `def test_sanitize_password()` |
| `_load_gen_module` | function | `tests/test_dataset_generator.py:13` | `def _load_gen_module()` |
| `test_build_dataset_filters_noise` | function | `tests/test_dataset_generator.py:42` | `def test_build_dataset_filters_noise()` |
| `test_is_noisy_generic_verb_empty_arg` | function | `tests/test_dataset_generator.py:30` | `def test_is_noisy_generic_verb_empty_arg()` |
| `test_is_noisy_permitted_with_arg` | function | `tests/test_dataset_generator.py:36` | `def test_is_noisy_permitted_with_arg()` |
| `test_is_noisy_short_instruction` | function | `tests/test_dataset_generator.py:24` | `def test_is_noisy_short_instruction()` |
| `test_d_model_compatible_with_checkpoint` | function | `tests/test_model_config.py:11` | `def test_d_model_compatible_with_checkpoint()` |
| `TestKeywordRouter` | class | `tests/test_orchestrator.py:56` | `class TestKeywordRouter` |
| `TestNeuralRouter` | class | `tests/test_orchestrator.py:89` | `class TestNeuralRouter` |
| `TestOrchestratorRun` | class | `tests/test_orchestrator.py:193` | `class TestOrchestratorRun` |
| `TestSessionContext` | class | `tests/test_orchestrator.py:15` | `class TestSessionContext` |
| `_load_ctx` | method | `tests/test_orchestrator.py:18` | `def _load_ctx(self)` |
| `_load_router` | method | `tests/test_orchestrator.py:59` | `def _load_router(self)` |
| `mock_model_forward` | method | `tests/test_orchestrator.py:141` | `def mock_model_forward(ids)` |
| `mock_model_forward` | method | `tests/test_orchestrator.py:175` | `def mock_model_forward(ids)` |
| `mock_register_forward_hook` | method | `tests/test_orchestrator.py:135` | `def mock_register_forward_hook(cb)` |
| `mock_register_forward_hook` | method | `tests/test_orchestrator.py:169` | `def mock_register_forward_hook(cb)` |
| `orchestrator` | method | `tests/test_orchestrator.py:93` | `def orchestrator(self)` |
| `test_c2_keyword` | method | `tests/test_orchestrator.py:74` | `def test_c2_keyword(self)` |
| `test_config_keyword` | method | `tests/test_orchestrator.py:69` | `def test_config_keyword(self)` |
| `test_empty_prefix` | method | `tests/test_orchestrator.py:23` | `def test_empty_prefix(self)` |
| `test_extract_arg_ip` | method | `tests/test_orchestrator.py:84` | `def test_extract_arg_ip(self)` |
| `test_fallback_search` | method | `tests/test_orchestrator.py:79` | `def test_fallback_search(self)` |
| `test_findings_from_output` | method | `tests/test_orchestrator.py:49` | `def test_findings_from_output(self)` |
| `test_neural_route_low_confidence_fallback` | method | `tests/test_orchestrator.py:159` | `def test_neural_route_low_confidence_fallback(self, orchestrator)` |
| `test_neural_route_none_when_no_engine` | method | `tests/test_orchestrator.py:120` | `def test_neural_route_none_when_no_engine(self, orchestrator)` |
| `test_neural_route_with_mock_head` | method | `tests/test_orchestrator.py:123` | `def test_neural_route_with_mock_head(self, orchestrator)` |
| `test_phase_progression` | method | `tests/test_orchestrator.py:43` | `def test_phase_progression(self)` |
| `test_prefix_with_target` | method | `tests/test_orchestrator.py:28` | `def test_prefix_with_target(self)` |
| `test_recon_keyword` | method | `tests/test_orchestrator.py:63` | `def test_recon_keyword(self)` |
| `test_run_updates_session` | method | `tests/test_orchestrator.py:196` | `def test_run_updates_session(self)` |
| `test_update_extracts_ip` | method | `tests/test_orchestrator.py:35` | `def test_update_extracts_ip(self)` |
| `BPETokenizer` | class | `topo_swarm_agent.py:1693` | `class BPETokenizer` |
| `CheckpointManager` | class | `topo_swarm_agent.py:2046` | `class CheckpointManager` |
| `EpisodicMemory` | class | `topo_swarm_agent.py:1487` | `class EpisodicMemory` |
| `HRMModule` | class | `topo_swarm_agent.py:1103` | `class HRMModule(Module)` |
| `KappaDetector` | class | `topo_swarm_agent.py:2149` | `class KappaDetector` |
| `QuaternionAttention` | class | `topo_swarm_agent.py:998` | `class QuaternionAttention(Module)` |
| `QuaternionLinear` | class | `topo_swarm_agent.py:330` | `class QuaternionLinear(Module)` |
| `QuaternionOps` | class | `topo_swarm_agent.py:282` | `class QuaternionOps` |
| `QuaternionTorusBrain` | class | `topo_swarm_agent.py:807` | `class QuaternionTorusBrain(Module)` |
| `RMSNorm` | class | `topo_swarm_agent.py:465` | `class RMSNorm(Module)` |
| `RotaryEmbedding` | class | `topo_swarm_agent.py:489` | `class RotaryEmbedding(Module)` |
| `SpectralBottleneck` | class | `topo_swarm_agent.py:394` | `class SpectralBottleneck(Module)` |
| `SwarmConfig` | class | `topo_swarm_agent.py:84` | `class SwarmConfig` |
| `SwarmMoE` | class | `topo_swarm_agent.py:608` | `class SwarmMoE(Module)` |
| `SwarmMoEAdapter` | class | `topo_swarm_agent.py:665` | `class SwarmMoEAdapter(Module)` |
| `SwarmMoEGate` | class | `topo_swarm_agent.py:587` | `class SwarmMoEGate(Module)` |
| `SwarmOrchestrator` | class | `topo_swarm_agent.py:1602` | `class SwarmOrchestrator` |
| `SwarmTrainer` | class | `topo_swarm_agent.py:2192` | `class SwarmTrainer` |
| `SwiGLU` | class | `topo_swarm_agent.py:548` | `class SwiGLU(Module)` |
| `ToolBenchDataset` | class | `topo_swarm_agent.py:1811` | `class ToolBenchDataset(Dataset)` |
| `TopoSwarmLayer` | class | `topo_swarm_agent.py:1205` | `class TopoSwarmLayer(Module)` |
| `TopoSwarmModel` | class | `topo_swarm_agent.py:1273` | `class TopoSwarmModel(Module)` |
| `__getitem__` | method | `topo_swarm_agent.py:2020` | `def __getitem__(self, idx)` |
| `__init__` | method | `topo_swarm_agent.py:341` | `def __init__(self, in_features, out_features, bias, init_std)` |
| `__init__` | method | `topo_swarm_agent.py:406` | `def __init__(self, cfg)` |
| `__init__` | method | `topo_swarm_agent.py:468` | `def __init__(self, d_model, eps)` |
| `__init__` | method | `topo_swarm_agent.py:497` | `def __init__(self, d_head, max_seq_len, base, ntk_factor)` |
| `__init__` | method | `topo_swarm_agent.py:551` | `def __init__(self, d_model, hidden_dim, dropout)` |
| `__init__` | method | `topo_swarm_agent.py:590` | `def __init__(self, d_model, n_experts, top_k)` |
| `__init__` | method | `topo_swarm_agent.py:620` | `def __init__(self, d_model, expert_hidden_dim, n_experts, top_k, dropout)` |
| `__init__` | method | `topo_swarm_agent.py:679` | `def __init__(self, d_model, n_experts, top_k, bottleneck, dropout)` |
| `__init__` | method | `topo_swarm_agent.py:825` | `def __init__(self, cfg)` |
| `__init__` | method | `topo_swarm_agent.py:1006` | `def __init__(self, cfg)` |
| `__init__` | method | `topo_swarm_agent.py:1119` | `def __init__(self, cfg)` |
| `__init__` | method | `topo_swarm_agent.py:1213` | `def __init__(self, cfg)` |
| `__init__` | method | `topo_swarm_agent.py:1287` | `def __init__(self, cfg)` |
| `__init__` | method | `topo_swarm_agent.py:1497` | `def __init__(self, cfg)` |
| `__init__` | method | `topo_swarm_agent.py:1622` | `def __init__(self, model, cfg)` |
| `__init__` | method | `topo_swarm_agent.py:1701` | `def __init__(self, cfg)` |
| `__init__` | method | `topo_swarm_agent.py:1824` | `def __init__(self, cfg, tokenizer, split, logger)` |
| `__init__` | method | `topo_swarm_agent.py:2054` | `def __init__(self, cfg, logger)` |
| `__init__` | method | `topo_swarm_agent.py:2159` | `def __init__(self, cfg)` |
| `__init__` | method | `topo_swarm_agent.py:2206` | `def __init__(self, model, cfg, tokenizer, logger)` |
| `__len__` | method | `topo_swarm_agent.py:2017` | `def __len__(self)` |
| `__post_init__` | method | `topo_swarm_agent.py:202` | `def __post_init__(self)` |
| `_attn_fn` | method | `topo_swarm_agent.py:1237` | `def _attn_fn(self, x)` |
| `_build_cache` | method | `topo_swarm_agent.py:522` | `def _build_cache(self, seq_len)` |
| `_build_torus_graph` | method | `topo_swarm_agent.py:855` | `def _build_torus_graph(self)` |
| `_chunked_ce` | method | `topo_swarm_agent.py:1445` | `def _chunked_ce(logits, targets, chunk_size)` |
| `_decay` | method | `topo_swarm_agent.py:1591` | `def _decay(self)` |
| `_encode_record` | method | `topo_swarm_agent.py:1927` | `def _encode_record(self, rec)` |
| `_evaluate` | method | `topo_swarm_agent.py:2476` | `def _evaluate(self, val_dl)` |
| `_filter` | method | `topo_swarm_agent.py:428` | `def _filter(self, x, kr, ki)` |
| `_get_torus_positions` | method | `topo_swarm_agent.py:264` | `def _get_torus_positions(n_angular, n_radial, device)` |
| `_h_step` | method | `topo_swarm_agent.py:1163` | `def _h_step(self, z)` |
| `_head_filter` | method | `topo_swarm_agent.py:1039` | `def _head_filter(self, x)` |
| `_l_step` | method | `topo_swarm_agent.py:1156` | `def _l_step(self, x, state)` |
| `_load` | method | `topo_swarm_agent.py:1846` | `def _load(self, split)` |
| `_make_optimizer` | method | `topo_swarm_agent.py:2233` | `def _make_optimizer(self, lr)` |
| `_manual_attn` | method | `topo_swarm_agent.py:1072` | `def _manual_attn()` |
| `_message_passing` | method | `topo_swarm_agent.py:909` | `def _message_passing(self, node_feat)` |
| `_param_count` | method | `topo_swarm_agent.py:253` | `def _param_count(module)` |
| `_phase0_calibrate` | method | `topo_swarm_agent.py:2322` | `def _phase0_calibrate(self, dataloader, n_steps)` |
| `_rotate_half` | method | `topo_swarm_agent.py:530` | `def _rotate_half(self, x)` |
| `_set_seed` | method | `topo_swarm_agent.py:243` | `def _set_seed(seed, device)` |
| `_setup_logger` | method | `topo_swarm_agent.py:225` | `def _setup_logger(name, level)` |
| `_synthetic_stubs` | method | `topo_swarm_agent.py:1984` | `def _synthetic_stubs(self, n)` |
| `_torus_soft_assign` | method | `topo_swarm_agent.py:887` | `def _torus_soft_assign(self, phi1, phi2)` |
| `_train_one_batch` | method | `topo_swarm_agent.py:2280` | `def _train_one_batch(self, optimizer, input_ids, targets, accum_step, berry_phase)` |
| `_warmup_cosine_lr` | method | `topo_swarm_agent.py:2263` | `def _warmup_cosine_lr(self, optimizer, step, total_steps, warmup_steps, base_lr)` |
| `berry_phase_rotation` | method | `topo_swarm_agent.py:309` | `def berry_phase_rotation(q, phase)` |
| `build_dataloaders` | method | `topo_swarm_agent.py:2509` | `def build_dataloaders(cfg, tokenizer, logger)` |
| `compute_surprise` | method | `topo_swarm_agent.py:1512` | `def compute_surprise(logits, targets, gate_mean)` |
| `decode` | method | `topo_swarm_agent.py:1751` | `def decode(self, ids)` |
| `encode` | method | `topo_swarm_agent.py:1739` | `def encode(self, text)` |
| `encode_tool_trace` | method | `topo_swarm_agent.py:1778` | `def encode_tool_trace(self, instruction, tool_name, result)` |
| `forward` | method | `topo_swarm_agent.py:370` | `def forward(self, x)` |
| `forward` | method | `topo_swarm_agent.py:436` | `def forward(self, x)` |
| `forward` | method | `topo_swarm_agent.py:478` | `def forward(self, x)` |
| `forward` | method | `topo_swarm_agent.py:534` | `def forward(self, x, seq_len)` |
| `forward` | method | `topo_swarm_agent.py:566` | `def forward(self, x)` |
| `forward` | method | `topo_swarm_agent.py:597` | `def forward(self, x)` |
| `forward` | method | `topo_swarm_agent.py:637` | `def forward(self, x)` |
| `forward` | method | `topo_swarm_agent.py:705` | `def forward(self, x)` |
| `forward` | method | `topo_swarm_agent.py:940` | `def forward(self, x, berry_phase)` |
| `forward` | method | `topo_swarm_agent.py:1045` | `def forward(self, x, is_causal)` |
| `forward` | method | `topo_swarm_agent.py:1167` | `def forward(self, x)` |
| `forward` | method | `topo_swarm_agent.py:1240` | `def forward(self, x, berry_phase)` |
| `forward` | method | `topo_swarm_agent.py:1311` | `def forward(self, input_ids, berry_phase, targets)` |
| `generate` | method | `topo_swarm_agent.py:1392` | `def generate(self, input_ids, max_new_tokens, temperature, top_k, berry_phase, act_halt_threshold)` |
| `hamilton_product` | method | `topo_swarm_agent.py:289` | `def hamilton_product(q1, q2)` |
| `infer` | method | `topo_swarm_agent.py:1640` | `def infer(self, input_ids, tokenizer, max_new_tokens, temperature, top_k)` |
| `inject_moe_adapter` | method | `topo_swarm_agent.py:749` | `def inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)` |
| `load` | method | `topo_swarm_agent.py:738` | `def load(cls, path)` |
| `load` | method | `topo_swarm_agent.py:2108` | `def load(self, model, optimizer, device)` |
| `main` | method | `topo_swarm_agent.py:2552` | `def main()` |
| `normalize` | method | `topo_swarm_agent.py:304` | `def normalize(q, eps)` |
| `sample` | method | `topo_swarm_agent.py:1558` | `def sample(self, n)` |
| `save` | method | `topo_swarm_agent.py:727` | `def save(self, path)` |
| `save` | method | `topo_swarm_agent.py:2066` | `def save(self, model, optimizer, meta, force)` |
| `store` | method | `topo_swarm_agent.py:1537` | `def store(self, episode, surprise)` |
| `tool_token` | method | `topo_swarm_agent.py:1756` | `def tool_token(self, tool_name)` |
| `train` | method | `topo_swarm_agent.py:2363` | `def train(self, train_dl, val_dl, resume)` |
| `update` | method | `topo_swarm_agent.py:2167` | `def update(self, loss)` |
| `BPETokenizer` | class | `topogpt2_1.py:1082` | `class BPETokenizer` |
| `CheckpointManager` | class | `topogpt2_1.py:1220` | `class CheckpointManager` |
| `CorpusDownloader` | class | `topogpt2_1.py:1107` | `class CorpusDownloader` |
| `MechanisticMetrics` | class | `topogpt2_1.py:1746` | `class MechanisticMetrics` |
| `MultiHeadAttention` | class | `topogpt2_1.py:847` | `class MultiHeadAttention(Module)` |
| `Phase0_KernelOptimizer` | class | `topogpt2_1.py:1983` | `class Phase0_KernelOptimizer` |
| `Phase1_BatchProspector` | class | `topogpt2_1.py:2058` | `class Phase1_BatchProspector` |
| `Phase2_SeedMiner` | class | `topogpt2_1.py:2141` | `class Phase2_SeedMiner` |
| `Phase4_AnnealingRefiner` | class | `topogpt2_1.py:2223` | `class Phase4_AnnealingRefiner` |
| `QuaternionLinear` | class | `topogpt2_1.py:216` | `class QuaternionLinear(Module)` |
| `QuaternionOps` | class | `topogpt2_1.py:177` | `class QuaternionOps` |
| `QuaternionSpectralLayer` | class | `topogpt2_1.py:261` | `class QuaternionSpectralLayer(Module)` |
| `QuaternionTorusBrain` | class | `topogpt2_1.py:431` | `class QuaternionTorusBrain(Module)` |
| `RMSNorm` | class | `topogpt2_1.py:696` | `class RMSNorm(Module)` |
| `RotaryEmbedding` | class | `topogpt2_1.py:648` | `class RotaryEmbedding(Module)` |
| `SpectralAutoencoder` | class | `topogpt2_1.py:348` | `class SpectralAutoencoder(Module)` |
| `SwiGLU` | class | `topogpt2_1.py:713` | `class SwiGLU(Module)` |
| `TokenizedDataset` | class | `topogpt2_1.py:1170` | `class TokenizedDataset(Dataset)` |
| `TopoGPT2` | class | `topogpt2_1.py:976` | `class TopoGPT2(Module)` |
| `TopoGPT2Config` | class | `topogpt2_1.py:55` | `class TopoGPT2Config` |
| `TopoGPT2Layer` | class | `topogpt2_1.py:929` | `class TopoGPT2Layer(Module)` |
| `TopoGPT2Trainer` | class | `topogpt2_1.py:1453` | `class TopoGPT2Trainer` |
| `TopoMoEBrain` | class | `topogpt2_1.py:742` | `class TopoMoEBrain(Module)` |
| `TopoPhasePipeline` | class | `topogpt2_1.py:2384` | `class TopoPhasePipeline` |
| `__getitem__` | method | `topogpt2_1.py:1209` | `def __getitem__(self, idx)` |
| `__init__` | method | `topogpt2_1.py:228` | `def __init__(self, in_features, out_features, bias)` |
| `__init__` | method | `topogpt2_1.py:281` | `def __init__(self, in_q, out_q, grid_h, grid_w, init_scale)` |
| `__init__` | method | `topogpt2_1.py:361` | `def __init__(self, config)` |
| `__init__` | method | `topogpt2_1.py:449` | `def __init__(self, d_model, config)` |
| `__init__` | method | `topogpt2_1.py:655` | `def __init__(self, d_head, max_seq_len, base)` |
| `__init__` | method | `topogpt2_1.py:699` | `def __init__(self, d_model, eps)` |
| `__init__` | method | `topogpt2_1.py:720` | `def __init__(self, d_model, expansion, dropout)` |
| `__init__` | method | `topogpt2_1.py:757` | `def __init__(self, d_model, config)` |
| `__init__` | method | `topogpt2_1.py:857` | `def __init__(self, d_model, n_heads, config)` |
| `__init__` | method | `topogpt2_1.py:938` | `def __init__(self, d_model, n_heads, config)` |
| `__init__` | method | `topogpt2_1.py:987` | `def __init__(self, config)` |
| `__init__` | method | `topogpt2_1.py:1085` | `def __init__(self, encoding)` |
| `__init__` | method | `topogpt2_1.py:1119` | `def __init__(self, corpus, data_dir, logger)` |
| `__init__` | method | `topogpt2_1.py:1179` | `def __init__(self, text, tokenizer, seq_len, max_tokens, cache_dir, split_tag)` |
| `__init__` | method | `topogpt2_1.py:1245` | `def __init__(self, config, logger)` |
| `__init__` | method | `topogpt2_1.py:1465` | `def __init__(self, model, config, tokenizer)` |
| `__init__` | method | `topogpt2_1.py:1766` | `def __init__(self, config)` |
| `__init__` | method | `topogpt2_1.py:2001` | `def __init__(self, config, logger)` |
| `__init__` | method | `topogpt2_1.py:2074` | `def __init__(self, config, logger)` |
| `__init__` | method | `topogpt2_1.py:2157` | `def __init__(self, config, logger)` |
| `__init__` | method | `topogpt2_1.py:2243` | `def __init__(self, trainer, t0, cooling_rate, stagnation_patience)` |
| `__init__` | method | `topogpt2_1.py:2404` | `def __init__(self, config, train_dataset, val_dataset, tokenizer, logger)` |
| `__len__` | method | `topogpt2_1.py:1206` | `def __len__(self)` |
| `__post_init__` | method | `topogpt2_1.py:124` | `def __post_init__(self)` |
| `_build_cache` | method | `topogpt2_1.py:661` | `def _build_cache(self, seq_len)` |
| `_build_torus_graph` | method | `topogpt2_1.py:489` | `def _build_torus_graph(self)` |
| `_contract` | method | `topogpt2_1.py:303` | `def _contract(self, W, X)` |
| `_cosine_lr` | method | `topogpt2_1.py:1536` | `def _cosine_lr(self, step_in_session, total_steps_session)` |
| `_current_state` | method | `topogpt2_1.py:1525` | `def _current_state(self)` |
| `_download_hf` | method | `topogpt2_1.py:1150` | `def _download_hf(self, dataset_name, split, text_column, name)` |
| `_filter1d` | method | `topogpt2_1.py:393` | `def _filter1d(self, x, kr, ki)` |
| `_forward_impl` | method | `topogpt2_1.py:947` | `def _forward_impl(self, x, past_kv)` |
| `_init_weights` | method | `topogpt2_1.py:1006` | `def _init_weights(self)` |
| `_kernel` | method | `topogpt2_1.py:300` | `def _kernel(self, c)` |
| `_load_model` | method | `topogpt2_1.py:1297` | `def _load_model(self, model, directory)` |
| `_load_optimizer` | method | `topogpt2_1.py:1331` | `def _load_optimizer(self, optimizer, directory, device)` |
| `_load_state` | method | `topogpt2_1.py:1345` | `def _load_state(self, directory)` |
| `_make_dataloaders` | method | `topogpt2_1.py:2414` | `def _make_dataloaders(self, batch_size)` |
| `_measure_ratio` | method | `topogpt2_1.py:2005` | `def _measure_ratio(self, ratio, sample_batch)` |
| `_message_passing` | method | `topogpt2_1.py:550` | `def _message_passing(self, node_feat)` |
| `_rotate_half` | method | `topogpt2_1.py:668` | `def _rotate_half(self, x)` |
| `_route` | method | `topogpt2_1.py:778` | `def _route(self, x)` |
| `_sample_text` | method | `topogpt2_1.py:1684` | `def _sample_text(self, tokenizer, prompts, max_new, temperature, top_k)` |
| `_save_model` | method | `topogpt2_1.py:1284` | `def _save_model(self, model, directory)` |
| `_save_optimizer` | method | `topogpt2_1.py:1328` | `def _save_optimizer(self, optimizer, directory)` |
| `_save_state` | method | `topogpt2_1.py:1340` | `def _save_state(self, state, directory)` |
| `_set_lr` | method | `topogpt2_1.py:1544` | `def _set_lr(self, lr)` |
| `_torus_soft_assign` | method | `topogpt2_1.py:523` | `def _torus_soft_assign(self, phi1, phi2)` |
| `ckpt_fn` | method | `topogpt2_1.py:964` | `def ckpt_fn(x_in)` |
| `classify_phase` | method | `topogpt2_1.py:1921` | `def classify_phase(self, delta, kappa, berry)` |
| `compute_all` | method | `topogpt2_1.py:1940` | `def compute_all(self, model, lr, dataloader, compute_kappa)` |
| `compute_alpha` | method | `topogpt2_1.py:1781` | `def compute_alpha(self, delta)` |
| `compute_berry_phase` | method | `topogpt2_1.py:1878` | `def compute_berry_phase(self, model)` |
| `compute_delta` | method | `topogpt2_1.py:1774` | `def compute_delta(self, model)` |
| `compute_kappa` | method | `topogpt2_1.py:1820` | `def compute_kappa(self, model, dataloader, n_batches)` |
| `compute_lc` | method | `topogpt2_1.py:1891` | `def compute_lc(self, model)` |
| `compute_sp` | method | `topogpt2_1.py:1905` | `def compute_sp(self, model)` |
| `compute_t_eff` | method | `topogpt2_1.py:1812` | `def compute_t_eff(self, lr)` |
| `conjugate` | method | `topogpt2_1.py:201` | `def conjugate(q)` |
| `count_params` | method | `topogpt2_1.py:1036` | `def count_params(self)` |
| `decode` | method | `topogpt2_1.py:404` | `def decode(self, z)` |
| `decode` | method | `topogpt2_1.py:1096` | `def decode(self, tokens)` |
| `encode` | method | `topogpt2_1.py:399` | `def encode(self, x)` |
| `encode` | method | `topogpt2_1.py:1093` | `def encode(self, text)` |
| `eot_token` | method | `topogpt2_1.py:1099` | `def eot_token(self)` |
| `evaluate` | method | `topogpt2_1.py:1716` | `def evaluate(self, dataloader)` |
| `format_log` | method | `topogpt2_1.py:1965` | `def format_log(self, m)` |
| `forward` | method | `topogpt2_1.py:244` | `def forward(self, x)` |
| `forward` | method | `topogpt2_1.py:307` | `def forward(self, x)` |
| `forward` | method | `topogpt2_1.py:409` | `def forward(self, x)` |
| `forward` | method | `topogpt2_1.py:587` | `def forward(self, x)` |
| `forward` | method | `topogpt2_1.py:672` | `def forward(self, q, k, seq_len, offset)` |
| `forward` | method | `topogpt2_1.py:704` | `def forward(self, x)` |
| `forward` | method | `topogpt2_1.py:734` | `def forward(self, x)` |
| `forward` | method | `topogpt2_1.py:820` | `def forward(self, x)` |
| `forward` | method | `topogpt2_1.py:875` | `def forward(self, x, is_causal, past_kv)` |
| `forward` | method | `topogpt2_1.py:956` | `def forward(self, x, past_kv)` |
| `forward` | method | `topogpt2_1.py:1013` | `def forward(self, token_ids, past_kvs)` |
| `generate` | method | `topogpt2_1.py:1042` | `def generate(self, token_ids, max_new_tokens, temperature, top_k)` |
| `get_text` | method | `topogpt2_1.py:1125` | `def get_text(self, split)` |
| `hamilton_product` | method | `topogpt2_1.py:185` | `def hamilton_product(q1, q2)` |
| `has_checkpoint` | method | `topogpt2_1.py:1443` | `def has_checkpoint(self)` |
| `load_best` | method | `topogpt2_1.py:1431` | `def load_best(self, model)` |
| `load_latest` | method | `topogpt2_1.py:1404` | `def load_latest(self, model, optimizer)` |
| `main` | method | `topogpt2_1.py:2506` | `def main()` |
| `mine` | method | `topogpt2_1.py:2161` | `def mine(self, seed_start, n_seeds, train_dataset, prospect_steps)` |
| `normalize` | method | `topogpt2_1.py:197` | `def normalize(q, eps)` |
| `optimize` | method | `topogpt2_1.py:2034` | `def optimize(self, dataloader)` |
| `patch_config_for_resume` | method | `topogpt2_1.py:1255` | `def patch_config_for_resume(self, cfg)` |
| `process_torus_grid` | method | `topogpt2_1.py:416` | `def process_torus_grid(self, grid)` |
| `prospect` | method | `topogpt2_1.py:2078` | `def prospect(self, candidates, train_dataset, prospect_steps)` |
| `refine` | method | `topogpt2_1.py:2252` | `def refine(self, train_dl, val_dl, refine_epochs)` |
| `resume` | method | `topogpt2_1.py:1500` | `def resume(self)` |
| `rotate_vector` | method | `topogpt2_1.py:206` | `def rotate_vector(v, q)` |
| `run` | method | `topogpt2_1.py:2426` | `def run(self, run_prospect, refine_epochs, resume, prospect_steps, probe_seeds, seed_start)` |
| `save` | method | `topogpt2_1.py:1359` | `def save(self, model, optimizer, state, is_best)` |
| `set_seed` | method | `topogpt2_1.py:165` | `def set_seed(seed, device)` |
| `setup_logger` | method | `topogpt2_1.py:155` | `def setup_logger(name, level)` |
| `should_save` | method | `topogpt2_1.py:1356` | `def should_save(self)` |
| `train` | method | `topogpt2_1.py:1548` | `def train(self, train_dl, val_dl)` |
| `update_grad_buffer` | method | `topogpt2_1.py:1786` | `def update_grad_buffer(self, model)` |
| `CoEvolutionEngine` | class | `toposwarm_coevolve.py:451` | `class CoEvolutionEngine` |
| `HarnessEvaluator` | class | `toposwarm_coevolve.py:233` | `class HarnessEvaluator` |
| `HarnessMutation` | class | `toposwarm_coevolve.py:128` | `class HarnessMutation` |
| `MockLazyOwnBridge` | class | `toposwarm_coevolve.py:183` | `class MockLazyOwnBridge` |
| `WeightTrainer` | class | `toposwarm_coevolve.py:391` | `class WeightTrainer` |
| `__init__` | method | `toposwarm_coevolve.py:190` | `def __init__(self)` |
| `__init__` | method | `toposwarm_coevolve.py:244` | `def __init__(self, prompts, lazyown_dir, logger, use_mock_bridge)` |
| `__init__` | method | `toposwarm_coevolve.py:397` | `def __init__(self, logger)` |
| `__init__` | method | `toposwarm_coevolve.py:456` | `def __init__(self, generations, population_size, train_steps_per_gen, proposer_interval, lazyown_dir, logger)` |
| `_build_orchestrator` | method | `toposwarm_coevolve.py:313` | `def _build_orchestrator(self, cfg_dict)` |
| `_clip` | method | `toposwarm_coevolve.py:175` | `def _clip(x, lo, hi)` |
| `_is_on_frontier` | method | `toposwarm_coevolve.py:575` | `def _is_on_frontier(self, cfg, metrics)` |
| `_load` | method | `toposwarm_coevolve.py:402` | `def _load(self)` |
| `_log_run` | method | `toposwarm_coevolve.py:343` | `def _log_run(self, orch, prompt, result, latency_ms, ctx_len, ok, cfg_dict)` |
| `_next_generation` | method | `toposwarm_coevolve.py:550` | `def _next_generation(self, scores)` |
| `_report_frontier` | method | `toposwarm_coevolve.py:635` | `def _report_frontier(self)` |
| `_resolve_lazyown_dir` | function | `toposwarm_coevolve.py:63` | `def _resolve_lazyown_dir()` |
| `_run_proposer` | method | `toposwarm_coevolve.py:596` | `def _run_proposer(self)` |
| `_save_state` | method | `toposwarm_coevolve.py:619` | `def _save_state(self, generation)` |
| `_setup_logger` | function | `toposwarm_coevolve.py:90` | `def _setup_logger(name, level)` |
| `_tournament_select` | method | `toposwarm_coevolve.py:567` | `def _tournament_select(sorted_scores, k)` |
| `available` | method | `toposwarm_coevolve.py:196` | `def available(self)` |
| `crossover` | method | `toposwarm_coevolve.py:167` | `def crossover(a, b)` |
| `evaluate` | method | `toposwarm_coevolve.py:256` | `def evaluate(self, cfg_dict)` |
| `fine_tune` | method | `toposwarm_coevolve.py:418` | `def fine_tune(self, dataset_path, steps, learning_rate)` |
| `get_config` | method | `toposwarm_coevolve.py:222` | `def get_config(self)` |
| `is_available` | method | `toposwarm_coevolve.py:415` | `def is_available(self)` |
| `load_state` | method | `toposwarm_coevolve.py:628` | `def load_state(self, path)` |
| `main` | method | `toposwarm_coevolve.py:646` | `def main()` |
| `mutate` | method | `toposwarm_coevolve.py:132` | `def mutate(cfg_dict)` |
| `run` | method | `toposwarm_coevolve.py:199` | `def run(self, command, timeout)` |
| `run` | method | `toposwarm_coevolve.py:490` | `def run(self)` |
| `set_config` | method | `toposwarm_coevolve.py:225` | `def set_config(self, key, value)` |
| `ContinualConfig` | class | `toposwarm_continual_trainer.py:111` | `class ContinualConfig` |
| `ContinualTrainer` | class | `toposwarm_continual_trainer.py:730` | `class ContinualTrainer` |
| `EWC` | class | `toposwarm_continual_trainer.py:365` | `class EWC` |
| `ReplayBuffer` | class | `toposwarm_continual_trainer.py:334` | `class ReplayBuffer` |
| `RoutingHead` | class | `toposwarm_continual_trainer.py:600` | `class RoutingHead(Module)` |
| `SurpriseBuffer` | class | `toposwarm_continual_trainer.py:166` | `class SurpriseBuffer` |
| `SwarmLiquidNeuron` | class | `toposwarm_continual_trainer.py:514` | `class SwarmLiquidNeuron(Module)` |
| `ToolBenchDataset` | class | `toposwarm_continual_trainer.py:300` | `class ToolBenchDataset(Dataset)` |
| `__getitem__` | method | `toposwarm_continual_trainer.py:315` | `def __getitem__(self, idx)` |
| `__init__` | method | `toposwarm_continual_trainer.py:180` | `def __init__(self, maxsize, replay_ratio)` |
| `__init__` | method | `toposwarm_continual_trainer.py:301` | `def __init__(self, records, tok, cfg)` |
| `__init__` | method | `toposwarm_continual_trainer.py:343` | `def __init__(self, records, max_size, tok, cfg)` |
| `__init__` | method | `toposwarm_continual_trainer.py:380` | `def __init__(self, model, cfg, cl_cfg, tok, logger)` |
| `__init__` | method | `toposwarm_continual_trainer.py:534` | `def __init__(self, d_model, n_tools)` |
| `__init__` | method | `toposwarm_continual_trainer.py:614` | `def __init__(self, d_model, tool_names, n_experts, top_k, hidden_dim)` |
| `__init__` | method | `toposwarm_continual_trainer.py:746` | `def __init__(self, model, cfg, cl_cfg, tok, ewc, replay, logger, routing_head)` |
| `__len__` | method | `toposwarm_continual_trainer.py:223` | `def __len__(self)` |
| `__len__` | method | `toposwarm_continual_trainer.py:312` | `def __len__(self)` |
| `__len__` | method | `toposwarm_continual_trainer.py:356` | `def __len__(self)` |
| `_accuracy` | method | `toposwarm_continual_trainer.py:1153` | `def _accuracy(records, label)` |
| `_capture` | method | `toposwarm_continual_trainer.py:995` | `def _capture(module, inp, out_h)` |
| `_collate` | method | `toposwarm_continual_trainer.py:319` | `def _collate(batch)` |
| `_encode_record` | method | `toposwarm_continual_trainer.py:247` | `def _encode_record(record, tok, cfg)` |
| `_hook` | method | `toposwarm_continual_trainer.py:887` | `def _hook(m, i, o)` |
| `_import` | function | `toposwarm_continual_trainer.py:91` | `def _import(name, filename)` |
| `_load_jsonl` | method | `toposwarm_continual_trainer.py:232` | `def _load_jsonl(path)` |
| `_lr_schedule` | method | `toposwarm_continual_trainer.py:821` | `def _lr_schedule(optimizer, step, total, warmup, base_lr)` |
| `_make_optimizer` | method | `toposwarm_continual_trainer.py:782` | `def _make_optimizer(self)` |
| `_merge_with_replay` | method | `toposwarm_continual_trainer.py:830` | `def _merge_with_replay(self, ids, tgt)` |
| `_routing_accuracy` | method | `toposwarm_continual_trainer.py:863` | `def _routing_accuracy(self, records)` |
| `_setup_logger` | method | `toposwarm_continual_trainer.py:158` | `def _setup_logger(level)` |
| `build_model_and_tok` | method | `toposwarm_continual_trainer.py:1195` | `def build_model_and_tok(cl_cfg, logger)` |
| `compute` | method | `toposwarm_continual_trainer.py:401` | `def compute(self, toolbench_records)` |
| `evaluate_routing` | method | `toposwarm_continual_trainer.py:1137` | `def evaluate_routing(model, cfg, tok, lazyown_records, toolbench_records, logger)` |
| `forward` | method | `toposwarm_continual_trainer.py:551` | `def forward(self, x)` |
| `forward` | method | `toposwarm_continual_trainer.py:654` | `def forward(self, hidden)` |
| `hebbian_update` | method | `toposwarm_continual_trainer.py:570` | `def hebbian_update(self, pre, labels)` |
| `label` | method | `toposwarm_continual_trainer.py:685` | `def label(self, tool_name)` |
| `load` | method | `toposwarm_continual_trainer.py:470` | `def load(self, path)` |
| `load` | method | `toposwarm_continual_trainer.py:706` | `def load(cls, d_model, path)` |
| `main` | method | `toposwarm_continual_trainer.py:1384` | `def main()` |
| `n_tools` | method | `toposwarm_continual_trainer.py:651` | `def n_tools(self)` |
| `penalty` | method | `toposwarm_continual_trainer.py:481` | `def penalty(self)` |
| `predict` | method | `toposwarm_continual_trainer.py:688` | `def predict(self, hidden)` |
| `run_full_pipeline` | method | `toposwarm_continual_trainer.py:1217` | `def run_full_pipeline(cl_cfg, logger)` |
| `sample` | method | `toposwarm_continual_trainer.py:213` | `def sample(self, batch_size)` |
| `sample` | method | `toposwarm_continual_trainer.py:351` | `def sample(self, n)` |
| `save` | method | `toposwarm_continual_trainer.py:465` | `def save(self, path)` |
| `save` | method | `toposwarm_continual_trainer.py:695` | `def save(self, path)` |
| `train` | method | `toposwarm_continual_trainer.py:923` | `def train(self, lazyown_dataset, train_records, val_records)` |
| `update` | method | `toposwarm_continual_trainer.py:186` | `def update(self, records, task_losses, logits)` |
| `HybridConfig` | class | `toposwarm_hybrid.py:115` | `class HybridConfig` |
| `HybridOrchestrator` | class | `toposwarm_hybrid.py:977` | `class HybridOrchestrator` |
| `HybridResult` | class | `toposwarm_hybrid.py:946` | `class HybridResult` |
| `LanguageBackend` | class | `toposwarm_hybrid.py:465` | `class LanguageBackend` |
| `ToolRegistry` | class | `toposwarm_hybrid.py:231` | `class ToolRegistry` |
| `ToolResult` | class | `toposwarm_hybrid.py:218` | `class ToolResult` |
| `TopoSwarmRouter` | class | `toposwarm_hybrid.py:396` | `class TopoSwarmRouter` |
| `__init__` | method | `toposwarm_hybrid.py:221` | `def __init__(self, tool_name, arg, output, ok)` |
| `__init__` | method | `toposwarm_hybrid.py:234` | `def __init__(self, cfg)` |
| `__init__` | method | `toposwarm_hybrid.py:409` | `def __init__(self, cfg, registry, logger)` |
| `__init__` | method | `toposwarm_hybrid.py:475` | `def __init__(self, cfg, logger)` |
| `__init__` | method | `toposwarm_hybrid.py:988` | `def __init__(self, cfg, logger)` |
| `__str__` | method | `toposwarm_hybrid.py:227` | `def __str__(self)` |
| `_cfg_score` | method | `toposwarm_hybrid.py:703` | `def _cfg_score(cls)` |
| `_eval` | method | `toposwarm_hybrid.py:192` | `def _eval(node)` |
| `_generate` | method | `toposwarm_hybrid.py:540` | `def _generate(prompt_text)` |
| `_generate` | method | `toposwarm_hybrid.py:812` | `def _generate(prompt_text)` |
| `_generate` | method | `toposwarm_hybrid.py:835` | `def _generate(prompt_text)` |
| `_http_get` | method | `toposwarm_hybrid.py:299` | `def _http_get(self, url)` |
| `_import_agent` | function | `toposwarm_hybrid.py:85` | `def _import_agent()` |
| `_import_topogpt` | method | `toposwarm_hybrid.py:563` | `def _import_topogpt(self)` |
| `_is_useful_output` | method | `toposwarm_hybrid.py:918` | `def _is_useful_output(text, min_chars)` |
| `_load` | method | `toposwarm_hybrid.py:428` | `def _load(self)` |
| `_load` | method | `toposwarm_hybrid.py:486` | `def _load(self)` |
| `_load_checkpoint` | method | `toposwarm_hybrid.py:588` | `def _load_checkpoint(self)` |
| `_load_tinystories` | method | `toposwarm_hybrid.py:507` | `def _load_tinystories(self)` |
| `_register` | method | `toposwarm_hybrid.py:240` | `def _register(self)` |
| `_register_all` | method | `toposwarm_hybrid.py:304` | `def _register_all(self)` |
| `_safe_eval` | method | `toposwarm_hybrid.py:182` | `def _safe_eval(expr)` |
| `_setup_logger` | method | `toposwarm_hybrid.py:164` | `def _setup_logger(name, level)` |
| `_template_answer` | method | `toposwarm_hybrid.py:887` | `def _template_answer(tool_name, tool_arg, tool_result)` |
| `calc_expr` | method | `toposwarm_hybrid.py:331` | `def calc_expr(expr)` |
| `decorator` | method | `toposwarm_hybrid.py:241` | `def decorator(fn)` |
| `echo` | method | `toposwarm_hybrid.py:383` | `def echo(text)` |
| `execute` | method | `toposwarm_hybrid.py:287` | `def execute(self, tool_name, arg)` |
| `generate` | method | `toposwarm_hybrid.py:859` | `def generate(self, prompt, tool_result)` |
| `get_datetime` | method | `toposwarm_hybrid.py:335` | `def get_datetime(tz_hint)` |
| `get_news` | method | `toposwarm_hybrid.py:373` | `def get_news(topic)` |
| `get_weather` | method | `toposwarm_hybrid.py:308` | `def get_weather(city)` |
| `main` | method | `toposwarm_hybrid.py:1051` | `def main()` |
| `pretty` | method | `toposwarm_hybrid.py:958` | `def pretty(self)` |
| `resolve` | method | `toposwarm_hybrid.py:249` | `def resolve(self, raw)` |
| `route` | method | `toposwarm_hybrid.py:261` | `def route(self, prompt)` |
| `route` | method | `toposwarm_hybrid.py:441` | `def route(self, prompt)` |
| `run` | method | `toposwarm_hybrid.py:1000` | `def run(self, prompt)` |
| `search_web` | method | `toposwarm_hybrid.py:319` | `def search_web(query)` |
| `tool_names` | method | `toposwarm_hybrid.py:387` | `def tool_names(self)` |
| `translate` | method | `toposwarm_hybrid.py:341` | `def translate(text)` |
| `InferenceConfig` | class | `toposwarm_infer.py:84` | `class InferenceConfig` |
| `InferenceEngine` | class | `toposwarm_infer.py:483` | `class InferenceEngine` |
| `InferenceResult` | class | `toposwarm_infer.py:883` | `class InferenceResult` |
| `ToolCallParser` | class | `toposwarm_infer.py:438` | `class ToolCallParser` |
| `ToolRegistry` | class | `toposwarm_infer.py:210` | `class ToolRegistry` |
| `ToolResult` | class | `toposwarm_infer.py:189` | `class ToolResult` |
| `__init__` | method | `toposwarm_infer.py:192` | `def __init__(self, tool_name, arg, output, ok)` |
| `__init__` | method | `toposwarm_infer.py:219` | `def __init__(self, cfg)` |
| `__init__` | method | `toposwarm_infer.py:446` | `def __init__(self, cfg)` |
| `__init__` | method | `toposwarm_infer.py:495` | `def __init__(self, cfg, agent_cfg, logger)` |
| `__str__` | method | `toposwarm_infer.py:205` | `def __str__(self)` |
| `_encode_prompt` | method | `toposwarm_infer.py:538` | `def _encode_prompt(self, text)` |
| `_eval` | method | `toposwarm_infer.py:157` | `def _eval(node)` |
| `_generate` | method | `toposwarm_infer.py:586` | `def _generate(self, prompt_ids, max_new_tokens, temperature)` |
| `_http_get` | method | `toposwarm_infer.py:292` | `def _http_get(self, url)` |
| `_import_agent` | function | `toposwarm_infer.py:51` | `def _import_agent()` |
| `_infer_tool_and_arg` | method | `toposwarm_infer.py:844` | `def _infer_tool_and_arg(self, prompt)` |
| `_load_checkpoint` | method | `toposwarm_infer.py:521` | `def _load_checkpoint(self)` |
| `_register_builtin_tools` | method | `toposwarm_infer.py:301` | `def _register_builtin_tools(self)` |
| `_safe_eval` | method | `toposwarm_infer.py:138` | `def _safe_eval(expr)` |
| `_setup_logger` | method | `toposwarm_infer.py:920` | `def _setup_logger(name, level)` |
| `_template_answer` | method | `toposwarm_infer.py:818` | `def _template_answer(self, tool_name, tool_arg, tool_result)` |
| `calc_expr` | method | `toposwarm_infer.py:340` | `def calc_expr(expr)` |
| `decorator` | method | `toposwarm_infer.py:231` | `def decorator(fn)` |
| `echo` | method | `toposwarm_infer.py:428` | `def echo(text)` |
| `execute` | method | `toposwarm_infer.py:262` | `def execute(self, raw_name, arg)` |
| `get_datetime` | method | `toposwarm_infer.py:345` | `def get_datetime(tz_hint)` |
| `get_news` | method | `toposwarm_infer.py:409` | `def get_news(topic)` |
| `get_weather` | method | `toposwarm_infer.py:305` | `def get_weather(city)` |
| `main` | method | `toposwarm_infer.py:938` | `def main()` |
| `parse` | method | `toposwarm_infer.py:453` | `def parse(self, text)` |
| `pretty` | method | `toposwarm_infer.py:895` | `def pretty(self)` |
| `register` | method | `toposwarm_infer.py:229` | `def register(self)` |
| `resolve` | method | `toposwarm_infer.py:239` | `def resolve(self, raw_name)` |
| `run` | method | `toposwarm_infer.py:679` | `def run(self, prompt)` |
| `search_web` | method | `toposwarm_infer.py:323` | `def search_web(query)` |
| `translate` | method | `toposwarm_infer.py:351` | `def translate(text)` |
| `LazyOwnBridge` | class | `toposwarm_lazyown_orchestrator.py:227` | `class LazyOwnBridge` |
| `LazyOwnOrchestrator` | class | `toposwarm_lazyown_orchestrator.py:764` | `class LazyOwnOrchestrator` |
| `LazyOwnToolRegistry` | class | `toposwarm_lazyown_orchestrator.py:372` | `class LazyOwnToolRegistry(ToolRegistry)` |
| `SessionContext` | class | `toposwarm_lazyown_orchestrator.py:170` | `class SessionContext` |
| `__init__` | method | `toposwarm_lazyown_orchestrator.py:251` | `def __init__(self, lazyown_dir, default_timeout)` |
| `__init__` | method | `toposwarm_lazyown_orchestrator.py:455` | `def __init__(self, cfg, bridge)` |
| `__init__` | method | `toposwarm_lazyown_orchestrator.py:780` | `def __init__(self, cfg, agent_cfg, bridge, logger, load_model, meta_cfg)` |
| `_extract_arg` | method | `toposwarm_lazyown_orchestrator.py:716` | `def _extract_arg(prompt, tool_name)` |
| `_hook` | method | `toposwarm_lazyown_orchestrator.py:863` | `def _hook(module, inp, out)` |
| `_import_agent` | function | `toposwarm_lazyown_orchestrator.py:113` | `def _import_agent()` |
| `_import_infer` | function | `toposwarm_lazyown_orchestrator.py:93` | `def _import_infer()` |
| `_import_meta_harness` | function | `toposwarm_lazyown_orchestrator.py:128` | `def _import_meta_harness()` |
| `_import_routing_head` | function | `toposwarm_lazyown_orchestrator.py:147` | `def _import_routing_head()` |
| `_load_routing_head` | method | `toposwarm_lazyown_orchestrator.py:825` | `def _load_routing_head(self)` |
| `_neural_route` | method | `toposwarm_lazyown_orchestrator.py:847` | `def _neural_route(self, prompt)` |
| `_register_lazyown_tools` | method | `toposwarm_lazyown_orchestrator.py:460` | `def _register_lazyown_tools(self)` |
| `_resolve_lazyown_dir` | function | `toposwarm_lazyown_orchestrator.py:56` | `def _resolve_lazyown_dir()` |
| `_serve` | method | `toposwarm_lazyown_orchestrator.py:1317` | `def _serve()` |
| `_setup_logger` | method | `toposwarm_lazyown_orchestrator.py:1329` | `def _setup_logger(level)` |
| `ack_event` | method | `toposwarm_lazyown_orchestrator.py:540` | `def ack_event(arg)` |
| `add_rule` | method | `toposwarm_lazyown_orchestrator.py:544` | `def add_rule(arg)` |
| `add_target` | method | `toposwarm_lazyown_orchestrator.py:572` | `def add_target(arg)` |
| `agent_result` | method | `toposwarm_lazyown_orchestrator.py:590` | `def agent_result(arg)` |
| `agent_status` | method | `toposwarm_lazyown_orchestrator.py:586` | `def agent_status(arg)` |
| `auto_loop` | method | `toposwarm_lazyown_orchestrator.py:662` | `def auto_loop(arg)` |
| `auto_populate` | method | `toposwarm_lazyown_orchestrator.py:622` | `def auto_populate(_)` |
| `available` | method | `toposwarm_lazyown_orchestrator.py:257` | `def available(self)` |
| `c2_adversary` | method | `toposwarm_lazyown_orchestrator.py:654` | `def c2_adversary(arg)` |
| `c2_command` | method | `toposwarm_lazyown_orchestrator.py:491` | `def c2_command(arg)` |
| `c2_notes` | method | `toposwarm_lazyown_orchestrator.py:606` | `def c2_notes(arg)` |
| `c2_redop` | method | `toposwarm_lazyown_orchestrator.py:642` | `def c2_redop(arg)` |
| `c2_script` | method | `toposwarm_lazyown_orchestrator.py:650` | `def c2_script(arg)` |
| `c2_search_agent` | method | `toposwarm_lazyown_orchestrator.py:646` | `def c2_search_agent(arg)` |
| `c2_status` | method | `toposwarm_lazyown_orchestrator.py:514` | `def c2_status(_)` |
| `c2_vuln_analysis` | method | `toposwarm_lazyown_orchestrator.py:638` | `def c2_vuln_analysis(arg)` |
| `call_tool` | method | `toposwarm_lazyown_orchestrator.py:1307` | `def call_tool(name, arguments)` |
| `campaign_lessons` | method | `toposwarm_lazyown_orchestrator.py:618` | `def campaign_lessons(_)` |
| `campaign_sitrep` | method | `toposwarm_lazyown_orchestrator.py:602` | `def campaign_sitrep(_)` |
| `command_help` | method | `toposwarm_lazyown_orchestrator.py:568` | `def command_help(arg)` |
| `create_addon` | method | `toposwarm_lazyown_orchestrator.py:518` | `def create_addon(arg)` |
| `create_tool` | method | `toposwarm_lazyown_orchestrator.py:666` | `def create_tool(arg)` |
| `credentials` | method | `toposwarm_lazyown_orchestrator.py:610` | `def credentials(_)` |
| `discover_commands` | method | `toposwarm_lazyown_orchestrator.py:560` | `def discover_commands(arg)` |
| `finetune_on_lazyown` | method | `toposwarm_lazyown_orchestrator.py:1173` | `def finetune_on_lazyown(dataset_path, agent_cfg, logger)` |
| `generate_dataset` | method | `toposwarm_lazyown_orchestrator.py:1092` | `def generate_dataset(output_path, bridge)` |
| `get_beacons` | method | `toposwarm_lazyown_orchestrator.py:487` | `def get_beacons(_)` |
| `get_config` | method | `toposwarm_lazyown_orchestrator.py:344` | `def get_config(self)` |
| `get_config` | method | `toposwarm_lazyown_orchestrator.py:470` | `def get_config(_)` |
| `heartbeat_status` | method | `toposwarm_lazyown_orchestrator.py:552` | `def heartbeat_status(_)` |
| `infer_lazyown_tool` | method | `toposwarm_lazyown_orchestrator.py:691` | `def infer_lazyown_tool(prompt)` |
| `inject_objective` | method | `toposwarm_lazyown_orchestrator.py:674` | `def inject_objective(arg)` |
| `list_addons` | method | `toposwarm_lazyown_orchestrator.py:522` | `def list_addons(_)` |
| `list_agents` | method | `toposwarm_lazyown_orchestrator.py:594` | `def list_agents(_)` |
| `list_event_rules` | method | `toposwarm_lazyown_orchestrator.py:548` | `def list_event_rules(_)` |
| `list_modules` | method | `toposwarm_lazyown_orchestrator.py:483` | `def list_modules(_)` |
| `list_plugins` | method | `toposwarm_lazyown_orchestrator.py:529` | `def list_plugins(_)` |
| `list_sessions` | method | `toposwarm_lazyown_orchestrator.py:499` | `def list_sessions(_)` |
| `list_targets` | method | `toposwarm_lazyown_orchestrator.py:578` | `def list_targets(_)` |
| `list_tools` | method | `toposwarm_lazyown_orchestrator.py:1273` | `def list_tools()` |
| `llm_ask` | method | `toposwarm_lazyown_orchestrator.py:670` | `def llm_ask(arg)` |
| `main` | method | `toposwarm_lazyown_orchestrator.py:1346` | `def main()` |
| `next_objective` | method | `toposwarm_lazyown_orchestrator.py:678` | `def next_objective(_)` |
| `phase_guide` | method | `toposwarm_lazyown_orchestrator.py:564` | `def phase_guide(arg)` |
| `policy_status` | method | `toposwarm_lazyown_orchestrator.py:658` | `def policy_status(_)` |
| `poll_events` | method | `toposwarm_lazyown_orchestrator.py:536` | `def poll_events(_)` |
| `read_prompt` | method | `toposwarm_lazyown_orchestrator.py:682` | `def read_prompt(arg)` |
| `read_session_file` | method | `toposwarm_lazyown_orchestrator.py:507` | `def read_session_file(arg)` |
| `recommend_next` | method | `toposwarm_lazyown_orchestrator.py:630` | `def recommend_next(_)` |
| `report_update` | method | `toposwarm_lazyown_orchestrator.py:614` | `def report_update(arg)` |
| `run` | method | `toposwarm_lazyown_orchestrator.py:265` | `def run(self, command, timeout)` |
| `run` | method | `toposwarm_lazyown_orchestrator.py:887` | `def run(self, prompt)` |
| `run_agent` | method | `toposwarm_lazyown_orchestrator.py:582` | `def run_agent(arg)` |
| `run_api` | method | `toposwarm_lazyown_orchestrator.py:495` | `def run_api(arg)` |
| `run_command` | method | `toposwarm_lazyown_orchestrator.py:466` | `def run_command(arg)` |
| `run_mcp_server` | method | `toposwarm_lazyown_orchestrator.py:1250` | `def run_mcp_server(orchestrator)` |
| `session_init` | method | `toposwarm_lazyown_orchestrator.py:556` | `def session_init(arg)` |
| `session_state` | method | `toposwarm_lazyown_orchestrator.py:626` | `def session_state(_)` |
| `set_active_target` | method | `toposwarm_lazyown_orchestrator.py:598` | `def set_active_target(arg)` |
| `set_config` | method | `toposwarm_lazyown_orchestrator.py:353` | `def set_config(self, key, value)` |
| `set_config` | method | `toposwarm_lazyown_orchestrator.py:475` | `def set_config(arg)` |
| `timeline` | method | `toposwarm_lazyown_orchestrator.py:634` | `def timeline(_)` |
| `to_prompt_prefix` | method | `toposwarm_lazyown_orchestrator.py:181` | `def to_prompt_prefix(self)` |
| `update` | method | `toposwarm_lazyown_orchestrator.py:195` | `def update(self, tool_name, arg, output, ok)` |
| `generate_prompts` | function | `toposwarm_lazyown_sweep.py:130` | `def generate_prompts(n)` |
| `main` | function | `toposwarm_lazyown_sweep.py:223` | `def main()` |
| `run_sweep` | function | `toposwarm_lazyown_sweep.py:155` | `def run_sweep(prompts, bridge, logger)` |
| `setup_logger` | function | `toposwarm_lazyown_sweep.py:145` | `def setup_logger()` |
| `write_results` | function | `toposwarm_lazyown_sweep.py:189` | `def write_results(results, out_path)` |
| `DenseMemoryRetriever` | class | `toposwarm_meta_harness.py:322` | `class DenseMemoryRetriever` |
| `DraftVerifier` | class | `toposwarm_meta_harness.py:738` | `class DraftVerifier` |
| `EnvironmentBootstrapper` | class | `toposwarm_meta_harness.py:583` | `class EnvironmentBootstrapper` |
| `MetaHarnessConfig` | class | `toposwarm_meta_harness.py:60` | `class MetaHarnessConfig` |
| `MetaHarnessLogger` | class | `toposwarm_meta_harness.py:121` | `class MetaHarnessLogger` |
| `MetaHarnessMemory` | class | `toposwarm_meta_harness.py:430` | `class MetaHarnessMemory` |
| `MetaHarnessOptimizer` | class | `toposwarm_meta_harness.py:948` | `class MetaHarnessOptimizer` |
| `ParetoFrontier` | class | `toposwarm_meta_harness.py:837` | `class ParetoFrontier` |
| `__init__` | method | `toposwarm_meta_harness.py:138` | `def __init__(self, cfg, logger)` |
| `__init__` | method | `toposwarm_meta_harness.py:335` | `def __init__(self, logger)` |
| `__init__` | method | `toposwarm_meta_harness.py:441` | `def __init__(self, logger, capacity, dense)` |
| `__init__` | method | `toposwarm_meta_harness.py:592` | `def __init__(self, cfg, logger)` |
| `__init__` | method | `toposwarm_meta_harness.py:754` | `def __init__(self, cfg, memory, keyword_router, logger)` |
| `__init__` | method | `toposwarm_meta_harness.py:846` | `def __init__(self, cfg, logger)` |
| `__init__` | method | `toposwarm_meta_harness.py:965` | `def __init__(self, cfg)` |
| `_build_index` | method | `toposwarm_meta_harness.py:453` | `def _build_index(self)` |
| `_count_existing_runs` | method | `toposwarm_meta_harness.py:149` | `def _count_existing_runs(self)` |
| `_demo` | method | `toposwarm_meta_harness.py:1013` | `def _demo()` |
| `_episode_text` | method | `toposwarm_meta_harness.py:482` | `def _episode_text(score, traces)` |
| `_is_on_frontier` | method | `toposwarm_meta_harness.py:911` | `def _is_on_frontier(self, candidate)` |
| `_load_episode` | method | `toposwarm_meta_harness.py:464` | `def _load_episode(self, run_dir)` |
| `_next_run_dir` | method | `toposwarm_meta_harness.py:152` | `def _next_run_dir(self, hint)` |
| `_now_iso` | method | `toposwarm_meta_harness.py:112` | `def _now_iso()` |
| `_parse_list` | method | `toposwarm_meta_harness.py:680` | `def _parse_list(raw)` |
| `_prune` | method | `toposwarm_meta_harness.py:933` | `def _prune(self)` |
| `_prune_old` | method | `toposwarm_meta_harness.py:158` | `def _prune_old(self)` |
| `_rebuild_tfidf` | method | `toposwarm_meta_harness.py:368` | `def _rebuild_tfidf(self)` |
| `_reextract_arg` | method | `toposwarm_meta_harness.py:820` | `def _reextract_arg(prompt, tool_name, fallback)` |
| `_search_st` | method | `toposwarm_meta_harness.py:401` | `def _search_st(self, query, top_k)` |
| `_search_tfidf` | method | `toposwarm_meta_harness.py:412` | `def _search_tfidf(self, query, top_k)` |
| `_setup_logger` | method | `toposwarm_meta_harness.py:95` | `def _setup_logger(name, level)` |
| `_stable_id` | method | `toposwarm_meta_harness.py:107` | `def _stable_id(text)` |
| `_tokenise` | method | `toposwarm_meta_harness.py:573` | `def _tokenise(text)` |
| `add` | method | `toposwarm_meta_harness.py:362` | `def add(self, text, episode)` |
| `add` | method | `toposwarm_meta_harness.py:855` | `def add(self, config, metrics)` |
| `bulk_index` | method | `toposwarm_meta_harness.py:376` | `def bulk_index(self, texts, episodes)` |
| `format_snapshot` | method | `toposwarm_meta_harness.py:687` | `def format_snapshot(self, snapshot, max_chars)` |
| `frontier_configs` | method | `toposwarm_meta_harness.py:907` | `def frontier_configs(self)` |
| `gather_snapshot` | method | `toposwarm_meta_harness.py:596` | `def gather_snapshot(self, bridge)` |
| `get_best_harness_config` | method | `toposwarm_meta_harness.py:999` | `def get_best_harness_config(self)` |
| `get_pareto_runs` | method | `toposwarm_meta_harness.py:269` | `def get_pareto_runs(self, metrics)` |
| `get_scores` | method | `toposwarm_meta_harness.py:257` | `def get_scores(self)` |
| `grep_traces` | method | `toposwarm_meta_harness.py:238` | `def grep_traces(self, pattern, max_results)` |
| `list_runs` | method | `toposwarm_meta_harness.py:229` | `def list_runs(self, n)` |
| `log_run` | method | `toposwarm_meta_harness.py:176` | `def log_run(self, harness_snapshot, trace_steps, score, reasoning)` |
| `log_run` | method | `toposwarm_meta_harness.py:986` | `def log_run(self, harness_snapshot, trace_steps, score, reasoning)` |
| `query_experience` | method | `toposwarm_meta_harness.py:1003` | `def query_experience(self, prompt, tool_hint, top_k)` |
| `retrieve_confirmers_and_challengers` | method | `toposwarm_meta_harness.py:549` | `def retrieve_confirmers_and_challengers(self, draft_tool, prompt, top_k)` |
| `retrieve_similar` | method | `toposwarm_meta_harness.py:505` | `def retrieve_similar(self, prompt, tool_hint, top_k, min_score)` |
| `route` | method | `toposwarm_meta_harness.py:766` | `def route(self, prompt, snapshot_text)` |
| `search` | method | `toposwarm_meta_harness.py:392` | `def search(self, query, top_k)` |
| `select_best` | method | `toposwarm_meta_harness.py:875` | `def select_best(self, preference)` |
| `set_router` | method | `toposwarm_meta_harness.py:980` | `def set_router(self, keyword_router)` |
| `store` | method | `toposwarm_meta_harness.py:493` | `def store(self, score, traces)` |
| `_cached_encode` | function | `ts_utils.py:94` | `def _cached_encode(text)` |
| `_cached_tool_token` | function | `ts_utils.py:103` | `def _cached_tool_token(tool_name)` |
| `import_module` | function | `ts_utils.py:62` | `def import_module(name)` |
| `make_cached_encode` | function | `ts_utils.py:86` | `def make_cached_encode(tokenizer)` |
| `make_cached_tool_token` | function | `ts_utils.py:100` | `def make_cached_tool_token(tokenizer)` |
| `safe_eval` | function | `ts_utils.py:42` | `def safe_eval(expr)` |
| `setup_logger` | function | `ts_utils.py:25` | `def setup_logger(name, level)` |
