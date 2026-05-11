"""Tests for dataset enhancer PII sanitizer."""

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import importlib.util


def _load_enhancer_module():
    spec = importlib.util.spec_from_file_location(
        "lazyown_dataset_enhancer",
        _PROJECT_ROOT / "lazyown_dataset_enhancer.py",
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["lazyown_dataset_enhancer"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_sanitize_ip():
    mod = _load_enhancer_module()
    text = "Found host 192.168.1.100 open"
    assert "[REDACTED_IP]" in mod._sanitize_output(text)
    assert "192.168.1.100" not in mod._sanitize_output(text)


def test_sanitize_password():
    mod = _load_enhancer_module()
    text = "password=SuperSecret123"
    assert "[REDACTED]" in mod._sanitize_output(text)
    assert "SuperSecret123" not in mod._sanitize_output(text)


def test_sanitize_ntlm_hash():
    mod = _load_enhancer_module()
    text = "hash is aabbccdd11223344556677889900aabb"
    assert "[REDACTED_HASH]" in mod._sanitize_output(text)


def test_sanitize_email():
    mod = _load_enhancer_module()
    text = "contact admin@corp.local for access"
    assert "[REDACTED_EMAIL]" in mod._sanitize_output(text)


def test_sanitize_idempotent_on_clean_text():
    mod = _load_enhancer_module()
    text = "nmap scan completed on target"
    assert mod._sanitize_output(text) == text
