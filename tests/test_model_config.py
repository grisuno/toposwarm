"""Tests for model configuration defaults."""

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))


def test_d_model_compatible_with_checkpoint():
    pytest = __import__("pytest")
    pytest.importorskip("torch")
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "topo_swarm_agent", _PROJECT_ROOT / "topo_swarm_agent.py"
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["topo_swarm_agent"] = mod
    spec.loader.exec_module(mod)

    cfg = mod.SwarmConfig()
    # D_MODEL must stay at 64 to remain compatible with existing checkpoints.
    assert cfg.D_MODEL == 64, f"D_MODEL changed to {cfg.D_MODEL}; existing checkpoints will break"
    assert cfg.D_MODEL % 4 == 0
    assert cfg.D_MODEL % cfg.N_HEADS == 0
