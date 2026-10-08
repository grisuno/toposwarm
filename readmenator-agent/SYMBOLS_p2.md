# Symbols (page 2 of 2)
Previous: [SYMBOLS.md](SYMBOLS.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_next_generation` | method | `toposwarm_coevolve.py:553` | `def _next_generation(self, scores)` |
| `_report_frontier` | method | `toposwarm_coevolve.py:638` | `def _report_frontier(self)` |
| `_resolve_lazyown_dir` | function | `toposwarm_coevolve.py:63` | `def _resolve_lazyown_dir()` |
| `_run_proposer` | method | `toposwarm_coevolve.py:599` | `def _run_proposer(self)` |
| `_save_state` | method | `toposwarm_coevolve.py:622` | `def _save_state(self, generation)` |
| `_setup_logger` | function | `toposwarm_coevolve.py:90` | `def _setup_logger(name, level)` |
| `_tournament_select` | method | `toposwarm_coevolve.py:570` | `def _tournament_select(sorted_scores, k)` |
| `available` | method | `toposwarm_coevolve.py:196` | `def available(self)` |
| `crossover` | method | `toposwarm_coevolve.py:167` | `def crossover(a, b)` |
| `evaluate` | method | `toposwarm_coevolve.py:256` | `def evaluate(self, cfg_dict)` |
| `fine_tune` | method | `toposwarm_coevolve.py:419` | `def fine_tune(self, dataset_path, steps, learning_rate)` |
| `get_config` | method | `toposwarm_coevolve.py:222` | `def get_config(self)` |
| `is_available` | method | `toposwarm_coevolve.py:416` | `def is_available(self)` |
| `load_state` | method | `toposwarm_coevolve.py:631` | `def load_state(self, path)` |
| `main` | method | `toposwarm_coevolve.py:649` | `def main()` |
| `mutate` | method | `toposwarm_coevolve.py:132` | `def mutate(cfg_dict)` |
| `run` | method | `toposwarm_coevolve.py:199` | `def run(self, command, timeout)` |
| `run` | method | `toposwarm_coevolve.py:491` | `def run(self)` |
| `set_config` | method | `toposwarm_coevolve.py:225` | `def set_config(self, key, value)` |
| `ContinualConfig` | class | `toposwarm_continual_trainer.py:111` | `class ContinualConfig` |
| `ContinualTrainer` | class | `toposwarm_continual_trainer.py:740` | `class ContinualTrainer` |
| `EWC` | class | `toposwarm_continual_trainer.py:375` | `class EWC` |
| `ReplayBuffer` | class | `toposwarm_continual_trainer.py:344` | `class ReplayBuffer` |
| `RoutingHead` | class | `toposwarm_continual_trainer.py:610` | `class RoutingHead(Module)` |
| `SurpriseBuffer` | class | `toposwarm_continual_trainer.py:166` | `class SurpriseBuffer` |
| `SwarmLiquidNeuron` | class | `toposwarm_continual_trainer.py:524` | `class SwarmLiquidNeuron(Module)` |
| `ToolBenchDataset` | class | `toposwarm_continual_trainer.py:310` | `class ToolBenchDataset(Dataset)` |
| `__getitem__` | method | `toposwarm_continual_trainer.py:325` | `def __getitem__(self, idx)` |
| `__init__` | method | `toposwarm_continual_trainer.py:180` | `def __init__(self, maxsize, replay_ratio)` |
| `__init__` | method | `toposwarm_continual_trainer.py:311` | `def __init__(self, records, tok, cfg)` |
| `__init__` | method | `toposwarm_continual_trainer.py:353` | `def __init__(self, records, max_size, tok, cfg)` |
| `__init__` | method | `toposwarm_continual_trainer.py:390` | `def __init__(self, model, cfg, cl_cfg, tok, logger)` |
| `__init__` | method | `toposwarm_continual_trainer.py:544` | `def __init__(self, d_model, n_tools)` |
| `__init__` | method | `toposwarm_continual_trainer.py:624` | `def __init__(self, d_model, tool_names, n_experts, top_k, hidden_dim)` |
| `__init__` | method | `toposwarm_continual_trainer.py:756` | `def __init__(self, model, cfg, cl_cfg, tok, ewc, replay, logger, routing_head)` |
| `__len__` | method | `toposwarm_continual_trainer.py:223` | `def __len__(self)` |
| `__len__` | method | `toposwarm_continual_trainer.py:322` | `def __len__(self)` |
| `__len__` | method | `toposwarm_continual_trainer.py:366` | `def __len__(self)` |
| `_accuracy` | method | `toposwarm_continual_trainer.py:1163` | `def _accuracy(records, label)` |
| `_capture` | method | `toposwarm_continual_trainer.py:1005` | `def _capture(module, inp, out_h)` |
| `_collate` | method | `toposwarm_continual_trainer.py:329` | `def _collate(batch)` |
| `_encode_record` | method | `toposwarm_continual_trainer.py:247` | `def _encode_record(record, tok, cfg)` |
| `_hook` | method | `toposwarm_continual_trainer.py:897` | `def _hook(m, i, o)` |
| `_import` | function | `toposwarm_continual_trainer.py:91` | `def _import(name, filename)` |
| `_load_jsonl` | method | `toposwarm_continual_trainer.py:232` | `def _load_jsonl(path)` |
| `_lr_schedule` | method | `toposwarm_continual_trainer.py:831` | `def _lr_schedule(optimizer, step, total, warmup, base_lr)` |
| `_make_optimizer` | method | `toposwarm_continual_trainer.py:792` | `def _make_optimizer(self)` |
| `_merge_with_replay` | method | `toposwarm_continual_trainer.py:840` | `def _merge_with_replay(self, ids, tgt)` |
| `_routing_accuracy` | method | `toposwarm_continual_trainer.py:873` | `def _routing_accuracy(self, records)` |
| `_setup_logger` | method | `toposwarm_continual_trainer.py:158` | `def _setup_logger(level)` |
| `build_model_and_tok` | method | `toposwarm_continual_trainer.py:1205` | `def build_model_and_tok(cl_cfg, logger)` |
| `compute` | method | `toposwarm_continual_trainer.py:411` | `def compute(self, toolbench_records)` |
| `evaluate_routing` | method | `toposwarm_continual_trainer.py:1147` | `def evaluate_routing(model, cfg, tok, lazyown_records, toolbench_records, logger)` |
| `forward` | method | `toposwarm_continual_trainer.py:561` | `def forward(self, x)` |
| `forward` | method | `toposwarm_continual_trainer.py:664` | `def forward(self, hidden)` |
| `hebbian_update` | method | `toposwarm_continual_trainer.py:580` | `def hebbian_update(self, pre, labels)` |
| `label` | method | `toposwarm_continual_trainer.py:695` | `def label(self, tool_name)` |
| `load` | method | `toposwarm_continual_trainer.py:480` | `def load(self, path)` |
| `load` | method | `toposwarm_continual_trainer.py:716` | `def load(cls, d_model, path)` |
| `main` | method | `toposwarm_continual_trainer.py:1394` | `def main()` |
| `n_tools` | method | `toposwarm_continual_trainer.py:661` | `def n_tools(self)` |
| `penalty` | method | `toposwarm_continual_trainer.py:491` | `def penalty(self)` |
| `predict` | method | `toposwarm_continual_trainer.py:698` | `def predict(self, hidden)` |
| `run_full_pipeline` | method | `toposwarm_continual_trainer.py:1227` | `def run_full_pipeline(cl_cfg, logger)` |
| `sample` | method | `toposwarm_continual_trainer.py:213` | `def sample(self, batch_size)` |
| `sample` | method | `toposwarm_continual_trainer.py:361` | `def sample(self, n)` |
| `save` | method | `toposwarm_continual_trainer.py:475` | `def save(self, path)` |
| `save` | method | `toposwarm_continual_trainer.py:705` | `def save(self, path)` |
| `train` | method | `toposwarm_continual_trainer.py:933` | `def train(self, lazyown_dataset, train_records, val_records)` |
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
| `LazyOwnOrchestrator` | class | `toposwarm_lazyown_orchestrator.py:613` | `class LazyOwnOrchestrator` |
| `LazyOwnToolRegistry` | class | `toposwarm_lazyown_orchestrator.py:219` | `class LazyOwnToolRegistry(ToolRegistry)` |
| `SessionContext` | class | `toposwarm_lazyown_orchestrator.py:155` | `class SessionContext` |
| `__init__` | method | `toposwarm_lazyown_orchestrator.py:304` | `def __init__(self, cfg, bridge)` |
| `__init__` | method | `toposwarm_lazyown_orchestrator.py:629` | `def __init__(self, cfg, agent_cfg, bridge, logger, load_model, meta_cfg)` |
| `_extract_arg` | method | `toposwarm_lazyown_orchestrator.py:565` | `def _extract_arg(prompt, tool_name)` |
| `_hook` | method | `toposwarm_lazyown_orchestrator.py:712` | `def _hook(module, inp, out)` |
| `_import_agent` | function | `toposwarm_lazyown_orchestrator.py:80` | `def _import_agent()` |
| `_import_infer` | function | `toposwarm_lazyown_orchestrator.py:60` | `def _import_infer()` |
| `_import_lazyown_bridge` | function | `toposwarm_lazyown_orchestrator.py:134` | `def _import_lazyown_bridge()` |
| `_import_meta_harness` | function | `toposwarm_lazyown_orchestrator.py:95` | `def _import_meta_harness()` |
| `_import_routing_head` | function | `toposwarm_lazyown_orchestrator.py:114` | `def _import_routing_head()` |
| `_load_routing_head` | method | `toposwarm_lazyown_orchestrator.py:674` | `def _load_routing_head(self)` |
| `_neural_route` | method | `toposwarm_lazyown_orchestrator.py:696` | `def _neural_route(self, prompt)` |
| `_register_lazyown_tools` | method | `toposwarm_lazyown_orchestrator.py:309` | `def _register_lazyown_tools(self)` |
| `_serve` | method | `toposwarm_lazyown_orchestrator.py:1187` | `def _serve()` |
| `_setup_logger` | method | `toposwarm_lazyown_orchestrator.py:1199` | `def _setup_logger(level)` |
| `ack_event` | method | `toposwarm_lazyown_orchestrator.py:389` | `def ack_event(arg)` |
| `add_rule` | method | `toposwarm_lazyown_orchestrator.py:393` | `def add_rule(arg)` |
| `add_target` | method | `toposwarm_lazyown_orchestrator.py:421` | `def add_target(arg)` |
| `agent_result` | method | `toposwarm_lazyown_orchestrator.py:439` | `def agent_result(arg)` |
| `agent_status` | method | `toposwarm_lazyown_orchestrator.py:435` | `def agent_status(arg)` |
| `auto_loop` | method | `toposwarm_lazyown_orchestrator.py:511` | `def auto_loop(arg)` |
| `auto_populate` | method | `toposwarm_lazyown_orchestrator.py:471` | `def auto_populate(_)` |
| `c2_adversary` | method | `toposwarm_lazyown_orchestrator.py:503` | `def c2_adversary(arg)` |
| `c2_command` | method | `toposwarm_lazyown_orchestrator.py:340` | `def c2_command(arg)` |
| `c2_notes` | method | `toposwarm_lazyown_orchestrator.py:455` | `def c2_notes(arg)` |
| `c2_redop` | method | `toposwarm_lazyown_orchestrator.py:491` | `def c2_redop(arg)` |
| `c2_script` | method | `toposwarm_lazyown_orchestrator.py:499` | `def c2_script(arg)` |
| `c2_search_agent` | method | `toposwarm_lazyown_orchestrator.py:495` | `def c2_search_agent(arg)` |
| `c2_status` | method | `toposwarm_lazyown_orchestrator.py:363` | `def c2_status(_)` |
| `c2_vuln_analysis` | method | `toposwarm_lazyown_orchestrator.py:487` | `def c2_vuln_analysis(arg)` |
| `call_tool` | method | `toposwarm_lazyown_orchestrator.py:1177` | `def call_tool(name, arguments)` |
| `campaign_lessons` | method | `toposwarm_lazyown_orchestrator.py:467` | `def campaign_lessons(_)` |
| `campaign_sitrep` | method | `toposwarm_lazyown_orchestrator.py:451` | `def campaign_sitrep(_)` |
| `command_help` | method | `toposwarm_lazyown_orchestrator.py:417` | `def command_help(arg)` |
| `create_addon` | method | `toposwarm_lazyown_orchestrator.py:367` | `def create_addon(arg)` |
| `create_tool` | method | `toposwarm_lazyown_orchestrator.py:515` | `def create_tool(arg)` |
| `credentials` | method | `toposwarm_lazyown_orchestrator.py:459` | `def credentials(_)` |
| `discover_commands` | method | `toposwarm_lazyown_orchestrator.py:409` | `def discover_commands(arg)` |
| `finetune_on_lazyown` | method | `toposwarm_lazyown_orchestrator.py:1043` | `def finetune_on_lazyown(dataset_path, agent_cfg, logger)` |
| `generate_dataset` | method | `toposwarm_lazyown_orchestrator.py:962` | `def generate_dataset(output_path, bridge)` |
| `get_beacons` | method | `toposwarm_lazyown_orchestrator.py:336` | `def get_beacons(_)` |
| `get_config` | method | `toposwarm_lazyown_orchestrator.py:319` | `def get_config(_)` |
| `heartbeat_status` | method | `toposwarm_lazyown_orchestrator.py:401` | `def heartbeat_status(_)` |
| `infer_lazyown_tool` | method | `toposwarm_lazyown_orchestrator.py:540` | `def infer_lazyown_tool(prompt)` |
| `inject_objective` | method | `toposwarm_lazyown_orchestrator.py:523` | `def inject_objective(arg)` |
| `list_addons` | method | `toposwarm_lazyown_orchestrator.py:371` | `def list_addons(_)` |
| `list_agents` | method | `toposwarm_lazyown_orchestrator.py:443` | `def list_agents(_)` |
| `list_event_rules` | method | `toposwarm_lazyown_orchestrator.py:397` | `def list_event_rules(_)` |
| `list_modules` | method | `toposwarm_lazyown_orchestrator.py:332` | `def list_modules(_)` |
| `list_plugins` | method | `toposwarm_lazyown_orchestrator.py:378` | `def list_plugins(_)` |
| `list_sessions` | method | `toposwarm_lazyown_orchestrator.py:348` | `def list_sessions(_)` |
| `list_targets` | method | `toposwarm_lazyown_orchestrator.py:427` | `def list_targets(_)` |
| `list_tools` | method | `toposwarm_lazyown_orchestrator.py:1143` | `def list_tools()` |
| `llm_ask` | method | `toposwarm_lazyown_orchestrator.py:519` | `def llm_ask(arg)` |
| `main` | method | `toposwarm_lazyown_orchestrator.py:1216` | `def main()` |
| `next_objective` | method | `toposwarm_lazyown_orchestrator.py:527` | `def next_objective(_)` |
| `phase_guide` | method | `toposwarm_lazyown_orchestrator.py:413` | `def phase_guide(arg)` |
| `policy_status` | method | `toposwarm_lazyown_orchestrator.py:507` | `def policy_status(_)` |
| `poll_events` | method | `toposwarm_lazyown_orchestrator.py:385` | `def poll_events(_)` |
| `read_prompt` | method | `toposwarm_lazyown_orchestrator.py:531` | `def read_prompt(arg)` |
| `read_session_file` | method | `toposwarm_lazyown_orchestrator.py:356` | `def read_session_file(arg)` |
| `recommend_next` | method | `toposwarm_lazyown_orchestrator.py:479` | `def recommend_next(_)` |
| `report_update` | method | `toposwarm_lazyown_orchestrator.py:463` | `def report_update(arg)` |
| `run` | method | `toposwarm_lazyown_orchestrator.py:737` | `def run(self, prompt)` |
| `run_agent` | method | `toposwarm_lazyown_orchestrator.py:431` | `def run_agent(arg)` |
| `run_api` | method | `toposwarm_lazyown_orchestrator.py:344` | `def run_api(arg)` |
| `run_command` | method | `toposwarm_lazyown_orchestrator.py:315` | `def run_command(arg)` |
| `run_mcp_server` | method | `toposwarm_lazyown_orchestrator.py:1120` | `def run_mcp_server(orchestrator)` |
| `session_init` | method | `toposwarm_lazyown_orchestrator.py:405` | `def session_init(arg)` |
| `session_state` | method | `toposwarm_lazyown_orchestrator.py:475` | `def session_state(_)` |
| `set_active_target` | method | `toposwarm_lazyown_orchestrator.py:447` | `def set_active_target(arg)` |
| `set_config` | method | `toposwarm_lazyown_orchestrator.py:324` | `def set_config(arg)` |
| `timeline` | method | `toposwarm_lazyown_orchestrator.py:483` | `def timeline(_)` |
| `to_prompt_prefix` | method | `toposwarm_lazyown_orchestrator.py:166` | `def to_prompt_prefix(self)` |
| `update` | method | `toposwarm_lazyown_orchestrator.py:180` | `def update(self, tool_name, arg, output, ok)` |
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
| `MetaHarnessOptimizer` | class | `toposwarm_meta_harness.py:992` | `class MetaHarnessOptimizer` |
| `ParetoFrontier` | class | `toposwarm_meta_harness.py:881` | `class ParetoFrontier` |
| `__init__` | method | `toposwarm_meta_harness.py:138` | `def __init__(self, cfg, logger)` |
| `__init__` | method | `toposwarm_meta_harness.py:335` | `def __init__(self, logger)` |
| `__init__` | method | `toposwarm_meta_harness.py:441` | `def __init__(self, logger, capacity, dense)` |
| `__init__` | method | `toposwarm_meta_harness.py:592` | `def __init__(self, cfg, logger)` |
| `__init__` | method | `toposwarm_meta_harness.py:754` | `def __init__(self, cfg, memory, keyword_router, logger)` |
| `__init__` | method | `toposwarm_meta_harness.py:890` | `def __init__(self, cfg, logger)` |
| `__init__` | method | `toposwarm_meta_harness.py:1009` | `def __init__(self, cfg)` |
| `_build_index` | method | `toposwarm_meta_harness.py:453` | `def _build_index(self)` |
| `_count_existing_runs` | method | `toposwarm_meta_harness.py:149` | `def _count_existing_runs(self)` |
| `_demo` | method | `toposwarm_meta_harness.py:1057` | `def _demo()` |
| `_episode_text` | method | `toposwarm_meta_harness.py:482` | `def _episode_text(score, traces)` |
| `_episode_weight` | method | `toposwarm_meta_harness.py:813` | `def _episode_weight(ep, query_prompt)` |
| `_is_on_frontier` | method | `toposwarm_meta_harness.py:955` | `def _is_on_frontier(self, candidate)` |
| `_load_episode` | method | `toposwarm_meta_harness.py:464` | `def _load_episode(self, run_dir)` |
| `_next_run_dir` | method | `toposwarm_meta_harness.py:152` | `def _next_run_dir(self, hint)` |
| `_now_iso` | method | `toposwarm_meta_harness.py:112` | `def _now_iso()` |
| `_parse_list` | method | `toposwarm_meta_harness.py:680` | `def _parse_list(raw)` |
| `_prune` | method | `toposwarm_meta_harness.py:977` | `def _prune(self)` |
| `_prune_old` | method | `toposwarm_meta_harness.py:158` | `def _prune_old(self)` |
| `_rebuild_tfidf` | method | `toposwarm_meta_harness.py:368` | `def _rebuild_tfidf(self)` |
| `_reextract_arg` | method | `toposwarm_meta_harness.py:864` | `def _reextract_arg(prompt, tool_name, fallback)` |
| `_revise_from_challengers` | method | `toposwarm_meta_harness.py:831` | `def _revise_from_challengers(self, draft_tool, draft_arg, prompt, challengers)` |
| `_search_st` | method | `toposwarm_meta_harness.py:401` | `def _search_st(self, query, top_k)` |
| `_search_tfidf` | method | `toposwarm_meta_harness.py:412` | `def _search_tfidf(self, query, top_k)` |
| `_setup_logger` | method | `toposwarm_meta_harness.py:95` | `def _setup_logger(name, level)` |
| `_stable_id` | method | `toposwarm_meta_harness.py:107` | `def _stable_id(text)` |
| `_tokenise` | method | `toposwarm_meta_harness.py:573` | `def _tokenise(text)` |
| `add` | method | `toposwarm_meta_harness.py:362` | `def add(self, text, episode)` |
| `add` | method | `toposwarm_meta_harness.py:899` | `def add(self, config, metrics)` |
| `bulk_index` | method | `toposwarm_meta_harness.py:376` | `def bulk_index(self, texts, episodes)` |
| `format_snapshot` | method | `toposwarm_meta_harness.py:687` | `def format_snapshot(self, snapshot, max_chars)` |
| `frontier_configs` | method | `toposwarm_meta_harness.py:951` | `def frontier_configs(self)` |
| `gather_snapshot` | method | `toposwarm_meta_harness.py:596` | `def gather_snapshot(self, bridge)` |
| `get_best_harness_config` | method | `toposwarm_meta_harness.py:1043` | `def get_best_harness_config(self)` |
| `get_pareto_runs` | method | `toposwarm_meta_harness.py:269` | `def get_pareto_runs(self, metrics)` |
| `get_scores` | method | `toposwarm_meta_harness.py:257` | `def get_scores(self)` |
| `grep_traces` | method | `toposwarm_meta_harness.py:238` | `def grep_traces(self, pattern, max_results)` |
| `list_runs` | method | `toposwarm_meta_harness.py:229` | `def list_runs(self, n)` |
| `log_run` | method | `toposwarm_meta_harness.py:176` | `def log_run(self, harness_snapshot, trace_steps, score, reasoning)` |
| `log_run` | method | `toposwarm_meta_harness.py:1030` | `def log_run(self, harness_snapshot, trace_steps, score, reasoning)` |
| `query_experience` | method | `toposwarm_meta_harness.py:1047` | `def query_experience(self, prompt, tool_hint, top_k)` |
| `retrieve_confirmers_and_challengers` | method | `toposwarm_meta_harness.py:549` | `def retrieve_confirmers_and_challengers(self, draft_tool, prompt, top_k)` |
| `retrieve_similar` | method | `toposwarm_meta_harness.py:505` | `def retrieve_similar(self, prompt, tool_hint, top_k, min_score)` |
| `route` | method | `toposwarm_meta_harness.py:766` | `def route(self, prompt, snapshot_text)` |
| `search` | method | `toposwarm_meta_harness.py:392` | `def search(self, query, top_k)` |
| `select_best` | method | `toposwarm_meta_harness.py:919` | `def select_best(self, preference)` |
| `set_router` | method | `toposwarm_meta_harness.py:1024` | `def set_router(self, keyword_router)` |
| `store` | method | `toposwarm_meta_harness.py:493` | `def store(self, score, traces)` |
| `_cached_encode` | function | `ts_utils.py:94` | `def _cached_encode(text)` |
| `_cached_tool_token` | function | `ts_utils.py:103` | `def _cached_tool_token(tool_name)` |
| `import_module` | function | `ts_utils.py:62` | `def import_module(name)` |
| `make_cached_encode` | function | `ts_utils.py:86` | `def make_cached_encode(tokenizer)` |
| `make_cached_tool_token` | function | `ts_utils.py:100` | `def make_cached_tool_token(tokenizer)` |
| `safe_eval` | function | `ts_utils.py:42` | `def safe_eval(expr)` |
| `setup_logger` | function | `ts_utils.py:25` | `def setup_logger(name, level)` |

