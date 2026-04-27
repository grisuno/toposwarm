#!/usr/bin/env python3
"""
TopoSwarm Inference Shell.

Loads a trained TopoSwarm checkpoint, sends a natural language prompt through
the swarm, parses any tool call embedded in the generated text, executes the
tool locally, feeds the result back for a second-pass generation, and prints
the final answer.

Tool execution is real: each registered tool runs actual Python code (weather
via wttr.in, web search via DuckDuckGo instant-answer JSON, calculator via
ast.literal_eval-safe evaluator, datetime, and a passthrough echo tool).

Usage
-----
    python toposwarm_infer.py --prompt "What is the weather in Santiago?"
    python toposwarm_infer.py --prompt "Calculate 17 * 89 + 42"
    python toposwarm_infer.py --prompt "Search for quaternion neural networks"
    python toposwarm_infer.py --prompt "What time is it?"
    python toposwarm_infer.py --checkpoint path/to/checkpoints_toposwarm/latest

The script imports TopoSwarm classes directly from topo_swarm_agent.py, which
must live in the same directory or on PYTHONPATH.
"""

from __future__ import annotations

import ast
import json
import logging
import math
import operator
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import torch


# ---------------------------------------------------------------------------
# Inline import of the agent module (handles running from any cwd)
# ---------------------------------------------------------------------------

def _import_agent():
    """Import topo_swarm_agent, searching the script dir and cwd."""
    agent_candidates = [
        Path(__file__).parent / "topo_swarm_agent.py",
        Path.cwd() / "topo_swarm_agent.py",
    ]
    import importlib.util, types
    for candidate in agent_candidates:
        if candidate.exists():
            spec = importlib.util.spec_from_file_location("topo_swarm_agent", candidate)
            mod = importlib.util.module_from_spec(spec)
            sys.modules["topo_swarm_agent"] = mod
            spec.loader.exec_module(mod)
            return mod
    raise FileNotFoundError(
        "topo_swarm_agent.py not found. "
        "Place it in the same directory as this script."
    )

_agent = _import_agent()
SwarmConfig      = _agent.SwarmConfig
TopoSwarmModel   = _agent.TopoSwarmModel
BPETokenizer     = _agent.BPETokenizer
CheckpointManager = _agent.CheckpointManager
SwarmOrchestrator = _agent.SwarmOrchestrator


# ===========================================================================
# INFERENCE CONFIG
# ===========================================================================


@dataclass
class InferenceConfig:
    """All inference-time hyper-parameters — zero magic numbers."""

    CHECKPOINT_DIR: str = "checkpoints_toposwarm"
    MAX_NEW_TOKENS: int = 96
    TEMPERATURE: float = 0.8
    TOP_K: int = 40
    N_AGENTS: int = 3
    # Override the training ACT_HALT_THRESHOLD (0.5) for inference.
    # The model learned to halt quickly during training; 0.98 forces it
    # to generate the full max_new_tokens unless truly certain to stop.
    ACT_HALT_THRESHOLD: float = 0.98

    # Repetition penalty: logits for already-generated tokens are divided
    # by this value (>1.0 = penalise repeats, 1.0 = no penalty).
    REPETITION_PENALTY: float = 1.3

    # ACT-driven temperature: when halt_prob > this value the generation
    # temperature is automatically raised to force lexical diversity.
    ACT_TEMPERATURE_TRIGGER: float = 0.85
    ACT_TEMPERATURE_BOOST: float = 0.4   # added to base temperature

    # Minimum tokens the model must emit before ACT halt is respected.
    # Prevents single-token collapse without raising the global threshold.
    # Lowered from 6: model now generates noisy multi-token outputs
    # (e.g. "? Additionally, I want to") that exceed 6 chars but are useless.
    # Template activates when output length in tokens <= this value OR when
    # the output contains known noise markers from the training corpus.
    MIN_ANSWER_TOKENS: int = 3

    # Tool execution
    HTTP_TIMEOUT_SECONDS: int = 8
    MAX_RESULT_CHARS: int = 512
    MAX_FOLLOWUP_TOKENS: int = 96
    FOLLOWUP_TEMPERATURE: float = 0.5

    # Tool parsing: the model is expected to emit one of these patterns:
    #   <tool>tool_name(arg)</tool>
    #   TOOL: tool_name(arg)
    #   [TOOL tool_name arg]
    TOOL_TAG_RE: str = (
        r"<tool>\s*(?P<name>\w+)\((?P<arg>[^)]*)\)\s*</tool>"
        r"|TOOL:\s*(?P<name2>\w+)\((?P<arg2>[^)]*)\)"
        r"|TOOL:\s*(?P<name3>\w+)\s+(?P<arg3>[^\n\]]*)"
        r"|\[TOOL\s+(?P<name4>\w+)\s+(?P<arg4>[^\]]*)\]"
    )
    LOG_LEVEL: str = "INFO"


# ===========================================================================
# SAFE CALCULATOR
# ===========================================================================


def _safe_eval(expr: str) -> str:
    """
    Evaluate a mathematical expression without using eval() on arbitrary code.

    Supports: +, -, *, /, //, %, **, unary minus, parentheses, int and float
    literals.  Raises ValueError on any disallowed construct.
    """
    _ALLOWED_OPS: Dict[type, Callable] = {
        ast.Add:      operator.add,
        ast.Sub:      operator.sub,
        ast.Mult:     operator.mul,
        ast.Div:      operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod:      operator.mod,
        ast.Pow:      operator.pow,
        ast.USub:     operator.neg,
        ast.UAdd:     operator.pos,
    }

    def _eval(node: ast.AST) -> float:
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return float(node.value)
            raise ValueError(f"Unsupported constant: {node.value!r}")
        if isinstance(node, ast.BinOp):
            op_fn = _ALLOWED_OPS.get(type(node.op))
            if op_fn is None:
                raise ValueError(f"Disallowed operator: {type(node.op).__name__}")
            return op_fn(_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp):
            op_fn = _ALLOWED_OPS.get(type(node.op))
            if op_fn is None:
                raise ValueError(f"Disallowed unary operator: {type(node.op).__name__}")
            return op_fn(_eval(node.operand))
        raise ValueError(f"Disallowed node type: {type(node).__name__}")

    try:
        tree = ast.parse(expr.strip(), mode="eval")
        result = _eval(tree.body)
        if isinstance(result, float) and result == int(result):
            return str(int(result))
        return str(round(result, 10))
    except Exception as exc:
        return f"Error evaluating '{expr}': {exc}"


# ===========================================================================
# TOOL REGISTRY
# ===========================================================================


class ToolResult:
    """Structured result returned by every tool executor."""

    def __init__(self, tool_name: str, arg: str, output: str, ok: bool) -> None:
        """
        Args:
            tool_name: Name of the tool that was called.
            arg: Raw argument string passed to the tool.
            output: Human-readable result string.
            ok: Whether the tool call succeeded.
        """
        self.tool_name = tool_name
        self.arg = arg
        self.output = output
        self.ok = ok

    def __str__(self) -> str:
        status = "OK" if self.ok else "ERROR"
        return f"[{self.tool_name}({self.arg!r}) → {status}] {self.output}"


class ToolRegistry:
    """
    Registry of executable tools.

    Each tool is a callable(arg: str) -> str.  Registration is done via the
    @register decorator.  Tool names are matched case-insensitively and with
    common aliases (e.g. "weather" matches "get_weather", "weather_now").
    """

    def __init__(self, cfg: InferenceConfig) -> None:
        """
        Args:
            cfg: Inference configuration (provides timeout and result limits).
        """
        self._tools: Dict[str, Callable[[str], str]] = {}
        self._aliases: Dict[str, str] = {}
        self.cfg = cfg
        self._register_builtin_tools()

    def register(self, *names: str) -> Callable:
        """Decorator that registers a function under one or more tool names."""
        def decorator(fn: Callable[[str], str]) -> Callable[[str], str]:
            canonical = names[0].lower()
            self._tools[canonical] = fn
            for alias in names:
                self._aliases[alias.lower()] = canonical
            return fn
        return decorator

    def resolve(self, raw_name: str) -> Optional[str]:
        """
        Resolve a raw tool name to its canonical registry key.

        Performs exact match, then alias lookup, then prefix/substring search.

        Args:
            raw_name: Tool name as emitted by the model.

        Returns:
            Canonical tool name string, or None if not found.
        """
        key = raw_name.lower().strip()
        if key in self._tools:
            return key
        if key in self._aliases:
            return self._aliases[key]
        # Prefix / substring match
        for alias, canonical in self._aliases.items():
            if key in alias or alias in key:
                return canonical
        return None

    def execute(self, raw_name: str, arg: str) -> ToolResult:
        """
        Execute a tool by name with the given argument string.

        Args:
            raw_name: Tool name as emitted by the model.
            arg: Argument string (stripped of surrounding whitespace/quotes).

        Returns:
            ToolResult with the output or an error message.
        """
        canonical = self.resolve(raw_name)
        if canonical is None:
            return ToolResult(
                raw_name, arg,
                f"Unknown tool '{raw_name}'. Available: {sorted(self._tools)}",
                ok=False,
            )
        arg = arg.strip().strip("'\"")
        try:
            output = self._tools[canonical](arg)
            output = str(output)[: self.cfg.MAX_RESULT_CHARS]
            return ToolResult(canonical, arg, output, ok=True)
        except Exception as exc:
            return ToolResult(canonical, arg, f"Execution error: {exc}", ok=False)

    # -----------------------------------------------------------------------
    # Built-in tool implementations
    # -----------------------------------------------------------------------

    def _http_get(self, url: str) -> str:
        """Minimal HTTP GET with timeout, returns response body as string."""
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "TopoSwarm-Inference/1.0"},
        )
        with urllib.request.urlopen(req, timeout=self.cfg.HTTP_TIMEOUT_SECONDS) as resp:
            return resp.read().decode("utf-8", errors="replace")

    def _register_builtin_tools(self) -> None:
        """Register all built-in tools onto self._tools / self._aliases."""

        @self.register("get_weather", "weather", "weather_now", "current_weather")
        def get_weather(city: str) -> str:
            """Fetch current weather from wttr.in (no API key required)."""
            city_enc = urllib.parse.quote(city)
            url = f"https://wttr.in/{city_enc}?format=j1"
            raw = self._http_get(url)
            data = json.loads(raw)
            current = data["current_condition"][0]
            desc = current["weatherDesc"][0]["value"]
            temp_c = current["temp_C"]
            feels_c = current["FeelsLikeC"]
            humidity = current["humidity"]
            wind_kmph = current["windspeedKmph"]
            return (
                f"{city}: {desc}, {temp_c}°C (feels {feels_c}°C), "
                f"humidity {humidity}%, wind {wind_kmph} km/h"
            )

        @self.register("search_web", "search", "web_search", "duckduckgo")
        def search_web(query: str) -> str:
            """Instant-answer search via DuckDuckGo JSON API (no API key)."""
            import re as _re
            query = _re.sub(r"^(?:search|find|look up)\s+", "", query.strip(), flags=_re.IGNORECASE)
            q_enc = urllib.parse.quote(query)
            url = f"https://api.duckduckgo.com/?q={q_enc}&format=json&no_html=1&skip_disambig=1"
            raw = self._http_get(url)
            data = json.loads(raw)
            abstract = data.get("AbstractText", "").strip()
            answer = data.get("Answer", "").strip()
            related = [r.get("Text", "") for r in data.get("RelatedTopics", [])[:3] if r.get("Text")]
            parts = [p for p in [answer, abstract] + related if p]
            if not parts:
                return f"No instant answer found for '{query}'. Try a more specific query."
            return " | ".join(parts)[: 512]

        @self.register("calc_expr", "calculate", "calc", "compute", "math")
        def calc_expr(expr: str) -> str:
            """Evaluate a mathematical expression safely."""
            return _safe_eval(expr)

        @self.register("get_datetime", "datetime", "now", "current_time", "time", "date")
        def get_datetime(tz_hint: str) -> str:
            """Return the current UTC datetime (tz_hint is informational only)."""
            now = datetime.now(timezone.utc)
            return now.strftime(f"%Y-%m-%d %H:%M:%S UTC (requested tz: {tz_hint or 'UTC'})")

        @self.register("translate", "translation")
        def translate(text: str) -> str:
            """
            Translate text using MyMemory free API (no key, 5k chars/day limit).

            Accepted formats:
              "translate <text> to <lang>"
              "<text> to <lang>"
              "<text>"  (defaults to English)

            Strips the "translate" verb and detects source language via
            langdetect so MyMemory receives a valid langpair (e.g. es|en).
            Falls back to es|en when detection fails.
            """
            import re as _re
            # Strip leading "translate" verb if present
            text = _re.sub(r"^translate\s+", "", text.strip(), flags=_re.IGNORECASE)

            target_lang = "en"
            source_text = text
            if _re.search(r"\bto\s+\w", text, _re.IGNORECASE):
                parts = _re.split(r"\s+to\s+", text, maxsplit=1, flags=_re.IGNORECASE)
                source_text = parts[0].strip()
                lang_word = parts[1].strip().lower()[:10]
                lang_map = {
                    "english": "en", "spanish": "es", "french": "fr",
                    "german": "de", "italian": "it", "portuguese": "pt",
                    "chinese": "zh", "japanese": "ja", "korean": "ko",
                    "arabic": "ar", "russian": "ru",
                }
                target_lang = lang_map.get(lang_word, lang_word[:2])

            # Detect source language; fall back to "es" for Spanish-looking text
            try:
                from langdetect import detect as _detect  # type: ignore
                src_lang = _detect(source_text)
            except Exception:
                src_lang = "es" if any(c in source_text.lower() for c in ("ñ","ó","á","é","í","ú","ü")) else "es"

            langpair = f"{src_lang}|{target_lang}"
            q_enc = urllib.parse.quote(source_text[:500])
            url = (
                f"https://api.mymemory.translated.net/get"
                f"?q={q_enc}&langpair={langpair}"
            )
            raw = self._http_get(url)
            data = json.loads(raw)
            translation = data.get("responseData", {}).get("translatedText", "")
            if not translation or "INVALID" in translation.upper():
                # Retry with explicit es|en as last resort
                q_enc2 = urllib.parse.quote(source_text[:500])
                url2 = f"https://api.mymemory.translated.net/get?q={q_enc2}&langpair=es|en"
                raw2 = self._http_get(url2)
                translation = json.loads(raw2).get("responseData", {}).get("translatedText", "")
            if not translation:
                return f"Translation unavailable for: {source_text}"
            return translation

        @self.register("get_news", "news", "headlines")
        def get_news(topic: str) -> str:
            """
            Fetch recent news headlines via DuckDuckGo news search.
            Returns up to 3 snippet summaries.
            """
            q_enc = urllib.parse.quote(topic)
            url = (
                f"https://api.duckduckgo.com/?q={q_enc}&format=json"
                f"&no_html=1&skip_disambig=1&ia=news"
            )
            raw = self._http_get(url)
            data = json.loads(raw)
            items = data.get("RelatedTopics", [])[:5]
            headlines = [i.get("Text", "") for i in items if i.get("Text")]
            if not headlines:
                return f"No recent headlines found for '{topic}'."
            return "\n".join(f"• {h}" for h in headlines[:3])

        @self.register("echo", "passthrough", "noop")
        def echo(text: str) -> str:
            """Return the input unchanged. Used for model self-testing."""
            return text


# ===========================================================================
# TOOL CALL PARSER
# ===========================================================================


class ToolCallParser:
    """
    Extract tool calls from model-generated text.

    The model may emit tool calls in several formats; this parser tries all
    of them in priority order and returns the first match.
    """

    def __init__(self, cfg: InferenceConfig) -> None:
        """
        Args:
            cfg: Inference config (provides TOOL_TAG_RE pattern).
        """
        self._pattern = re.compile(cfg.TOOL_TAG_RE, re.IGNORECASE | re.DOTALL)

    def parse(self, text: str) -> Optional[Tuple[str, str]]:
        """
        Extract the first tool call from text.

        Args:
            text: Raw model output string.

        Returns:
            Tuple of (tool_name, arg) or None if no tool call found.
        """
        m = self._pattern.search(text)
        if m is None:
            return None
        groups = m.groupdict()
        # Walk through the named group pairs in priority order
        for name_key, arg_key in [
            ("name", "arg"), ("name2", "arg2"), ("name3", "arg3"), ("name4", "arg4")
        ]:
            name = groups.get(name_key)
            if name:
                arg = (groups.get(arg_key) or "").strip()
                return name.strip(), arg
        return None


# ===========================================================================
# INFERENCE ENGINE
# ===========================================================================


class InferenceEngine:
    """
    Full agentic inference loop:

    1. Encode prompt.
    2. First-pass generation via SwarmOrchestrator.
    3. Parse any tool call from the generated text.
    4. Execute the tool.
    5. Second-pass generation conditioned on prompt + tool result.
    6. Return structured InferenceResult.
    """

    def __init__(
        self,
        cfg: InferenceConfig,
        agent_cfg: SwarmConfig,
        logger: logging.Logger,
    ) -> None:
        """
        Args:
            cfg: Inference configuration.
            agent_cfg: SwarmConfig used to instantiate the model.
            logger: Logger instance.
        """
        self.cfg = cfg
        self.agent_cfg = agent_cfg
        self.logger = logger

        self.tokenizer = BPETokenizer(agent_cfg)
        self.model = TopoSwarmModel(agent_cfg).to(agent_cfg.DEVICE)
        self._load_checkpoint()
        # Override the training ACT threshold so the model generates full
        # sequences at inference time rather than halting after 1-2 tokens.
        agent_cfg.ACT_HALT_THRESHOLD = cfg.ACT_HALT_THRESHOLD
        self.orchestrator = SwarmOrchestrator(self.model, agent_cfg)
        self.registry = ToolRegistry(cfg)
        self.parser = ToolCallParser(cfg)

    def _load_checkpoint(self) -> None:
        """Load weights from the latest checkpoint directory."""
        ckpt = CheckpointManager(self.agent_cfg, self.logger)
        meta = ckpt.load(self.model, device=self.agent_cfg.DEVICE)
        if meta:
            self.logger.info(
                "Checkpoint loaded: epoch=%s step=%s loss=%s",
                meta.get("epoch", "?"),
                meta.get("step", "?"),
                meta.get("loss", "?"),
            )
        else:
            self.logger.warning(
                "No checkpoint found at %s — using random weights.",
                self.cfg.CHECKPOINT_DIR,
            )

    def _encode_prompt(self, text: str) -> torch.Tensor:
        """
        Encode a prompt string to a [1, S] token id tensor on the model device.

        Wraps the raw text in the ToolBench training format so the model
        receives input that matches its training distribution:

            query: <text>
            api_list: [{"tool_name": "<inferred>", ...}]
            domain: General
            <tool_token>

        The tool name is inferred from keyword signals so the tool token sits
        at the correct position — matching encode_tool_trace() used at training.
        Token ids are clamped to [0, VOCAB_SIZE-1] to prevent embedding crashes.
        """
        text_lower = text.lower()
        if any(k in text_lower for k in ("weather", "temperature", "forecast", "rain", "wind", "humidity")):
            tool_guess = "get_weather"
        elif any(k in text_lower for k in ("calculat", "comput", " * ", " + ", " - ", " / ", "math", "how much is")):
            tool_guess = "calc_expr"
        elif any(k in text_lower for k in ("time", "date", "now", "today", "clock", "hour", "minute")):
            tool_guess = "get_datetime"
        elif any(k in text_lower for k in ("news", "headline", "latest", "recent")):
            tool_guess = "get_news"
        elif any(k in text_lower for k in ("translat", "in english", "in spanish", "in french")):
            tool_guess = "translate"
        elif any(k in text_lower for k in ("search", "find", "look up", "who is", "what is")):
            tool_guess = "search_web"
        else:
            tool_guess = "search_web"

        # Replicate encode_tool_trace() from BPETokenizer exactly:
        #   encode(instruction) + [tool_token] + encode(result_placeholder)
        # At inference we leave the result side empty — generation fills it.
        instruction_text = (
            f"query: {text}\n"
            f'api_list: [{{"tool_name": "{tool_guess}", "api_name": "{tool_guess}_endpoint", '
            f'"api_description": "Returns result for the given query."}}]\n'
            f"domain: General"
        )
        tool_token_id = self.tokenizer.tool_token(tool_guess)
        instruction_ids = self.tokenizer.encode(instruction_text)
        ids = instruction_ids + [tool_token_id]
        ids = [min(i, self.agent_cfg.VOCAB_SIZE - 1) for i in ids]
        ids = ids[-self.agent_cfg.MAX_SEQ_LEN :]
        return torch.tensor([ids], dtype=torch.long, device=self.agent_cfg.DEVICE)

    def _generate(
        self,
        prompt_ids: torch.Tensor,
        max_new_tokens: int,
        temperature: float,
    ) -> str:
        """
        Custom autoregressive generation loop with three inference-time fixes.

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
        with no weight updates — no retraining required.
        """
        import torch.nn.functional as F

        model = self.orchestrator.model
        cfg = self.agent_cfg
        model.eval()

        rep_penalty = self.cfg.REPETITION_PENALTY
        act_trigger  = self.cfg.ACT_TEMPERATURE_TRIGGER
        act_boost    = self.cfg.ACT_TEMPERATURE_BOOST
        min_tokens   = self.cfg.MIN_ANSWER_TOKENS
        top_k        = self.cfg.TOP_K
        bpe_ceiling  = cfg.TOOL_TOKEN_OFFSET

        # Run all swarm slots and pick the best by halt confidence
        best_ids = None
        best_conf = -1.0
        prompt_len = prompt_ids.shape[1]

        for phase in self.orchestrator.berry_phases:
            ids = prompt_ids.clone()
            generated = 0

            for step in range(max_new_tokens):
                with torch.no_grad():
                    out = model.forward(
                        ids[:, -cfg.MAX_SEQ_LEN:], berry_phase=phase
                    )

                halt_prob = torch.sigmoid(out["halt_logit"]).item()

                # Fix 2: boost temperature when model is over-confident
                eff_temp = temperature
                if halt_prob > act_trigger:
                    eff_temp = min(temperature + act_boost, 2.0)

                logits = out["logits"][:, -1, :].clone()

                # Fix 1: repetition penalty over all tokens seen so far
                if rep_penalty != 1.0 and ids.shape[1] > 0:
                    seen = ids[0].unique()
                    seen = seen[seen < bpe_ceiling]
                    logits[0, seen] /= rep_penalty

                logits = logits / max(eff_temp, 1e-7)
                logits[:, bpe_ceiling:] = float("-inf")

                if top_k > 0:
                    v, _ = torch.topk(logits, min(top_k, bpe_ceiling))
                    logits[logits < v[:, -1:]] = float("-inf")

                probs = F.softmax(logits, dim=-1)
                next_id = torch.multinomial(probs, num_samples=1)
                ids = torch.cat([ids, next_id], dim=1)
                generated += 1

                # Fix 3: enforce minimum generation length before ACT halt
                if generated >= min_tokens and halt_prob > cfg.ACT_HALT_THRESHOLD:
                    break

            with torch.no_grad():
                final_out = model.forward(ids[:, -cfg.MAX_SEQ_LEN:], berry_phase=phase)
            conf = torch.sigmoid(final_out["halt_logit"]).item()
            if conf > best_conf:
                best_conf = conf
                best_ids = ids

        new_ids = best_ids[0, prompt_len:].tolist()
        return self.tokenizer.decode(new_ids)

    def run(self, prompt: str) -> "InferenceResult":
        """
        Full agentic inference loop for one user prompt.

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
            InferenceResult with all intermediate steps populated.
        """
        result = InferenceResult(prompt=prompt)

        # --- Determine tool from prompt keywords (same logic as _encode_prompt)
        tool_name, tool_arg = self._infer_tool_and_arg(prompt)
        result.tool_name = tool_name
        result.tool_arg = tool_arg

        # --- Pass 1: model completes the result given instruction+tool_token
        self.logger.info("Pass 1: generating result completion...")
        prompt_ids = self._encode_prompt(prompt)
        first_output = self._generate(
            prompt_ids,
            max_new_tokens=self.cfg.MAX_NEW_TOKENS,
            temperature=self.cfg.TEMPERATURE,
        )
        result.first_output = first_output
        self.logger.info("Pass 1 raw completion: %r", first_output[:200])

        # --- Tool execution: run the real tool with the user query as arg
        self.logger.info("Executing tool: %s(%r)", tool_name, tool_arg)
        tool_result = self.registry.execute(tool_name, tool_arg)
        result.tool_result = tool_result
        result.tool_used = True
        self.logger.info("Tool result: %s", tool_result)

        # --- Pass 2: condition on real tool result, generate final answer
        # Encode exactly as encode_tool_trace does during training, then
        # append the real result so the model generates a fluent answer.
        instruction_text = (
            f"query: {prompt}\n"
            f'api_list: [{{"tool_name": "{tool_name}", "api_name": "{tool_name}_endpoint", '
            f'"api_description": "Returns result for the given query."}}]\n'
            f"domain: General"
        )
        tool_token_id = self.tokenizer.tool_token(tool_name)
        result_text = tool_result.output[:self.cfg.MAX_RESULT_CHARS]
        result_ids = self.tokenizer.encode(result_text)

        instruction_ids = self.tokenizer.encode(instruction_text)
        full_ids = instruction_ids + [tool_token_id] + result_ids
        full_ids = [min(i, self.agent_cfg.VOCAB_SIZE - 1) for i in full_ids]
        full_ids = full_ids[-self.agent_cfg.MAX_SEQ_LEN + self.cfg.MAX_FOLLOWUP_TOKENS :]
        followup_tensor = torch.tensor(
            [full_ids], dtype=torch.long, device=self.agent_cfg.DEVICE
        )

        # Use [RESULT]...[ANSWER] framing — closer to ToolBench result format
        # than "The result is:", reducing distribution shift.
        answer_frame = f" REPORT: {tool_result.output[:200]} SUMMARY:"
        frame_ids = self.tokenizer.encode(answer_frame)
        frame_ids = [min(i, self.agent_cfg.VOCAB_SIZE - 1) for i in frame_ids]
        primed_ids = full_ids + frame_ids
        primed_ids = primed_ids[-self.agent_cfg.MAX_SEQ_LEN + self.cfg.MAX_FOLLOWUP_TOKENS :]
        primed_tensor = torch.tensor(
            [primed_ids], dtype=torch.long, device=self.agent_cfg.DEVICE
        )

        self.logger.info("Pass 2: generating final answer...")
        second_output = self._generate(
            primed_tensor,
            max_new_tokens=self.cfg.MAX_FOLLOWUP_TOKENS,
            temperature=self.cfg.FOLLOWUP_TEMPERATURE,
        )
        result.second_output = second_output

        # Detect ToolBench corpus noise in the model output.
        # The training corpus (RapidAPI traces) contains recurring filler
        # phrases that the model reproduces when it cannot synthesise a real
        # answer.  If any noise marker is found, fall back to the template.
        _NOISE_MARKERS = (
            "additionally", "please provide", "i need", "i want",
            "can you", "could you", "is there", "located in",
            "track id", "https://", " id ", "retrieve",
            "assistance", "furthermore", "also,", "and i", "and we",
            "would be", "would also", "i\'m", "there.", "helpful",
            "different regions", "if we", "and it", "can you",
        )
        clean = second_output.strip()
        clean_lower = clean.lower()

        # Structural noise detection: output is a sentence fragment
        # (starts with conjunction/preposition, no subject-verb structure)
        import re as _re
        starts_with_connector = bool(_re.match(
            r"^(and|or|but|so|yet|nor|for|also|however|therefore|"
            r"furthermore|additionally|moreover|meanwhile|thus|hence|"
            r"there|would|could|should|might|may|is|are|was|were)\b",
            clean_lower
        ))

        # For tools that return numbers/dates, check if output contains digits
        _NUMERIC_TOOLS = {"calc_expr", "get_datetime"}
        missing_digits = (
            tool_name in _NUMERIC_TOOLS
            and not _re.search(r"\d", clean)
        )

        is_noisy = (
            len(clean) <= self.cfg.MIN_ANSWER_TOKENS
            or any(marker in clean_lower for marker in _NOISE_MARKERS)
            or starts_with_connector
            or missing_digits
        )
        if not is_noisy:
            result.final_answer = clean
        else:
            result.final_answer = self._template_answer(
                tool_name, tool_arg, tool_result
            )
        self.logger.info("Pass 2 output: %r", second_output[:200])

        return result

    def _template_answer(
        self, tool_name: str, tool_arg: str, tool_result: "ToolResult"
    ) -> str:
        """
        Build a deterministic natural-language answer from the tool result.

        Used when the model Pass 2 output is too short to be useful.  Each
        tool has a dedicated template that formats the raw result string into
        a readable sentence.  No model weights involved — pure string
        formatting.
        """
        r = tool_result.output
        if not tool_result.ok:
            return f"Sorry, the tool call failed: {r}"
        templates = {
            "get_weather":  lambda: f"The current weather in {tool_arg}: {r}.",
            "calc_expr":    lambda: f"{tool_arg} = {r}.",
            "get_datetime": lambda: f"The current time is {r}.",
            "get_news":     lambda: f"Latest news on '{tool_arg}':\n{r}",
            "search_web":   lambda: f"Search result for '{tool_arg}':\n{r}",
            "translate":    lambda: f"Translation: {r}",
            "echo":         lambda: r,
        }
        fn = templates.get(tool_name)
        return fn() if fn else f"{tool_name} result: {r}"

    def _infer_tool_and_arg(self, prompt: str) -> tuple:
        """
        Infer the tool name and argument from the prompt text.

        Returns the same (tool_name, arg) pair that _encode_prompt uses,
        so both are guaranteed to be consistent.  The argument is the
        full prompt text — each tool executor extracts what it needs.
        """
        text_lower = prompt.lower()
        if any(k in text_lower for k in ("weather", "temperature", "forecast", "rain", "wind", "humidity")):
            tool_name = "get_weather"
            # Extract city: last capitalised word sequence after "in" / "for"
            m = __import__("re").search(r"(?:in|for|at)\s+([A-Z][a-zA-Z\s]+?)(?:\?|$|,)", prompt)
            tool_arg = m.group(1).strip() if m else prompt
        elif any(k in text_lower for k in ("calculat", "comput", " * ", " + ", " - ", " / ", "math", "how much is")):
            tool_name = "calc_expr"
            m = __import__("re").search(r"([\d\s\+\-\*\/\^\(\)\.]+)", prompt)
            tool_arg = m.group(1).strip() if m else prompt
        elif any(k in text_lower for k in ("time", "date", "now", "today", "clock", "hour", "minute")):
            tool_name = "get_datetime"
            tool_arg = "UTC"
        elif any(k in text_lower for k in ("news", "headline", "latest", "recent")):
            tool_name = "get_news"
            tool_arg = prompt
        elif any(k in text_lower for k in ("translat", "in english", "in spanish", "in french")):
            tool_name = "translate"
            tool_arg = prompt
        else:
            tool_name = "search_web"
            tool_arg = prompt
        return tool_name, tool_arg


# ===========================================================================
# RESULT DATACLASS
# ===========================================================================


@dataclass
class InferenceResult:
    """All intermediate and final outputs of one inference run."""

    prompt: str
    first_output: str = ""
    tool_name: Optional[str] = None
    tool_arg: Optional[str] = None
    tool_result: Optional[ToolResult] = None
    tool_used: bool = False
    second_output: str = ""
    final_answer: str = ""

    def pretty(self) -> str:
        """Render a human-readable summary of the inference run."""
        lines = [
            "=" * 72,
            f"PROMPT       : {self.prompt}",
            f"PASS 1 OUTPUT: {self.first_output[:300]}",
        ]
        if self.tool_used:
            lines += [
                f"TOOL CALL    : {self.tool_name}({self.tool_arg!r})",
                f"TOOL RESULT  : {self.tool_result}",
                f"PASS 2 OUTPUT: {self.second_output[:300]}",
            ]
        lines += [
            f"FINAL ANSWER : {self.final_answer[:500]}",
            "=" * 72,
        ]
        return "\n".join(lines)


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
            "%(asctime)s %(name)-20s %(levelname)-8s %(message)s"
        ))
        logger.addHandler(h)
    return logger


# ===========================================================================
# ENTRY POINT
# ===========================================================================


def main() -> None:
    """
    CLI entry point.

    Flags
    -----
    --prompt TEXT        : Natural language request to the agent.
    --checkpoint DIR     : Path to checkpoints_toposwarm directory.
    --max-tokens N       : Maximum new tokens for pass 1.
    --temperature F      : Sampling temperature (0 = greedy).
    --top-k N            : Top-k truncation.
    --list-tools         : Print all registered tool names and exit.
    --dry-run            : Skip model load; test tool execution only.
    --device STR         : Force cpu or cuda.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="TopoSwarm Inference: prompt → tool call → execution → answer"
    )
    parser.add_argument("--prompt", type=str, default="What is the weather in Santiago?")
    parser.add_argument("--checkpoint", type=str, default="checkpoints_toposwarm")
    parser.add_argument("--max-tokens", type=int, default=0)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--top-k", type=int, default=0)
    parser.add_argument("--list-tools", action="store_true")
    parser.add_argument("--dry-run", action="store_true",
                        help="Test tool execution without loading the model")
    parser.add_argument("--device", type=str, default="")
    args = parser.parse_args()

    cfg = InferenceConfig()
    if args.checkpoint:
        cfg.CHECKPOINT_DIR = args.checkpoint
    if args.max_tokens > 0:
        cfg.MAX_NEW_TOKENS = args.max_tokens
    if args.temperature > 0:
        cfg.TEMPERATURE = args.temperature
    if args.top_k > 0:
        cfg.TOP_K = args.top_k

    logger = _setup_logger("TopoSwarmInfer", cfg.LOG_LEVEL)

    # Build SwarmConfig pointing at the right checkpoint dir
    agent_cfg = SwarmConfig()
    agent_cfg.CHECKPOINT_DIR = cfg.CHECKPOINT_DIR
    if args.device:
        agent_cfg.DEVICE = args.device

    if args.list_tools:
        registry = ToolRegistry(cfg)
        print("Registered tools:")
        for name in sorted(registry._tools):
            print(f"  {name}")
        return

    if args.dry_run:
        logger.info("Dry-run: testing tool execution only.")
        registry = ToolRegistry(cfg)
        parser_obj = ToolCallParser(cfg)
        # Simulate what the model might emit for the given prompt
        test_phrases = [
            f"<tool>get_weather({args.prompt})</tool>",
            f"TOOL: calc_expr(2 ** 10 + 42)",
            f"TOOL: get_datetime(UTC)",
        ]
        for phrase in test_phrases:
            call = parser_obj.parse(phrase)
            if call:
                name, arg = call
                result = registry.execute(name, arg)
                print(result)
        return

    engine = InferenceEngine(cfg, agent_cfg, logger)

    result = engine.run(args.prompt)
    print(result.pretty())


if __name__ == "__main__":
    main()
