"""Tests for model configuration defaults."""

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))


def _load_mod():
    pytest = __import__("pytest")
    pytest.importorskip("torch")
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "topo_swarm_agent", _PROJECT_ROOT / "topo_swarm_agent.py"
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["topo_swarm_agent"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_default_scale_is_xl150m():
    mod = _load_mod()
    cfg = mod.SwarmConfig()
    # Default must be the ~150M model.
    assert cfg.SCALE == "xl150m", f"SCALE is {cfg.SCALE!r}, expected 'xl150m'"
    assert cfg.D_MODEL == 1024, f"D_MODEL is {cfg.D_MODEL}, expected 1024"
    assert cfg.N_LAYERS == 12, f"N_LAYERS is {cfg.N_LAYERS}, expected 12"
    assert cfg.D_MODEL % 4 == 0
    assert cfg.D_MODEL % cfg.N_HEADS == 0


def test_micro_preset_compatible_with_legacy_checkpoint():
    mod = _load_mod()
    cfg = mod.SwarmConfig(SCALE="micro")
    # Legacy micro model keeps old dims for existing checkpoints.
    assert cfg.D_MODEL == 64, f"D_MODEL changed to {cfg.D_MODEL}; existing checkpoints will break"
    assert cfg.D_MODEL % 4 == 0
    assert cfg.D_MODEL % cfg.N_HEADS == 0
