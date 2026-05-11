"""Tests for LazyOwn orchestrator improvements."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure project root is on path
_PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))


class TestSessionContext:
    """Unit tests for the multi-turn SessionContext."""

    def _load_ctx(self):
        # Import inside test so torch-heavy top-levels are deferred
        from toposwarm_lazyown_orchestrator import SessionContext
        return SessionContext

    def test_empty_prefix(self):
        Ctx = self._load_ctx()
        ctx = Ctx()
        assert ctx.to_prompt_prefix() == ""

    def test_prefix_with_target(self):
        Ctx = self._load_ctx()
        ctx = Ctx(target_ip="10.10.11.78")
        prefix = ctx.to_prompt_prefix()
        assert "Target: 10.10.11.78" in prefix
        assert "Phase: recon" in prefix

    def test_update_extracts_ip(self):
        Ctx = self._load_ctx()
        ctx = Ctx()
        ctx.update("lazyown_add_target", "10.10.11.50", "ok", True)
        assert ctx.target_ip == "10.10.11.50"
        assert ctx.last_tool == "lazyown_add_target"
        assert ctx.turn_count == 1

    def test_phase_progression(self):
        Ctx = self._load_ctx()
        ctx = Ctx()
        ctx.update("lazyown_run_command", "lazynmap", "open ports found", True)
        assert ctx.current_phase == "exploit"

    def test_findings_from_output(self):
        Ctx = self._load_ctx()
        ctx = Ctx()
        ctx.update("lazyown_run_command", "", "password is secret123", True)
        assert any("credentials" in f for f in ctx.findings)


class TestKeywordRouter:
    """Tests for the deterministic keyword fallback router."""

    def _load_router(self):
        from toposwarm_lazyown_orchestrator import infer_lazyown_tool, _extract_arg
        return infer_lazyown_tool, _extract_arg

    def test_recon_keyword(self):
        infer, _ = self._load_router()
        tool, arg = infer("scan 10.10.11.78 for open ports")
        assert tool == "lazyown_run_command"
        assert "10.10.11.78" in arg

    def test_config_keyword(self):
        infer, _ = self._load_router()
        tool, arg = infer("show the current configuration")
        assert tool == "lazyown_get_config"

    def test_c2_keyword(self):
        infer, _ = self._load_router()
        tool, arg = infer("list active beacons")
        assert tool == "lazyown_get_beacons"

    def test_fallback_search(self):
        infer, _ = self._load_router()
        tool, arg = infer("something completely unrelated to pentesting")
        assert tool == "lazyown_c2_search_agent"

    def test_extract_arg_ip(self):
        _, extract = self._load_router()
        assert "10.0.0.1" in extract("set rhost 10.0.0.1", "lazyown_set_config")


class TestNeuralRouter:
    """Tests for the neural route path using mocks."""

    @pytest.fixture
    def orchestrator(self):
        pytest.importorskip("torch")
        # Patch heavy imports before loading orchestrator module fresh
        import importlib
        import toposwarm_lazyown_orchestrator as orch_mod
        importlib.reload(orch_mod)

        # Minimal mocks
        mock_cfg = MagicMock()
        mock_cfg.DEVICE = "cpu"
        mock_cfg.CHECKPOINT_DIR = "checkpoints_toposwarm"

        mock_bridge = MagicMock()
        mock_bridge.available = False

        mock_logger = MagicMock()

        # Build orchestrator without loading real model
        orch = orch_mod.LazyOwnOrchestrator(
            cfg=MagicMock(),
            agent_cfg=mock_cfg,
            bridge=mock_bridge,
            logger=mock_logger,
            load_model=False,
        )
        return orch

    def test_neural_route_none_when_no_engine(self, orchestrator):
        assert orchestrator._neural_route("scan target") is None

    def test_neural_route_with_mock_head(self, orchestrator):
        pytest.importorskip("torch")
        import torch

        # Mock tokenizer + engine
        orchestrator._engine = MagicMock()
        orchestrator._engine.tokenizer.encode.return_value = [1, 2, 3]
        orchestrator._engine.model.norm_out = MagicMock()

        # Capture hook callbacks manually because MagicMock doesn't emulate PyTorch hooks
        _callbacks = []

        def mock_register_forward_hook(cb):
            _callbacks.append(cb)
            return MagicMock()

        orchestrator._engine.model.norm_out.register_forward_hook.side_effect = mock_register_forward_hook

        def mock_model_forward(ids):
            mock_out = torch.zeros(1, ids.shape[1], orchestrator.agent_cfg.D_MODEL)
            for cb in _callbacks:
                cb(None, (ids,), mock_out)
            return MagicMock()

        orchestrator._engine.model.side_effect = mock_model_forward

        # Mock routing head
        mock_head = MagicMock()
        mock_head.tool_names = ["lazyown_run_command", "lazyown_get_config"]
        mock_head.return_value = torch.tensor([[2.0, 0.1]])  # high confidence for idx 0
        orchestrator._routing_head = mock_head

        result = orchestrator._neural_route("scan 10.10.11.78")
        assert result is not None
        assert result[0] == "lazyown_run_command"

    def test_neural_route_low_confidence_fallback(self, orchestrator):
        pytest.importorskip("torch")
        import torch

        orchestrator._engine = MagicMock()
        orchestrator._engine.tokenizer.encode.return_value = [1, 2, 3]
        orchestrator._engine.model.norm_out = MagicMock()

        _callbacks = []

        def mock_register_forward_hook(cb):
            _callbacks.append(cb)
            return MagicMock()

        orchestrator._engine.model.norm_out.register_forward_hook.side_effect = mock_register_forward_hook

        def mock_model_forward(ids):
            mock_out = torch.zeros(1, ids.shape[1], orchestrator.agent_cfg.D_MODEL)
            for cb in _callbacks:
                cb(None, (ids,), mock_out)
            return MagicMock()

        orchestrator._engine.model.side_effect = mock_model_forward

        mock_head = MagicMock()
        mock_head.tool_names = ["lazyown_run_command", "lazyown_get_config", "lazyown_list_modules"]
        # Low confidence: equal logits with 3 classes → softmax ~0.33 each (< 0.5)
        mock_head.return_value = torch.tensor([[0.0, 0.0, 0.0]])
        orchestrator._routing_head = mock_head

        result = orchestrator._neural_route("scan target")
        assert result is None


class TestOrchestratorRun:
    """Integration-level tests for the run() method."""

    def test_run_updates_session(self):
        pytest.importorskip("torch")
        import importlib
        import toposwarm_lazyown_orchestrator as orch_mod
        importlib.reload(orch_mod)

        mock_cfg = MagicMock()
        mock_cfg.DEVICE = "cpu"
        mock_cfg.CHECKPOINT_DIR = "checkpoints_toposwarm"

        mock_bridge = MagicMock()
        mock_bridge.available = False

        mock_logger = MagicMock()

        orch = orch_mod.LazyOwnOrchestrator(
            cfg=MagicMock(),
            agent_cfg=mock_cfg,
            bridge=mock_bridge,
            logger=mock_logger,
            load_model=False,
        )
        # Patch registry so execute doesn't need real tools
        orch.registry = MagicMock()
        orch.registry.execute.return_value = MagicMock(output="nmap done", ok=True)

        result = orch.run("scan 10.10.11.78")
        assert orch.session.last_tool is not None
        assert orch.session.turn_count == 1
        assert result.tool_used is True
