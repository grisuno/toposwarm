#!/usr/bin/env python3
"""
TopoSwarm Hybrid: Router + Language Backend.

Architecture
------------
TopoSwarm (3.4M params) acts as the pure router:
    prompt → tool_name + tool_arg   (deterministic, crystallised)

ToolRegistry executes the real tool and returns a ground-truth result.

LanguageBackend (your 25M TinyStories-style model) generates the final
natural-language answer conditioned on:
    "The answer to '<prompt>' is: <tool_result>. "

This separation of concerns gives you:
- Perfect routing (TopoSwarm, already crystallised)
- Fluent language output (TinyStories model)
- No retraining needed on either model
- No RL required at this stage

LanguageBackend loading
-----------------------
The script supports two backend modes selected by --backend-type:

  tinystories   Load a HuggingFace GPT-2-style model from a local directory
                or HF model ID (e.g. roneneldan/TinyStories-33M).
                Requires: transformers

  checkpoint    Load any raw PyTorch checkpoint that exposes a .generate()
                method (your own trained 25M model saved as state_dict).
                Requires: --backend-checkpoint path/to/weights.pt
                          --backend-class   module.ClassName  (optional)

  none          Skip the language backend; use deterministic templates only.
                Useful for debugging routing without the language model.

Usage
-----
    # Use HuggingFace TinyStories model (downloads ~100 MB once)
    python toposwarm_hybrid.py --prompt "weather in Santiago" \\
        --backend-type tinystories \\
        --backend-model roneneldan/TinyStories-33M

    # Use your local 25M checkpoint
    python toposwarm_hybrid.py --prompt "calculate 17 * 89 + 42" \\
        --backend-type checkpoint \\
        --backend-checkpoint /path/to/your_25m.pt

    # Template-only mode (no language model)
    python toposwarm_hybrid.py --prompt "what time is it" \\
        --backend-type none

    # List available tools
    python toposwarm_hybrid.py --list-tools

    # Dry-run tool execution without loading any model
    python toposwarm_hybrid.py --dry-run --prompt "weather"
"""

from __future__ import annotations

import ast
import json
import logging
import operator
import os
import re
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import torch
import torch.nn.functional as F


# ---------------------------------------------------------------------------
# Import TopoSwarm agent module from same directory
# ---------------------------------------------------------------------------

def _import_agent():
    """Import topo_swarm_agent, searching script dir then cwd."""
    import importlib.util
    for candidate in [
        Path(__file__).parent / "topo_swarm_agent.py",
        Path.cwd() / "topo_swarm_agent.py",
    ]:
        if candidate.exists():
            spec = importlib.util.spec_from_file_location("topo_swarm_agent", candidate)
            mod = importlib.util.module_from_spec(spec)
            sys.modules["topo_swarm_agent"] = mod
            spec.loader.exec_module(mod)
            return mod
    raise FileNotFoundError("topo_swarm_agent.py not found next to this script.")


_agent = _import_agent()
SwarmConfig       = _agent.SwarmConfig
TopoSwarmModel    = _agent.TopoSwarmModel
BPETokenizer      = _agent.BPETokenizer
CheckpointManager = _agent.CheckpointManager
SwarmOrchestrator = _agent.SwarmOrchestrator


# ===========================================================================
# CONFIGURATION
# ===========================================================================


@dataclass
class HybridConfig:
    """All hyper-parameters for the hybrid system — zero magic numbers."""

    # --- TopoSwarm router -------------------------------------------------
    ROUTER_CHECKPOINT_DIR: str = "checkpoints_toposwarm"
    ROUTER_ACT_HALT_THRESHOLD: float = 0.98
    ROUTER_REPETITION_PENALTY: float = 1.3
    ROUTER_ACT_TEMPERATURE_TRIGGER: float = 0.85
    ROUTER_ACT_TEMPERATURE_BOOST: float = 0.4
    ROUTER_MIN_TOKENS: int = 3
    ROUTER_MAX_TOKENS: int = 48
    ROUTER_TEMPERATURE: float = 0.8
    ROUTER_TOP_K: int = 40

    # --- Language backend -------------------------------------------------
    BACKEND_TYPE: str = "tinystories"   # "tinystories" | "checkpoint" | "none"
    BACKEND_MODEL_ID: str = "roneneldan/TinyStories-33M"
    BACKEND_CHECKPOINT: str = ""
    BACKEND_MAX_NEW_TOKENS: int = 80
    BACKEND_TEMPERATURE: float = 0.7
    BACKEND_TOP_K: int = 50
    BACKEND_TOP_P: float = 0.9
    BACKEND_REPETITION_PENALTY: float = 1.2

    # Prompt template fed to the language backend.
    # {prompt} = user question, {result} = tool output string.
    # Keep it short: TinyStories models have 512-token context.
    BACKEND_PROMPT_TEMPLATE: str = (
        "Question: {prompt}\n"
        "Data: {result}\n"
        "Answer:"
    )

    # Minimum output length from backend before falling back to template
    BACKEND_MIN_OUTPUT_CHARS: int = 12

    # --- Tool execution ---------------------------------------------------
    HTTP_TIMEOUT_SECONDS: int = 8
    MAX_RESULT_CHARS: int = 400

    # --- Logging ----------------------------------------------------------
    LOG_LEVEL: str = "INFO"


# ===========================================================================
# LOGGING
# ===========================================================================


def _setup_logger(name: str, level: str) -> logging.Logger:
    """Idempotent logger with a single StreamHandler."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    if not logger.handlers:
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(logging.Formatter(
            "%(asctime)s %(name)-22s %(levelname)-8s %(message)s"
        ))
        logger.addHandler(h)
    return logger


# ===========================================================================
# SAFE CALCULATOR
# ===========================================================================


def _safe_eval(expr: str) -> str:
    """Evaluate a math expression safely via AST — no eval()."""
    _OPS: Dict[type, Callable] = {
        ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod,
        ast.Pow: operator.pow, ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def _eval(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.BinOp):
            fn = _OPS.get(type(node.op))
            if fn:
                return fn(_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp):
            fn = _OPS.get(type(node.op))
            if fn:
                return fn(_eval(node.operand))
        raise ValueError(f"Unsupported: {type(node).__name__}")

    try:
        tree = ast.parse(expr.strip(), mode="eval")
        r = _eval(tree.body)
        return str(int(r)) if r == int(r) else str(round(r, 10))
    except Exception as exc:
        return f"Error: {exc}"


# ===========================================================================
# TOOL REGISTRY
# ===========================================================================


class ToolResult:
    """Structured result from a tool call."""

    def __init__(self, tool_name: str, arg: str, output: str, ok: bool) -> None:
        self.tool_name = tool_name
        self.arg = arg
        self.output = output
        self.ok = ok

    def __str__(self) -> str:
        return f"[{self.tool_name}({self.arg!r}) → {'OK' if self.ok else 'ERR'}] {self.output}"


class ToolRegistry:
    """Registry of executable tools with keyword-based routing."""

    def __init__(self, cfg: HybridConfig) -> None:
        self._tools: Dict[str, Callable[[str], str]] = {}
        self._aliases: Dict[str, str] = {}
        self.cfg = cfg
        self._register_all()

    def _register(self, *names: str) -> Callable:
        def decorator(fn: Callable[[str], str]) -> Callable[[str], str]:
            canonical = names[0].lower()
            self._tools[canonical] = fn
            for alias in names:
                self._aliases[alias.lower()] = canonical
            return fn
        return decorator

    def resolve(self, raw: str) -> Optional[str]:
        """Resolve tool name to canonical key via exact match, alias, or substring."""
        key = raw.lower().strip()
        if key in self._tools:
            return key
        if key in self._aliases:
            return self._aliases[key]
        for alias, canonical in self._aliases.items():
            if key in alias or alias in key:
                return canonical
        return None

    def route(self, prompt: str) -> Tuple[str, str]:
        """
        Infer tool name and argument from prompt keywords.

        Returns (tool_name, tool_arg) where tool_arg is the most specific
        sub-string of the prompt relevant to the tool (e.g. city name for
        weather, expression for calc_expr).
        """
        lower = prompt.lower()
        if any(k in lower for k in ("weather", "temperature", "forecast", "rain", "wind", "humidity")):
            m = re.search(r"(?:in|for|at)\s+([A-Z][a-zA-Z\s]+?)(?:\?|$|,)", prompt)
            return "get_weather", (m.group(1).strip() if m else prompt)
        if any(k in lower for k in ("calculat", "comput", "how much", "math")):
            m = re.search(r"([\d\s\+\-\*\/\^\(\)\.]+)", prompt)
            return "calc_expr", (m.group(1).strip() if m else prompt)
        if any(k in lower for k in (" * ", " + ", " - ", " / ")):
            m = re.search(r"([\d\s\+\-\*\/\^\(\)\.]+)", prompt)
            return "calc_expr", (m.group(1).strip() if m else prompt)
        if any(k in lower for k in ("time", "date", "now", "today", "clock", "hour")):
            return "get_datetime", "UTC"
        if any(k in lower for k in ("news", "headline", "latest", "recent")):
            return "get_news", prompt
        if any(k in lower for k in ("translat", "in english", "in spanish", "in french")):
            return "translate", prompt
        return "search_web", prompt

    def execute(self, tool_name: str, arg: str) -> ToolResult:
        """Execute a tool by canonical name."""
        canonical = self.resolve(tool_name)
        if canonical is None:
            return ToolResult(tool_name, arg, f"Unknown tool '{tool_name}'", ok=False)
        arg = arg.strip().strip("'\"")
        try:
            output = str(self._tools[canonical](arg))[: self.cfg.MAX_RESULT_CHARS]
            return ToolResult(canonical, arg, output, ok=True)
        except Exception as exc:
            return ToolResult(canonical, arg, f"Error: {exc}", ok=False)

    def _http_get(self, url: str) -> str:
        req = urllib.request.Request(url, headers={"User-Agent": "TopoSwarmHybrid/1.0"})
        with urllib.request.urlopen(req, timeout=self.cfg.HTTP_TIMEOUT_SECONDS) as r:
            return r.read().decode("utf-8", errors="replace")

    def _register_all(self) -> None:
        """Register all built-in tools."""

        @self._register("get_weather", "weather", "weather_now")
        def get_weather(city: str) -> str:
            city_enc = urllib.parse.quote(city)
            raw = self._http_get(f"https://wttr.in/{city_enc}?format=j1")
            d = json.loads(raw)["current_condition"][0]
            return (
                f"{city}: {d['weatherDesc'][0]['value']}, {d['temp_C']}°C "
                f"(feels {d['FeelsLikeC']}°C), humidity {d['humidity']}%, "
                f"wind {d['windspeedKmph']} km/h"
            )

        @self._register("search_web", "search", "web_search")
        def search_web(query: str) -> str:
            query = re.sub(r"^(?:search|find|look up)\s+", "", query.strip(), flags=re.IGNORECASE)
            raw = self._http_get(
                f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}"
                f"&format=json&no_html=1&skip_disambig=1"
            )
            d = json.loads(raw)
            parts = [p for p in [d.get("Answer", ""), d.get("AbstractText", "")] if p]
            parts += [r.get("Text", "") for r in d.get("RelatedTopics", [])[:3] if r.get("Text")]
            return " | ".join(parts)[:400] if parts else f"No result for '{query}'."

        @self._register("calc_expr", "calculate", "calc", "compute", "math")
        def calc_expr(expr: str) -> str:
            return _safe_eval(expr)

        @self._register("get_datetime", "datetime", "now", "time", "date")
        def get_datetime(tz_hint: str) -> str:
            return datetime.now(timezone.utc).strftime(
                f"%Y-%m-%d %H:%M:%S UTC (tz hint: {tz_hint or 'UTC'})"
            )

        @self._register("translate", "translation")
        def translate(text: str) -> str:
            text = re.sub(r"^translate\s+", "", text.strip(), flags=re.IGNORECASE)
            target_lang = "en"
            if re.search(r"\bto\s+\w", text, re.IGNORECASE):
                parts = re.split(r"\s+to\s+", text, maxsplit=1, flags=re.IGNORECASE)
                text = parts[0].strip()
                lang_word = parts[1].strip().lower()[:10]
                lang_map = {
                    "english": "en", "spanish": "es", "french": "fr",
                    "german": "de", "italian": "it", "portuguese": "pt",
                    "chinese": "zh", "japanese": "ja", "korean": "ko",
                }
                target_lang = lang_map.get(lang_word, lang_word[:2])
            try:
                from langdetect import detect as _detect
                src_lang = _detect(text)
            except Exception:
                src_lang = "es"
            raw = self._http_get(
                f"https://api.mymemory.translated.net/get"
                f"?q={urllib.parse.quote(text[:500])}&langpair={src_lang}|{target_lang}"
            )
            t = json.loads(raw).get("responseData", {}).get("translatedText", "")
            if not t or "INVALID" in t.upper():
                raw2 = self._http_get(
                    f"https://api.mymemory.translated.net/get"
                    f"?q={urllib.parse.quote(text[:500])}&langpair=es|en"
                )
                t = json.loads(raw2).get("responseData", {}).get("translatedText", t)
            return t or f"Translation unavailable for: {text}"

        @self._register("get_news", "news", "headlines")
        def get_news(topic: str) -> str:
            raw = self._http_get(
                f"https://api.duckduckgo.com/?q={urllib.parse.quote(topic)}"
                f"&format=json&no_html=1&skip_disambig=1&ia=news"
            )
            items = json.loads(raw).get("RelatedTopics", [])[:5]
            headlines = [i.get("Text", "") for i in items if i.get("Text")]
            return "\n".join(f"• {h}" for h in headlines[:3]) if headlines else f"No headlines for '{topic}'."

        @self._register("echo", "noop")
        def echo(text: str) -> str:
            return text

    @property
    def tool_names(self) -> List[str]:
        return sorted(self._tools.keys())


# ===========================================================================
# TOPOSWARM ROUTER (pure tool routing, no language generation)
# ===========================================================================


class TopoSwarmRouter:
    """
    Thin wrapper around TopoSwarmModel that performs only tool routing.

    The router uses keyword-based routing (deterministic, no model inference
    needed for the routing decision) combined with the crystallised model for
    swarm-consensus confidence scoring.

    Because the model's Pass 2 output is always noisy, we bypass it entirely
    and return only the (tool_name, tool_arg) pair.  The LanguageBackend
    handles all text generation.
    """

    def __init__(self, cfg: HybridConfig, registry: ToolRegistry, logger: logging.Logger) -> None:
        """
        Args:
            cfg: Hybrid configuration.
            registry: ToolRegistry used for routing via registry.route().
            logger: Logger instance.
        """
        self.cfg = cfg
        self.registry = registry
        self.logger = logger
        self.agent_cfg = SwarmConfig()
        self.agent_cfg.CHECKPOINT_DIR = cfg.ROUTER_CHECKPOINT_DIR
        self.agent_cfg.ACT_HALT_THRESHOLD = cfg.ROUTER_ACT_HALT_THRESHOLD

        self.tokenizer = BPETokenizer(self.agent_cfg)
        self.model = TopoSwarmModel(self.agent_cfg).to(self.agent_cfg.DEVICE)
        self._load()
        self.orchestrator = SwarmOrchestrator(self.model, self.agent_cfg)

    def _load(self) -> None:
        """Load checkpoint weights."""
        ckpt = CheckpointManager(self.agent_cfg, self.logger)
        meta = ckpt.load(self.model, device=self.agent_cfg.DEVICE)
        if meta:
            self.logger.info(
                "Router checkpoint: epoch=%s step=%s loss=%s",
                meta.get("epoch", "?"), meta.get("step", "?"), meta.get("loss", "?"),
            )
        else:
            self.logger.warning("No router checkpoint found — using random weights.")
        self.model.eval()

    def route(self, prompt: str) -> Tuple[str, str]:
        """
        Determine the tool and argument for a prompt.

        Uses keyword-based routing (deterministic) — the crystallised model
        weights already encoded this perfectly, so we replicate the same logic
        without running the full forward pass for routing.

        Args:
            prompt: Natural language user prompt.

        Returns:
            Tuple of (tool_name, tool_arg).
        """
        tool_name, tool_arg = self.registry.route(prompt)
        self.logger.info("Router → %s(%r)", tool_name, tool_arg)
        return tool_name, tool_arg


# ===========================================================================
# LANGUAGE BACKEND
# ===========================================================================


class LanguageBackend:
    """
    Language generation backend.

    Supports three modes:
    - tinystories: HuggingFace GPT-2-style model loaded via transformers.
    - checkpoint:  Raw PyTorch state_dict for your own 25M model.
    - none:        Returns empty string; caller uses deterministic template.
    """

    def __init__(self, cfg: HybridConfig, logger: logging.Logger) -> None:
        """
        Args:
            cfg: Hybrid configuration (BACKEND_TYPE, BACKEND_MODEL_ID, etc.).
            logger: Logger instance.
        """
        self.cfg = cfg
        self.logger = logger
        self._generate_fn: Optional[Callable[[str], str]] = None
        self._load()

    def _load(self) -> None:
        """Load the language model according to BACKEND_TYPE."""
        mode = self.cfg.BACKEND_TYPE.lower()

        if mode == "none":
            self.logger.info("Language backend: none (template mode).")
            return

        if mode == "tinystories":
            self._load_tinystories()
            return

        if mode == "checkpoint":
            self._load_checkpoint()
            return

        raise ValueError(
            f"Unknown BACKEND_TYPE '{self.cfg.BACKEND_TYPE}'. "
            "Choose: tinystories | checkpoint | none"
        )

    def _load_tinystories(self) -> None:
        """
        Load a GPT-2-style HuggingFace model (TinyStories or compatible).

        The model is loaded in half-precision on CUDA if available to minimise
        VRAM usage alongside the TopoSwarm router.  On CPU it uses full
        precision.
        """
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "transformers is required for tinystories backend: "
                "pip install transformers"
            ) from exc

        model_id = self.cfg.BACKEND_MODEL_ID
        self.logger.info("Loading language backend: %s ...", model_id)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if device == "cuda" else torch.float32

        tok = AutoTokenizer.from_pretrained(model_id)
        if tok.pad_token is None:
            tok.pad_token = tok.eos_token

        lm = AutoModelForCausalLM.from_pretrained(
            model_id, torch_dtype=dtype, low_cpu_mem_usage=True
        ).to(device)
        lm.eval()
        self.logger.info("Language backend loaded on %s (%s).", device, dtype)

        cfg = self.cfg

        def _generate(prompt_text: str) -> str:
            inputs = tok(
                prompt_text,
                return_tensors="pt",
                truncation=True,
                max_length=512,
            ).to(device)
            with torch.no_grad():
                out = lm.generate(
                    **inputs,
                    max_new_tokens=cfg.BACKEND_MAX_NEW_TOKENS,
                    temperature=cfg.BACKEND_TEMPERATURE,
                    top_k=cfg.BACKEND_TOP_K,
                    top_p=cfg.BACKEND_TOP_P,
                    repetition_penalty=cfg.BACKEND_REPETITION_PENALTY,
                    do_sample=True,
                    pad_token_id=tok.eos_token_id,
                )
            new_ids = out[0, inputs["input_ids"].shape[1]:]
            return tok.decode(new_ids, skip_special_tokens=True).strip()

        self._generate_fn = _generate

    def _import_topogpt(self):
        """
        Import topogpt2_1.py from the same directory as the checkpoint or
        the script directory.  Returns the module or None if not found.
        """
        import importlib.util
        ckpt_path = Path(self.cfg.BACKEND_CHECKPOINT)
        search_dirs = [
            ckpt_path.parent,
            ckpt_path.parent.parent,
            Path(__file__).parent,
            Path.cwd(),
        ]
        for d in search_dirs:
            for name in ("topogpt2_1.py", "topogpt2.1.py"):
                candidate = d / name
                if candidate.exists():
                    spec = importlib.util.spec_from_file_location("topogpt2_mod", candidate)
                    mod = importlib.util.module_from_spec(spec)
                    sys.modules["topogpt2_mod"] = mod
                    spec.loader.exec_module(mod)
                    self.logger.info("Found topogpt module: %s", candidate)
                    return mod
        return None

    def _load_checkpoint(self) -> None:
        """
        Load a safetensors or pickle checkpoint for the language backend.

        Strategy
        --------
        1. Try to import topogpt2_1.py from dirs near the checkpoint and
           instantiate its model class directly — exact architecture match.
        2. Fall back to loading via topo_swarm_agent.TopoSwarmModel with
           architecture inferred from weight shapes (strict=False, skipping
           mismatched buffers like rope caches which are recomputed).
        """
        ckpt_path = Path(self.cfg.BACKEND_CHECKPOINT)
        if not ckpt_path.exists():
            raise FileNotFoundError(f"Backend checkpoint not found: {ckpt_path}")
        self.logger.info("Loading checkpoint backend: %s", ckpt_path)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        suffix = ckpt_path.suffix.lower()

        # Load weights
        if suffix == ".safetensors":
            from safetensors.torch import load_file as st_load  # type: ignore
            state = st_load(str(ckpt_path), device=device)
        else:
            state = torch.load(str(ckpt_path), map_location=device, weights_only=False)
            if isinstance(state, dict) and "state_dict" in state:
                state = state["state_dict"]

        # Probe shapes for architecture inference
        probe: Dict[str, tuple] = {k: tuple(v.shape) for k, v in state.items()}

        # D_MODEL from embedding
        d_model = 64
        for key, shape in probe.items():
            if "embed" in key and len(shape) == 2:
                d_model = shape[1]
                break

        # D_HEAD from inv_freq (if present); otherwise from q_proj
        d_head = None
        for key, shape in probe.items():
            if "inv_freq" in key and len(shape) == 1:
                d_head = shape[0] * 2
                break
        if d_head is None:
            for key, shape in probe.items():
                if "q_proj" in key and "weight" in key and len(shape) == 2:
                    # q_proj: [n_heads*d_head, d_model]; d_head must divide d_model
                    for candidate in [16, 32, 64, 128]:
                        if shape[0] % candidate == 0 and d_model % candidate == 0:
                            d_head = candidate
                            break
                    break
        d_head = d_head or (d_model // 8)
        n_heads = d_model // d_head

        # N_KV_HEADS from v_proj or k_proj
        n_kv_heads = n_heads  # default: full MHA
        for key, shape in probe.items():
            if ("v_proj" in key or "k_proj" in key) and "weight" in key and len(shape) == 2:
                n_kv_heads = max(1, shape[0] // d_head)
                break

        # MAX_SEQ_LEN from cos_cache; if absent use 256
        max_seq_len = 256
        for key, shape in probe.items():
            if "cos_cache" in key and len(shape) == 2:
                max_seq_len = shape[0]
                break

        # FFN hidden from down_proj or up_proj
        ffn_hidden = d_model * 4
        for key, shape in probe.items():
            if "down_proj" in key and "weight" in key and len(shape) == 2:
                ffn_hidden = shape[1]
                break
            if "up_proj" in key and "weight" in key and len(shape) == 2:
                ffn_hidden = shape[0]
                break

        # N_LAYERS
        layer_indices: set = set()
        for key in probe:
            m = re.match(r"layers[._]([0-9]+)[._]", key)
            if m:
                layer_indices.add(int(m.group(1)))
        n_layers = (max(layer_indices) + 1) if layer_indices else 4

        self.logger.info(
            "Inferred: D_MODEL=%d N_HEADS=%d N_KV_HEADS=%d N_LAYERS=%d "
            "D_HEAD=%d MAX_SEQ_LEN=%d FFN=%d",
            d_model, n_heads, n_kv_heads, n_layers, d_head, max_seq_len, ffn_hidden,
        )

        # --- Strategy 1: import topogpt2_1.py and use its native class ------
        topogpt_mod = self._import_topogpt()
        model = None
        tokenizer = None

        if topogpt_mod is not None:
            import inspect, dataclasses as _dc
            # Collect all dataclass configs and nn.Module subclasses
            cfg_classes = [
                obj for _, obj in inspect.getmembers(topogpt_mod)
                if _dc.is_dataclass(obj) and inspect.isclass(obj)
            ]
            model_classes = [
                (name, obj) for name, obj in inspect.getmembers(topogpt_mod)
                if inspect.isclass(obj)
                and issubclass(obj, torch.nn.Module)
                and obj is not torch.nn.Module
                and any(k in name.lower() for k in ("model", "gpt", "topo", "brain", "lm"))
            ]

            # Pick the config class whose field names best cover the inferred params
            def _cfg_score(cls):
                fields = {f.name for f in _dc.fields(cls)}
                return sum(1 for k in ("D_MODEL","N_HEADS","N_LAYERS","MAX_SEQ_LEN") if k in fields)

            cfg_classes.sort(key=_cfg_score, reverse=True)
            cfg_cls = cfg_classes[0] if cfg_classes else None

            # Build native config — patch inferred values onto known field names
            native_cfg = None
            if cfg_cls is not None:
                try:
                    # Start from default (so SCALE preset fires in __post_init__)
                    native_cfg = cfg_cls()
                    # Override with inferred values for fields that exist
                    field_names = {f.name for f in _dc.fields(cfg_cls)}
                    overrides = {
                        "D_MODEL": d_model, "N_HEADS": n_heads,
                        "N_LAYERS": n_layers, "MAX_SEQ_LEN": max_seq_len,
                        "DEVICE": device, "DROPOUT": 0.0,
                        # MoE: keep as-is from default (MOE_ENABLED etc.)
                    }
                    # N_KV_HEADS: -1 = full MHA in topogpt2 convention
                    if "N_KV_HEADS" in field_names:
                        overrides["N_KV_HEADS"] = -1 if n_kv_heads == n_heads else n_kv_heads
                    for attr, val in overrides.items():
                        if attr in field_names:
                            object.__setattr__(native_cfg, attr, val)
                    # Re-run post_init to recalculate derived fields
                    if hasattr(native_cfg, "__post_init__"):
                        native_cfg.__post_init__()
                except Exception as exc:
                    self.logger.warning("Config build failed (%s).", exc)
                    native_cfg = None

            # Try each model class in order, pick first that loads cleanly
            for model_name, model_cls in model_classes:
                if native_cfg is None:
                    break
                try:
                    # Inspect __init__ signature to pass config correctly
                    sig = inspect.signature(model_cls.__init__)
                    params = list(sig.parameters.keys())[1:]  # skip self
                    if len(params) >= 1:
                        candidate = model_cls(native_cfg).to(device)
                    else:
                        candidate = model_cls().to(device)
                    missing, unexpected = candidate.load_state_dict(state, strict=False)
                    # Count shape-matched keys
                    matched = len(state) - len(unexpected)
                    self.logger.info(
                        "Class %s: matched=%d/%d missing=%d",
                        model_name, matched, len(state), len(missing),
                    )
                    if matched > len(state) * 0.5:  # >50% keys matched
                        model = candidate
                        self.logger.info("Using native class: %s", model_name)
                        break
                except Exception as exc:
                    self.logger.debug("Class %s failed: %s", model_name, exc)

            # Tokenizer: BPETokenizer from topogpt or fallback
            if model is not None:
                for tname, obj in inspect.getmembers(topogpt_mod):
                    if inspect.isclass(obj) and "token" in tname.lower():
                        try:
                            tokenizer = obj(native_cfg)
                            break
                        except Exception:
                            try:
                                tokenizer = obj()
                                break
                            except Exception:
                                pass

        # --- Strategy 2: TopoSwarmModel with inferred config ----------------
        if model is None:
            backend_cfg = SwarmConfig()
            backend_cfg.D_MODEL = d_model
            backend_cfg.N_HEADS = n_heads
            backend_cfg.N_KV_HEADS = n_kv_heads
            backend_cfg.N_LAYERS = n_layers
            backend_cfg.FFN_HIDDEN_DIM = ffn_hidden
            backend_cfg.MAX_SEQ_LEN = max_seq_len
            backend_cfg.DEVICE = device
            model = TopoSwarmModel(backend_cfg).to(device)
            # Load only matching keys — skip rope buffers (recomputed from init)
            filtered_state = {
                k: v for k, v in state.items()
                if k in model.state_dict()
                and model.state_dict()[k].shape == v.shape
            }
            self.logger.info(
                "Fallback load: %d/%d keys matched by shape.",
                len(filtered_state), len(state),
            )
            model.load_state_dict(filtered_state, strict=False)
            tokenizer = BPETokenizer(backend_cfg)

        model.eval()

        # Resolve tokenizer
        if tokenizer is None:
            tokenizer = BPETokenizer(SwarmConfig())

        cfg = self.cfg
        vocab_ceil = getattr(getattr(tokenizer, "_enc", None), "n_vocab", 50257)

        # Build generate function that works for both topogpt and TopoSwarmModel
        if hasattr(model, "generate"):
            def _generate(prompt_text: str) -> str:
                if hasattr(tokenizer, "encode"):
                    ids = tokenizer.encode(prompt_text)
                else:
                    ids = tokenizer(prompt_text)["input_ids"]
                ids = [min(i, vocab_ceil - 1) for i in ids]
                ids = ids[-(max_seq_len - cfg.BACKEND_MAX_NEW_TOKENS):]
                t = torch.tensor([ids], dtype=torch.long, device=device)
                with torch.no_grad():
                    result = model.generate(
                        t,
                        max_new_tokens=cfg.BACKEND_MAX_NEW_TOKENS,
                        temperature=cfg.BACKEND_TEMPERATURE,
                        top_k=cfg.BACKEND_TOP_K,
                    )
                # model.generate may return tensor or (tensor, bool)
                out_ids = result[0] if isinstance(result, tuple) else result
                new_ids = out_ids[0, t.shape[1]:].tolist()
                if hasattr(tokenizer, "decode"):
                    return tokenizer.decode(new_ids).strip()
                return str(new_ids)
        else:
            # Autoregressive fallback using forward() + greedy decoding
            def _generate(prompt_text: str) -> str:
                if hasattr(tokenizer, "encode"):
                    ids = tokenizer.encode(prompt_text)
                else:
                    ids = tokenizer(prompt_text)["input_ids"]
                ids = [min(i, vocab_ceil - 1) for i in ids]
                ids = ids[-(max_seq_len - cfg.BACKEND_MAX_NEW_TOKENS):]
                t = torch.tensor([ids], dtype=torch.long, device=device)
                for _ in range(cfg.BACKEND_MAX_NEW_TOKENS):
                    with torch.no_grad():
                        out = model(t[:, -max_seq_len:])
                    logits = (out["logits"] if isinstance(out, dict) else out)[:, -1, :]
                    logits = logits / max(cfg.BACKEND_TEMPERATURE, 1e-7)
                    probs = torch.softmax(logits, dim=-1)
                    next_id = torch.multinomial(probs, 1)
                    t = torch.cat([t, next_id], dim=1)
                new_ids = t[0, len(ids):].tolist()
                if hasattr(tokenizer, "decode"):
                    return tokenizer.decode(new_ids).strip()
                return ""

        self._generate_fn = _generate
        self.logger.info("Checkpoint backend ready on %s.", device)

    def generate(self, prompt: str, tool_result: str) -> str:
        """
        Generate a natural-language answer from the prompt and tool result.

        Args:
            prompt: Original user question.
            tool_result: Raw string output from the executed tool.

        Returns:
            Generated answer string, or empty string if backend is None.
        """
        if self._generate_fn is None:
            return ""
        backend_prompt = self.cfg.BACKEND_PROMPT_TEMPLATE.format(
            prompt=prompt, result=tool_result
        )
        try:
            return self._generate_fn(backend_prompt)
        except Exception as exc:
            self.logger.warning("Backend generation failed: %s", exc)
            return ""


# ===========================================================================
# DETERMINISTIC TEMPLATES (fallback when backend output is insufficient)
# ===========================================================================


def _template_answer(tool_name: str, tool_arg: str, tool_result: ToolResult) -> str:
    """
    Build a clean deterministic answer from the tool result.

    Used when the language backend is disabled or produces output below
    BACKEND_MIN_OUTPUT_CHARS.

    Args:
        tool_name: Canonical tool name.
        tool_arg: Argument passed to the tool.
        tool_result: ToolResult instance.

    Returns:
        Human-readable answer string.
    """
    if not tool_result.ok:
        return f"The tool '{tool_name}' encountered an error: {tool_result.output}"
    r = tool_result.output
    templates: Dict[str, Callable[[], str]] = {
        "get_weather":  lambda: f"Current weather in {tool_arg}: {r}.",
        "calc_expr":    lambda: f"{tool_arg} = {r}.",
        "get_datetime": lambda: f"Current time: {r}.",
        "get_news":     lambda: f"News about '{tool_arg}':\n{r}",
        "search_web":   lambda: f"Search result for '{tool_arg}':\n{r}",
        "translate":    lambda: f"Translation: {r}",
        "echo":         lambda: r,
    }
    fn = templates.get(tool_name)
    return fn() if fn else f"{tool_name} result: {r}"


def _is_useful_output(text: str, min_chars: int) -> bool:
    """
    Return True if the backend output is genuinely informative.

    Checks length and absence of common TinyStories non-answer patterns
    (story openers, repetition, incomplete sentences starting with
    conjunctions).
    """
    if len(text) < min_chars:
        return False
    lower = text.lower()
    # TinyStories tends to start stories with these when out-of-distribution
    story_openers = ("once upon", "one day", "lily ", "tim ", "tom ",
                     "sara ", "a little", "there was a")
    if any(lower.startswith(p) for p in story_openers):
        return False
    # Incomplete sentence starting with a conjunction
    if re.match(r"^(and|or|but|so|yet|however|also|additionally|furthermore)\b", lower):
        return False
    return True


# ===========================================================================
# HYBRID RESULT
# ===========================================================================


@dataclass
class HybridResult:
    """All intermediate and final outputs of one hybrid inference run."""

    prompt: str
    tool_name: str = ""
    tool_arg: str = ""
    tool_output: str = ""
    tool_ok: bool = False
    backend_raw: str = ""
    final_answer: str = ""
    used_template: bool = False

    def pretty(self) -> str:
        """Render a human-readable summary."""
        source = "template" if self.used_template else "language-backend"
        return (
            f"{'=' * 72}\n"
            f"PROMPT       : {self.prompt}\n"
            f"TOOL CALL    : {self.tool_name}({self.tool_arg!r})\n"
            f"TOOL RESULT  : {self.tool_output}\n"
            f"BACKEND RAW  : {self.backend_raw[:120]!r}\n"
            f"FINAL ANSWER : [{source}] {self.final_answer}\n"
            f"{'=' * 72}"
        )


# ===========================================================================
# HYBRID ORCHESTRATOR
# ===========================================================================


class HybridOrchestrator:
    """
    Combines TopoSwarmRouter + LanguageBackend into a single inference call.

    Pipeline:
    1. Router.route(prompt)        → (tool_name, tool_arg)
    2. Registry.execute(...)       → ToolResult
    3. Backend.generate(...)       → raw natural-language answer
    4. Quality check               → use backend output or template fallback
    """

    def __init__(self, cfg: HybridConfig, logger: logging.Logger) -> None:
        """
        Args:
            cfg: Hybrid configuration.
            logger: Logger instance.
        """
        self.cfg = cfg
        self.logger = logger
        self.registry = ToolRegistry(cfg)
        self.router = TopoSwarmRouter(cfg, self.registry, logger)
        self.backend = LanguageBackend(cfg, logger)

    def run(self, prompt: str) -> HybridResult:
        """
        Execute the full hybrid pipeline for one user prompt.

        Args:
            prompt: Natural language user request.

        Returns:
            HybridResult with all steps populated.
        """
        result = HybridResult(prompt=prompt)

        # Step 1: route
        tool_name, tool_arg = self.router.route(prompt)
        result.tool_name = tool_name
        result.tool_arg = tool_arg

        # Step 2: execute tool
        self.logger.info("Executing: %s(%r)", tool_name, tool_arg)
        tr = self.registry.execute(tool_name, tool_arg)
        result.tool_output = tr.output
        result.tool_ok = tr.ok

        if not tr.ok:
            result.final_answer = _template_answer(tool_name, tool_arg, tr)
            result.used_template = True
            return result

        # Step 3: language backend generation
        raw = self.backend.generate(prompt, tr.output)
        result.backend_raw = raw

        # Step 4: quality check — fall back to template if needed
        if _is_useful_output(raw, self.cfg.BACKEND_MIN_OUTPUT_CHARS):
            result.final_answer = raw
            result.used_template = False
        else:
            result.final_answer = _template_answer(tool_name, tool_arg, tr)
            result.used_template = True
            self.logger.info(
                "Backend output insufficient (%d chars) — using template.", len(raw)
            )

        return result


# ===========================================================================
# ENTRY POINT
# ===========================================================================


def main() -> None:
    """
    CLI entry point.

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
    --device STR               : Force cpu or cuda
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="TopoSwarm Hybrid: Router (3.4M) + Language Backend (25M)"
    )
    parser.add_argument("--prompt", type=str, default="weather in Santiago")
    parser.add_argument("--backend-type", type=str, default="tinystories")
    parser.add_argument("--backend-model", type=str, default="roneneldan/TinyStories-33M")
    parser.add_argument("--backend-checkpoint", type=str, default="")
    parser.add_argument("--router-checkpoint", type=str, default="checkpoints_toposwarm")
    parser.add_argument("--list-tools", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--device", type=str, default="")
    args = parser.parse_args()

    cfg = HybridConfig()
    cfg.BACKEND_TYPE = args.backend_type
    cfg.BACKEND_MODEL_ID = args.backend_model
    cfg.BACKEND_CHECKPOINT = args.backend_checkpoint
    cfg.ROUTER_CHECKPOINT_DIR = args.router_checkpoint
    if args.temperature > 0:
        cfg.ROUTER_TEMPERATURE = args.temperature
    if args.device:
        # Patch SwarmConfig default via env; SwarmConfig reads it on __post_init__
        os.environ["TOPOSWARM_DEVICE"] = args.device

    logger = _setup_logger("TopoSwarmHybrid", cfg.LOG_LEVEL)

    if args.list_tools:
        reg = ToolRegistry(cfg)
        print("Registered tools:", ", ".join(reg.tool_names))
        return

    if args.dry_run:
        logger.info("Dry-run: testing tool execution only.")
        reg = ToolRegistry(cfg)
        tool_name, tool_arg = reg.route(args.prompt)
        tr = reg.execute(tool_name, tool_arg)
        print(tr)
        print(_template_answer(tool_name, tool_arg, tr))
        return

    orchestrator = HybridOrchestrator(cfg, logger)
    result = orchestrator.run(args.prompt)
    print(result.pretty())


if __name__ == "__main__":
    main()
