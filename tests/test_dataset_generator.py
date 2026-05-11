"""Tests for dataset generator noise filter."""

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import importlib.util


def _load_gen_module():
    spec = importlib.util.spec_from_file_location(
        "lazyown_dataset_generator",
        _PROJECT_ROOT / "lazyown_dataset_generator.py",
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["lazyown_dataset_generator"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_is_noisy_short_instruction():
    mod = _load_gen_module()
    assert mod._is_noisy_phrasing("run command", "") is True
    assert mod._is_noisy_phrasing("scan the target with nmap", "nmap") is False


def test_is_noisy_generic_verb_empty_arg():
    mod = _load_gen_module()
    assert mod._is_noisy_phrasing("Execute a specific LazyOwn command", "") is True
    assert mod._is_noisy_phrasing("Execute lazynmap on target", "lazynmap") is False


def test_is_noisy_permitted_with_arg():
    mod = _load_gen_module()
    # Even if it starts with generic verb, if arg is non-empty it passes
    assert mod._is_noisy_phrasing("Run a full port scan", "lazynmap") is False


def test_build_dataset_filters_noise():
    mod = _load_gen_module()
    records = mod.build_dataset()
    # Ensure no record has empty arg combined with generic verb start
    for r in records:
        instr = r["instruction"]
        arg = r["api_list"][0].get("required_parameters", [{}])[0].get("description", "")
        # Re-construct arg from the answer field if needed
        m = __import__("re").search(r"\[TOOL_CALL:[^\(]+\(([^)]*)\)\]", r["answer"])
        extracted_arg = m.group(1) if m else ""
        assert not mod._is_noisy_phrasing(instr, extracted_arg)
    assert len(records) > 0
