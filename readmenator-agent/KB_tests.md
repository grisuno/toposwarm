# Subsystem: tests

## tests/test_dataset_enhancer.py
- Doc: Tests for dataset enhancer PII sanitizer.
- Layer: testing
- Language: py
- Symbols:
  - `_load_enhancer_module` (function, line 13) `def _load_enhancer_module()`
  - `test_sanitize_ip` (function, line 24) `def test_sanitize_ip()`
  - `test_sanitize_password` (function, line 31) `def test_sanitize_password()`
  - `test_sanitize_ntlm_hash` (function, line 38) `def test_sanitize_ntlm_hash()`
  - `test_sanitize_email` (function, line 44) `def test_sanitize_email()`
  - `test_sanitize_idempotent_on_clean_text` (function, line 50) `def test_sanitize_idempotent_on_clean_text()`

## tests/test_dataset_generator.py
- Doc: Tests for dataset generator noise filter.
- Layer: testing
- Language: py
- Symbols:
  - `_load_gen_module` (function, line 13) `def _load_gen_module()`
  - `test_is_noisy_short_instruction` (function, line 24) `def test_is_noisy_short_instruction()`
  - `test_is_noisy_generic_verb_empty_arg` (function, line 30) `def test_is_noisy_generic_verb_empty_arg()`
  - `test_is_noisy_permitted_with_arg` (function, line 36) `def test_is_noisy_permitted_with_arg()`
  - `test_build_dataset_filters_noise` (function, line 42) `def test_build_dataset_filters_noise()`

## tests/test_model_config.py
- Doc: Tests for model configuration defaults.
- Layer: testing
- Language: py
- Symbols:
  - `_load_mod` (function, line 11) `def _load_mod()`
  - `test_default_scale_is_xl150m` (function, line 25) `def test_default_scale_is_xl150m()`
  - `test_micro_preset_compatible_with_legacy_checkpoint` (function, line 36) `def test_micro_preset_compatible_with_legacy_checkpoint()`

## tests/test_orchestrator.py
- Doc: Tests for LazyOwn orchestrator improvements.
- Layer: testing
- Language: py
- Symbols:
  - `TestSessionContext` (class, line 15) `class TestSessionContext`
  - `TestKeywordRouter` (class, line 56) `class TestKeywordRouter`
  - `TestNeuralRouter` (class, line 89) `class TestNeuralRouter`
  - `TestOrchestratorRun` (class, line 193) `class TestOrchestratorRun`
  - `_load_ctx` (method, line 18) `def _load_ctx(self)`
  - `test_empty_prefix` (method, line 23) `def test_empty_prefix(self)`
  - `test_prefix_with_target` (method, line 28) `def test_prefix_with_target(self)`
  - `test_update_extracts_ip` (method, line 35) `def test_update_extracts_ip(self)`
  - `test_phase_progression` (method, line 43) `def test_phase_progression(self)`
  - `test_findings_from_output` (method, line 49) `def test_findings_from_output(self)`
  - `_load_router` (method, line 59) `def _load_router(self)`
  - `test_recon_keyword` (method, line 63) `def test_recon_keyword(self)`
  - `test_config_keyword` (method, line 69) `def test_config_keyword(self)`
  - `test_c2_keyword` (method, line 74) `def test_c2_keyword(self)`
  - `test_fallback_search` (method, line 79) `def test_fallback_search(self)`
  - `test_extract_arg_ip` (method, line 84) `def test_extract_arg_ip(self)`
  - `orchestrator` (method, line 93) `def orchestrator(self)`
  - `test_neural_route_none_when_no_engine` (method, line 120) `def test_neural_route_none_when_no_engine(self, orchestrator)`
  - `test_neural_route_with_mock_head` (method, line 123) `def test_neural_route_with_mock_head(self, orchestrator)`
  - `test_neural_route_low_confidence_fallback` (method, line 159) `def test_neural_route_low_confidence_fallback(self, orchestrator)`
  - `test_run_updates_session` (method, line 196) `def test_run_updates_session(self)`
  - `mock_register_forward_hook` (method, line 135) `def mock_register_forward_hook(cb)`
  - `mock_model_forward` (method, line 141) `def mock_model_forward(ids)`
  - `mock_register_forward_hook` (method, line 169) `def mock_register_forward_hook(cb)`
  - `mock_model_forward` (method, line 175) `def mock_model_forward(ids)`
- Depends on: `toposwarm_lazyown_orchestrator.py`
