# Polyglot Codebase Knowledge Graph

> Generated offline by **readmenator**. Supports C, C++, Python, Go, Rust, JS/TS, Java, C#, Shell, PHP, Dart, GDScript, Nim, ASM.
> No LLMs. No tokens. Pure static analysis.

**Total Files Parsed:** 17 | **Total Symbols Extracted:** 636 | **Total Imports:** 258

## Structural Knowledge Map
```mermaid
graph TD
    classDef mod fill:#1e1e1e,stroke:#ff6666,stroke-width:2px,color:#fff;
    classDef cls fill:#2d2d2d,stroke:#4ec9b0,stroke-width:2px,color:#fff;
    classDef fn fill:#333,stroke:#dcdcaa,stroke-width:1px,color:#dcdcaa;
    classDef ext fill:#111,stroke:#666,stroke-dasharray: 5 5,color:#aaa;
    toposwarm_lazyown_orchestrator_py["toposwarm_lazyown_orchestrator.py (py)"]
    class toposwarm_lazyown_orchestrator_py mod;
    toposwarm_lazyown_orchestrator_py__resolve_lazyown_dir["_resolve_lazyown_dir"]
    class toposwarm_lazyown_orchestrator_py__resolve_lazyown_dir fn;
    toposwarm_lazyown_orchestrator_py --> toposwarm_lazyown_orchestrator_py__resolve_lazyown_dir
    toposwarm_lazyown_orchestrator_py__import_infer["_import_infer"]
    class toposwarm_lazyown_orchestrator_py__import_infer fn;
    toposwarm_lazyown_orchestrator_py --> toposwarm_lazyown_orchestrator_py__import_infer
    toposwarm_lazyown_orchestrator_py__import_agent["_import_agent"]
    class toposwarm_lazyown_orchestrator_py__import_agent fn;
    toposwarm_lazyown_orchestrator_py --> toposwarm_lazyown_orchestrator_py__import_agent
    toposwarm_lazyown_orchestrator_py__import_meta_harness["_import_meta_harness"]
    class toposwarm_lazyown_orchestrator_py__import_meta_harness fn;
    toposwarm_lazyown_orchestrator_py --> toposwarm_lazyown_orchestrator_py__import_meta_harness
    toposwarm_lazyown_orchestrator_py__import_routing_head["_import_routing_head"]
    class toposwarm_lazyown_orchestrator_py__import_routing_head fn;
    toposwarm_lazyown_orchestrator_py --> toposwarm_lazyown_orchestrator_py__import_routing_head
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
    toposwarm_meta_harness_py["toposwarm_meta_harness.py (py)"]
    class toposwarm_meta_harness_py mod;
    toposwarm_meta_harness_py_MetaHarnessConfig["MetaHarnessConfig"]
    class toposwarm_meta_harness_py_MetaHarnessConfig cls;
    toposwarm_meta_harness_py --> toposwarm_meta_harness_py_MetaHarnessConfig
    toposwarm_meta_harness_py__setup_logger["_setup_logger"]
    class toposwarm_meta_harness_py__setup_logger fn;
    toposwarm_meta_harness_py --> toposwarm_meta_harness_py__setup_logger
    toposwarm_meta_harness_py__stable_id["_stable_id"]
    class toposwarm_meta_harness_py__stable_id fn;
    toposwarm_meta_harness_py --> toposwarm_meta_harness_py__stable_id
    toposwarm_meta_harness_py__now_iso["_now_iso"]
    class toposwarm_meta_harness_py__now_iso fn;
    toposwarm_meta_harness_py --> toposwarm_meta_harness_py__now_iso
    toposwarm_meta_harness_py_MetaHarnessLogger["MetaHarnessLogger"]
    class toposwarm_meta_harness_py_MetaHarnessLogger cls;
    toposwarm_meta_harness_py --> toposwarm_meta_harness_py_MetaHarnessLogger
    toposwarm_infer_py["toposwarm_infer.py (py)"]
    class toposwarm_infer_py mod;
    toposwarm_infer_py__import_agent["_import_agent"]
    class toposwarm_infer_py__import_agent fn;
    toposwarm_infer_py --> toposwarm_infer_py__import_agent
    toposwarm_infer_py_InferenceConfig["InferenceConfig"]
    class toposwarm_infer_py_InferenceConfig cls;
    toposwarm_infer_py --> toposwarm_infer_py_InferenceConfig
    toposwarm_infer_py__safe_eval["_safe_eval"]
    class toposwarm_infer_py__safe_eval fn;
    toposwarm_infer_py --> toposwarm_infer_py__safe_eval
    toposwarm_infer_py_ToolResult["ToolResult"]
    class toposwarm_infer_py_ToolResult cls;
    toposwarm_infer_py --> toposwarm_infer_py_ToolResult
    toposwarm_infer_py_ToolRegistry["ToolRegistry"]
    class toposwarm_infer_py_ToolRegistry cls;
    toposwarm_infer_py --> toposwarm_infer_py_ToolRegistry
    toposwarm_hybrid_py["toposwarm_hybrid.py (py)"]
    class toposwarm_hybrid_py mod;
    toposwarm_hybrid_py__import_agent["_import_agent"]
    class toposwarm_hybrid_py__import_agent fn;
    toposwarm_hybrid_py --> toposwarm_hybrid_py__import_agent
    toposwarm_hybrid_py_HybridConfig["HybridConfig"]
    class toposwarm_hybrid_py_HybridConfig cls;
    toposwarm_hybrid_py --> toposwarm_hybrid_py_HybridConfig
    toposwarm_hybrid_py__setup_logger["_setup_logger"]
    class toposwarm_hybrid_py__setup_logger fn;
    toposwarm_hybrid_py --> toposwarm_hybrid_py__setup_logger
    toposwarm_hybrid_py__safe_eval["_safe_eval"]
    class toposwarm_hybrid_py__safe_eval fn;
    toposwarm_hybrid_py --> toposwarm_hybrid_py__safe_eval
    toposwarm_hybrid_py_ToolResult["ToolResult"]
    class toposwarm_hybrid_py_ToolResult cls;
    toposwarm_hybrid_py --> toposwarm_hybrid_py_ToolResult
    topogpt2_1_py["topogpt2_1.py (py)"]
    class topogpt2_1_py mod;
    topogpt2_1_py_TopoGPT2Config["TopoGPT2Config"]
    class topogpt2_1_py_TopoGPT2Config cls;
    topogpt2_1_py --> topogpt2_1_py_TopoGPT2Config
    topogpt2_1_py_setup_logger["setup_logger"]
    class topogpt2_1_py_setup_logger fn;
    topogpt2_1_py --> topogpt2_1_py_setup_logger
    topogpt2_1_py_set_seed["set_seed"]
    class topogpt2_1_py_set_seed fn;
    topogpt2_1_py --> topogpt2_1_py_set_seed
    topogpt2_1_py_QuaternionOps["QuaternionOps"]
    class topogpt2_1_py_QuaternionOps cls;
    topogpt2_1_py --> topogpt2_1_py_QuaternionOps
    topogpt2_1_py_QuaternionLinear["QuaternionLinear"]
    class topogpt2_1_py_QuaternionLinear cls;
    topogpt2_1_py --> topogpt2_1_py_QuaternionLinear
    toposwarm_coevolve_py["toposwarm_coevolve.py (py)"]
    class toposwarm_coevolve_py mod;
    toposwarm_coevolve_py__resolve_lazyown_dir["_resolve_lazyown_dir"]
    class toposwarm_coevolve_py__resolve_lazyown_dir fn;
    toposwarm_coevolve_py --> toposwarm_coevolve_py__resolve_lazyown_dir
    toposwarm_coevolve_py__setup_logger["_setup_logger"]
    class toposwarm_coevolve_py__setup_logger fn;
    toposwarm_coevolve_py --> toposwarm_coevolve_py__setup_logger
    toposwarm_coevolve_py_HarnessMutation["HarnessMutation"]
    class toposwarm_coevolve_py_HarnessMutation cls;
    toposwarm_coevolve_py --> toposwarm_coevolve_py_HarnessMutation
    toposwarm_coevolve_py__clip["_clip"]
    class toposwarm_coevolve_py__clip fn;
    toposwarm_coevolve_py --> toposwarm_coevolve_py__clip
    toposwarm_coevolve_py_MockLazyOwnBridge["MockLazyOwnBridge"]
    class toposwarm_coevolve_py_MockLazyOwnBridge cls;
    toposwarm_coevolve_py --> toposwarm_coevolve_py_MockLazyOwnBridge
    toposwarm_continual_trainer_py["toposwarm_continual_trainer.py (py)"]
    class toposwarm_continual_trainer_py mod;
    toposwarm_continual_trainer_py__import["_import"]
    class toposwarm_continual_trainer_py__import fn;
    toposwarm_continual_trainer_py --> toposwarm_continual_trainer_py__import
    toposwarm_continual_trainer_py_ContinualConfig["ContinualConfig"]
    class toposwarm_continual_trainer_py_ContinualConfig cls;
    toposwarm_continual_trainer_py --> toposwarm_continual_trainer_py_ContinualConfig
    toposwarm_continual_trainer_py__setup_logger["_setup_logger"]
    class toposwarm_continual_trainer_py__setup_logger fn;
    toposwarm_continual_trainer_py --> toposwarm_continual_trainer_py__setup_logger
    toposwarm_continual_trainer_py_SurpriseBuffer["SurpriseBuffer"]
    class toposwarm_continual_trainer_py_SurpriseBuffer cls;
    toposwarm_continual_trainer_py --> toposwarm_continual_trainer_py_SurpriseBuffer
    toposwarm_continual_trainer_py__load_jsonl["_load_jsonl"]
    class toposwarm_continual_trainer_py__load_jsonl fn;
    toposwarm_continual_trainer_py --> toposwarm_continual_trainer_py__load_jsonl
    meta_harness_proposer_py["meta_harness_proposer.py (py)"]
    class meta_harness_proposer_py mod;
    meta_harness_proposer_py__setup_logger["_setup_logger"]
    class meta_harness_proposer_py__setup_logger fn;
    meta_harness_proposer_py --> meta_harness_proposer_py__setup_logger
    meta_harness_proposer_py_LLMConfig["LLMConfig"]
    class meta_harness_proposer_py_LLMConfig cls;
    meta_harness_proposer_py --> meta_harness_proposer_py_LLMConfig
    meta_harness_proposer_py_LLMClient["LLMClient"]
    class meta_harness_proposer_py_LLMClient cls;
    meta_harness_proposer_py --> meta_harness_proposer_py_LLMClient
    meta_harness_proposer_py_ExperienceReader["ExperienceReader"]
    class meta_harness_proposer_py_ExperienceReader cls;
    meta_harness_proposer_py --> meta_harness_proposer_py_ExperienceReader
    meta_harness_proposer_py_PatchEngine["PatchEngine"]
    class meta_harness_proposer_py_PatchEngine cls;
    meta_harness_proposer_py --> meta_harness_proposer_py_PatchEngine
    tests_test_orchestrator_py["test_orchestrator.py (py)"]
    class tests_test_orchestrator_py mod;
    tests_test_orchestrator_py_TestSessionContext["TestSessionContext"]
    class tests_test_orchestrator_py_TestSessionContext cls;
    tests_test_orchestrator_py --> tests_test_orchestrator_py_TestSessionContext
    tests_test_orchestrator_py_TestKeywordRouter["TestKeywordRouter"]
    class tests_test_orchestrator_py_TestKeywordRouter cls;
    tests_test_orchestrator_py --> tests_test_orchestrator_py_TestKeywordRouter
    tests_test_orchestrator_py_TestNeuralRouter["TestNeuralRouter"]
    class tests_test_orchestrator_py_TestNeuralRouter cls;
    tests_test_orchestrator_py --> tests_test_orchestrator_py_TestNeuralRouter
    tests_test_orchestrator_py_TestOrchestratorRun["TestOrchestratorRun"]
    class tests_test_orchestrator_py_TestOrchestratorRun cls;
    tests_test_orchestrator_py --> tests_test_orchestrator_py_TestOrchestratorRun
    tests_test_orchestrator_py__load_ctx["_load_ctx"]
    class tests_test_orchestrator_py__load_ctx fn;
    tests_test_orchestrator_py --> tests_test_orchestrator_py__load_ctx
    toposwarm_lazyown_sweep_py["toposwarm_lazyown_sweep.py (py)"]
    class toposwarm_lazyown_sweep_py mod;
    toposwarm_lazyown_sweep_py_generate_prompts["generate_prompts"]
    class toposwarm_lazyown_sweep_py_generate_prompts fn;
    toposwarm_lazyown_sweep_py --> toposwarm_lazyown_sweep_py_generate_prompts
    toposwarm_lazyown_sweep_py_setup_logger["setup_logger"]
    class toposwarm_lazyown_sweep_py_setup_logger fn;
    toposwarm_lazyown_sweep_py --> toposwarm_lazyown_sweep_py_setup_logger
    toposwarm_lazyown_sweep_py_run_sweep["run_sweep"]
    class toposwarm_lazyown_sweep_py_run_sweep fn;
    toposwarm_lazyown_sweep_py --> toposwarm_lazyown_sweep_py_run_sweep
    toposwarm_lazyown_sweep_py_write_results["write_results"]
    class toposwarm_lazyown_sweep_py_write_results fn;
    toposwarm_lazyown_sweep_py --> toposwarm_lazyown_sweep_py_write_results
    toposwarm_lazyown_sweep_py_main["main"]
    class toposwarm_lazyown_sweep_py_main fn;
    toposwarm_lazyown_sweep_py --> toposwarm_lazyown_sweep_py_main
    lazyown_dataset_generator_py["lazyown_dataset_generator.py (py)"]
    class lazyown_dataset_generator_py mod;
    lazyown_dataset_generator_py__make_record["_make_record"]
    class lazyown_dataset_generator_py__make_record fn;
    lazyown_dataset_generator_py --> lazyown_dataset_generator_py__make_record
    lazyown_dataset_generator_py__apply_pentest_synonyms["_apply_pentest_synonyms"]
    class lazyown_dataset_generator_py__apply_pentest_synonyms fn;
    lazyown_dataset_generator_py --> lazyown_dataset_generator_py__apply_pentest_synonyms
    lazyown_dataset_generator_py__expand["_expand"]
    class lazyown_dataset_generator_py__expand fn;
    lazyown_dataset_generator_py --> lazyown_dataset_generator_py__expand
    lazyown_dataset_generator_py__is_noisy_phrasing["_is_noisy_phrasing"]
    class lazyown_dataset_generator_py__is_noisy_phrasing fn;
    lazyown_dataset_generator_py --> lazyown_dataset_generator_py__is_noisy_phrasing
    lazyown_dataset_generator_py_build_dataset["build_dataset"]
    class lazyown_dataset_generator_py_build_dataset fn;
    lazyown_dataset_generator_py --> lazyown_dataset_generator_py_build_dataset
    ts_utils_py["ts_utils.py (py)"]
    class ts_utils_py mod;
    ts_utils_py_setup_logger["setup_logger"]
    class ts_utils_py_setup_logger fn;
    ts_utils_py --> ts_utils_py_setup_logger
    ts_utils_py_safe_eval["safe_eval"]
    class ts_utils_py_safe_eval fn;
    ts_utils_py --> ts_utils_py_safe_eval
    ts_utils_py_import_module["import_module"]
    class ts_utils_py_import_module fn;
    ts_utils_py --> ts_utils_py_import_module
    ts_utils_py_make_cached_encode["make_cached_encode"]
    class ts_utils_py_make_cached_encode fn;
    ts_utils_py --> ts_utils_py_make_cached_encode
    ts_utils_py_make_cached_tool_token["make_cached_tool_token"]
    class ts_utils_py_make_cached_tool_token fn;
    ts_utils_py --> ts_utils_py_make_cached_tool_token
    lazyown_dataset_enhancer_py["lazyown_dataset_enhancer.py (py)"]
    class lazyown_dataset_enhancer_py mod;
    lazyown_dataset_enhancer_py__difficulty["_difficulty"]
    class lazyown_dataset_enhancer_py__difficulty fn;
    lazyown_dataset_enhancer_py --> lazyown_dataset_enhancer_py__difficulty
    lazyown_dataset_enhancer_py_ExperienceStoreReader["ExperienceStoreReader"]
    class lazyown_dataset_enhancer_py_ExperienceStoreReader cls;
    lazyown_dataset_enhancer_py --> lazyown_dataset_enhancer_py_ExperienceStoreReader
    lazyown_dataset_enhancer_py__sanitize_output["_sanitize_output"]
    class lazyown_dataset_enhancer_py__sanitize_output fn;
    lazyown_dataset_enhancer_py --> lazyown_dataset_enhancer_py__sanitize_output
    lazyown_dataset_enhancer_py__build_toolbench_record["_build_toolbench_record"]
    class lazyown_dataset_enhancer_py__build_toolbench_record fn;
    lazyown_dataset_enhancer_py --> lazyown_dataset_enhancer_py__build_toolbench_record
    lazyown_dataset_enhancer_py_DatasetEnhancer["DatasetEnhancer"]
    class lazyown_dataset_enhancer_py_DatasetEnhancer cls;
    lazyown_dataset_enhancer_py --> lazyown_dataset_enhancer_py_DatasetEnhancer
    tests_test_dataset_enhancer_py["test_dataset_enhancer.py (py)"]
    class tests_test_dataset_enhancer_py mod;
    tests_test_dataset_enhancer_py__load_enhancer_module["_load_enhancer_module"]
    class tests_test_dataset_enhancer_py__load_enhancer_module fn;
    tests_test_dataset_enhancer_py --> tests_test_dataset_enhancer_py__load_enhancer_module
    tests_test_dataset_enhancer_py_test_sanitize_ip["test_sanitize_ip"]
    class tests_test_dataset_enhancer_py_test_sanitize_ip fn;
    tests_test_dataset_enhancer_py --> tests_test_dataset_enhancer_py_test_sanitize_ip
    tests_test_dataset_enhancer_py_test_sanitize_password["test_sanitize_password"]
    class tests_test_dataset_enhancer_py_test_sanitize_password fn;
    tests_test_dataset_enhancer_py --> tests_test_dataset_enhancer_py_test_sanitize_password
    tests_test_dataset_enhancer_py_test_sanitize_ntlm_hash["test_sanitize_ntlm_hash"]
    class tests_test_dataset_enhancer_py_test_sanitize_ntlm_hash fn;
    tests_test_dataset_enhancer_py --> tests_test_dataset_enhancer_py_test_sanitize_ntlm_hash
    tests_test_dataset_enhancer_py_test_sanitize_email["test_sanitize_email"]
    class tests_test_dataset_enhancer_py_test_sanitize_email fn;
    tests_test_dataset_enhancer_py --> tests_test_dataset_enhancer_py_test_sanitize_email
    tests_test_dataset_generator_py["test_dataset_generator.py (py)"]
    class tests_test_dataset_generator_py mod;
    tests_test_dataset_generator_py__load_gen_module["_load_gen_module"]
    class tests_test_dataset_generator_py__load_gen_module fn;
    tests_test_dataset_generator_py --> tests_test_dataset_generator_py__load_gen_module
    tests_test_dataset_generator_py_test_is_noisy_short_instruction["test_is_noisy_short_instruction"]
    class tests_test_dataset_generator_py_test_is_noisy_short_instruction fn;
    tests_test_dataset_generator_py --> tests_test_dataset_generator_py_test_is_noisy_short_instruction
    tests_test_dataset_generator_py_test_is_noisy_generic_verb_empty_arg["test_is_noisy_generic_verb_empty_arg"]
    class tests_test_dataset_generator_py_test_is_noisy_generic_verb_empty_arg fn;
    tests_test_dataset_generator_py --> tests_test_dataset_generator_py_test_is_noisy_generic_verb_empty_arg
    tests_test_dataset_generator_py_test_is_noisy_permitted_with_arg["test_is_noisy_permitted_with_arg"]
    class tests_test_dataset_generator_py_test_is_noisy_permitted_with_arg fn;
    tests_test_dataset_generator_py --> tests_test_dataset_generator_py_test_is_noisy_permitted_with_arg
    tests_test_dataset_generator_py_test_build_dataset_filters_noise["test_build_dataset_filters_noise"]
    class tests_test_dataset_generator_py_test_build_dataset_filters_noise fn;
    tests_test_dataset_generator_py --> tests_test_dataset_generator_py_test_build_dataset_filters_noise
    tests_test_model_config_py["test_model_config.py (py)"]
    class tests_test_model_config_py mod;
    tests_test_model_config_py_test_d_model_compatible_with_checkpoint["test_d_model_compatible_with_checkpoint"]
    class tests_test_model_config_py_test_d_model_compatible_with_checkpoint fn;
    tests_test_model_config_py --> tests_test_model_config_py_test_d_model_compatible_with_checkpoint
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

## Architecture Reference

### PY (17 files)

#### `lazyown_dataset_enhancer.py`
**Path:** `lazyown_dataset_enhancer.py`

**Classs:**
- `ExperienceStoreReader` (line 87)
- `DatasetEnhancer` (line 165)

**Functions:**
- `_difficulty` (line 64) - *Lower = easier.  Factors:
  - prompt length (shorter = easier)
  - number of words (fewer = easier)
  - output length (shorter = easier)
  - has error markers (harder)*
- `_sanitize_output` (line 136) - *Redact potential PII / sensitive data from LazyOwn output traces.*
- `_build_toolbench_record` (line 149) - *Standard ToolBench-format record.*
- `print_stats` (line 348)
- `main` (line 375)
- `__init__` (line 88)
- `list_runs` (line 91)
- `read_trace` (line 98)
- `read_score` (line 113)
- `read_harness` (line 122)
- `__init__` (line 166)
- `enhance` (line 171)
- `add_negative_examples` (line 236) - *Add examples where the prompt is ambiguous and the model must NOT
pick a random tool, or where the user asks something outside LazyOwn's scope.*
- `curriculum_sort` (line 261) - *Sort by difficulty (easy → hard).*
- `deduplicate` (line 265) - *Deduplicate by instruction text only (same prompt can have different outputs).*
- `augment_simple` (line 276) - *Lightweight augmentation: replace IP addresses, hostnames, and common
keywords with variants to increase diversity without an LLM.*
- `run` (line 301)

#### `lazyown_dataset_generator.py`
**Path:** `lazyown_dataset_generator.py`

**Functions:**
- `_make_record` (line 3321)
- `_apply_pentest_synonyms` (line 3414) - *Replace common pentest terms with synonyms to increase diversity.*
- `_expand` (line 3430) - *Generate additional phrasings via IP substitution, prefix injection, verb swap, and synonym replacement.*
- `_is_noisy_phrasing` (line 3554) - *Return True if the phrasing is too generic and likely to dilute training.
Criteria:
  - empty arg AND the instruction starts with a generic verb
  - instruction has fewer than 4 meaningful tokens*
- `build_dataset` (line 3571)
- `write_jsonl` (line 3595)
- `print_stats` (line 3602)
- `main` (line 3616)

#### `meta_harness_proposer.py`
**Path:** `meta_harness_proposer.py`

**Classs:**
- `LLMConfig` (line 75)
- `LLMClient` (line 86) - *Minimal OpenAI-compatible chat client using only urllib.

Auto-falls back to local Ollama if the primary endpoint returns
401/403/404 (auth or routing errors).*
- `ExperienceReader` (line 150) - *Reads meta_harness_logs/ and builds diagnostic context.*
- `PatchEngine` (line 243) - *Applies code patches safely.*
- `MetaHarnessProposer` (line 392) - *Coding-agent proposer for harness optimisation.

Workflow:
    1. Read experience store (scores + traces).
    2. Build diagnostic context.
    3. Read current harness source.
    4. Prompt LLM to propose a patch.
    5. Validate & apply patch.
    6. Log the proposal as a new run.*

**Functions:**
- `_setup_logger` (line 58)
- `main` (line 572)
- `__init__` (line 93)
- `_try_chat` (line 97)
- `chat` (line 121) - *Send a chat request and return the assistant message content.*
- `__init__` (line 153)
- `list_runs` (line 157)
- `load_run` (line 165)
- `build_diagnostic_context` (line 193) - *Build a rich diagnostic string containing:
- failed runs with their traces
- successful runs for contrast
- aggregate statistics*
- `__init__` (line 246)
- `validate_syntax` (line 249) - *Return (ok, error_message).*
- `apply_full_rewrite` (line 265) - *Validate and optionally write a full file rewrite.*
- `_strip_line_numbers` (line 283) - *Remove leading ' 123: ' line numbers that the LLM may copy.*
- `apply_line_range` (line 287) - *Replace a range of lines (1-indexed) with new text.*
- `apply_diff_hunk` (line 316) - *Apply a targeted string replacement after validation.

Tries exact match first, then fuzzy match (ignoring leading/trailing
whitespace per line), then without line numbers.  If all fail, prints
the patch for manual apply.*
- `__init__` (line 434)
- `propose_patch` (line 445) - *End-to-end propose-and-apply cycle.

Returns True if a patch was successfully applied (or validated in dry-run).*
- `_log_proposal` (line 538) - *Store the proposer's reasoning so future loops can evaluate it.*
- `_norm` (line 331)

#### `test_dataset_enhancer.py`
**Path:** `tests/test_dataset_enhancer.py`

**Functions:**
- `_load_enhancer_module` (line 13)
- `test_sanitize_ip` (line 24)
- `test_sanitize_password` (line 31)
- `test_sanitize_ntlm_hash` (line 38)
- `test_sanitize_email` (line 44)
- `test_sanitize_idempotent_on_clean_text` (line 50)

#### `test_dataset_generator.py`
**Path:** `tests/test_dataset_generator.py`

**Functions:**
- `_load_gen_module` (line 13)
- `test_is_noisy_short_instruction` (line 24)
- `test_is_noisy_generic_verb_empty_arg` (line 30)
- `test_is_noisy_permitted_with_arg` (line 36)
- `test_build_dataset_filters_noise` (line 42)

#### `test_model_config.py`
**Path:** `tests/test_model_config.py`

**Functions:**
- `test_d_model_compatible_with_checkpoint` (line 11)

#### `test_orchestrator.py`
**Path:** `tests/test_orchestrator.py`

**Classs:**
- `TestSessionContext` (line 15) - *Unit tests for the multi-turn SessionContext.*
- `TestKeywordRouter` (line 56) - *Tests for the deterministic keyword fallback router.*
- `TestNeuralRouter` (line 89) - *Tests for the neural route path using mocks.*
- `TestOrchestratorRun` (line 193) - *Integration-level tests for the run() method.*

**Functions:**
- `_load_ctx` (line 18)
- `test_empty_prefix` (line 23)
- `test_prefix_with_target` (line 28)
- `test_update_extracts_ip` (line 35)
- `test_phase_progression` (line 43)
- `test_findings_from_output` (line 49)
- `_load_router` (line 59)
- `test_recon_keyword` (line 63)
- `test_config_keyword` (line 69)
- `test_c2_keyword` (line 74)
- `test_fallback_search` (line 79)
- `test_extract_arg_ip` (line 84)
- `orchestrator` (line 93)
- `test_neural_route_none_when_no_engine` (line 120)
- `test_neural_route_with_mock_head` (line 123)
- `test_neural_route_low_confidence_fallback` (line 159)
- `test_run_updates_session` (line 196)
- `mock_register_forward_hook` (line 135)
- `mock_model_forward` (line 141)
- `mock_register_forward_hook` (line 169)
- `mock_model_forward` (line 175)

#### `topo_swarm_agent.py`
**Path:** `topo_swarm_agent.py`

**Classs:**
- `SwarmConfig` (line 84) - *All architectural and training hyper-parameters in one place.

Scale target: fit inside 6 GB VRAM on an RTX 2060.
- Weights: ~2 M params × 4 bytes = ~8 MB
- Activations (B=4, S=256): ~256 MB peak with gradient checkpointing
- Swarm overhead: N_AGENTS × D_MODEL × 4 bytes per Berry-phase tensor*
- `QuaternionOps` (line 282) - *Pure-functional quaternion operations over arbitrary leading batch dims.
Tensors have shape [..., 4] where the last dim is [w, x, y, z].*
- `QuaternionLinear` (line 330) - *Linear map in the quaternion algebra.

Implements W ⊗ x via a single batched einsum over stacked weight matrices,
reducing CUDA kernel launches from 16 (naive 4×4 matmul loop) to 1.

Input  x: [..., 4*in_q]
Output  : [..., 4*out_q]*
- `SpectralBottleneck` (line 394) - *1-D spectral autoencoder acting as the function-call signal filter.

Compresses the token representation via rfft → learned complex kernel →
irfft → QuaternionLinear bottleneck → decode.  The bottleneck forces the
model to route function-call intent through a harmonic low-band subspace,
suppressing lexical noise from the surrounding context.

Returns (latent [B,S,latent_dim], recon_loss scalar).*
- `RMSNorm` (line 465) - *Root Mean Square Layer Normalisation (LLaMA-style, no bias).*
- `RotaryEmbedding` (line 489) - *NTK-aware Rotary Position Embeddings.

Extends the standard RoPE base frequency when the requested sequence length
exceeds the training context, preventing aliasing in high-frequency dims.*
- `SwiGLU` (line 548) - *SwiGLU feed-forward: SiLU(gate(x)) * up(x) → down(...).*
- `SwarmMoEGate` (line 587) - *Sigmoid gate: selects top-k experts per token, weights normalised.*
- `SwarmMoE` (line 608) - *Drop-in MoE replacement for SwiGLU in TopoSwarmLayer.

Architecture: N_EXPERTS independent SwiGLU experts + sigmoid gate.
Each token routes to top_k experts; outputs are weighted-summed.

For a 2M-param model (D=64, FFN_DIM=128):
  - 4 experts, top-2, expert_dim=128 → same FLOP as one dense FFN
    but 4× more representational capacity.*
- `SwarmMoEAdapter` (line 665) - *Residual MoE adapter: output = LayerNorm(input + moe(input)).

Plugs between model.norm_out and model.lm_head.  Zero-init on the output
projection of every expert means the adapter is an identity at init time —
the model starts at its existing accuracy and the adapter learns on top.

Expert architecture: d_model → d_model//2 → d_model (small bottleneck)
Gate: sigmoid (MiMo V2 style) → top-k selection, normalised weights.*
- `QuaternionTorusBrain` (line 807) - *Toroidal message-passing FFN replacement.

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
- `QuaternionAttention` (line 998) - *Grouped-query attention (GQA) with RoPE and quaternion Q/K projections.

A lightweight per-head 1-D spectral filter compresses the query and key
vectors before dot-product attention, forcing harmonic representations.*
- `HRMModule` (line 1103) - *Hierarchical Reasoning Model embedded in the torus agent.

L-module (fast / action): recurrent GRU-gated unit responsible for
the syntax of tool calls (the "how").

H-module (slow / strategy): a wider linear unit responsible for
tool selection (the "what").

The ACT (Adaptive Computational Time) halt logit is computed from the
Hamilton-product norm of the final H-state quaternion: when the norm
exceeds ACT_HALT_THRESHOLD the agent emits a decision; otherwise it
re-enters the message-passing loop (the "swarm consult" step).*
- `TopoSwarmLayer` (line 1205) - *Single transformer layer: GQA attention + QuaternionTorusBrain FFN.

Both sub-layers use pre-norm (RMSNorm) and residual connections.
Gradient checkpointing is applied to the attention sub-layer.*
- `TopoSwarmModel` (line 1273) - *Micro quaternionic toroidal transformer for tool-use reasoning.

Architecture:
- Token embedding + learned positional bias.
- N_LAYERS of TopoSwarmLayer (GQA + QuaternionTorusBrain).
- HRM module on the pooled representation for ACT control.
- Language-model head (tied weights with embedding).

The Berry-phase offset is passed through every layer to specialise each
swarm agent slot without duplicating weight tensors.*
- `EpisodicMemory` (line 1487) - *Three-tier episodic memory inspired by the tricameral neurology architecture.

Tier assignment is driven by a surprise score: cross-entropy modulated by
the mean ACT gate activity.  High-surprise events go to working memory
(highest replay priority); low-surprise events to long-term if their
computed importance exceeds a threshold.*
- `SwarmOrchestrator` (line 1602) - *Coordinates N_AGENTS lightweight agent slots over a shared weight tensor.

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
- `BPETokenizer` (line 1693) - *Thin wrapper around tiktoken's GPT-2 BPE encoding.

Adds special tool tokens by reserving a range at the top of the
vocabulary [TOOL_TOKEN_OFFSET, TOOL_TOKEN_OFFSET + TOOL_VOCAB_SIZE).*
- `ToolBenchDataset` (line 1811) - *ToolBench "Instruction-Tool-Result" dataset loader.

Attempts to load from HuggingFace datasets first; falls back to a local
JSONL file at cfg.DATASET_LOCAL_PATH.  Only successful traces
(is_halt=True or equivalent) are retained.

Each sample is a flat token sequence:
    [instruction tokens] [tool token] [result tokens]
truncated to MAX_SEQ_LEN.  Training targets are the input shifted by 1.*
- `CheckpointManager` (line 2046) - *Manages safetensors checkpoints with JSON metadata in a single directory.

Writes to checkpoints_toposwarm/latest/ atomically by writing a temp
file and renaming it.*
- `KappaDetector` (line 2149) - *Tracks the kappa coherence metric over a sliding window to detect grokking.

Kappa is defined as the inverse of the cross-entropy loss (clipped),
normalised to [0, 1].  A sharp upward jump of more than KAPPA_JUMP_THRESHOLD
within the window signals that the model has found the function-call
structure (the ToolBench grokking point).*
- `SwarmTrainer` (line 2192) - *Three-phase training pipeline for the TopoSwarm agent.

Phase 0 (Kernel Calibration): Pre-trains only the SpectralBottleneck
parameters on the API schema strings to seed the harmonic filter.

Phase 1 (Main Training): Full model training with grokking detection
via the KappaDetector.

Phase 2 (Annealing): Fine-tunes with a reduced learning rate and
cosine schedule to stabilise the tool-call routing.*

**Functions:**
- `_setup_logger` (line 225) - *Return an idempotent logger. Delegates to ts_utils.setup_logger.*
- `_set_seed` (line 243) - *Deterministic seed across torch, numpy, and CUDA.*
- `_param_count` (line 253) - *Return total and trainable parameter counts.*
- `_get_torus_positions` (line 264) - *Cached angular / radial position linspaces for soft torus assignment.*
- `inject_moe_adapter` (line 749) - *Inject a SwarmMoEAdapter into an already-loaded TopoSwarmModel.

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
- `_chunked_ce` (line 1445) - *Cross-entropy over the sequence without materialising the full [N, V] matrix.

Processes the sequence in chunks of chunk_size to bound peak memory to
O(chunk_size × VOCAB_SIZE) instead of O(B*S × VOCAB_SIZE).

Args:
    logits: [B, S, V] or [N, V].
    targets: [B, S] or [N] integer targets.
    chunk_size: Tokens per chunk.

Returns:
    Scalar mean cross-entropy.*
- `build_dataloaders` (line 2509) - *Build train and validation DataLoaders from the ToolBench dataset.

Args:
    cfg: Swarm configuration.
    tokenizer: BPETokenizer for encoding.
    logger: Logger instance.

Returns:
    Tuple of (train_loader, val_loader).*
- `main` (line 2552) - *CLI entry point.

Modes:
    --train             : Run the full three-phase training pipeline.
    --resume            : Resume training from the latest checkpoint.
    --infer --prompt P  : Load checkpoint and run swarm inference.
    --param-count       : Print model parameter counts and exit.*
- `__post_init__` (line 202)
- `hamilton_product` (line 289) - *Hamilton (cross) product q1 ⊗ q2 for tensors of shape [..., 4].*
- `normalize` (line 304) - *Unit-normalise quaternion tensors.*
- `berry_phase_rotation` (line 309) - *Apply a Berry-phase rotation around the w-axis of the quaternion manifold.

Multiplies the (x, y, z) imaginary components by the complex phase
e^{i*phase} encoded as a rotation in the yz-plane, leaving the real
component w unchanged.  Used to differentiate swarm agent slots.*
- `__init__` (line 341) - *Initialise quaternion weight matrices.

Args:
    in_features: Must be divisible by 4.
    out_features: Must be divisible by 4.
    bias: Whether to add a bias parameter.
    init_std: Normal initialisation standard deviation.*
- `forward` (line 370) - *Fused Hamilton product via a single batched einsum.*
- `__init__` (line 406) - *Build encoder/decoder spectral kernels and quaternion projections.

Args:
    cfg: Swarm configuration object.*
- `_filter` (line 428) - *Apply a learned complex spectral filter in the rfft domain.*
- `forward` (line 436) - *Encode x through the spectral bottleneck.

A single rfft of x is computed and reused by both the encode branch
and the high-frequency penalty, avoiding a redundant FFT call.

Args:
    x: Input tensor [..., D_MODEL].

Returns:
    Tuple of (latent [..., latent_dim], scalar auxiliary loss).*
- `__init__` (line 468) - *Args:
    d_model: Feature dimension.
    eps: Numerical stability epsilon.*
- `forward` (line 478) - *Normalise by the RMS of x and rescale by learned weight.*
- `__init__` (line 497) - *Args:
    d_head: Attention head dimension.
    max_seq_len: Maximum sequence length to pre-cache.
    base: RoPE base frequency.
    ntk_factor: Set to max_seq / train_seq when extrapolating.*
- `_build_cache` (line 522) - *Pre-compute cos/sin tables up to seq_len.*
- `_rotate_half` (line 530)
- `forward` (line 534) - *Apply rotary embedding to query or key tensor [B, H, S, d_head].*
- `__init__` (line 551) - *Args:
    d_model: Input and output feature dimension.
    hidden_dim: Intermediate expansion dimension.
    dropout: Dropout probability after the output projection.*
- `forward` (line 566) - *Gated SiLU activation with residual dropout.*
- `__init__` (line 590)
- `forward` (line 597) - *x: [..., D] → (topk_idx [... K], topk_weight [..., K])*
- `__init__` (line 620)
- `forward` (line 637) - *x: [B, S, D] → [B, S, D]  (autograd-safe, no in-place scatter)*
- `__init__` (line 679)
- `forward` (line 705) - *x: [B, S, D] → [B, S, D]  (residual)

Autograd-safe: no in-place scatter — computes all expert outputs at
once and weights them via a sparse weight tensor.*
- `save` (line 727)
- `load` (line 738)
- `__init__` (line 825) - *Args:
    cfg: Swarm configuration.*
- `_build_torus_graph` (line 855) - *Construct the adjacency structure of the discrete torus.

Each node (r, a) connects angularly to (r, a±1) and radially to
(r±1, a).  Angular neighbours wrap around (periodic boundary).
Radial neighbours are open (no wrap).  Edge types encode direction:
0=ang-left, 1=ang-right, 2=rad-inner, 3=rad-outer.*
- `_torus_soft_assign` (line 887) - *Soft assignment of token coordinates to torus nodes via haversine distance.

Args:
    phi1: Angular coordinate [-pi, pi] of shape [N].
    phi2: Radial coordinate [-pi, pi] of shape [N].

Returns:
    Soft assignment weights [N, N_TORUS_NODES] summing to 1.*
- `_message_passing` (line 909) - *One round of quaternion message-passing on the torus graph.

Messages are Hamilton-product-rotated by a learnable edge quaternion
and aggregated via scatter-add to each destination node.

Args:
    node_feat: Node feature tensor [N_chunk, N_NODES, D_MODEL].

Returns:
    Updated node features [N_chunk, N_NODES, D_MODEL].*
- `forward` (line 940) - *Full torus forward with optional Berry-phase offset for swarm slots.

Processes tokens in chunks to bound peak VRAM.

Args:
    x: Input [B, S, D_MODEL].
    berry_phase: Phase offset applied to the torus projection output
                 for this agent slot, rotating the soft assignment
                 and inducing specialisation.

Returns:
    Tuple of (output [B, S, D_MODEL], scalar auxiliary recon loss).*
- `__init__` (line 1006) - *Args:
    cfg: Swarm configuration.*
- `_head_filter` (line 1039) - *Apply the shared per-head spectral filter [B, H, S, d_head].*
- `forward` (line 1045) - *GQA forward pass with RoPE and optional gradient checkpointing.

Args:
    x: Input [B, S, D].
    is_causal: Whether to apply causal masking.

Returns:
    Output [B, S, D].*
- `__init__` (line 1119) - *Args:
    cfg: Swarm configuration.*
- `_l_step` (line 1156) - *One GRU-gated L-module step.*
- `_h_step` (line 1163) - *One H-module strategy update.*
- `forward` (line 1167) - *Run the HRM hierarchy and return the updated state with ACT signal.

Args:
    x: Pooled context embedding [B, D].

Returns:
    Tuple of (h_state [B, D], halt_logit [B, 1], act_loss scalar).*
- `__init__` (line 1213) - *Args:
    cfg: Swarm configuration.*
- `_attn_fn` (line 1237)
- `forward` (line 1240) - *Pre-norm layer forward.

Args:
    x: Input [B, S, D].
    berry_phase: Swarm Berry-phase offset for the torus brain.

Returns:
    Tuple of (output [B, S, D], torus recon loss scalar).*
- `__init__` (line 1287) - *Args:
    cfg: Swarm configuration.*
- `forward` (line 1311) - *Full forward pass for one agent slot.

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
- `generate` (line 1392) - *Autoregressive generation with ACT-driven early stopping.

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
- `__init__` (line 1497) - *Args:
    cfg: Swarm configuration for capacity and threshold parameters.*
- `compute_surprise` (line 1512) - *Surprise = cross-entropy × (1 - gate_mean), clipped to [0, 10].

A high gate_mean (confident model) attenuates the surprise signal;
a low gate_mean (uncertain) amplifies it.

Args:
    logits: Raw model logits [B, S, V] or [N, V].
    targets: Integer targets matching logits.
    gate_mean: Mean ACT halt probability in [0, 1].

Returns:
    Scalar surprise value.*
- `store` (line 1537) - *Store an episode in the appropriate memory tier.

Args:
    episode: Dict of tensors/metadata describing the experience.
    surprise: Scalar surprise score from compute_surprise.*
- `sample` (line 1558) - *Sample n episodes with priority proportional to surprise / importance.

Draws from all three tiers; working memory contributes the most
samples (50 %), short-term 30 %, long-term 20 %.

Args:
    n: Number of episodes to sample.

Returns:
    List of episode dicts.*
- `_decay` (line 1591) - *Apply exponential forgetting to the long-term memory scores.*
- `__init__` (line 1622) - *Args:
    model: Shared TopoSwarmModel instance.
    cfg: Swarm configuration.*
- `infer` (line 1640) - *Run swarm inference and return the decoded output string.

Args:
    input_ids: Prompt token ids [1, S].
    tokenizer: BPETokenizer used to decode output ids.
    max_new_tokens: Maximum tokens any slot may generate.
    temperature: Sampling temperature.
    top_k: Top-k sampling truncation.

Returns:
    Decoded string of the winning slot's output.*
- `__init__` (line 1701) - *Args:
    cfg: Swarm config (provides TOOL_TOKEN_OFFSET and TOOL_VOCAB_SIZE).*
- `encode` (line 1739) - *Encode text to BPE token ids, clamped to the BPE vocab ceiling.

tiktoken encodes exclusively within [0, bpe_vocab_size), but we clamp
defensively to prevent any edge-case overflow from reaching the
embedding table lookup.*
- `decode` (line 1751) - *Decode token ids to text, silently dropping tool tokens.*
- `tool_token` (line 1756) - *Return a stable integer token id for a named tool.

Assigns a deterministic id within the tool-token range based on the
MD5 hash of the tool name, ensuring consistent mapping across runs.
The result is always in [TOOL_TOKEN_OFFSET, TOOL_TOKEN_OFFSET + TOOL_VOCAB_SIZE)
which is guaranteed to be < VOCAB_SIZE by the __init__ check above.

Args:
    tool_name: Canonical tool identifier string.

Returns:
    Integer token id in [TOOL_TOKEN_OFFSET, TOOL_TOKEN_OFFSET + TOOL_VOCAB_SIZE).*
- `encode_tool_trace` (line 1778) - *Encode a ToolBench-style (instruction, tool, result) triple.

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
- `__init__` (line 1824) - *Args:
    cfg: Swarm configuration.
    tokenizer: BPETokenizer for encoding traces.
    split: Dataset split name.
    logger: Optional logger instance.*
- `_load` (line 1846) - *Load and tokenise tool traces with three-level fallback.

Level 1 – Maurus/ToolBench (HuggingFace parquet, no loading script).
    Schema: {query, api_list, domain}.  api_list is a JSON list of
    dicts each with keys tool_name and api_name.
Level 2 – local JSONL at cfg.DATASET_LOCAL_PATH.
    Accepted schemas: any dict with recognisable query/tool/result keys.
Level 3 – synthetic stubs of fixed length MAX_SEQ_LEN with token ids
    inside [0, VOCAB_SIZE).  Safe dry-run fallback.*
- `_encode_record` (line 1927) - *Encode a tool-trace record to token ids.

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
- `_synthetic_stubs` (line 1984) - *Generate n synthetic tool-trace stubs safe for dry-run training.

All token ids produced from these stubs are guaranteed to be within
[0, VOCAB_SIZE) because:
- instruction and result text encode to ids within [0, bpe_vocab_size).
- tool_token() returns ids within [TOOL_TOKEN_OFFSET, TOOL_TOKEN_OFFSET
  + TOOL_VOCAB_SIZE) < VOCAB_SIZE (validated in BPETokenizer.__init__).*
- `__len__` (line 2017)
- `__getitem__` (line 2020) - *Return a (input_ids, target_ids) pair of length MAX_SEQ_LEN.

Token ids are clamped to [0, VOCAB_SIZE - 1] as a hard safety guard
against any upstream encoding edge case that could produce an
out-of-bounds embedding lookup on the GPU.*
- `__init__` (line 2054) - *Args:
    cfg: Swarm configuration.
    logger: Logger instance.*
- `save` (line 2066) - *Save model weights and metadata if the interval has elapsed.

Args:
    model: Model to checkpoint.
    optimizer: Optimizer state to checkpoint.
    meta: Scalar metadata dict (epoch, step, loss, etc.).
    force: If True, save regardless of the time interval.*
- `load` (line 2108) - *Load model weights and metadata from the latest checkpoint.

Args:
    model: Target model (mutated in-place).
    optimizer: Optional optimizer to restore state into.
    device: Device string for weight map.

Returns:
    Metadata dict if found, None otherwise.*
- `__init__` (line 2159) - *Args:
    cfg: Swarm configuration (window and threshold).*
- `update` (line 2167) - *Update the detector with the latest loss value.

Args:
    loss: Scalar training loss.

Returns:
    Tuple of (current_kappa, grokking_detected bool).*
- `__init__` (line 2206) - *Args:
    model: TopoSwarmModel instance.
    cfg: Swarm configuration.
    tokenizer: BPETokenizer.
    logger: Logger instance.*
- `_make_optimizer` (line 2233) - *Build AdamW with weight decay applied only to non-bias, non-norm params.

Args:
    lr: Learning rate.

Returns:
    Configured AdamW optimizer.*
- `_warmup_cosine_lr` (line 2263) - *Apply warmup + cosine decay learning rate schedule.*
- `_train_one_batch` (line 2280) - *Forward + backward for one micro-batch, returns detached loss.

Args:
    optimizer: Current optimizer.
    input_ids: [B, S] token ids.
    targets: [B, S] target ids.
    accum_step: Index within the gradient accumulation window.
    berry_phase: Agent slot phase for this forward pass.

Returns:
    Scalar loss value (Python float).*
- `_phase0_calibrate` (line 2322) - *Phase 0: Kernel calibration on API schema tokens.

Freezes all parameters except the SpectralBottleneck kernels,
training only the spectral filter to recognise API intent.

Args:
    dataloader: Training dataloader.
    n_steps: Number of calibration gradient steps.*
- `train` (line 2363) - *Full three-phase training loop.

Phase 0: Kernel calibration (50 steps, spectral params only).
Phase 1: Main training for cfg.EPOCHS epochs with kappa detection.
Phase 2: Cosine annealing for 1 extra epoch at half learning rate.

Args:
    train_dl: Training DataLoader.
    val_dl: Validation DataLoader.
    resume: If True, attempt to restore from the latest checkpoint.*
- `_evaluate` (line 2476) - *Compute mean validation loss over the first EVAL_INTERVAL_STEPS batches.

Args:
    val_dl: Validation DataLoader.

Returns:
    Mean loss scalar.*
- `_manual_attn` (line 1072)

#### `topogpt2_1.py`
**Path:** `topogpt2_1.py`

**Classs:**
- `TopoGPT2Config` (line 55) - *Configuración completa para TopoGPT2.*
- `QuaternionOps` (line 177) - *Operaciones de cuaterniones puras en PyTorch.
Representación: [..., 4]  donde last dim = [w, x, y, z]
q = w + x*i + y*j + z*k*
- `QuaternionLinear` (line 216) - *Capa lineal con pesos cuaterniones.

Implementa la multiplicación W * x en el álgebra de cuaterniones:
- W = Ww + Wx*i + Wy*j + Wz*k  (cuaternión de pesos)
- x = xw + xx*i + xy*j + xz*k  (cuaternión de entrada)
- out = W * x  (producto de Hamilton extendido a vectores)

Parámetros: 4 matrices reales de forma [out_q, in_q]*
- `QuaternionSpectralLayer` (line 261) - *Convolución espectral 2D con cuaterniones y producto de Hamilton completo.

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
- `SpectralAutoencoder` (line 348) - *Autoencoder espectral con cuaterniones.

Opera en dos niveles:
1. Espectral 1D sobre el vector de features (FFT sobre dim D_MODEL):
   captura la espectrografía global del embedding.
2. Espectral 2D sobre el grid del toro (QuaternionSpectralLayer):
   captura correlaciones espaciales en la topología.

Devuelve (latent, recon_loss) para regularización.*
- `QuaternionTorusBrain` (line 431) - *Reemplaza el MLP en cada capa del transformer.

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
- `RotaryEmbedding` (line 648) - *Rotary Position Embeddings (RoPE) - Su et al., 2021.
Codifica la posición como rotaciones del espacio de atención,
naturalmente relativas y sin parámetros extra.*
- `RMSNorm` (line 696) - *Root Mean Square Layer Normalization (sin bias). Más estable que LayerNorm.*
- `SwiGLU` (line 713) - *SwiGLU: SiLU(gate(x)) * up(x) -> down
Usado en LLaMA 2/3, Qwen, Mistral en lugar de GELU-FFN.
Dimension interna: 8/3 * d_model (convención LLaMA, redondeada a múltiplo de 4).*
- `TopoMoEBrain` (line 742) - *Mixture of Experts sobre la capa topologica.

Arquitectura (inspirada en DeepSeek-MoE / Mixtral):
  - 1 experto compartido: QuaternionTorusBrain (siempre activo)
  - N_EXPERTS expertos SwiGLU ligeros (activacion esparsa: Top-K por token)
  - Router: Linear(D, N_EXPERTS) + softmax → top-K

Load-balancing loss (auxiliar): penaliza si un experto acapara todos los tokens.
Activa MOE_TOP_K de N_EXPERTS expertos por token.

Sin MoE (MOE_ENABLED=False): se comporta como QuaternionTorusBrain puro.*
- `MultiHeadAttention` (line 847) - *Multi-head attention con:
- Flash Attention (scaled_dot_product_attention de PyTorch 2.0+)
- Rotary Position Embeddings (RoPE)
- GQA (Grouped Query Attention): N_KV_HEADS < N_HEADS, reduce VRAM de K/V
- KV Cache para inferencia autoregresiva eficiente
- Temperatura termodinámica aprendible*
- `TopoGPT2Layer` (line 929) - *Capa del transformer con TopoMoEBrain (TopoBrain + MoE SwiGLU experts).

Esquema pre-norm (estilo LLaMA):
    x = x + Attention_GQA(RMSNorm(x))
    x = x + TopoMoEBrain(RMSNorm(x))*
- `TopoGPT2` (line 976) - *TopoGPT2: Transformer de lenguaje con TopoBrain cuaternión-espectral.

Arquitectura:
    Embedding de tokens + RoPE (en Attention)
    N_LAYERS × TopoGPT2Layer (Attention + QuaternionTorusBrain)
    RMSNorm final
    Proyección a vocabulario (weight-tied con embeddings)*
- `BPETokenizer` (line 1082) - *Wrapper alrededor de tiktoken (GPT-2 compatible).*
- `CorpusDownloader` (line 1107) - *Descarga corpus de texto para entrenamiento.

Soporta:
- 'tinystories': ~2GB de cuentos cortos (ideal para pruebas)
- 'wikitext103': ~500MB de Wikipedia curada
- 'file': archivo de texto local

Usa HuggingFace 'datasets' para TinyStories y WikiText.*
- `TokenizedDataset` (line 1170) - *Dataset de tokens para language modeling (next-token prediction).

Guarda los tokens tokenizados en disco la primera vez (cache .pt)
para evitar re-tokenizar en cada ejecucion. La clave de cache incluye
un hash del contenido del corpus + tokenizador + max_tokens.*
- `CheckpointManager` (line 1220) - *Gestiona checkpoints de forma acumulativa y segura.

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
- `TopoGPT2Trainer` (line 1453) - *Entrenador acumulativo y resumible.

Caracteristicas:
- Checkpoint automatico en safetensors cada N minutos + cada epoch
- Historial acumulativo entre sesiones (--resume agrega al historial existente)
- Guarda el mejor modelo en checkpoints/best/ automaticamente
- LR schedule: cosine con warmup relativo a los steps de ESTA sesion
- Mixed Precision (AMP) + acumulacion de gradientes*
- `MechanisticMetrics` (line 1746) - *Calcula todas las metricas del diagrama de fases de Book.md.

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
- `Phase0_KernelOptimizer` (line 1983) - *Encuentra el ratio imaginario/real optimo para los kernels espectrales.

Analogia con main.py: evalua la transicion GOE→GUE en el espacio
de kernels. Un ratio optimo promueve estructura topologica (insulador)
vs estructura amorfa (vidrio).

Metodo: calibra con un mini-batch y mide la varianza del gradiente
en funcion del ratio. Ratios que minimizan la varianza de gradiente
(maxima coherencia espectral) son preferibles.

No entrena: solo inicializa los kernels con distintos ratios y mide.
Tiempo tipico: < 30 segundos.*
- `Phase1_BatchProspector` (line 2058) - *Encuentra el batch size optimo testando candidatos con pocos pasos.

De main.py: el batch size regula la temperatura del horno de cristalizacion.
Batch sizes demasiado chicos -> ruido excesivo (vidrio frio).
Batch sizes demasiado grandes -> sin presion annealing (amorfos).
La ventana optima empirica de main.py: [24, 128] para Strassen.

Para LM, testeamos candidatos midiendo:
- delta (δ): velocidad de descenso en prospect_steps pasos
- T_eff: temperatura efectiva del gradiente

Tiempo tipico: < 2 minutos para 3 candidatos × 30 pasos.*
- `Phase2_SeedMiner` (line 2141) - *Encuentra semillas prometedoras midiendo la trayectoria de delta.

De main.py: una semilla "buena" muestra delta descendente en los
primeros N pasos (enfriamiento). Una semilla "mala" se estanca en
el plateau vidrioso (~0.49).

Criterio de seleccion:
1. Semillas con delta_velocity < 0 (enfriando) AND kappa bajo.
2. Si no hay, semillas solo enfriando.
3. Fallback: semilla con menor delta final.

Tiempo tipico: < 3 minutos para 5 semillas × 50 pasos.*
- `Phase4_AnnealingRefiner` (line 2223) - *Refinamiento post-entrenamiento mediante recocido simulado.

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
- `TopoPhasePipeline` (line 2384) - *Orquesta las 5 fases de entrenamiento segun main.py + Book.md.

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

**Functions:**
- `setup_logger` (line 155)
- `set_seed` (line 165)
- `main` (line 2506)
- `__post_init__` (line 124)
- `hamilton_product` (line 185) - *Producto de Hamilton q1 ⊗ q2. Ambos [..., 4].*
- `normalize` (line 197)
- `conjugate` (line 201)
- `rotate_vector` (line 206) - *Rota vector 3D v por cuaternión unitario q. v:[...,3] q:[...,4]*
- `__init__` (line 228)
- `forward` (line 244) - *x: [..., in_features] → [..., out_features]*
- `__init__` (line 281)
- `_kernel` (line 300)
- `_contract` (line 303) - *Suma sobre canales in_q: Y[b,o,h,w] = Σ_i W[i,o,h,w]·X[b,i,h,w]*
- `forward` (line 307) - *x: [B, 4*in_q, H, W]  (4 canales cuaterniones sobre grid espacial)
→ [B, 4*out_q, H, W]*
- `__init__` (line 361)
- `_filter1d` (line 393) - *Filtro espectral 1D: x[..., D] → filtrado[..., D]*
- `encode` (line 399) - *x: [..., D_MODEL] → latent: [..., D_LAT]*
- `decode` (line 404) - *z: [..., D_LAT] → recon: [..., D_MODEL]*
- `forward` (line 409) - *Devuelve (latent, recon_loss)*
- `process_torus_grid` (line 416) - *Procesa el grid del toro con QuaternionSpectralLayer.
grid: [B, 4*D_QUAT, RADIAL, ANGULAR]  →  [B, 4*D_QUAT, RADIAL, ANGULAR]*
- `__init__` (line 449)
- `_build_torus_graph` (line 489) - *Construye las aristas del grafo toro 2×4.

Nodos indexados como: node = r * N_ANGULAR + a
  r ∈ [0, RADIAL-1], a ∈ [0, ANGULAR-1]

Aristas angulares: nodo ↔ nodo a la izquierda/derecha (periódico)
Aristas radiales:  nodo ↔ nodo del anillo interior/exterior*
- `_torus_soft_assign` (line 523) - *Asignación blanda de tokens a los 8 nodos del toro via distancia circular.

phi1: [BS] ángulo angular ∈ [-π, π]
phi2: [BS] ángulo radial ∈ [-π, π]
→ weights: [BS, N_NODES]  (suma a 1, softmax de distancias negativas)*
- `_message_passing` (line 550) - *Message-passing VECTORIZADO con rotaciones cuaterniones.
Sin bucles Python: todas las aristas se procesan en paralelo.

node_feat: [BS, N_NODES, D_MODEL]
→ [BS, N_NODES, D_MODEL]*
- `forward` (line 587) - *x: [B, S, D_MODEL]
→ output: [B, S, D_MODEL], recon_loss: scalar*
- `__init__` (line 655)
- `_build_cache` (line 661)
- `_rotate_half` (line 668)
- `forward` (line 672) - *q, k: [B, n_heads, S_q/S_k, d_head]
offset: posicion inicial (para KV cache: longitud del cache existente)
Aplica posiciones [offset .. offset+S-1] a q y k.*
- `__init__` (line 699)
- `forward` (line 704)
- `__init__` (line 720)
- `forward` (line 734)
- `__init__` (line 757)
- `_route` (line 778) - *x: [N, D] donde N = B*S (tokens aplanados)
Retorna:
expert_out: [N, D]  suma ponderada de top-K expertos
aux_loss:   escalar  load-balancing loss
Routing vectorizado sin boolean indexing ni sincronizacion CUDA.
Usa dispatch por indices agrupados (estilo Mixtral/DeepSeek) para
compatibilidad total con torch.utils.checkpoint.*
- `forward` (line 820) - *x: [B, S, D]
→ output: [B, S, D], aux_loss: escalar*
- `__init__` (line 857)
- `forward` (line 875) - *Args:
    x:        [B, S, D]
    is_causal: usar mascara causal
    past_kv:  (K_cache, V_cache) de pasos anteriores o None
Returns:
    out:      [B, S, D]
    kv_cache: (K, V) completos para cachear en generate()*
- `__init__` (line 938)
- `_forward_impl` (line 947)
- `forward` (line 956) - *Retorna (x_out, aux_loss, kv_cache).
Con gradient checkpointing en training (solo cuando no hay KV cache).*
- `__init__` (line 987)
- `_init_weights` (line 1006)
- `forward` (line 1013) - *token_ids: [B, S]  (enteros)
past_kvs:  lista de (K, V) por capa, o None para entrenamiento
→ logits: [B, S, VOCAB_SIZE], aux_loss: scalar, new_kvs: list[(K,V)]*
- `count_params` (line 1036)
- `generate` (line 1042) - *Generacion autoregresiva con KV cache y muestreo top-k.
En el primer paso procesa el prompt completo y guarda el cache.
En pasos siguientes solo procesa 1 token nuevo (O(n) en lugar de O(n^2)).*
- `__init__` (line 1085)
- `encode` (line 1093)
- `decode` (line 1096)
- `eot_token` (line 1099)
- `__init__` (line 1119)
- `get_text` (line 1125) - *Devuelve el texto del corpus. Descarga si es necesario.*
- `_download_hf` (line 1150)
- `__init__` (line 1179)
- `__len__` (line 1206)
- `__getitem__` (line 1209)
- `__init__` (line 1245)
- `patch_config_for_resume` (line 1255) - *Lee el checkpoint 'latest' y ajusta cfg.N_KV_HEADS / cfg.GQA_GROUPS
para que coincidan con la arquitectura guardada.
Necesario cuando el codigo cambio GQA despues de guardar el checkpoint.*
- `_save_model` (line 1284)
- `_load_model` (line 1297)
- `_save_optimizer` (line 1328)
- `_load_optimizer` (line 1331)
- `_save_state` (line 1340)
- `_load_state` (line 1345)
- `should_save` (line 1356)
- `save` (line 1359) - *Guarda checkpoint completo.

state debe contener al menos: completed_epochs, global_step,
best_val_loss, history, config.*
- `load_latest` (line 1404) - *Carga el ultimo checkpoint guardado.
Devuelve el state dict (vacio si no hay checkpoint).*
- `load_best` (line 1431) - *Carga el mejor modelo guardado (solo pesos, sin optimizador).*
- `has_checkpoint` (line 1443)
- `__init__` (line 1465)
- `resume` (line 1500) - *Carga el ultimo checkpoint disponible.
Restaura: pesos del modelo, estado del optimizador, historial acumulado,
epoch/step completados y mejor val_loss.
Devuelve True si se cargo un checkpoint, False si empieza de cero.*
- `_current_state` (line 1525) - *Construye el dict de estado para persistir en state.json.*
- `_cosine_lr` (line 1536) - *Cosine decay con warmup. El schedule es relativo a la sesion actual.*
- `_set_lr` (line 1544)
- `train` (line 1548) - *Entrena cfg.EPOCHS epocas adicionales a partir de completed_epochs.
El historial se acumula sobre sesiones previas.*
- `_sample_text` (line 1684) - *Genera una muestra de texto al final de cada epoch para monitorear
la calidad cualitativa del modelo (detecta degeneracion, repeticion, etc.).*
- `evaluate` (line 1716)
- `__init__` (line 1766)
- `compute_delta` (line 1774)
- `compute_alpha` (line 1781)
- `update_grad_buffer` (line 1786) - *Captura gradientes de forma segura, ignorando tensores corruptos.*
- `compute_t_eff` (line 1812) - *T_eff = lr/2 * Var(gradiente). Temperatura termodinamica efectiva.*
- `compute_kappa` (line 1820) - *κ = λ_max / λ_min de la covarianza del gradiente.
Parámetro de orden para cristalización (κ≈1 = cristal).
Nota: requiere pasadas backward adicionales. Se ejecuta con protección
para no corromper el estado AMP del trainer principal.*
- `compute_berry_phase` (line 1878) - *Fase de Berry de los kernels espectrales imaginarios.
Surge de los parametros ki_w, ki_x, ki_y, ki_z de QuaternionSpectralLayer.
|berry|>pi/2 con winding!=0 indica estructura topologica.*
- `compute_lc` (line 1891) - *Complejidad local: 1 - similitud coseno promedio entre filas de pesos.*
- `compute_sp` (line 1905) - *Superposicion: correlacion inter-fila promedio (entrelazamiento de features).*
- `classify_phase` (line 1921) - *Clasificacion de fase segun Book.md:

discrete_crystal:       delta<0.05, kappa<1.5
topological_insulator:  |berry|>pi/2, winding!=0
cold_glass:             kappa>>1, delta>0.3
functional_glass:       intermedio (lo mas comun en LM)*
- `compute_all` (line 1940) - *Calcula todas las metricas.
compute_kappa=True hace pasadas backward adicionales (caro, usar cada N epochs).*
- `format_log` (line 1965)
- `__init__` (line 2001)
- `_measure_ratio` (line 2005) - *Mide la coherencia espectral para un ratio dado.
Retorna: varianza del gradiente (menor = mas coherente = mejor).*
- `optimize` (line 2034) - *Retorna el mejor ratio de inicializacion de kernels espectrales.*
- `__init__` (line 2074)
- `prospect` (line 2078) - *Retorna el mejor batch size segun delta y T_eff.*
- `__init__` (line 2157)
- `mine` (line 2161) - *Retorna la semilla con la mejor trayectoria de delta.*
- `__init__` (line 2243)
- `refine` (line 2252) - *Ejecuta refine_epochs epocas de recocido simulado.
Retorna el historial de refinamiento.*
- `__init__` (line 2404)
- `_make_dataloaders` (line 2414)
- `run` (line 2426) - *Ejecuta el pipeline completo.
Retorna el trainer con el modelo entrenado.*
- `ckpt_fn` (line 964)

#### `toposwarm_coevolve.py`
**Path:** `toposwarm_coevolve.py`

**Classs:**
- `HarnessMutation` (line 128) - *Simple mutation operators over MetaHarnessConfig dicts.*
- `MockLazyOwnBridge` (line 183) - *Deterministic mock of LazyOwnBridge for isolated harness evaluation.
Returns canned responses so the orchestrator can be exercised even when
LazyOwn is not present.*
- `HarnessEvaluator` (line 233) - *Evaluates a harness configuration by running the LazyOwn orchestrator
on a suite of validation prompts and aggregating scores.

Uses in-process evaluation (no subprocess) so:
- Meta-Harness logs are written to the same filesystem store.
- Import errors are visible immediately.
- Latencies are realistic.*
- `WeightTrainer` (line 391) - *Thin wrapper around toposwarm_continual_trainer.py for inner-loop
weight updates.*
- `CoEvolutionEngine` (line 451) - *Outer-loop harness evolution with optional inner-loop weight co-evolution.*

**Functions:**
- `_resolve_lazyown_dir` (line 63) - *Discover LazyOwn installation directory.

Priority:
  1. LAZYOWN_DIR environment variable (expanded ~).
  2. Default relative to this script: <repo>/LazyOwn.
  3. User home directory: ~/LazyOwn.
  4. Return the relative default anyway (caller will see available=False).*
- `_setup_logger` (line 90)
- `_clip` (line 175)
- `main` (line 646)
- `mutate` (line 132)
- `crossover` (line 167)
- `__init__` (line 190)
- `available` (line 196)
- `run` (line 199)
- `get_config` (line 222)
- `set_config` (line 225)
- `__init__` (line 244)
- `evaluate` (line 256) - *Run each prompt through the orchestrator and collect metrics.

Also logs every evaluation to the Meta-Harness experience store so the
proposer has data to diagnose.*
- `_build_orchestrator` (line 313) - *Build a LazyOwnOrchestrator with the given MetaHarnessConfig.*
- `_log_run` (line 343) - *Write one evaluation to the Meta-Harness experience store.*
- `__init__` (line 397)
- `_load` (line 402)
- `is_available` (line 415)
- `fine_tune` (line 418) - *Run a short fine-tuning burst and return metrics.*
- `__init__` (line 456)
- `run` (line 490)
- `_next_generation` (line 550)
- `_tournament_select` (line 567)
- `_is_on_frontier` (line 575)
- `_run_proposer` (line 596)
- `_save_state` (line 619)
- `load_state` (line 628)
- `_report_frontier` (line 635)

#### `toposwarm_continual_trainer.py`
**Path:** `toposwarm_continual_trainer.py`

**Classs:**
- `ContinualConfig` (line 111) - *All hyper-parameters for the continual learning run.*
- `SurpriseBuffer` (line 166) - *Tracks per-example surprise scores and returns a priority-weighted
replay sample so the trainer oversamples examples the model is failing on.

Surprise (from NeuroLogos tricameral):
    surprise = CE_loss × (1 − confidence)
where confidence = softmax_max of the LM-head logits at the routing position.

High surprise = model is wrong AND was overconfident → hardest to learn.
These examples are stored and mixed into subsequent mini-batches at a
configurable ratio (default 25 % of each batch).*
- `ToolBenchDataset` (line 300)
- `ReplayBuffer` (line 334) - *Circular buffer of ToolBench examples.

Randomly selects REPLAY_RATIO * batch_size samples to mix into every
fine-tuning batch, ensuring the model continuously sees original-task
examples during LazyOwn training.*
- `EWC` (line 365) - *Elastic Weight Consolidation.

Computes the diagonal of the Fisher Information Matrix on a sample of
ToolBench data, then adds the quadratic penalty to the loss at every
fine-tuning step.

The penalty is:
    L_ewc = λ/2 · Σ_i  F_i · (θ_i − θ*_i)²

where θ* is the snapshot of parameters BEFORE fine-tuning begins, and
F_i is the empirical Fisher diagonal (mean squared gradient of log-prob).*
- `SwarmLiquidNeuron` (line 514) - *Liquid neuron for routing: slow proj (gradient) + fast Hebbian weights.

Architecture:
    slow_out  = W_slow(x)            # [B, n_tools], gradient path
    fast_out  = x @ W_fast.T         # [B, n_tools], Hebbian path, no grad
    output    = LayerNorm(slow_out + fast_scale * fast_out)

W_fast is updated after each training step via:
    ΔW_fast = lr_hebb × (post.T @ pre) / B   (clamped ±0.3)
where pre = hidden states, post = one-hot tool labels.

Homeostasis clips output norm to [0.5, 2.0] to prevent explosion.*
- `RoutingHead` (line 600) - *Thin linear probe: d_model → n_tools.

Trained on top of the frozen (or lightly-tuned) backbone with standard
cross-entropy over the N LazyOwn tools.  Bypasses the 50k-token LM head
so 100% of the gradient goes to the routing decision.

Tool-to-index mapping is deterministic (sorted tool name list), so the
head can be saved/loaded independently of the backbone checkpoint.*
- `ContinualTrainer` (line 730) - *Fine-tuning loop with EWC + Replay.

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
- `_import` (line 91)
- `_setup_logger` (line 158)
- `_load_jsonl` (line 232)
- `_encode_record` (line 247) - *Encode a ToolBench-format record into (input_ids, target_ids).

Uses the same compact format as topo_swarm_agent.ToolBenchDataset._encode_record:
    [instruction BPE tokens]  [tool token]  [compact result BPE tokens]

This matches the pretraining distribution exactly, keeping cross-entropy in
the same range as the original training (1-2 nats) rather than the full
vocabulary baseline (~10.8 nats for random predictions over 50k+ tokens).*
- `_collate` (line 319)
- `evaluate_routing` (line 1137) - *Measure routing accuracy on a held-out subset of both datasets.

Routing accuracy = fraction of examples where the highest-probability
tool token matches the ground-truth tool in the api_list.*
- `build_model_and_tok` (line 1195)
- `run_full_pipeline` (line 1217) - *Generate dataset → compute Fisher → fine-tune → evaluate.*
- `main` (line 1384)
- `__init__` (line 180)
- `update` (line 186) - *Add batch examples to buffer, keyed by surprise score.*
- `sample` (line 213) - *Return a priority-weighted sample of hard examples.*
- `__len__` (line 223)
- `__init__` (line 301)
- `__len__` (line 312)
- `__getitem__` (line 315)
- `__init__` (line 343)
- `sample` (line 351)
- `__len__` (line 356)
- `__init__` (line 380)
- `compute` (line 401) - *Compute Fisher diagonal on a sample of ToolBench records and snapshot θ*.

Uses label log-prob gradients (empirical Fisher):
    F_i = (1/N) Σ_n  (∂ log p(y_n|x_n, θ) / ∂ θ_i)²*
- `save` (line 465)
- `load` (line 470)
- `penalty` (line 481) - *Returns the EWC penalty term to add to the task loss.

Complexity: O(params) per step — negligible for a 2M-param model.*
- `__init__` (line 534)
- `forward` (line 551) - *x: [B, d_model] → logits [B, n_tools]*
- `hebbian_update` (line 570) - *Strengthen W_fast associations after correct predictions.

pre:    [B, d_model] — hidden states (instruction-end position)
labels: [B]          — true tool class indices*
- `__init__` (line 614)
- `n_tools` (line 651)
- `forward` (line 654) - *hidden: [B, d_model] → logits [B, n_tools]

Pipeline:
  0. Pre-MLP: enrich representation capacity
  1. LiquidNeuron: slow grad + fast Hebbian → base logits [B, n_tools]
  2. MoE gate: select top-k specialty expert refinements
  3. Weighted sum of expert-refined logits*
- `label` (line 685)
- `predict` (line 688) - *hidden: [B, d_model] → list of predicted tool name strings*
- `save` (line 695)
- `load` (line 706)
- `__init__` (line 746)
- `_make_optimizer` (line 782)
- `_lr_schedule` (line 821)
- `_merge_with_replay` (line 830) - *Append replay samples to the LazyOwn batch.*
- `_routing_accuracy` (line 863) - *Routing accuracy using the LM head (primary) and routing head (secondary).

Feeds only instruction tokens; evaluates the last-position logits.
Uses cached encode for speed.  Always returns LM-head accuracy (which
matches the training objective) so the metric is honest.*
- `train` (line 923)
- `_accuracy` (line 1153)
- `_hook` (line 887)
- `_capture` (line 995)

#### `toposwarm_hybrid.py`
**Path:** `toposwarm_hybrid.py`

**Classs:**
- `HybridConfig` (line 115) - *All hyper-parameters for the hybrid system — zero magic numbers.*
- `ToolResult` (line 218) - *Structured result from a tool call.*
- `ToolRegistry` (line 231) - *Registry of executable tools with keyword-based routing.*
- `TopoSwarmRouter` (line 396) - *Thin wrapper around TopoSwarmModel that performs only tool routing.

The router uses keyword-based routing (deterministic, no model inference
needed for the routing decision) combined with the crystallised model for
swarm-consensus confidence scoring.

Because the model's Pass 2 output is always noisy, we bypass it entirely
and return only the (tool_name, tool_arg) pair.  The LanguageBackend
handles all text generation.*
- `LanguageBackend` (line 465) - *Language generation backend.

Supports three modes:
- tinystories: HuggingFace GPT-2-style model loaded via transformers.
- checkpoint:  Raw PyTorch state_dict for your own 25M model.
- none:        Returns empty string; caller uses deterministic template.*
- `HybridResult` (line 946) - *All intermediate and final outputs of one hybrid inference run.*
- `HybridOrchestrator` (line 977) - *Combines TopoSwarmRouter + LanguageBackend into a single inference call.

Pipeline:
1. Router.route(prompt)        → (tool_name, tool_arg)
2. Registry.execute(...)       → ToolResult
3. Backend.generate(...)       → raw natural-language answer
4. Quality check               → use backend output or template fallback*

**Functions:**
- `_import_agent` (line 85) - *Import topo_swarm_agent, searching script dir then cwd.*
- `_setup_logger` (line 164) - *Idempotent logger with a single StreamHandler.*
- `_safe_eval` (line 182) - *Evaluate a math expression safely via AST — no eval().*
- `_template_answer` (line 887) - *Build a clean deterministic answer from the tool result.

Used when the language backend is disabled or produces output below
BACKEND_MIN_OUTPUT_CHARS.

Args:
    tool_name: Canonical tool name.
    tool_arg: Argument passed to the tool.
    tool_result: ToolResult instance.

Returns:
    Human-readable answer string.*
- `_is_useful_output` (line 918) - *Return True if the backend output is genuinely informative.

Checks length and absence of common TinyStories non-answer patterns
(story openers, repetition, incomplete sentences starting with
conjunctions).*
- `main` (line 1051) - *CLI entry point.

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
- `_eval` (line 192)
- `__init__` (line 221)
- `__str__` (line 227)
- `__init__` (line 234)
- `_register` (line 240)
- `resolve` (line 249) - *Resolve tool name to canonical key via exact match, alias, or substring.*
- `route` (line 261) - *Infer tool name and argument from prompt keywords.

Returns (tool_name, tool_arg) where tool_arg is the most specific
sub-string of the prompt relevant to the tool (e.g. city name for
weather, expression for calc_expr).*
- `execute` (line 287) - *Execute a tool by canonical name.*
- `_http_get` (line 299)
- `_register_all` (line 304) - *Register all built-in tools.*
- `tool_names` (line 387)
- `__init__` (line 409) - *Args:
    cfg: Hybrid configuration.
    registry: ToolRegistry used for routing via registry.route().
    logger: Logger instance.*
- `_load` (line 428) - *Load checkpoint weights.*
- `route` (line 441) - *Determine the tool and argument for a prompt.

Uses keyword-based routing (deterministic) — the crystallised model
weights already encoded this perfectly, so we replicate the same logic
without running the full forward pass for routing.

Args:
    prompt: Natural language user prompt.

Returns:
    Tuple of (tool_name, tool_arg).*
- `__init__` (line 475) - *Args:
    cfg: Hybrid configuration (BACKEND_TYPE, BACKEND_MODEL_ID, etc.).
    logger: Logger instance.*
- `_load` (line 486) - *Load the language model according to BACKEND_TYPE.*
- `_load_tinystories` (line 507) - *Load a GPT-2-style HuggingFace model (TinyStories or compatible).

The model is loaded in half-precision on CUDA if available to minimise
VRAM usage alongside the TopoSwarm router.  On CPU it uses full
precision.*
- `_import_topogpt` (line 563) - *Import topogpt2_1.py from the same directory as the checkpoint or
the script directory.  Returns the module or None if not found.*
- `_load_checkpoint` (line 588) - *Load a safetensors or pickle checkpoint for the language backend.

Strategy
--------
1. Try to import topogpt2_1.py from dirs near the checkpoint and
   instantiate its model class directly — exact architecture match.
2. Fall back to loading via topo_swarm_agent.TopoSwarmModel with
   architecture inferred from weight shapes (strict=False, skipping
   mismatched buffers like rope caches which are recomputed).*
- `generate` (line 859) - *Generate a natural-language answer from the prompt and tool result.

Args:
    prompt: Original user question.
    tool_result: Raw string output from the executed tool.

Returns:
    Generated answer string, or empty string if backend is None.*
- `pretty` (line 958) - *Render a human-readable summary.*
- `__init__` (line 988) - *Args:
    cfg: Hybrid configuration.
    logger: Logger instance.*
- `run` (line 1000) - *Execute the full hybrid pipeline for one user prompt.

Args:
    prompt: Natural language user request.

Returns:
    HybridResult with all steps populated.*
- `decorator` (line 241)
- `get_weather` (line 308)
- `search_web` (line 319)
- `calc_expr` (line 331)
- `get_datetime` (line 335)
- `translate` (line 341)
- `get_news` (line 373)
- `echo` (line 383)
- `_generate` (line 540)
- `_cfg_score` (line 703)
- `_generate` (line 812)
- `_generate` (line 835)

#### `toposwarm_infer.py`
**Path:** `toposwarm_infer.py`

**Classs:**
- `InferenceConfig` (line 84) - *All inference-time hyper-parameters — zero magic numbers.*
- `ToolResult` (line 189) - *Structured result returned by every tool executor.*
- `ToolRegistry` (line 210) - *Registry of executable tools.

Each tool is a callable(arg: str) -> str.  Registration is done via the
@register decorator.  Tool names are matched case-insensitively and with
common aliases (e.g. "weather" matches "get_weather", "weather_now").*
- `ToolCallParser` (line 438) - *Extract tool calls from model-generated text.

The model may emit tool calls in several formats; this parser tries all
of them in priority order and returns the first match.*
- `InferenceEngine` (line 483) - *Full agentic inference loop:

1. Encode prompt.
2. First-pass generation via SwarmOrchestrator.
3. Parse any tool call from the generated text.
4. Execute the tool.
5. Second-pass generation conditioned on prompt + tool result.
6. Return structured InferenceResult.*
- `InferenceResult` (line 883) - *All intermediate and final outputs of one inference run.*

**Functions:**
- `_import_agent` (line 51) - *Import topo_swarm_agent, searching the script dir and cwd.*
- `_safe_eval` (line 138) - *Evaluate a mathematical expression without using eval() on arbitrary code.

Supports: +, -, *, /, //, %, **, unary minus, parentheses, int and float
literals.  Raises ValueError on any disallowed construct.*
- `_setup_logger` (line 920) - *Idempotent logger with a single StreamHandler.*
- `main` (line 938) - *CLI entry point.

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
- `_eval` (line 157)
- `__init__` (line 192) - *Args:
    tool_name: Name of the tool that was called.
    arg: Raw argument string passed to the tool.
    output: Human-readable result string.
    ok: Whether the tool call succeeded.*
- `__str__` (line 205)
- `__init__` (line 219) - *Args:
    cfg: Inference configuration (provides timeout and result limits).*
- `register` (line 229) - *Decorator that registers a function under one or more tool names.*
- `resolve` (line 239) - *Resolve a raw tool name to its canonical registry key.

Performs exact match, then alias lookup, then prefix/substring search.

Args:
    raw_name: Tool name as emitted by the model.

Returns:
    Canonical tool name string, or None if not found.*
- `execute` (line 262) - *Execute a tool by name with the given argument string.

Args:
    raw_name: Tool name as emitted by the model.
    arg: Argument string (stripped of surrounding whitespace/quotes).

Returns:
    ToolResult with the output or an error message.*
- `_http_get` (line 292) - *Minimal HTTP GET with timeout, returns response body as string.*
- `_register_builtin_tools` (line 301) - *Register all built-in tools onto self._tools / self._aliases.*
- `__init__` (line 446) - *Args:
    cfg: Inference config (provides TOOL_TAG_RE pattern).*
- `parse` (line 453) - *Extract the first tool call from text.

Args:
    text: Raw model output string.

Returns:
    Tuple of (tool_name, arg) or None if no tool call found.*
- `__init__` (line 495) - *Args:
    cfg: Inference configuration.
    agent_cfg: SwarmConfig used to instantiate the model.
    logger: Logger instance.*
- `_load_checkpoint` (line 521) - *Load weights from the latest checkpoint directory.*
- `_encode_prompt` (line 538) - *Encode a prompt string to a [1, S] token id tensor on the model device.

Wraps the raw text in the ToolBench training format so the model
receives input that matches its training distribution:

    query: <text>
    api_list: [{"tool_name": "<inferred>", ...}]
    domain: General
    <tool_token>

The tool name is inferred from keyword signals so the tool token sits
at the correct position — matching encode_tool_trace() used at training.
Token ids are clamped to [0, VOCAB_SIZE-1] to prevent embedding crashes.*
- `_generate` (line 586) - *Custom autoregressive generation loop with three inference-time fixes.

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
- `run` (line 679) - *Full agentic inference loop for one user prompt.

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
- `_template_answer` (line 818) - *Build a deterministic natural-language answer from the tool result.

Used when the model Pass 2 output is too short to be useful.  Each
tool has a dedicated template that formats the raw result string into
a readable sentence.  No model weights involved — pure string
formatting.*
- `_infer_tool_and_arg` (line 844) - *Infer the tool name and argument from the prompt text.

Returns the same (tool_name, arg) pair that _encode_prompt uses,
so both are guaranteed to be consistent.  The argument is the
full prompt text — each tool executor extracts what it needs.*
- `pretty` (line 895) - *Render a human-readable summary of the inference run.*
- `decorator` (line 231)
- `get_weather` (line 305) - *Fetch current weather from wttr.in (no API key required).*
- `search_web` (line 323) - *Instant-answer search via DuckDuckGo JSON API (no API key).*
- `calc_expr` (line 340) - *Evaluate a mathematical expression safely.*
- `get_datetime` (line 345) - *Return the current UTC datetime (tz_hint is informational only).*
- `translate` (line 351) - *Translate text using MyMemory free API (no key, 5k chars/day limit).

Accepted formats:
  "translate <text> to <lang>"
  "<text> to <lang>"
  "<text>"  (defaults to English)

Strips the "translate" verb and detects source language via
langdetect so MyMemory receives a valid langpair (e.g. es|en).
Falls back to es|en when detection fails.*
- `get_news` (line 409) - *Fetch recent news headlines via DuckDuckGo news search.
Returns up to 3 snippet summaries.*
- `echo` (line 428) - *Return the input unchanged. Used for model self-testing.*

#### `toposwarm_lazyown_orchestrator.py`
**Path:** `toposwarm_lazyown_orchestrator.py`

**Classs:**
- `SessionContext` (line 170) - *Persistent session state across multiple prompts.*
- `LazyOwnBridge` (line 227) - *Thin wrapper around LazyOwn's _run_lazyown_command logic.

Calls LazyOwn non-interactively via a PTY subprocess so the terminal-size
ioctl does not crash.  Strips ANSI codes from output.

All heavy imports (pty, fcntl, termios, select, struct) are lazy so the
bridge can be imported on non-Linux systems for dataset generation.*
- `LazyOwnToolRegistry` (line 372) - *Extends TopoSwarm's ToolRegistry with all LazyOwn MCP tools.

Each tool is a thin wrapper that calls LazyOwnBridge.run() with the
appropriate LazyOwn shell command or payload manipulation.

Tools are grouped by category so keyword routing maps naturally.*
- `LazyOwnOrchestrator` (line 764) - *Combines TopoSwarm router with LazyOwn tool execution.

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
- `_resolve_lazyown_dir` (line 56) - *Discover LazyOwn installation directory.

Priority:
  1. LAZYOWN_DIR environment variable (expanded ~).
  2. Default relative to this script: <repo>/LazyOwn.
  3. User home directory: ~/LazyOwn.
  4. Return the relative default anyway (caller will see available=False).*
- `_import_infer` (line 93)
- `_import_agent` (line 113)
- `_import_meta_harness` (line 128)
- `_import_routing_head` (line 147)
- `infer_lazyown_tool` (line 691) - *Map a natural-language security prompt to a (tool_name, tool_arg) pair.

Priority: explicit LazyOwn keywords → security domain keywords → fallback.
The returned tool_arg is the most useful sub-string to pass to that tool.*
- `_extract_arg` (line 716) - *Extract the most useful argument string for each tool category.*
- `generate_dataset` (line 1092) - *Generate a rich ToolBench-format JSONL for fine-tuning the TopoSwarm router.

Uses lazyown_dataset_generator.py (80 tools × 5-10 phrasings + chain examples)
for ~420 high-quality training examples covering every LazyOwn MCP tool.
If LazyOwn is live, a random sample of tools are actually executed and their
real output replaces the placeholder in the `answer` field.

Returns the number of examples written.*
- `finetune_on_lazyown` (line 1173) - *Fine-tune the TopoSwarm router on the full LazyOwn tool dataset using
EWC + Experience Replay to prevent catastrophic forgetting.

Pipeline (delegated to toposwarm_continual_trainer.py):
  1. Load the 420-example lazyown_full.jsonl.
  2. Compute / load Fisher Information diagonal on any available ToolBench
     data (anchors critical weights so general routing is preserved).
  3. Build a ToolBench replay buffer (20 % of every mini-batch).
  4. Fine-tune with combined loss: L_task + λ/2 · Σ F_i(θ_i − θ*_i)²
  5. Evaluate routing accuracy on held-out LazyOwn + ToolBench samples.
  6. Print final checkpoint stats (epoch, step, task_loss, ewc_lambda).*
- `run_mcp_server` (line 1250) - *Expose the TopoSwarm→LazyOwn orchestrator as an MCP stdio server.

Tools exposed:
  toposwarm_query   — NL prompt → routed LazyOwn tool → answer
  lazyown_*         — direct passthrough to every registered tool*
- `_setup_logger` (line 1329)
- `main` (line 1346)
- `to_prompt_prefix` (line 181) - *Compact context block injected before the user prompt.*
- `update` (line 195)
- `__init__` (line 251)
- `available` (line 257)
- `run` (line 265) - *Execute a LazyOwn shell command and return cleaned output.*
- `get_config` (line 344)
- `set_config` (line 353)
- `__init__` (line 455)
- `_register_lazyown_tools` (line 460) - *Register every LazyOwn MCP tool as a ToolRegistry callable.*
- `__init__` (line 780)
- `_load_routing_head` (line 825) - *Load the trained RoutingHead if a checkpoint exists.*
- `_neural_route` (line 847) - *Use the TopoSwarm model + RoutingHead to predict the LazyOwn tool.
Returns (tool_name, tool_arg) or None if unavailable / uncertain.*
- `run` (line 887) - *Route prompt → LazyOwn tool → answer.*
- `list_tools` (line 1273)
- `call_tool` (line 1307)
- `_serve` (line 1317)
- `run_command` (line 466)
- `get_config` (line 470)
- `set_config` (line 475)
- `list_modules` (line 483)
- `get_beacons` (line 487)
- `c2_command` (line 491)
- `run_api` (line 495)
- `list_sessions` (line 499)
- `read_session_file` (line 507)
- `c2_status` (line 514)
- `create_addon` (line 518)
- `list_addons` (line 522)
- `list_plugins` (line 529)
- `poll_events` (line 536)
- `ack_event` (line 540)
- `add_rule` (line 544)
- `list_event_rules` (line 548)
- `heartbeat_status` (line 552)
- `session_init` (line 556)
- `discover_commands` (line 560)
- `phase_guide` (line 564)
- `command_help` (line 568)
- `add_target` (line 572)
- `list_targets` (line 578)
- `run_agent` (line 582)
- `agent_status` (line 586)
- `agent_result` (line 590)
- `list_agents` (line 594)
- `set_active_target` (line 598)
- `campaign_sitrep` (line 602)
- `c2_notes` (line 606)
- `credentials` (line 610)
- `report_update` (line 614)
- `campaign_lessons` (line 618)
- `auto_populate` (line 622)
- `session_state` (line 626)
- `recommend_next` (line 630)
- `timeline` (line 634)
- `c2_vuln_analysis` (line 638)
- `c2_redop` (line 642)
- `c2_search_agent` (line 646)
- `c2_script` (line 650)
- `c2_adversary` (line 654)
- `policy_status` (line 658)
- `auto_loop` (line 662)
- `create_tool` (line 666)
- `llm_ask` (line 670)
- `inject_objective` (line 674)
- `next_objective` (line 678)
- `read_prompt` (line 682)
- `_hook` (line 863)

#### `toposwarm_lazyown_sweep.py`
**Path:** `toposwarm_lazyown_sweep.py`

**Functions:**
- `generate_prompts` (line 130) - *Generate N diverse pentesting prompts.*
- `setup_logger` (line 145)
- `run_sweep` (line 155) - *Execute prompts against LazyOwn and collect results.*
- `write_results` (line 189) - *Write results as JSONL for continual trainer.

Matches the format of lazyown_dataset_generator.py:
- instruction: the prompt
- api_list: minimal tool metadata
- answer: [TOOL_CALL: tool_name(arg)]
- domain: Security/RealSuccess or Security/RealFailure*
- `main` (line 223)

#### `toposwarm_meta_harness.py`
**Path:** `toposwarm_meta_harness.py`

**Classs:**
- `MetaHarnessConfig` (line 60) - *All Meta-Harness hyper-parameters in one place.*
- `MetaHarnessLogger` (line 121) - *Append-only filesystem store for harness code, execution traces, and scores.

Each evaluated harness run gets its own directory:

    meta_harness_logs/
      run_0001_<hash>/
        harness.json   – config / code snapshot
        trace.jsonl    – step-by-step execution trace
        score.json     – metrics (success, latency, token count, ...)
        reasoning.txt  – optional proposer reasoning

The store is intentionally plain-text / JSON so a coding-agent proposer can
navigate it with standard tools (`grep`, `cat`, `ls`) without bespoke APIs.*
- `DenseMemoryRetriever` (line 322) - *Semantic episodic retrieval with graceful degradation.

Priority:
    1. sentence-transformers dense embeddings (best quality).
    2. sklearn TF-IDF + cosine similarity (no GPU, good quality).
    3. Return None so caller falls back to Jaccard token overlap.

The retriever is rebuildable incrementally: call `add()` for each new
episode, then `search()` for retrieval.*
- `MetaHarnessMemory` (line 430) - *Persistent episodic memory backed by the filesystem log store.

Unlike the in-RAM EpisodicMemory in topo_swarm_agent.py, this memory:
- Survives process restarts.
- Can be queried by keyword overlap, tool name, or simple TF-IDF cosine.
- Returns raw execution traces (not compressed summaries) so a proposer can
  perform causal diagnosis.*
- `EnvironmentBootstrapper` (line 583) - *Gathers a sandbox snapshot *before* the first router/tool turn and formats
it as a compact [Environment Snapshot] block.

This eliminates the 2-4 exploratory turns that the LazyOwn agent typically
spends discovering what targets, sessions, and modules are available.*
- `DraftVerifier` (line 738) - *Two-stage routing inspired by Meta-Harness's text-classification harness.

Stage 1 (Draft):  Produce an initial tool proposal using fast keyword
                  heuristics (same as the existing infer_lazyown_tool).

Stage 2 (Verify): Retrieve confirmers (same tool, past successes) and
                  challengers (different tool / failures) from the
                  MetaHarnessMemory, then decide whether to keep or revise
                  the draft.

This is lightweight — no LLM call — but gives the harness a structured
way to learn from prior executions without retraining model weights.*
- `ParetoFrontier` (line 837) - *Maintain a population of harness configurations and their evaluation scores.

The frontier is updated after every evaluation so the orchestrator can
dynamically switch to the best harness variant for the current task context
(accuracy vs. latency vs. context-cost trade-offs).*
- `MetaHarnessOptimizer` (line 948) - *Single entry-point that wires together Logger, Memory, Bootstrapper,
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

**Functions:**
- `_setup_logger` (line 95)
- `_stable_id` (line 107) - *Short stable hash for naming log directories.*
- `_now_iso` (line 112)
- `_demo` (line 1013)
- `__init__` (line 138)
- `_count_existing_runs` (line 149)
- `_next_run_dir` (line 152)
- `_prune_old` (line 158) - *Keep only the most recent MAX_LOGGED_RUNS directories.*
- `log_run` (line 176) - *Persist one complete harness evaluation.

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
- `list_runs` (line 229) - *Return run directories newest-first.*
- `grep_traces` (line 238) - *Simple regex search across all trace.jsonl files.
Returns list of (run_dir, line_no, matched_line).*
- `get_scores` (line 257) - *Load every score.json into a list.*
- `get_pareto_runs` (line 269) - *Return run directories that are on the Pareto frontier.

By default maximises success_rate and minimises latency_ms + context_chars.*
- `__init__` (line 335)
- `add` (line 362)
- `_rebuild_tfidf` (line 368)
- `bulk_index` (line 376)
- `search` (line 392)
- `_search_st` (line 401)
- `_search_tfidf` (line 412)
- `__init__` (line 441)
- `_build_index` (line 453)
- `_load_episode` (line 464)
- `_episode_text` (line 482)
- `store` (line 493) - *Index a newly logged episode.*
- `retrieve_similar` (line 505) - *Retrieve the top-k most similar prior episodes.

Uses dense semantic retrieval when available (sentence-transformers or
sklearn TF-IDF), then falls back to token-overlap Jaccard for anything
not covered by the dense index.  Results are fused by max-of-scores.*
- `retrieve_confirmers_and_challengers` (line 549) - *Split retrieved episodes into confirmers (same tool, success) and
challengers (different tool or failure).*
- `_tokenise` (line 573) - *Very simple whitespace + punctuation tokeniser.*
- `__init__` (line 592)
- `gather_snapshot` (line 596) - *Collect environment state via the LazyOwnBridge.

Returns a dict with keys:
    working_dir, lazyown_dir, config, targets, sessions,
    modules_available, beacons, languages, memory_estimate.*
- `_parse_list` (line 680) - *Best-effort parse of newline / comma list output.*
- `format_snapshot` (line 687) - *Render the snapshot as a compact [Environment Snapshot] block suitable
for injection into a prompt.*
- `__init__` (line 754)
- `route` (line 766) - *Draft-verify routing.

Returns:
    Tuple of (tool_name, tool_arg, confidence).*
- `_reextract_arg` (line 820) - *Best-effort arg re-extraction when the tool changes.*
- `__init__` (line 846)
- `add` (line 855) - *Add a candidate to the population and return True if it lies on the
current Pareto frontier.*
- `select_best` (line 875) - *Select the best harness config according to a scalarised preference.

preference maps metric name → weight (positive = maximise, negative = minimise).
Default: maximise success_rate, minimise latency_ms and context_chars.*
- `frontier_configs` (line 907) - *Return all configs currently on the Pareto frontier.*
- `_is_on_frontier` (line 911)
- `_prune` (line 933) - *Remove oldest non-frontier entries when population grows too large.*
- `__init__` (line 965)
- `set_router` (line 980) - *Bind the draft verifier to the existing keyword router.*
- `log_run` (line 986) - *Persist one run and update in-memory indexes.*
- `get_best_harness_config` (line 999) - *Return the current Pareto-best harness configuration.*
- `query_experience` (line 1003) - *Ad-hoc retrieval of prior episodes for prompt engineering.*

#### `ts_utils.py`
**Path:** `ts_utils.py`

**Functions:**
- `setup_logger` (line 25) - *Return an idempotent logger with a single StreamHandler.*
- `safe_eval` (line 42) - *Evaluate a numeric expression via AST — never calls eval() on arbitrary code.*
- `import_module` (line 62) - *Load a Python file as a named module.

Tries each candidate path in order; raises FileNotFoundError if none found.
Pre-registers the module in sys.modules before exec so that @dataclass
introspection works correctly on Python 3.13+.*
- `make_cached_encode` (line 86) - *Return a cached version of tokenizer.encode().

@lru_cache requires hashable args; str instructions are fine.
Cache survives the lifetime of the tokenizer object.*
- `make_cached_tool_token` (line 100) - *Return a cached version of tokenizer.tool_token().*
- `_cached_encode` (line 94)
- `_cached_tool_token` (line 103)
