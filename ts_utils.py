"""
ts_utils.py — Shared utilities for the TopoSwarm project.

Centralises everything that was copy-pasted across 6 modules:
  - logger factory
  - safe math evaluator
  - cached tokenizer wrappers
  - dynamic module importer
"""
from __future__ import annotations

import ast
import importlib.util
import logging
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Logger
# ---------------------------------------------------------------------------

def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Return an idempotent logger with a single StreamHandler."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    if not logger.handlers:
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(logging.Formatter(
            "%(asctime)s %(name)-22s %(levelname)-8s %(message)s"
        ))
        logger.addHandler(h)
    return logger


# ---------------------------------------------------------------------------
# Safe math evaluator
# ---------------------------------------------------------------------------

def safe_eval(expr: str) -> float:
    """Evaluate a numeric expression via AST — never calls eval() on arbitrary code."""
    _ALLOWED = (
        ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod,
        ast.FloorDiv, ast.UAdd, ast.USub,
    )
    try:
        tree = ast.parse(expr.strip(), mode="eval")
        if not all(isinstance(node, _ALLOWED) for node in ast.walk(tree)):
            return float("nan")
        return float(eval(compile(tree, "<expr>", "eval")))  # noqa: S307
    except Exception:
        return float("nan")


# ---------------------------------------------------------------------------
# Dynamic module importer
# ---------------------------------------------------------------------------

def import_module(name: str, *candidates: Path) -> Any:
    """
    Load a Python file as a named module.

    Tries each candidate path in order; raises FileNotFoundError if none found.
    Pre-registers the module in sys.modules before exec so that @dataclass
    introspection works correctly on Python 3.13+.
    """
    for path in candidates:
        if path.exists():
            spec = importlib.util.spec_from_file_location(name, path)
            mod  = importlib.util.module_from_spec(spec)
            sys.modules[name] = mod          # must happen before exec_module
            spec.loader.exec_module(mod)
            return mod
    raise FileNotFoundError(
        f"Module '{name}' not found. Tried: {[str(p) for p in candidates]}"
    )


# ---------------------------------------------------------------------------
# Cached tokenizer helpers
# ---------------------------------------------------------------------------

def make_cached_encode(tokenizer):
    """
    Return a cached version of tokenizer.encode().

    @lru_cache requires hashable args; str instructions are fine.
    Cache survives the lifetime of the tokenizer object.
    """
    @lru_cache(maxsize=4096)
    def _cached_encode(text: str):
        return tokenizer.encode(text)

    return _cached_encode


def make_cached_tool_token(tokenizer):
    """Return a cached version of tokenizer.tool_token()."""
    @lru_cache(maxsize=512)
    def _cached_tool_token(tool_name: str) -> int:
        return tokenizer.tool_token(tool_name)

    return _cached_tool_token
