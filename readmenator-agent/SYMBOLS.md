# Symbols (page 1 of 2)
Pages: [SYMBOLS.md](SYMBOLS.md), [SYMBOLS_p2.md](SYMBOLS_p2.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_import` | function | `debug_routing.py:14` | `def _import(name, filename)` |
| `load_model` | function | `diagnose_accuracy.py:13` | `def load_model()` |
| `main` | function | `diagnose_accuracy.py:33` | `def main()` |
| `ExecutionResult` | class | `lazyown_bridge.py:74` | `class ExecutionResult` |
| `LazyOwnBridge` | class | `lazyown_bridge.py:542` | `class LazyOwnBridge` |
| `LazyOwnCommandBuilder` | class | `lazyown_bridge.py:220` | `class LazyOwnCommandBuilder` |
| `LazyOwnOutputSanitizer` | class | `lazyown_bridge.py:505` | `class LazyOwnOutputSanitizer` |
| `LazyOwnPathResolver` | class | `lazyown_bridge.py:90` | `class LazyOwnPathResolver` |
| `LazyOwnPayloadManager` | class | `lazyown_bridge.py:162` | `class LazyOwnPayloadManager` |
| `LazyOwnProcessExecutor` | class | `lazyown_bridge.py:294` | `class LazyOwnProcessExecutor` |
| `_Defaults` | class | `lazyown_bridge.py:56` | `class _Defaults` |
| `_EnvKey` | class | `lazyown_bridge.py:41` | `class _EnvKey(str, Enum)` |
| `_FileName` | class | `lazyown_bridge.py:47` | `class _FileName(str, Enum)` |
| `__init__` | method | `lazyown_bridge.py:104` | `def __init__(self)` |
| `__init__` | method | `lazyown_bridge.py:171` | `def __init__(self, lazyown_dir)` |
| `__init__` | method | `lazyown_bridge.py:237` | `def __init__(self, lazyown_dir)` |
| `__init__` | method | `lazyown_bridge.py:331` | `def __init__(self, lazyown_dir)` |
| `__init__` | method | `lazyown_bridge.py:556` | `def __init__(self)` |
| `_drain_pty` | method | `lazyown_bridge.py:451` | `def _drain_pty(self, master_fd, chunks)` |
| `_execute_with_pipe` | method | `lazyown_bridge.py:464` | `def _execute_with_pipe(self, argv, stdin_payload, timeout, env)` |
| `_execute_with_pty` | method | `lazyown_bridge.py:387` | `def _execute_with_pty(self, argv, stdin_payload, timeout, env)` |
| `_from_cwd` | method | `lazyown_bridge.py:152` | `def _from_cwd(self)` |
| `_from_env` | method | `lazyown_bridge.py:133` | `def _from_env(self)` |
| `_from_home` | method | `lazyown_bridge.py:148` | `def _from_home(self)` |
| `_from_repo_sibling` | method | `lazyown_bridge.py:140` | `def _from_repo_sibling(self)` |
| `_resolve_timeout` | method | `lazyown_bridge.py:375` | `def _resolve_timeout(self, argv, override)` |
| `_validate_command` | method | `lazyown_bridge.py:276` | `def _validate_command(command)` |
| `_wait_or_kill` | method | `lazyown_bridge.py:491` | `def _wait_or_kill(self, proc)` |
| `available` | method | `lazyown_bridge.py:589` | `def available(self)` |
| `build_argv` | method | `lazyown_bridge.py:242` | `def build_argv(self, command)` |
| `builder` | method | `lazyown_bridge.py:577` | `def builder(self)` |
| `execute` | method | `lazyown_bridge.py:343` | `def execute(self, argv, stdin_payload, timeout)` |
| `executor` | method | `lazyown_bridge.py:583` | `def executor(self)` |
| `get` | method | `lazyown_bridge.py:198` | `def get(self, key, default)` |
| `get_config` | method | `lazyown_bridge.py:642` | `def get_config(self)` |
| `get_target` | method | `lazyown_bridge.py:659` | `def get_target(self)` |
| `lazyown_dir` | method | `lazyown_bridge.py:565` | `def lazyown_dir(self)` |
| `payload` | method | `lazyown_bridge.py:571` | `def payload(self)` |
| `payload_path` | method | `lazyown_bridge.py:176` | `def payload_path(self)` |
| `read` | method | `lazyown_bridge.py:179` | `def read(self)` |
| `resolve` | method | `lazyown_bridge.py:107` | `def resolve(self)` |
| `run` | method | `lazyown_bridge.py:598` | `def run(self, command, timeout)` |
| `run_clean` | method | `lazyown_bridge.py:634` | `def run_clean(self, command, timeout)` |
| `sanitize` | method | `lazyown_bridge.py:527` | `def sanitize(self, text)` |
| `set` | method | `lazyown_bridge.py:202` | `def set(self, key, value)` |
| `set_config` | method | `lazyown_bridge.py:646` | `def set_config(self, key, value)` |
| `set_target` | method | `lazyown_bridge.py:655` | `def set_target(self, ip)` |
| `update` | method | `lazyown_bridge.py:208` | `def update(self, mapping)` |
| `write` | method | `lazyown_bridge.py:189` | `def write(self, data)` |
| `DatasetEnhancer` | class | `lazyown_dataset_enhancer.py:165` | `class DatasetEnhancer` |
| `ExperienceStoreReader` | class | `lazyown_dataset_enhancer.py:87` | `class ExperienceStoreReader` |
| `__init__` | method | `lazyown_dataset_enhancer.py:88` | `def __init__(self, log_dir)` |
| `__init__` | method | `lazyown_dataset_enhancer.py:166` | `def __init__(self, log_dir, max_runs)` |
| `_build_toolbench_record` | method | `lazyown_dataset_enhancer.py:149` | `def _build_toolbench_record(instruction, tool_name, arg, answer, domain)` |
| `_difficulty` | function | `lazyown_dataset_enhancer.py:64` | `def _difficulty(record)` |
| `_generate_prerequisite_records` | method | `lazyown_dataset_enhancer.py:301` | `def _generate_prerequisite_records(prompt, tool, arg, output, ok)` |
| `_generate_recovery_records` | method | `lazyown_dataset_enhancer.py:239` | `def _generate_recovery_records(prompt, tool, arg, output)` |
| `_sanitize_output` | method | `lazyown_dataset_enhancer.py:136` | `def _sanitize_output(text)` |
| `add_negative_examples` | method | `lazyown_dataset_enhancer.py:330` | `def add_negative_examples(self, records, n)` |
| `augment_simple` | method | `lazyown_dataset_enhancer.py:370` | `def augment_simple(self, records, multiplier)` |
| `curriculum_sort` | method | `lazyown_dataset_enhancer.py:355` | `def curriculum_sort(self, records)` |
| `deduplicate` | method | `lazyown_dataset_enhancer.py:359` | `def deduplicate(self, records)` |
| `enhance` | method | `lazyown_dataset_enhancer.py:171` | `def enhance(self)` |
| `list_runs` | method | `lazyown_dataset_enhancer.py:91` | `def list_runs(self)` |
| `main` | method | `lazyown_dataset_enhancer.py:469` | `def main()` |
| `print_stats` | method | `lazyown_dataset_enhancer.py:442` | `def print_stats(records)` |
| `read_harness` | method | `lazyown_dataset_enhancer.py:122` | `def read_harness(self, run_dir)` |
| `read_score` | method | `lazyown_dataset_enhancer.py:113` | `def read_score(self, run_dir)` |
| `read_trace` | method | `lazyown_dataset_enhancer.py:98` | `def read_trace(self, run_dir)` |
| `run` | method | `lazyown_dataset_enhancer.py:395` | `def run(self, merge_with)` |
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
| `AudioEncoder` | class | `neurologos_tricameral_loss2.7.py:1652` | `class AudioEncoder(Module)` |
| `CausalReasoningEngine` | class | `neurologos_tricameral_loss2.7.py:927` | `class CausalReasoningEngine(Module)` |
| `CorpusCallosumTrimodal` | class | `neurologos_tricameral_loss2.7.py:1786` | `class CorpusCallosumTrimodal(Module)` |
| `EnhancedDiagnosticsTricameral` | class | `neurologos_tricameral_loss2.7.py:1939` | `class EnhancedDiagnosticsTricameral` |
| `Flickr8kMultimodalDataset` | class | `neurologos_tricameral_loss2.7.py:2250` | `class Flickr8kMultimodalDataset(Dataset)` |
| `HierarchicalEpisodicMemory` | class | `neurologos_tricameral_loss2.7.py:265` | `class HierarchicalEpisodicMemory` |
| `LanguageMetrics` | class | `neurologos_tricameral_loss2.7.py:693` | `class LanguageMetrics` |
| `LanguageMetrics` | class | `neurologos_tricameral_loss2.7.py:884` | `class LanguageMetrics` |
| `LanguageMetrics` | class | `neurologos_tricameral_loss2.7.py:1006` | `class LanguageMetrics` |
| `LeftHemisphere` | class | `neurologos_tricameral_loss2.7.py:1343` | `class LeftHemisphere(Module)` |
| `LinguisticFeedbackLoop` | class | `neurologos_tricameral_loss2.7.py:767` | `class LinguisticFeedbackLoop` |
| `NeuroLogosTricameral` | class | `neurologos_tricameral_loss2.7.py:2215` | `class NeuroLogosTricameral(Module)` |
| `NeurocognitiveSystem` | class | `neurologos_tricameral_loss2.7.py:496` | `class NeurocognitiveSystem` |
| `RightHemisphereTricameral` | class | `neurologos_tricameral_loss2.7.py:1702` | `class RightHemisphereTricameral(Module)` |
| `StableLiquidNeuron` | class | `neurologos_tricameral_loss2.7.py:1053` | `class StableLiquidNeuron(Module)` |
| `TriangulatedMedicalSystem` | class | `neurologos_tricameral_loss2.7.py:1192` | `class TriangulatedMedicalSystem` |
| `__getitem__` | method | `neurologos_tricameral_loss2.7.py:2305` | `def __getitem__(self, idx)` |
| `__init__` | method | `neurologos_tricameral_loss2.7.py:266` | `def __init__(self, working_capacity, short_term_capacity, importance_threshold)` |
| `__init__` | method | `neurologos_tricameral_loss2.7.py:497` | `def __init__(self)` |
| `__init__` | method | `neurologos_tricameral_loss2.7.py:768` | `def __init__(self, alpha, beta)` |
| `__init__` | method | `neurologos_tricameral_loss2.7.py:928` | `def __init__(self, hidden_dim)` |
| `__init__` | method | `neurologos_tricameral_loss2.7.py:1054` | `def __init__(self, in_dim, out_dim)` |
| `__init__` | method | `neurologos_tricameral_loss2.7.py:1193` | `def __init__(self)` |
| `__init__` | method | `neurologos_tricameral_loss2.7.py:1344` | `def __init__(self, vocab_size, embed_dim, hidden_dim)` |
| `__init__` | method | `neurologos_tricameral_loss2.7.py:1655` | `def __init__(self, output_dim)` |
| `__init__` | method | `neurologos_tricameral_loss2.7.py:1705` | `def __init__(self, output_dim)` |
| `__init__` | method | `neurologos_tricameral_loss2.7.py:1787` | `def __init__(self, dim)` |
| `__init__` | method | `neurologos_tricameral_loss2.7.py:1940` | `def __init__(self)` |
| `__init__` | method | `neurologos_tricameral_loss2.7.py:2218` | `def __init__(self, vocab_size)` |
| `__init__` | method | `neurologos_tricameral_loss2.7.py:2253` | `def __init__(self, images_dir, audio_dir, captions_file, vocab, img_transform, max_len, sample_rate)` |
| `__len__` | method | `neurologos_tricameral_loss2.7.py:2301` | `def __len__(self)` |
| `_apply_chain_of_thought` | method | `neurologos_tricameral_loss2.7.py:1473` | `def _apply_chain_of_thought(self, hidden_states, visual_context, use_reasoning)` |
| `_apply_multi_token_prediction` | method | `neurologos_tricameral_loss2.7.py:1574` | `def _apply_multi_token_prediction(self, hidden_states, input_ids)` |
| `_apply_structural_attention` | method | `neurologos_tricameral_loss2.7.py:1616` | `def _apply_structural_attention(self, lstm_out, channels, visual_context)` |
| `_calculate_homeostasis_metric` | method | `neurologos_tricameral_loss2.7.py:1112` | `def _calculate_homeostasis_metric(self, output)` |
| `_calculate_novelty` | method | `neurologos_tricameral_loss2.7.py:314` | `def _calculate_novelty(self, episode)` |
| `_get_cached_norm` | method | `neurologos_tricameral_loss2.7.py:1962` | `def _get_cached_norm(self, tensor, dim)` |
| `_get_init_state` | method | `neurologos_tricameral_loss2.7.py:1637` | `def _get_init_state(self, visual_context)` |
| `_get_ngrams` | method | `neurologos_tricameral_loss2.7.py:731` | `def _get_ngrams(tokens, n)` |
| `_get_ngrams_cached` | method | `neurologos_tricameral_loss2.7.py:782` | `def _get_ngrams_cached(sentence, n)` |
| `_greedy_decode` | method | `neurologos_tricameral_loss2.7.py:1513` | `def _greedy_decode(self, visual_context, channels, max_len, epoch)` |
| `_predict_interventions` | method | `neurologos_tricameral_loss2.7.py:969` | `def _predict_interventions(self, hypothesis, confidence)` |
| `_purge_low_score_memories` | method | `neurologos_tricameral_loss2.7.py:404` | `def _purge_low_score_memories(self)` |
| `_reset_liquid_neuron` | method | `neurologos_tricameral_loss2.7.py:1328` | `def _reset_liquid_neuron(self, liquid_neuron)` |
| `_sample_from_buffer` | method | `neurologos_tricameral_loss2.7.py:460` | `def _sample_from_buffer(self, buffer, scores, batch_size)` |
| `_update_unified_buffer` | method | `neurologos_tricameral_loss2.7.py:373` | `def _update_unified_buffer(self)` |
| `add` | method | `neurologos_tricameral_loss2.7.py:385` | `def add(self, image, audio, caption, surprise_score)` |
| `adjust_gates_by_fatigue` | method | `neurologos_tricameral_loss2.7.py:1918` | `def adjust_gates_by_fatigue(self)` |
| `apply_cognitive_intervention` | method | `neurologos_tricameral_loss2.7.py:607` | `def apply_cognitive_intervention(self, model, issues, severity, confidence, epoch, diagnostics)` |
| `apply_forgetting_curve` | method | `neurologos_tricameral_loss2.7.py:388` | `def apply_forgetting_curve(self)` |
| `apply_triangulated_intervention` | method | `neurologos_tricameral_loss2.7.py:1259` | `def apply_triangulated_intervention(self, model, issues, severity, confidence, epoch)` |
| `assess_cognitive_state` | method | `neurologos_tricameral_loss2.7.py:561` | `def assess_cognitive_state(self, cider_score, spice_score, combined_reward, epoch)` |
| `assess_reasoning_state` | method | `neurologos_tricameral_loss2.7.py:517` | `def assess_reasoning_state(self, mtp_loss, reasoning_steps, logical_coherence, epoch)` |
| `build_vocab_flickr` | function | `neurologos_tricameral_loss2.7.py:241` | `def build_vocab_flickr(captions_file, vocab_size)` |
| `calculate_health` | method | `neurologos_tricameral_loss2.7.py:2058` | `def calculate_health(self, visual_node, audio_node, callosal_flow, left_gate_mean, left_gate_std, liquid_norm)` |
| `calculate_importance` | method | `neurologos_tricameral_loss2.7.py:302` | `def calculate_importance(self, episode, surprise_score)` |
| `calculate_synergy` | method | `neurologos_tricameral_loss2.7.py:2047` | `def calculate_synergy(self, visual_node, audio_node, callosal_flow, left_gate_mean, left_gate_std)` |
| `compute_alignment_loss` | method | `neurologos_tricameral_loss2.7.py:2354` | `def compute_alignment_loss(visual_features, channels, alpha, epoch)` |
| `compute_cider` | method | `neurologos_tricameral_loss2.7.py:830` | `def compute_cider(self, reference, hypothesis)` |
| `compute_linguistic_reward` | method | `neurologos_tricameral_loss2.7.py:791` | `def compute_linguistic_reward(self, references, hypotheses)` |
| `compute_spice` | method | `neurologos_tricameral_loss2.7.py:844` | `def compute_spice(self, reference, hypothesis)` |
| `compute_surprise` | method | `neurologos_tricameral_loss2.7.py:292` | `def compute_surprise(self, predicted_logits, ground_truth, gate_mean)` |
| `compute_tricameral_loss` | method | `neurologos_tricameral_loss2.7.py:2382` | `def compute_tricameral_loss(logits, captions, gate, vocab, visual_post, audio_post, mtp_loss, linguistic_reward...` |
| `count_convergent_signals` | method | `neurologos_tricameral_loss2.7.py:1211` | `def count_convergent_signals(self, signals, pattern)` |
| `diagnose_with_triangulation` | method | `neurologos_tricameral_loss2.7.py:1214` | `def diagnose_with_triangulation(self, health_score, liquid_norm, gate_mean, gate_std, callosal_flow, epoch)` |
| `evaluate_reasoning_quality` | method | `neurologos_tricameral_loss2.7.py:2010` | `def evaluate_reasoning_quality(self, generated_texts, reference_texts, reasoning_steps)` |
| `forward` | method | `neurologos_tricameral_loss2.7.py:1096` | `def forward(self, x)` |
| `forward` | method | `neurologos_tricameral_loss2.7.py:1426` | `def forward(self, visual_context, captions, channels, max_len, epoch)` |
| `forward` | method | `neurologos_tricameral_loss2.7.py:1689` | `def forward(self, mel_spec)` |
| `forward` | method | `neurologos_tricameral_loss2.7.py:1745` | `def forward(self, image, audio)` |
| `forward` | method | `neurologos_tricameral_loss2.7.py:1835` | `def forward(self, right_features)` |
| `forward` | method | `neurologos_tricameral_loss2.7.py:2224` | `def forward(self, image, audio, captions, epoch)` |
| `get_cache_stats` | method | `neurologos_tricameral_loss2.7.py:856` | `def get_cache_stats(self)` |
| `get_recent_avg` | method | `neurologos_tricameral_loss2.7.py:2084` | `def get_recent_avg(self, key, n)` |
| `get_total_size` | method | `neurologos_tricameral_loss2.7.py:488` | `def get_total_size(self)` |
| `hebbian_update` | method | `neurologos_tricameral_loss2.7.py:1121` | `def hebbian_update(self, post, pre, plasticity)` |
| `measure_callosal_flow` | method | `neurologos_tricameral_loss2.7.py:1980` | `def measure_callosal_flow(self, right_features, left_context, channels)` |
| `query_causal_chain` | method | `neurologos_tricameral_loss2.7.py:992` | `def query_causal_chain(self, start_node, end_node)` |
| `reason_causally` | method | `neurologos_tricameral_loss2.7.py:955` | `def reason_causally(self, observation, context)` |
| `report` | method | `neurologos_tricameral_loss2.7.py:2136` | `def report(self, epoch)` |
| `sample` | method | `neurologos_tricameral_loss2.7.py:430` | `def sample(self, batch_size, memory_level)` |
| `sentence_bleu` | method | `neurologos_tricameral_loss2.7.py:697` | `def sentence_bleu(reference, hypothesis, weights)` |
| `sentence_bleu` | method | `neurologos_tricameral_loss2.7.py:886` | `def sentence_bleu(reference, hypothesis, weights)` |
| `sentence_bleu` | method | `neurologos_tricameral_loss2.7.py:1008` | `def sentence_bleu(reference, hypothesis, weights)` |
| `setup_flickr8k_with_audio` | function | `neurologos_tricameral_loss2.7.py:53` | `def setup_flickr8k_with_audio(data_dir)` |
| `store_episode` | method | `neurologos_tricameral_loss2.7.py:335` | `def store_episode(self, image, audio, caption, surprise_score)` |
| `token_accuracy` | method | `neurologos_tricameral_loss2.7.py:740` | `def token_accuracy(reference, hypothesis)` |
| `token_accuracy` | method | `neurologos_tricameral_loss2.7.py:909` | `def token_accuracy(reference, hypothesis)` |
| `token_accuracy` | method | `neurologos_tricameral_loss2.7.py:1031` | `def token_accuracy(reference, hypothesis)` |
| `train_tricameral` | method | `neurologos_tricameral_loss2.7.py:2429` | `def train_tricameral()` |
| `triangulate_signals` | method | `neurologos_tricameral_loss2.7.py:1200` | `def triangulate_signals(self, health_score, liquid_norm, gate_mean, gate_std, callosal_flow)` |
| `update` | method | `neurologos_tricameral_loss2.7.py:2067` | `def update(self)` |
| `update_channel_fatigue` | method | `neurologos_tricameral_loss2.7.py:1896` | `def update_channel_fatigue(self, visual_channel, audio_channel, semantic_channel)` |
| `update_knowledge_graph` | method | `neurologos_tricameral_loss2.7.py:986` | `def update_knowledge_graph(self, cause, effect, strength)` |
| `update_physiology_advanced` | method | `neurologos_tricameral_loss2.7.py:1159` | `def update_physiology_advanced(self, loss_value)` |
| `visualize_fatigue_distribution` | method | `neurologos_tricameral_loss2.7.py:2100` | `def visualize_fatigue_distribution(self, epoch)` |
| `visualize_reasoning_metrics` | method | `neurologos_tricameral_loss2.7.py:2124` | `def visualize_reasoning_metrics(self, epoch)` |
| `word_overlap` | method | `neurologos_tricameral_loss2.7.py:753` | `def word_overlap(reference, hypothesis)` |
| `word_overlap` | method | `neurologos_tricameral_loss2.7.py:919` | `def word_overlap(reference, hypothesis)` |
| `word_overlap` | method | `neurologos_tricameral_loss2.7.py:1041` | `def word_overlap(reference, hypothesis)` |
| `_Paths` | class | `test_full_pipeline.py:23` | `class _Paths` |
| `_run` | method | `test_full_pipeline.py:36` | `def _run(cmd, timeout)` |
| `main` | method | `test_full_pipeline.py:208` | `def main()` |
| `step1_regenerate_dataset` | method | `test_full_pipeline.py:53` | `def step1_regenerate_dataset()` |
| `step2_train` | method | `test_full_pipeline.py:84` | `def step2_train(epochs)` |
| `step3_evaluate` | method | `test_full_pipeline.py:108` | `def step3_evaluate()` |
| `step4_live_test` | method | `test_full_pipeline.py:134` | `def step4_live_test()` |
| `step5_validate_logs` | method | `test_full_pipeline.py:168` | `def step5_validate_logs()` |
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
| `_load_mod` | function | `tests/test_model_config.py:11` | `def _load_mod()` |
| `test_default_scale_is_xl150m` | function | `tests/test_model_config.py:25` | `def test_default_scale_is_xl150m()` |
| `test_micro_preset_compatible_with_legacy_checkpoint` | function | `tests/test_model_config.py:36` | `def test_micro_preset_compatible_with_legacy_checkpoint()` |
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
| `BPETokenizer` | class | `topo_swarm_agent.py:1735` | `class BPETokenizer` |
| `CheckpointManager` | class | `topo_swarm_agent.py:2088` | `class CheckpointManager` |
| `EpisodicMemory` | class | `topo_swarm_agent.py:1529` | `class EpisodicMemory` |
| `HRMModule` | class | `topo_swarm_agent.py:1144` | `class HRMModule(Module)` |
| `KappaDetector` | class | `topo_swarm_agent.py:2191` | `class KappaDetector` |
| `QuaternionAttention` | class | `topo_swarm_agent.py:1039` | `class QuaternionAttention(Module)` |
| `QuaternionLinear` | class | `topo_swarm_agent.py:370` | `class QuaternionLinear(Module)` |
| `QuaternionOps` | class | `topo_swarm_agent.py:322` | `class QuaternionOps` |
| `QuaternionTorusBrain` | class | `topo_swarm_agent.py:848` | `class QuaternionTorusBrain(Module)` |
| `RMSNorm` | class | `topo_swarm_agent.py:505` | `class RMSNorm(Module)` |
| `RotaryEmbedding` | class | `topo_swarm_agent.py:529` | `class RotaryEmbedding(Module)` |
| `SpectralBottleneck` | class | `topo_swarm_agent.py:434` | `class SpectralBottleneck(Module)` |
| `SwarmConfig` | class | `topo_swarm_agent.py:85` | `class SwarmConfig` |
| `SwarmMoE` | class | `topo_swarm_agent.py:648` | `class SwarmMoE(Module)` |
| `SwarmMoEAdapter` | class | `topo_swarm_agent.py:706` | `class SwarmMoEAdapter(Module)` |
| `SwarmMoEGate` | class | `topo_swarm_agent.py:627` | `class SwarmMoEGate(Module)` |
| `SwarmOrchestrator` | class | `topo_swarm_agent.py:1644` | `class SwarmOrchestrator` |
| `SwarmTrainer` | class | `topo_swarm_agent.py:2234` | `class SwarmTrainer` |
| `SwiGLU` | class | `topo_swarm_agent.py:588` | `class SwiGLU(Module)` |
| `ToolBenchDataset` | class | `topo_swarm_agent.py:1853` | `class ToolBenchDataset(Dataset)` |
| `TopoSwarmLayer` | class | `topo_swarm_agent.py:1246` | `class TopoSwarmLayer(Module)` |
| `TopoSwarmModel` | class | `topo_swarm_agent.py:1314` | `class TopoSwarmModel(Module)` |
| `__getitem__` | method | `topo_swarm_agent.py:2062` | `def __getitem__(self, idx)` |
| `__init__` | method | `topo_swarm_agent.py:381` | `def __init__(self, in_features, out_features, bias, init_std)` |
| `__init__` | method | `topo_swarm_agent.py:446` | `def __init__(self, cfg)` |
| `__init__` | method | `topo_swarm_agent.py:508` | `def __init__(self, d_model, eps)` |
| `__init__` | method | `topo_swarm_agent.py:537` | `def __init__(self, d_head, max_seq_len, base, ntk_factor)` |
| `__init__` | method | `topo_swarm_agent.py:591` | `def __init__(self, d_model, hidden_dim, dropout)` |
| `__init__` | method | `topo_swarm_agent.py:630` | `def __init__(self, d_model, n_experts, top_k)` |
| `__init__` | method | `topo_swarm_agent.py:661` | `def __init__(self, d_model, expert_hidden_dim, n_experts, top_k, dropout)` |
| `__init__` | method | `topo_swarm_agent.py:720` | `def __init__(self, d_model, n_experts, top_k, bottleneck, dropout)` |
| `__init__` | method | `topo_swarm_agent.py:866` | `def __init__(self, cfg)` |
| `__init__` | method | `topo_swarm_agent.py:1047` | `def __init__(self, cfg)` |
| `__init__` | method | `topo_swarm_agent.py:1160` | `def __init__(self, cfg)` |
| `__init__` | method | `topo_swarm_agent.py:1254` | `def __init__(self, cfg)` |
| `__init__` | method | `topo_swarm_agent.py:1329` | `def __init__(self, cfg)` |
| `__init__` | method | `topo_swarm_agent.py:1539` | `def __init__(self, cfg)` |
| `__init__` | method | `topo_swarm_agent.py:1664` | `def __init__(self, model, cfg)` |
| `__init__` | method | `topo_swarm_agent.py:1743` | `def __init__(self, cfg)` |
| `__init__` | method | `topo_swarm_agent.py:1866` | `def __init__(self, cfg, tokenizer, split, logger)` |
| `__init__` | method | `topo_swarm_agent.py:2096` | `def __init__(self, cfg, logger)` |
| `__init__` | method | `topo_swarm_agent.py:2201` | `def __init__(self, cfg)` |
| `__init__` | method | `topo_swarm_agent.py:2248` | `def __init__(self, model, cfg, tokenizer, logger)` |
| `__len__` | method | `topo_swarm_agent.py:2059` | `def __len__(self)` |
| `__post_init__` | method | `topo_swarm_agent.py:212` | `def __post_init__(self)` |
| `_attn_fn` | method | `topo_swarm_agent.py:1278` | `def _attn_fn(self, x)` |
| `_build_cache` | method | `topo_swarm_agent.py:562` | `def _build_cache(self, seq_len)` |
| `_build_torus_graph` | method | `topo_swarm_agent.py:896` | `def _build_torus_graph(self)` |
| `_chunked_ce` | method | `topo_swarm_agent.py:1487` | `def _chunked_ce(logits, targets, chunk_size)` |
| `_decay` | method | `topo_swarm_agent.py:1633` | `def _decay(self)` |
| `_encode_record` | method | `topo_swarm_agent.py:1969` | `def _encode_record(self, rec)` |
| `_evaluate` | method | `topo_swarm_agent.py:2518` | `def _evaluate(self, val_dl)` |
| `_filter` | method | `topo_swarm_agent.py:468` | `def _filter(self, x, kr, ki)` |
| `_get_torus_positions` | method | `topo_swarm_agent.py:304` | `def _get_torus_positions(n_angular, n_radial, device)` |
| `_h_step` | method | `topo_swarm_agent.py:1204` | `def _h_step(self, z)` |
| `_head_filter` | method | `topo_swarm_agent.py:1080` | `def _head_filter(self, x)` |
| `_l_step` | method | `topo_swarm_agent.py:1197` | `def _l_step(self, x, state)` |
| `_load` | method | `topo_swarm_agent.py:1888` | `def _load(self, split)` |
| `_make_optimizer` | method | `topo_swarm_agent.py:2275` | `def _make_optimizer(self, lr)` |
| `_manual_attn` | method | `topo_swarm_agent.py:1113` | `def _manual_attn()` |
| `_message_passing` | method | `topo_swarm_agent.py:950` | `def _message_passing(self, node_feat)` |
| `_param_count` | method | `topo_swarm_agent.py:293` | `def _param_count(module)` |
| `_phase0_calibrate` | method | `topo_swarm_agent.py:2364` | `def _phase0_calibrate(self, dataloader, n_steps)` |
| `_rotate_half` | method | `topo_swarm_agent.py:570` | `def _rotate_half(self, x)` |
| `_set_seed` | method | `topo_swarm_agent.py:283` | `def _set_seed(seed, device)` |
| `_setup_logger` | method | `topo_swarm_agent.py:265` | `def _setup_logger(name, level)` |
| `_synthetic_stubs` | method | `topo_swarm_agent.py:2026` | `def _synthetic_stubs(self, n)` |
| `_torus_soft_assign` | method | `topo_swarm_agent.py:928` | `def _torus_soft_assign(self, phi1, phi2)` |
| `_train_one_batch` | method | `topo_swarm_agent.py:2322` | `def _train_one_batch(self, optimizer, input_ids, targets, accum_step, berry_phase)` |
| `_warmup_cosine_lr` | method | `topo_swarm_agent.py:2305` | `def _warmup_cosine_lr(self, optimizer, step, total_steps, warmup_steps, base_lr)` |
| `berry_phase_rotation` | method | `topo_swarm_agent.py:349` | `def berry_phase_rotation(q, phase)` |
| `build_dataloaders` | method | `topo_swarm_agent.py:2551` | `def build_dataloaders(cfg, tokenizer, logger)` |
| `compute_surprise` | method | `topo_swarm_agent.py:1554` | `def compute_surprise(logits, targets, gate_mean)` |
| `decode` | method | `topo_swarm_agent.py:1793` | `def decode(self, ids)` |
| `encode` | method | `topo_swarm_agent.py:1781` | `def encode(self, text)` |
| `encode_tool_trace` | method | `topo_swarm_agent.py:1820` | `def encode_tool_trace(self, instruction, tool_name, result)` |
| `forward` | method | `topo_swarm_agent.py:410` | `def forward(self, x)` |
| `forward` | method | `topo_swarm_agent.py:476` | `def forward(self, x)` |
| `forward` | method | `topo_swarm_agent.py:518` | `def forward(self, x)` |
| `forward` | method | `topo_swarm_agent.py:574` | `def forward(self, x, seq_len)` |
| `forward` | method | `topo_swarm_agent.py:606` | `def forward(self, x)` |
| `forward` | method | `topo_swarm_agent.py:637` | `def forward(self, x)` |
| `forward` | method | `topo_swarm_agent.py:678` | `def forward(self, x)` |
| `forward` | method | `topo_swarm_agent.py:746` | `def forward(self, x)` |
| `forward` | method | `topo_swarm_agent.py:981` | `def forward(self, x, berry_phase)` |
| `forward` | method | `topo_swarm_agent.py:1086` | `def forward(self, x, is_causal)` |
| `forward` | method | `topo_swarm_agent.py:1208` | `def forward(self, x)` |
| `forward` | method | `topo_swarm_agent.py:1281` | `def forward(self, x, berry_phase)` |
| `forward` | method | `topo_swarm_agent.py:1353` | `def forward(self, input_ids, berry_phase, targets)` |
| `generate` | method | `topo_swarm_agent.py:1434` | `def generate(self, input_ids, max_new_tokens, temperature, top_k, berry_phase, act_halt_threshold)` |
| `hamilton_product` | method | `topo_swarm_agent.py:329` | `def hamilton_product(q1, q2)` |
| `infer` | method | `topo_swarm_agent.py:1682` | `def infer(self, input_ids, tokenizer, max_new_tokens, temperature, top_k)` |
| `inject_moe_adapter` | method | `topo_swarm_agent.py:790` | `def inject_moe_adapter(model, n_experts, top_k, dropout, freeze_backbone, adapter_path)` |
| `load` | method | `topo_swarm_agent.py:779` | `def load(cls, path)` |
| `load` | method | `topo_swarm_agent.py:2150` | `def load(self, model, optimizer, device)` |
| `main` | method | `topo_swarm_agent.py:2594` | `def main()` |
| `normalize` | method | `topo_swarm_agent.py:344` | `def normalize(q, eps)` |
| `sample` | method | `topo_swarm_agent.py:1600` | `def sample(self, n)` |
| `save` | method | `topo_swarm_agent.py:768` | `def save(self, path)` |
| `save` | method | `topo_swarm_agent.py:2108` | `def save(self, model, optimizer, meta, force)` |
| `store` | method | `topo_swarm_agent.py:1579` | `def store(self, episode, surprise)` |
| `tool_token` | method | `topo_swarm_agent.py:1798` | `def tool_token(self, tool_name)` |
| `train` | method | `topo_swarm_agent.py:2405` | `def train(self, train_dl, val_dl, resume)` |
| `update` | method | `topo_swarm_agent.py:2209` | `def update(self, loss)` |
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
| `CoEvolutionEngine` | class | `toposwarm_coevolve.py:452` | `class CoEvolutionEngine` |
| `HarnessEvaluator` | class | `toposwarm_coevolve.py:233` | `class HarnessEvaluator` |
| `HarnessMutation` | class | `toposwarm_coevolve.py:128` | `class HarnessMutation` |
| `MockLazyOwnBridge` | class | `toposwarm_coevolve.py:183` | `class MockLazyOwnBridge` |
| `WeightTrainer` | class | `toposwarm_coevolve.py:392` | `class WeightTrainer` |
| `__init__` | method | `toposwarm_coevolve.py:190` | `def __init__(self)` |
| `__init__` | method | `toposwarm_coevolve.py:244` | `def __init__(self, prompts, lazyown_dir, logger, use_mock_bridge)` |
| `__init__` | method | `toposwarm_coevolve.py:398` | `def __init__(self, logger)` |
| `__init__` | method | `toposwarm_coevolve.py:457` | `def __init__(self, generations, population_size, train_steps_per_gen, proposer_interval, lazyown_dir, logger)` |
| `_build_orchestrator` | method | `toposwarm_coevolve.py:313` | `def _build_orchestrator(self, cfg_dict)` |
| `_clip` | method | `toposwarm_coevolve.py:175` | `def _clip(x, lo, hi)` |
| `_is_on_frontier` | method | `toposwarm_coevolve.py:578` | `def _is_on_frontier(self, cfg, metrics)` |
| `_load` | method | `toposwarm_coevolve.py:403` | `def _load(self)` |
| `_log_run` | method | `toposwarm_coevolve.py:344` | `def _log_run(self, orch, prompt, result, latency_ms, ctx_len, ok, cfg_dict)` |

Next: [SYMBOLS_p2.md](SYMBOLS_p2.md)
