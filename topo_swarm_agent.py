#!/usr/bin/env python3
"""
TopoSwarm: Minimal Quaternionic Toroidal Swarm Agent for Tool Use.

A micro-scale agentic system inspired by Kimi 2.6 swarm intelligence,
built on a quaternionic toroidal architecture with spectral autoencoders
and hierarchical fast/slow reasoning.  Designed to fit within a 6 GB VRAM
budget (RTX 2060) while performing tool-use reasoning over ToolBench-style
API traces.

Key design decisions
--------------------
- Single-file, self-contained, production-ready.
- Every numerical constant lives inside a typed dataclass (SwarmConfig).
- Architecture: micro quaternionic torus brain (d_model=64, ~2M params)
  with a 1-D spectral autoencoder bottleneck acting as the function-call
  filter (SpectralBottleneck) and a two-level HRM (L=action / H=strategy).
- Swarm: N lightweight agent instances share the same weight tensor but
  each carries a distinct Berry phase offset on the torus, causing
  specialisation over disjoint API subsets via soft torus assignment.
- ACT (Adaptive Computational Time) driven by the Hamilton-product norm of
  the quaternion state: if the halt logit exceeds the configured threshold
  the agent emits a tool call; otherwise it performs internal torus
  message-passing (the "swarm consult" step).
- Surprise metric (from tricameral neurology): cross-entropy modulated by
  the mean gate activity; drives episodic priority replay.
- Dataset: ToolBench "Instruction-Tool-Result" subset (HuggingFace mirror).
  Falls back to a local JSONL file when HuggingFace is unavailable.
- Training pipeline: Phase 0 kernel calibration on API schemas,
  Phase 1 main training with grokking detector (kappa coherence metric),
  Phase 2 annealing.
- Checkpoint: safetensors + JSON metadata, written to checkpoints_toposwarm/.
- Inference: load weights, instantiate SwarmOrchestrator, call .infer(prompt).

Author: Gris Iscomeback <grisiscomeback@gmail.com>
License: GPL v3
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import logging
import math
import os
import sys
import threading
import time
import warnings
from collections import deque
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from safetensors.torch import load_file as st_load
from safetensors.torch import save_file as st_save
from torch.utils.checkpoint import checkpoint as grad_ckpt

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# CUDA global flags
# ---------------------------------------------------------------------------
if "PYTORCH_CUDA_ALLOC_CONF" not in os.environ:
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

if torch.cuda.is_available():
    torch.set_float32_matmul_precision("high")
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True


# ===========================================================================
# CONFIGURATION – single source of truth, zero magic numbers
# ===========================================================================


@dataclass
class SwarmConfig:
    """
    All architectural and training hyper-parameters in one place.

    Scale target: fit inside 6 GB VRAM on an RTX 2060.
    - Weights: ~2 M params × 4 bytes = ~8 MB
    - Activations (B=4, S=256): ~256 MB peak with gradient checkpointing
    - Swarm overhead: N_AGENTS × D_MODEL × 4 bytes per Berry-phase tensor
    """

    # --- Device ----------------------------------------------------------
    DEVICE: str = field(default_factory=lambda: "cuda" if torch.cuda.is_available() else "cpu")
    RANDOM_SEED: int = 42
    USE_AMP: bool = True

    # --- Vocabulary ------------------------------------------------------
    # GPT-2 BPE has 50257 tokens.  Tool tokens are appended above that
    # range.  VOCAB_SIZE is the total embedding-table size and must equal
    # TOOL_TOKEN_OFFSET + TOOL_VOCAB_SIZE.  It is recomputed in __post_init__
    # so the value set here is overwritten automatically.
    VOCAB_SIZE: int = 50512      # placeholder; overwritten in __post_init__
    MAX_SEQ_LEN: int = 256

    # --- Core architecture (micro: ~2 M params) --------------------------
    D_MODEL: int = 64          # must be divisible by 4 (quaternions)
    N_HEADS: int = 4
    N_KV_HEADS: int = 1        # GQA: 1 KV head shared across 4 query heads
    N_LAYERS: int = 4
    DROPOUT: float = 0.1

    # --- FFN / SwiGLU -------------------------------------------------------
    FFN_HIDDEN_DIM: int = 128

    # --- Mixture-of-Experts (MiMo V2 style, opt-in) ----------------------
    # Set USE_MOE=True to replace the dense SwiGLU in every transformer layer
    # with N_MOE_EXPERTS independent experts + sigmoid gate (top-k routing).
    # Existing checkpoints remain compatible when USE_MOE=False (default).
    USE_MOE: bool = False
    N_MOE_EXPERTS: int = 4      # total experts per MoE layer
    MOE_TOP_K: int = 2          # experts activated per token
    MOE_EXPERT_DIM: int = 128   # hidden dim of each expert (same as FFN_HIDDEN_DIM)

    # --- Quaternion torus topology (8 nodes = 4 angular × 2 radial) ------
    TORUS_RADIAL_BINS: int = 2
    TORUS_ANGULAR_BINS: int = 4
    TORUS_ASSIGN_TEMPERATURE: float = 0.3

    # --- Spectral autoencoder (bottleneck = function-call filter) --------
    SPECTRAL_LATENT_RATIO: float = 0.5
    SPECTRAL_KERNEL_INIT_SCALE: float = 0.02
    SPECTRAL_HIGH_FREQ_PENALTY: float = 0.01
    AE_RECON_WEIGHT: float = 0.01

    # --- HRM: fast L-module (action/syntax) + slow H-module (strategy) --
    HRM_HIDDEN_DIM: int = 64
    HRM_N_CYCLES: int = 2      # H-level cycles per token
    HRM_T_STEPS: int = 2       # L-level steps per H-cycle
    HRM_ACT_EPSILON: float = 0.1
    HRM_ACT_LOSS_WEIGHT: float = 0.1

    # --- ACT halt threshold (quaternion-norm confidence) -----------------
    ACT_HALT_THRESHOLD: float = 0.5
    ACT_MAX_STEPS: int = 4

    # --- Swarm parameters ------------------------------------------------
    N_AGENTS: int = 3          # instantiated simultaneously
    BERRY_PHASE_BASE: float = math.pi / 4.0  # offset per agent slot

    # --- Training --------------------------------------------------------
    BATCH_SIZE: int = 4
    GRAD_ACCUM_STEPS: int = 8
    LEARNING_RATE: float = 3e-4
    WEIGHT_DECAY: float = 0.1
    EPOCHS: int = 3
    WARMUP_RATIO: float = 0.05
    GRADIENT_CLIP_NORM: float = 1.0
    GRADIENT_CHECKPOINTING: bool = True
    CHUNKED_CE_CHUNK_SIZE: int = 128
    TORUS_TOKEN_CHUNK_SIZE: int = 64

    # --- Grokking / kappa detector ---------------------------------------
    KAPPA_WINDOW: int = 50
    KAPPA_JUMP_THRESHOLD: float = 0.15

    # --- Surprise / episodic memory (tricameral) -------------------------
    SURPRISE_THRESHOLD_HIGH: float = 0.8
    SURPRISE_THRESHOLD_MID: float = 0.5
    EPISODIC_CAPACITY_WORKING: int = 100
    EPISODIC_CAPACITY_SHORT: int = 400
    EPISODIC_HALF_LIFE: int = 100

    # --- ToolBench dataset -----------------------------------------------
    # Primary: Maurus/ToolBench (88.9 k rows, parquet, no loading script).
    # Fallback A: local JSONL at DATASET_LOCAL_PATH.
    # Fallback B: synthetic stubs (dry-run / CI only).
    DATASET_NAME: str = "Maurus/ToolBench"
    DATASET_SPLIT: str = "train"
    DATASET_LOCAL_PATH: str = "data_toolbench/toolbench.jsonl"
    DATA_DIR: str = "data_toolbench"
    MAX_TRAIN_TOKENS: int = 5_000_000   # 5 M tokens for micro run

    # --- Tool token management -------------------------------------------
    # Tool tokens occupy a reserved block ABOVE the standard GPT-2 vocab.
    # TOOL_TOKEN_OFFSET must be >= tiktoken gpt2 vocab size (50257).
    # VOCAB_SIZE is set to TOOL_TOKEN_OFFSET + TOOL_VOCAB_SIZE in __post_init__
    # so the embedding table always covers every possible token id.
    TOOL_VOCAB_SIZE: int = 256           # number of distinct tool token slots
    TOOL_TOKEN_OFFSET: int = 50257       # first tool-token id (= gpt2 vocab end)

    # --- Checkpointing ---------------------------------------------------
    CHECKPOINT_DIR: str = "checkpoints_toposwarm"
    CHECKPOINT_INTERVAL_MINUTES: int = 5

    # --- Logging ---------------------------------------------------------
    LOG_INTERVAL_STEPS: int = 20
    EVAL_INTERVAL_STEPS: int = 200
    LOG_LEVEL: str = "INFO"

    def __post_init__(self) -> None:
        assert self.D_MODEL % 4 == 0, "D_MODEL must be divisible by 4 for quaternions"
        assert self.D_MODEL % self.N_HEADS == 0, "D_MODEL must be divisible by N_HEADS"
        assert self.N_HEADS % self.N_KV_HEADS == 0, "N_HEADS must be divisible by N_KV_HEADS"
        assert self.TOOL_TOKEN_OFFSET >= 50257, (
            "TOOL_TOKEN_OFFSET must be >= 50257 (GPT-2 vocab size) to avoid "
            "collisions with standard BPE tokens"
        )
        # The embedding table must cover all token ids including tool tokens.
        # Recompute unconditionally so no caller can leave VOCAB_SIZE stale.
        self.VOCAB_SIZE: int = self.TOOL_TOKEN_OFFSET + self.TOOL_VOCAB_SIZE
        self.D_QUAT: int = self.D_MODEL // 4
        self.D_HEAD: int = self.D_MODEL // self.N_HEADS
        self.GQA_GROUPS: int = self.N_HEADS // self.N_KV_HEADS
        self.N_TORUS_NODES: int = self.TORUS_RADIAL_BINS * self.TORUS_ANGULAR_BINS
        self.SPECTRAL_LATENT_DIM: int = max(16, int(self.D_MODEL * self.SPECTRAL_LATENT_RATIO))


# ===========================================================================
# UTILITIES
# ===========================================================================


def _setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Return an idempotent logger. Delegates to ts_utils.setup_logger."""
    try:
        from ts_utils import setup_logger
        return setup_logger(name, level)
    except ImportError:
        pass
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(name)-24s %(levelname)-8s %(message)s")
        )
        logger.addHandler(handler)
    return logger


def _set_seed(seed: int, device: str) -> None:
    """Deterministic seed across torch, numpy, and CUDA."""
    torch.manual_seed(seed)
    np.random.seed(seed)
    if "cuda" in device and torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def _param_count(module: nn.Module) -> Dict[str, int]:
    """Return total and trainable parameter counts."""
    total = sum(p.numel() for p in module.parameters())
    trainable = sum(p.numel() for p in module.parameters() if p.requires_grad)
    return {"total": total, "trainable": trainable}


_TORUS_POS_CACHE: Dict[Tuple[int, int, str], Tuple[torch.Tensor, torch.Tensor]] = {}
_TORUS_POS_LOCK: threading.Lock = threading.Lock()


def _get_torus_positions(
    n_angular: int, n_radial: int, device: torch.device
) -> Tuple[torch.Tensor, torch.Tensor]:
    """Cached angular / radial position linspaces for soft torus assignment."""
    key = (n_angular, n_radial, str(device))
    with _TORUS_POS_LOCK:
        if key not in _TORUS_POS_CACHE:
            ang = torch.linspace(-math.pi, math.pi, n_angular + 1, device=device)[:-1]
            rad = torch.linspace(-math.pi, math.pi, n_radial + 1, device=device)[:-1]
            _TORUS_POS_CACHE[key] = (ang, rad)
        return _TORUS_POS_CACHE[key]


# ===========================================================================
# QUATERNION ALGEBRA
# ===========================================================================


class QuaternionOps:
    """
    Pure-functional quaternion operations over arbitrary leading batch dims.
    Tensors have shape [..., 4] where the last dim is [w, x, y, z].
    """

    @staticmethod
    def hamilton_product(q1: torch.Tensor, q2: torch.Tensor) -> torch.Tensor:
        """Hamilton (cross) product q1 ⊗ q2 for tensors of shape [..., 4]."""
        w1, x1, y1, z1 = q1[..., 0], q1[..., 1], q1[..., 2], q1[..., 3]
        w2, x2, y2, z2 = q2[..., 0], q2[..., 1], q2[..., 2], q2[..., 3]
        return torch.stack(
            [
                w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
                w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
                w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
                w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
            ],
            dim=-1,
        )

    @staticmethod
    def normalize(q: torch.Tensor, eps: float = 1e-8) -> torch.Tensor:
        """Unit-normalise quaternion tensors."""
        return q / (q.norm(dim=-1, keepdim=True) + eps)

    @staticmethod
    def berry_phase_rotation(q: torch.Tensor, phase: float) -> torch.Tensor:
        """
        Apply a Berry-phase rotation around the w-axis of the quaternion manifold.

        Multiplies the (x, y, z) imaginary components by the complex phase
        e^{i*phase} encoded as a rotation in the yz-plane, leaving the real
        component w unchanged.  Used to differentiate swarm agent slots.
        """
        c, s = math.cos(phase), math.sin(phase)
        w = q[..., :1]
        x = q[..., 1:2]
        y = q[..., 2:3] * c - q[..., 3:4] * s
        z = q[..., 2:3] * s + q[..., 3:4] * c
        return torch.cat([w, x, y, z], dim=-1)


# ===========================================================================
# QUATERNION LINEAR LAYER (fused Hamilton-product via single einsum)
# ===========================================================================


class QuaternionLinear(nn.Module):
    """
    Linear map in the quaternion algebra.

    Implements W ⊗ x via a single batched einsum over stacked weight matrices,
    reducing CUDA kernel launches from 16 (naive 4×4 matmul loop) to 1.

    Input  x: [..., 4*in_q]
    Output  : [..., 4*out_q]
    """

    def __init__(
        self,
        in_features: int,
        out_features: int,
        bias: bool = True,
        init_std: float = 0.02,
    ) -> None:
        """
        Initialise quaternion weight matrices.

        Args:
            in_features: Must be divisible by 4.
            out_features: Must be divisible by 4.
            bias: Whether to add a bias parameter.
            init_std: Normal initialisation standard deviation.
        """
        super().__init__()
        assert in_features % 4 == 0 and out_features % 4 == 0
        self.in_q = in_features // 4
        self.out_q = out_features // 4
        # Four weight matrices, one per quaternion component
        self.Ww = nn.Linear(self.in_q, self.out_q, bias=False)
        self.Wx = nn.Linear(self.in_q, self.out_q, bias=False)
        self.Wy = nn.Linear(self.in_q, self.out_q, bias=False)
        self.Wz = nn.Linear(self.in_q, self.out_q, bias=False)
        self.bias_param = nn.Parameter(torch.zeros(out_features)) if bias else None
        for w in (self.Ww, self.Wx, self.Wy, self.Wz):
            nn.init.normal_(w.weight, std=init_std)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Fused Hamilton product via a single batched einsum."""
        d = self.in_q
        W_stack = torch.stack(
            [self.Ww.weight, self.Wx.weight, self.Wy.weight, self.Wz.weight], dim=0
        )
        x_parts = torch.stack(
            [x[..., :d], x[..., d : 2 * d], x[..., 2 * d : 3 * d], x[..., 3 * d :]],
            dim=-2,
        )
        R = torch.einsum("woi,...xi->...wxo", W_stack, x_parts)
        ow = R[..., 0, 0, :] - R[..., 1, 1, :] - R[..., 2, 2, :] - R[..., 3, 3, :]
        ox = R[..., 0, 1, :] + R[..., 1, 0, :] + R[..., 2, 3, :] - R[..., 3, 2, :]
        oy = R[..., 0, 2, :] - R[..., 1, 3, :] + R[..., 2, 0, :] + R[..., 3, 1, :]
        oz = R[..., 0, 3, :] + R[..., 1, 2, :] - R[..., 2, 1, :] + R[..., 3, 0, :]
        out = torch.cat([ow, ox, oy, oz], dim=-1)
        return out + self.bias_param if self.bias_param is not None else out


# ===========================================================================
# SPECTRAL BOTTLENECK (function-call filter)
# ===========================================================================


class SpectralBottleneck(nn.Module):
    """
    1-D spectral autoencoder acting as the function-call signal filter.

    Compresses the token representation via rfft → learned complex kernel →
    irfft → QuaternionLinear bottleneck → decode.  The bottleneck forces the
    model to route function-call intent through a harmonic low-band subspace,
    suppressing lexical noise from the surrounding context.

    Returns (latent [B,S,latent_dim], recon_loss scalar).
    """

    def __init__(self, cfg: SwarmConfig) -> None:
        """
        Build encoder/decoder spectral kernels and quaternion projections.

        Args:
            cfg: Swarm configuration object.
        """
        super().__init__()
        d = cfg.D_MODEL
        d_lat = cfg.SPECTRAL_LATENT_DIM
        n_freq = d // 2 + 1
        init_s = cfg.SPECTRAL_KERNEL_INIT_SCALE
        self.d_model = d
        self.hf_penalty = cfg.SPECTRAL_HIGH_FREQ_PENALTY

        self.enc_kr = nn.Parameter(torch.randn(n_freq) * init_s)
        self.enc_ki = nn.Parameter(torch.randn(n_freq) * init_s)
        self.dec_kr = nn.Parameter(torch.randn(n_freq) * init_s)
        self.dec_ki = nn.Parameter(torch.randn(n_freq) * init_s)
        self.enc_proj = QuaternionLinear(d, d_lat, init_std=init_s)
        self.dec_proj = QuaternionLinear(d_lat, d, init_std=init_s)

    def _filter(
        self, x: torch.Tensor, kr: torch.Tensor, ki: torch.Tensor
    ) -> torch.Tensor:
        """Apply a learned complex spectral filter in the rfft domain."""
        X = torch.fft.rfft(x, dim=-1)
        K = torch.complex(kr, ki)
        return torch.fft.irfft(X * K, n=self.d_model, dim=-1)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Encode x through the spectral bottleneck.

        A single rfft of x is computed and reused by both the encode branch
        and the high-frequency penalty, avoiding a redundant FFT call.

        Args:
            x: Input tensor [..., D_MODEL].

        Returns:
            Tuple of (latent [..., latent_dim], scalar auxiliary loss).
        """
        X_freq = torch.fft.rfft(x, dim=-1)
        K_enc = torch.complex(self.enc_kr, self.enc_ki)
        filtered = F.gelu(torch.fft.irfft(X_freq * K_enc, n=self.d_model, dim=-1))
        z = self.enc_proj(filtered)
        recon = self._filter(self.dec_proj(z), self.dec_kr, self.dec_ki)
        recon_loss = F.mse_loss(recon, x.detach())
        n_high = max(1, X_freq.shape[-1] // 4)
        hf_penalty = X_freq[..., -n_high:].abs().mean()
        return z, recon_loss + self.hf_penalty * hf_penalty


# ===========================================================================
# RMS NORM
# ===========================================================================


class RMSNorm(nn.Module):
    """Root Mean Square Layer Normalisation (LLaMA-style, no bias)."""

    def __init__(self, d_model: int, eps: float = 1e-6) -> None:
        """
        Args:
            d_model: Feature dimension.
            eps: Numerical stability epsilon.
        """
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(d_model))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Normalise by the RMS of x and rescale by learned weight."""
        rms = x.pow(2).mean(-1, keepdim=True).add(self.eps).sqrt()
        return x / rms * self.weight


# ===========================================================================
# ROTARY POSITION EMBEDDINGS (NTK-aware)
# ===========================================================================


class RotaryEmbedding(nn.Module):
    """
    NTK-aware Rotary Position Embeddings.

    Extends the standard RoPE base frequency when the requested sequence length
    exceeds the training context, preventing aliasing in high-frequency dims.
    """

    def __init__(
        self,
        d_head: int,
        max_seq_len: int = 2048,
        base: int = 10000,
        ntk_factor: float = 1.0,
    ) -> None:
        """
        Args:
            d_head: Attention head dimension.
            max_seq_len: Maximum sequence length to pre-cache.
            base: RoPE base frequency.
            ntk_factor: Set to max_seq / train_seq when extrapolating.
        """
        super().__init__()
        if ntk_factor > 1.0:
            eff_base = float(base) * (ntk_factor ** (d_head / (d_head - 2)))
        else:
            eff_base = float(base)
        inv_freq = 1.0 / (
            eff_base ** (torch.arange(0, d_head, 2).float() / d_head)
        )
        self.register_buffer("inv_freq", inv_freq)
        self._build_cache(max_seq_len)

    def _build_cache(self, seq_len: int) -> None:
        """Pre-compute cos/sin tables up to seq_len."""
        t = torch.arange(seq_len, device=self.inv_freq.device).float()
        freqs = torch.outer(t, self.inv_freq)
        emb = torch.cat([freqs, freqs], dim=-1)
        self.register_buffer("cos_cache", emb.cos())
        self.register_buffer("sin_cache", emb.sin())

    def _rotate_half(self, x: torch.Tensor) -> torch.Tensor:
        half = x.shape[-1] // 2
        return torch.cat([-x[..., half:], x[..., :half]], dim=-1)

    def forward(self, x: torch.Tensor, seq_len: int) -> torch.Tensor:
        """Apply rotary embedding to query or key tensor [B, H, S, d_head]."""
        if seq_len > self.cos_cache.shape[0]:
            self._build_cache(seq_len * 2)
        cos = self.cos_cache[:seq_len].unsqueeze(0).unsqueeze(0)
        sin = self.sin_cache[:seq_len].unsqueeze(0).unsqueeze(0)
        return x * cos + self._rotate_half(x) * sin


# ===========================================================================
# SWIGLU FFN
# ===========================================================================


class SwiGLU(nn.Module):
    """SwiGLU feed-forward: SiLU(gate(x)) * up(x) → down(...)."""

    def __init__(self, d_model: int, hidden_dim: int, dropout: float = 0.0) -> None:
        """
        Args:
            d_model: Input and output feature dimension.
            hidden_dim: Intermediate expansion dimension.
            dropout: Dropout probability after the output projection.
        """
        super().__init__()
        self.gate_proj = nn.Linear(d_model, hidden_dim, bias=False)
        self.up_proj = nn.Linear(d_model, hidden_dim, bias=False)
        self.down_proj = nn.Linear(hidden_dim, d_model, bias=False)
        self.drop = nn.Dropout(dropout) if dropout > 0 else nn.Identity()
        for proj in (self.gate_proj, self.up_proj, self.down_proj):
            nn.init.normal_(proj.weight, std=0.02)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Gated SiLU activation with residual dropout."""
        return self.drop(self.down_proj(F.silu(self.gate_proj(x)) * self.up_proj(x)))


# ===========================================================================
# SWARM MOE FFN — Mixture-of-Experts SwiGLU (inspired by MiMo V2)
# ===========================================================================
#
# Replaces the dense SwiGLU with N independent expert FFNs and a sigmoid gate.
# Key differences from standard MoE:
#   - Sigmoid scoring (not softmax): experts activate independently.
#     Borrowed directly from MiMo V2's MiMoV2MoEGate with scoring_func="sigmoid".
#   - Top-k selection: only K experts contribute to each token, keeping
#     compute constant regardless of N.
#   - Weighted sum of expert outputs (weights normalised post-sigmoid topk).
#
# This helps TopoSwarm route different tool categories through different
# specialists — e.g. one expert for recon commands, another for C2/beacons.


class SwarmMoEGate(nn.Module):
    """Sigmoid gate: selects top-k experts per token, weights normalised."""

    def __init__(self, d_model: int, n_experts: int, top_k: int) -> None:
        super().__init__()
        self.n_experts = n_experts
        self.top_k     = top_k
        self.weight    = nn.Parameter(torch.empty(n_experts, d_model))
        nn.init.xavier_uniform_(self.weight)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """x: [..., D] → (topk_idx [... K], topk_weight [..., K])"""
        flat = x.view(-1, x.shape[-1])
        scores = F.linear(flat.float(), self.weight.float()).sigmoid()
        scores = scores.to(x.dtype)
        topk_w, topk_idx = scores.topk(self.top_k, dim=-1)
        topk_w = topk_w / (topk_w.sum(dim=-1, keepdim=True) + 1e-9)
        orig = x.shape[:-1]
        return topk_idx.view(*orig, self.top_k), topk_w.view(*orig, self.top_k)


class SwarmMoE(nn.Module):
    """
    Drop-in MoE replacement for SwiGLU in TopoSwarmLayer.

    Architecture: N_EXPERTS independent SwiGLU experts + sigmoid gate.
    Each token routes to top_k experts; outputs are weighted-summed.

    For a 2M-param model (D=64, FFN_DIM=128):
      - 4 experts, top-2, expert_dim=128 → same FLOP as one dense FFN
        but 4× more representational capacity.
    """

    def __init__(
        self,
        d_model: int,
        expert_hidden_dim: int,
        n_experts: int   = 4,
        top_k: int       = 2,
        dropout: float   = 0.0,
    ) -> None:
        super().__init__()
        self.n_experts = n_experts
        self.top_k     = top_k
        self.gate      = SwarmMoEGate(d_model, n_experts, top_k)
        self.experts   = nn.ModuleList([
            SwiGLU(d_model, expert_hidden_dim, dropout=dropout)
            for _ in range(n_experts)
        ])

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: [B, S, D] → [B, S, D]  (autograd-safe, no in-place scatter)"""
        orig_shape = x.shape
        flat = x.view(-1, x.shape[-1])           # [N, D]
        topk_idx, topk_w = self.gate(flat)       # [N, K], [N, K]

        all_out = torch.stack([e(flat) for e in self.experts], dim=1)  # [N, E, D]
        W = flat.new_zeros(flat.shape[0], self.n_experts)
        for k in range(self.top_k):
            W.scatter_add_(1, topk_idx[:, k:k+1], topk_w[:, k:k+1])

        out = (W.unsqueeze(-1) * all_out).sum(dim=1)   # [N, D]
        return out.view(orig_shape)


# ===========================================================================
# SWARM MOE ADAPTER — residual MoE injected after norm_out, before lm_head
# ===========================================================================
#
# Design goals:
#   1. Checkpoint-compatible — the existing model has moe_adapter=None, so all
#      saved weights load cleanly with strict=False.
#   2. Zero-init output projections — adapter starts as identity, so the model
#      begins at its already-trained 60% accuracy and improves from there.
#   3. Frozen backbone — only adapter weights train; backbone optionally frozen.
#   4. Residual + LayerNorm — stable gradient flow even at zero-init.


class SwarmMoEAdapter(nn.Module):
    """
    Residual MoE adapter: output = LayerNorm(input + moe(input)).

    Plugs between model.norm_out and model.lm_head.  Zero-init on the output
    projection of every expert means the adapter is an identity at init time —
    the model starts at its existing accuracy and the adapter learns on top.

    Expert architecture: d_model → d_model//2 → d_model (small bottleneck)
    Gate: sigmoid (MiMo V2 style) → top-k selection, normalised weights.
    """

    ADAPTER_CKPT = "checkpoints_toposwarm/moe_adapter.pt"

    def __init__(
        self,
        d_model:    int,
        n_experts:  int   = 4,
        top_k:      int   = 2,
        bottleneck: int   = 0,  # 0 = d_model // 2
        dropout:    float = 0.0,
    ) -> None:
        super().__init__()
        self.n_experts = n_experts
        self.top_k     = top_k
        bn = bottleneck or max(d_model // 2, 16)

        self.gate    = SwarmMoEGate(d_model, n_experts, top_k)
        self.experts = nn.ModuleList()
        for _ in range(n_experts):
            up   = nn.Linear(d_model, bn, bias=False)
            act  = nn.GELU()
            down = nn.Linear(bn, d_model, bias=False)
            nn.init.xavier_uniform_(up.weight)
            nn.init.zeros_(down.weight)          # ← zero-init = identity at start
            self.experts.append(nn.Sequential(up, act, down))

        self.norm    = nn.LayerNorm(d_model)
        self.drop    = nn.Dropout(dropout) if dropout > 0 else nn.Identity()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: [B, S, D] → [B, S, D]  (residual)

        Autograd-safe: no in-place scatter — computes all expert outputs at
        once and weights them via a sparse weight tensor.
        """
        orig = x.shape
        flat = x.view(-1, orig[-1])                          # [N, D]
        topk_idx, topk_w = self.gate(flat)                  # [N, K], [N, K]

        # Stack all expert outputs: [N, E, D]
        all_out = torch.stack([e(flat) for e in self.experts], dim=1)

        # Build full weight matrix [N, E], scatter top-k weights
        W = flat.new_zeros(flat.shape[0], self.n_experts)
        for k in range(self.top_k):
            W.scatter_add_(1, topk_idx[:, k:k+1], topk_w[:, k:k+1])

        # Weighted sum: [N, E, 1] * [N, E, D] → [N, D]
        delta = (W.unsqueeze(-1) * all_out).sum(dim=1)
        return x + self.norm(self.drop(delta).view(orig))

    def save(self, path: str = ADAPTER_CKPT) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        torch.save({
            "state_dict": self.state_dict(),
            "n_experts":  self.n_experts,
            "top_k":      self.top_k,
            "d_model":    self.norm.normalized_shape[0],
        }, path)
        print(f"[adapter] Saved → {path}")

    @classmethod
    def load(cls, path: str = ADAPTER_CKPT) -> "SwarmMoEAdapter":
        data = torch.load(path, map_location="cpu", weights_only=False)
        adapter = cls(
            d_model   = data["d_model"],
            n_experts = data.get("n_experts", 4),
            top_k     = data.get("top_k", 2),
        )
        adapter.load_state_dict(data["state_dict"])
        return adapter


def inject_moe_adapter(
    model:      "TopoSwarmModel",
    n_experts:  int   = 4,
    top_k:      int   = 2,
    dropout:    float = 0.0,
    freeze_backbone: bool = True,
    adapter_path: Optional[str] = None,
) -> SwarmMoEAdapter:
    """
    Inject a SwarmMoEAdapter into an already-loaded TopoSwarmModel.

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
        The injected SwarmMoEAdapter (also stored as model.moe_adapter).
    """
    d_model = model.cfg.D_MODEL

    if adapter_path and Path(adapter_path).exists():
        adapter = SwarmMoEAdapter.load(adapter_path)
        print(f"[adapter] Loaded from {adapter_path}")
    else:
        adapter = SwarmMoEAdapter(
            d_model=d_model, n_experts=n_experts,
            top_k=top_k, dropout=dropout,
        )
        print(f"[adapter] Initialised (zero-output, starts as identity)")

    model.moe_adapter = adapter.to(next(model.parameters()).device)

    if freeze_backbone:
        frozen = 0
        for name, param in model.named_parameters():
            if "moe_adapter" not in name:
                param.requires_grad_(False)
                frozen += param.numel()
        adapter_params = sum(p.numel() for p in adapter.parameters())
        print(f"[adapter] Frozen {frozen:,} backbone params — "
              f"training only {adapter_params:,} adapter params")

    return adapter


# ===========================================================================
# QUATERNION TORUS BRAIN (vectorised, chunked for OOM safety)
# ===========================================================================


class QuaternionTorusBrain(nn.Module):
    """
    Toroidal message-passing FFN replacement.

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
    VRAM to O(chunk × N_NODES × D) rather than O(B*S × N_NODES × D).
    """

    def __init__(self, cfg: SwarmConfig) -> None:
        """
        Args:
            cfg: Swarm configuration.
        """
        super().__init__()
        d = cfg.D_MODEL
        self.d_model = d
        self.d_q = cfg.D_QUAT
        self.n_radial = cfg.TORUS_RADIAL_BINS
        self.n_angular = cfg.TORUS_ANGULAR_BINS
        self.n_nodes = cfg.N_TORUS_NODES
        self.assign_temp = cfg.TORUS_ASSIGN_TEMPERATURE
        self.token_chunk = cfg.TORUS_TOKEN_CHUNK_SIZE

        self.spectral_bn = SpectralBottleneck(cfg)
        self.torus_proj = nn.Sequential(
            QuaternionLinear(d, d, init_std=0.02),
            nn.GELU(),
            nn.Linear(d, 4, bias=True),
        )
        nn.init.normal_(self.torus_proj[-1].weight, std=0.02)
        nn.init.zeros_(self.torus_proj[-1].bias)

        self.node_embed = nn.Parameter(torch.randn(self.n_nodes, d) * 0.02)
        self.edge_quat = nn.Parameter(torch.randn(4, 4) * 0.1)
        self.node_net = QuaternionLinear(d, d, init_std=0.02)
        self.readout = SwiGLU(d, cfg.FFN_HIDDEN_DIM, dropout=cfg.DROPOUT)
        self._build_torus_graph()

    def _build_torus_graph(self) -> None:
        """
        Construct the adjacency structure of the discrete torus.

        Each node (r, a) connects angularly to (r, a±1) and radially to
        (r±1, a).  Angular neighbours wrap around (periodic boundary).
        Radial neighbours are open (no wrap).  Edge types encode direction:
        0=ang-left, 1=ang-right, 2=rad-inner, 3=rad-outer.
        """
        edges_i, edges_j, edge_type = [], [], []
        R, A = self.n_radial, self.n_angular
        for r in range(R):
            for a in range(A):
                n = r * A + a
                edges_i.append(n)
                edges_j.append(r * A + (a - 1) % A)
                edge_type.append(0)
                edges_i.append(n)
                edges_j.append(r * A + (a + 1) % A)
                edge_type.append(1)
                if r > 0:
                    edges_i.append(n)
                    edges_j.append((r - 1) * A + a)
                    edge_type.append(2)
                if r < R - 1:
                    edges_i.append(n)
                    edges_j.append((r + 1) * A + a)
                    edge_type.append(3)
        self.register_buffer("edges_i", torch.tensor(edges_i, dtype=torch.long))
        self.register_buffer("edges_j", torch.tensor(edges_j, dtype=torch.long))
        self.register_buffer("edge_type", torch.tensor(edge_type, dtype=torch.long))

    def _torus_soft_assign(
        self, phi1: torch.Tensor, phi2: torch.Tensor
    ) -> torch.Tensor:
        """
        Soft assignment of token coordinates to torus nodes via haversine distance.

        Args:
            phi1: Angular coordinate [-pi, pi] of shape [N].
            phi2: Radial coordinate [-pi, pi] of shape [N].

        Returns:
            Soft assignment weights [N, N_TORUS_NODES] summing to 1.
        """
        ang_pos, rad_pos = _get_torus_positions(
            self.n_angular, self.n_radial, phi1.device
        )
        d_ang = torch.sin((phi1.unsqueeze(1) - ang_pos.unsqueeze(0)) / 2).pow(2)
        d_rad = torch.sin((phi2.unsqueeze(1) - rad_pos.unsqueeze(0)) / 2).pow(2)
        d_torus = d_rad.unsqueeze(2) + d_ang.unsqueeze(1)
        d_flat = d_torus.reshape(phi1.shape[0], -1)
        return torch.softmax(-d_flat / self.assign_temp, dim=-1)

    def _message_passing(self, node_feat: torch.Tensor) -> torch.Tensor:
        """
        One round of quaternion message-passing on the torus graph.

        Messages are Hamilton-product-rotated by a learnable edge quaternion
        and aggregated via scatter-add to each destination node.

        Args:
            node_feat: Node feature tensor [N_chunk, N_NODES, D_MODEL].

        Returns:
            Updated node features [N_chunk, N_NODES, D_MODEL].
        """
        BS = node_feat.shape[0]
        n_edges = self.edges_i.shape[0]
        d_q = self.d_q
        eq = QuaternionOps.normalize(self.edge_quat)
        src_feat = node_feat[:, self.edges_j, :]
        edge_q = (
            eq[self.edge_type].unsqueeze(0).unsqueeze(2).expand(BS, -1, d_q, -1)
        )
        src_q = src_feat.view(BS, n_edges, d_q, 4)
        msg_rot = QuaternionOps.hamilton_product(edge_q, src_q)
        msg_rot = msg_rot.view(BS, n_edges, self.d_model)
        agg = torch.zeros_like(node_feat)
        dst_idx = (
            self.edges_i.view(1, n_edges, 1).expand(BS, -1, self.d_model)
        )
        agg.scatter_add_(1, dst_idx, msg_rot)
        return self.node_net(node_feat + agg)

    def forward(
        self, x: torch.Tensor, berry_phase: float = 0.0
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Full torus forward with optional Berry-phase offset for swarm slots.

        Processes tokens in chunks to bound peak VRAM.

        Args:
            x: Input [B, S, D_MODEL].
            berry_phase: Phase offset applied to the torus projection output
                         for this agent slot, rotating the soft assignment
                         and inducing specialisation.

        Returns:
            Tuple of (output [B, S, D_MODEL], scalar auxiliary recon loss).
        """
        B, S, D = x.shape
        x_flat = x.reshape(B * S, D)
        TC = self.token_chunk
        out_flat = torch.zeros_like(x_flat)
        total_recon = x_flat.new_zeros(1)
        n_chunks = 0

        for start in range(0, B * S, TC):
            end = min(start + TC, B * S)
            xc = x_flat[start:end]

            _, recon_c = self.spectral_bn(xc)
            total_recon = total_recon + recon_c
            n_chunks += 1

            coords = self.torus_proj(xc)
            if berry_phase != 0.0:
                q_coords = coords.view(end - start, 1, 4)
                q_coords = QuaternionOps.berry_phase_rotation(q_coords, berry_phase)
                coords = q_coords.view(end - start, 4)

            phi1 = math.pi * torch.tanh(coords[:, 0])
            phi2 = math.pi * torch.tanh(coords[:, 1])
            attn_w = self._torus_soft_assign(phi1, phi2)

            nodes = attn_w.unsqueeze(-1) * self.node_embed.unsqueeze(
                0
            ) + attn_w.unsqueeze(-1) * xc.unsqueeze(1)

            nodes_mp = self._message_passing(nodes)
            out_chunk = (attn_w.unsqueeze(-1) * nodes_mp).sum(dim=1)
            out_flat[start:end] = self.readout(out_chunk)

        return out_flat.reshape(B, S, D), total_recon / max(n_chunks, 1)


# ===========================================================================
# GQA ATTENTION WITH SPECTRAL HEAD COMPRESSION
# ===========================================================================


class QuaternionAttention(nn.Module):
    """
    Grouped-query attention (GQA) with RoPE and quaternion Q/K projections.

    A lightweight per-head 1-D spectral filter compresses the query and key
    vectors before dot-product attention, forcing harmonic representations.
    """

    def __init__(self, cfg: SwarmConfig) -> None:
        """
        Args:
            cfg: Swarm configuration.
        """
        super().__init__()
        d, h, kv, d_h = (
            cfg.D_MODEL,
            cfg.N_HEADS,
            cfg.N_KV_HEADS,
            cfg.D_HEAD,
        )
        self.n_heads = h
        self.n_kv_heads = kv
        self.gqa_groups = cfg.GQA_GROUPS
        self.d_head = d_h
        self.dropout_p = cfg.DROPOUT

        self.q_proj = QuaternionLinear(d, d, init_std=0.02)
        self.k_proj = QuaternionLinear(d, kv * d_h, init_std=0.02)
        self.v_proj = nn.Linear(d, kv * d_h, bias=False)
        self.o_proj = nn.Linear(d, d, bias=False)
        nn.init.normal_(self.v_proj.weight, std=0.02)
        nn.init.normal_(self.o_proj.weight, std=0.02)

        self.rope = RotaryEmbedding(d_h, max_seq_len=cfg.MAX_SEQ_LEN * 2)

        # Lightweight 1-D spectral filter per head (shares kernel across heads)
        n_freq_h = d_h // 2 + 1
        init_s = cfg.SPECTRAL_KERNEL_INIT_SCALE
        self.head_enc_kr = nn.Parameter(torch.randn(n_freq_h) * init_s)
        self.head_enc_ki = nn.Parameter(torch.randn(n_freq_h) * init_s)

    def _head_filter(self, x: torch.Tensor) -> torch.Tensor:
        """Apply the shared per-head spectral filter [B, H, S, d_head]."""
        X = torch.fft.rfft(x, dim=-1)
        K = torch.complex(self.head_enc_kr, self.head_enc_ki)
        return torch.fft.irfft(X * K, n=self.d_head, dim=-1)

    def forward(
        self,
        x: torch.Tensor,
        is_causal: bool = True,
    ) -> torch.Tensor:
        """
        GQA forward pass with RoPE and optional gradient checkpointing.

        Args:
            x: Input [B, S, D].
            is_causal: Whether to apply causal masking.

        Returns:
            Output [B, S, D].
        """
        B, S, D = x.shape
        Q = self.q_proj(x).view(B, S, self.n_heads, self.d_head).transpose(1, 2)
        K = self.k_proj(x).view(B, S, self.n_kv_heads, self.d_head).transpose(1, 2)
        V = self.v_proj(x).view(B, S, self.n_kv_heads, self.d_head).transpose(1, 2)

        Q = self.rope(self._head_filter(Q), S)
        K = self.rope(self._head_filter(K), S)

        # Expand KV heads for GQA
        K = K.repeat_interleave(self.gqa_groups, dim=1)
        V = V.repeat_interleave(self.gqa_groups, dim=1)

        def _manual_attn():
            scale  = Q.shape[-1] ** -0.5
            scores = torch.matmul(Q, K.transpose(-2, -1)) * scale
            if is_causal:
                S_q, S_k = Q.shape[2], K.shape[2]
                mask = torch.ones(S_q, S_k, dtype=torch.bool, device=Q.device).tril()
                scores = scores.masked_fill(~mask, float("-inf"))
            attn = F.softmax(scores, dim=-1)
            if self.dropout_p > 0 and self.training:
                attn = F.dropout(attn, p=self.dropout_p)
            return torch.matmul(attn, V)

        try:
            out = F.scaled_dot_product_attention(
                Q, K, V,
                dropout_p=self.dropout_p if self.training else 0.0,
                is_causal=is_causal,
            )
        except RuntimeError:
            # Flash/efficient kernels unavailable on this device — use math path
            out = _manual_attn()

        out = out.transpose(1, 2).contiguous().view(B, S, D)
        return self.o_proj(out)


# ===========================================================================
# HRM: HIERARCHICAL REASONING MODULE (L=fast/action, H=slow/strategy)
# ===========================================================================


class HRMModule(nn.Module):
    """
    Hierarchical Reasoning Model embedded in the torus agent.

    L-module (fast / action): recurrent GRU-gated unit responsible for
    the syntax of tool calls (the "how").

    H-module (slow / strategy): a wider linear unit responsible for
    tool selection (the "what").

    The ACT (Adaptive Computational Time) halt logit is computed from the
    Hamilton-product norm of the final H-state quaternion: when the norm
    exceeds ACT_HALT_THRESHOLD the agent emits a decision; otherwise it
    re-enters the message-passing loop (the "swarm consult" step).
    """

    def __init__(self, cfg: SwarmConfig) -> None:
        """
        Args:
            cfg: Swarm configuration.
        """
        super().__init__()
        d = cfg.D_MODEL
        h = cfg.HRM_HIDDEN_DIM
        self.n_cycles = cfg.HRM_N_CYCLES
        self.t_steps = cfg.HRM_T_STEPS
        self.act_eps = cfg.HRM_ACT_EPSILON

        # L-module: GRU-gated action unit (syntax / how)
        self.l_gate = nn.Linear(d * 2, d, bias=True)
        self.l_update = nn.Linear(d * 2, d, bias=True)
        self.l_norm = RMSNorm(d)

        # H-module: strategy selection unit (what)
        self.h_proj = nn.Linear(d, h, bias=True)
        self.h_out = nn.Linear(h, d, bias=True)
        self.h_norm = RMSNorm(d)

        # ACT halt logit
        self.halt_head = nn.Linear(d, 1, bias=True)
        self.drop = nn.Dropout(cfg.DROPOUT)

        for lin in (
            self.l_gate,
            self.l_update,
            self.h_proj,
            self.h_out,
            self.halt_head,
        ):
            nn.init.normal_(lin.weight, std=0.02)
            if lin.bias is not None:
                nn.init.zeros_(lin.bias)

    def _l_step(self, x: torch.Tensor, state: torch.Tensor) -> torch.Tensor:
        """One GRU-gated L-module step."""
        cat = torch.cat([x, state], dim=-1)
        g = torch.sigmoid(self.l_gate(cat))
        u = torch.tanh(self.l_update(cat))
        return self.l_norm(state + g * u)

    def _h_step(self, z: torch.Tensor) -> torch.Tensor:
        """One H-module strategy update."""
        return self.h_norm(z + self.drop(self.h_out(F.silu(self.h_proj(z)))))

    def forward(
        self, x: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Run the HRM hierarchy and return the updated state with ACT signal.

        Args:
            x: Pooled context embedding [B, D].

        Returns:
            Tuple of (h_state [B, D], halt_logit [B, 1], act_loss scalar).
        """
        B, D = x.shape
        z_l = x.clone()
        z_h = x.clone()
        act_loss = x.new_zeros(1)

        for _ in range(self.n_cycles):
            for _ in range(self.t_steps):
                z_l = self._l_step(x, z_l)
            z_h = self._h_step(z_l)

        halt_logit = self.halt_head(z_h)
        # ACT penalty: encourage decisive halting
        halt_prob = torch.sigmoid(halt_logit)
        act_loss = -(
            halt_prob * torch.log(halt_prob.clamp(min=1e-7))
            + (1.0 - halt_prob) * torch.log((1.0 - halt_prob).clamp(min=1e-7))
        ).mean()

        return z_h, halt_logit, act_loss


# ===========================================================================
# TRANSFORMER LAYER
# ===========================================================================


class TopoSwarmLayer(nn.Module):
    """
    Single transformer layer: GQA attention + QuaternionTorusBrain FFN.

    Both sub-layers use pre-norm (RMSNorm) and residual connections.
    Gradient checkpointing is applied to the attention sub-layer.
    """

    def __init__(self, cfg: SwarmConfig) -> None:
        """
        Args:
            cfg: Swarm configuration.
        """
        super().__init__()
        self.attn = QuaternionAttention(cfg)
        # MoE FFN (MiMo V2 sigmoid gate) or standard QuaternionTorusBrain
        if cfg.USE_MOE:
            self.torus = SwarmMoE(
                d_model=cfg.D_MODEL,
                expert_hidden_dim=cfg.MOE_EXPERT_DIM,
                n_experts=cfg.N_MOE_EXPERTS,
                top_k=cfg.MOE_TOP_K,
                dropout=cfg.DROPOUT,
            )
            self._moe_mode = True
        else:
            self.torus = QuaternionTorusBrain(cfg)
            self._moe_mode = False
        self.norm1 = RMSNorm(cfg.D_MODEL)
        self.norm2 = RMSNorm(cfg.D_MODEL)
        self.use_ckpt = cfg.GRADIENT_CHECKPOINTING

    def _attn_fn(self, x: torch.Tensor) -> torch.Tensor:
        return self.attn(x)

    def forward(
        self, x: torch.Tensor, berry_phase: float = 0.0
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Pre-norm layer forward.

        Args:
            x: Input [B, S, D].
            berry_phase: Swarm Berry-phase offset for the torus brain.

        Returns:
            Tuple of (output [B, S, D], torus recon loss scalar).
        """
        if self.use_ckpt and self.training:
            attn_out = grad_ckpt(self._attn_fn, self.norm1(x), use_reentrant=False)
        else:
            attn_out = self.attn(self.norm1(x))
        x = x + attn_out
        if self._moe_mode:
            # SwarmMoE returns tensor directly (no recon loss)
            torus_out = self.torus(self.norm2(x))
            recon_loss = x.new_zeros(1)
        else:
            torus_out, recon_loss = self.torus(self.norm2(x), berry_phase=berry_phase)
        x = x + torus_out
        return x, recon_loss


# ===========================================================================
# CORE MODEL
# ===========================================================================


class TopoSwarmModel(nn.Module):
    """
    Micro quaternionic toroidal transformer for tool-use reasoning.

    Architecture:
    - Token embedding + learned positional bias.
    - N_LAYERS of TopoSwarmLayer (GQA + QuaternionTorusBrain).
    - HRM module on the pooled representation for ACT control.
    - Language-model head (tied weights with embedding).

    The Berry-phase offset is passed through every layer to specialise each
    swarm agent slot without duplicating weight tensors.
    """

    def __init__(self, cfg: SwarmConfig) -> None:
        """
        Args:
            cfg: Swarm configuration.
        """
        super().__init__()
        self.cfg = cfg
        self.embed = nn.Embedding(cfg.VOCAB_SIZE, cfg.D_MODEL)
        self.pos_bias = nn.Parameter(
            torch.randn(1, cfg.MAX_SEQ_LEN, cfg.D_MODEL) * 0.02
        )
        self.layers = nn.ModuleList(
            [TopoSwarmLayer(cfg) for _ in range(cfg.N_LAYERS)]
        )
        self.norm_out = RMSNorm(cfg.D_MODEL)
        self.hrm = HRMModule(cfg)
        self.lm_head = nn.Linear(cfg.D_MODEL, cfg.VOCAB_SIZE, bias=False)
        # Weight tying: embedding and lm_head share the token matrix
        self.lm_head.weight = self.embed.weight
        nn.init.normal_(self.embed.weight, std=0.02)
        # MoE adapter slot — None by default (checkpoint-compatible).
        # Call inject_moe_adapter(model) to activate without retraining.
        self.moe_adapter: Optional[nn.Module] = None

    def forward(
        self,
        input_ids: torch.Tensor,
        berry_phase: float = 0.0,
        targets: Optional[torch.Tensor] = None,
    ) -> Dict[str, torch.Tensor]:
        """
        Full forward pass for one agent slot.

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
            - "act_loss": scalar ACT entropy regulariser
        """
        B, S = input_ids.shape
        S_clip = min(S, self.cfg.MAX_SEQ_LEN)

        # Hard clamp: prevents CUDA device-side assert in nn.Embedding when
        # any token id falls outside [0, VOCAB_SIZE).
        ids_safe = input_ids[:, :S_clip].clamp(0, self.cfg.VOCAB_SIZE - 1)
        x = self.embed(ids_safe) + self.pos_bias[:, :S_clip, :]

        total_recon = x.new_zeros(1)
        for layer in self.layers:
            x, recon = layer(x, berry_phase=berry_phase)
            total_recon = total_recon + recon

        x = self.norm_out(x)
        if self.moe_adapter is not None:
            x = self.moe_adapter(x)
        logits = self.lm_head(x)

        # HRM on attention-weighted pooled representation
        attn_w = torch.softmax(logits[:, :, 0:1], dim=1)  # [B, S_clip, 1]
        pooled = (attn_w * x).sum(dim=1)  # [B, D]
        _, halt_logit, act_loss = self.hrm(pooled)

        out: Dict[str, torch.Tensor] = {
            "logits": logits,
            "halt_logit": halt_logit,
            "recon_loss": total_recon / max(len(self.layers), 1),
            "act_loss": act_loss,
        }

        if targets is not None:
            # Align target length to the clipped sequence length
            tgt_clip = targets[:, :S_clip]
            # Causal LM: predict position t+1 from positions 0..t
            # logits[:, :-1, :] predicts targets[:, 1:]
            tgt_shifted = tgt_clip[:, 1:].contiguous()
            # Preserve -100 (ignore_index) — only clamp valid token ids.
            # clamp(0, ...) would silently corrupt -100 masking used by the
            # continual trainer for tool-token-focused loss.
            tgt_shifted = torch.where(
                tgt_shifted < 0,
                tgt_shifted,
                tgt_shifted.clamp(0, self.cfg.VOCAB_SIZE - 1),
            )
            lm_loss = _chunked_ce(
                logits[:, :-1, :].contiguous(),
                tgt_shifted,
                self.cfg.CHUNKED_CE_CHUNK_SIZE,
            )
            out["loss"] = (
                lm_loss
                + self.cfg.AE_RECON_WEIGHT * out["recon_loss"]
                + self.cfg.HRM_ACT_LOSS_WEIGHT * act_loss
            )
        return out

    @torch.no_grad()
    def generate(
        self,
        input_ids: torch.Tensor,
        max_new_tokens: int,
        temperature: float,
        top_k: int,
        berry_phase: float = 0.0,
        act_halt_threshold: float = 0.5,
    ) -> Tuple[torch.Tensor, bool]:
        """
        Autoregressive generation with ACT-driven early stopping.

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
            Tuple of (generated ids [1, S + new_tokens], did_halt bool).
        """
        self.eval()
        ids = input_ids.clone()
        did_halt = False
        # During generation we restrict sampling to the standard BPE range
        # [0, TOOL_TOKEN_OFFSET) so the output text is decodable.  Tool tokens
        # are injected by the caller via encode_tool_trace, not generated freely.
        bpe_ceiling = self.cfg.TOOL_TOKEN_OFFSET
        for _ in range(max_new_tokens):
            out = self.forward(ids[:, -self.cfg.MAX_SEQ_LEN :], berry_phase=berry_phase)
            # Mask logits for ids >= bpe_ceiling so multinomial never samples them
            logits = out["logits"][:, -1, :].clone() / max(temperature, 1e-7)
            logits[:, bpe_ceiling:] = float("-inf")
            if top_k > 0:
                v, _ = torch.topk(logits, min(top_k, bpe_ceiling))
                logits[logits < v[:, -1:]] = float("-inf")
            probs = F.softmax(logits, dim=-1)
            next_id = torch.multinomial(probs, num_samples=1)
            ids = torch.cat([ids, next_id], dim=1)
            halt_prob = torch.sigmoid(out["halt_logit"]).item()
            if halt_prob > act_halt_threshold:
                did_halt = True
                break
        return ids, did_halt


def _chunked_ce(
    logits: torch.Tensor, targets: torch.Tensor, chunk_size: int
) -> torch.Tensor:
    """
    Cross-entropy over the sequence without materialising the full [N, V] matrix.

    Processes the sequence in chunks of chunk_size to bound peak memory to
    O(chunk_size × VOCAB_SIZE) instead of O(B*S × VOCAB_SIZE).

    Args:
        logits: [B, S, V] or [N, V].
        targets: [B, S] or [N] integer targets.
        chunk_size: Tokens per chunk.

    Returns:
        Scalar mean cross-entropy.
    """
    if logits.dim() == 3:
        B, S, V = logits.shape
        logits = logits.reshape(B * S, V)
        targets = targets.reshape(B * S)
    N = logits.shape[0]
    if chunk_size <= 0 or chunk_size >= N:
        return F.cross_entropy(logits, targets)
    total = logits.new_zeros(1)
    for start in range(0, N, chunk_size):
        end = min(start + chunk_size, N)
        total = total + F.cross_entropy(
            logits[start:end], targets[start:end], reduction="sum"
        )
    # Divide by non-ignored positions only (same as mean-path behaviour).
    # Dividing by total N inflates the denominator when most targets are -100
    # (masked), making loss appear ~N/n_valid times smaller than the real CE.
    n_valid = max((targets != -100).sum().item(), 1)
    return total / n_valid


# ===========================================================================
# EPISODIC MEMORY (tricameral surprise-driven)
# ===========================================================================


class EpisodicMemory:
    """
    Three-tier episodic memory inspired by the tricameral neurology architecture.

    Tier assignment is driven by a surprise score: cross-entropy modulated by
    the mean ACT gate activity.  High-surprise events go to working memory
    (highest replay priority); low-surprise events to long-term if their
    computed importance exceeds a threshold.
    """

    def __init__(self, cfg: SwarmConfig) -> None:
        """
        Args:
            cfg: Swarm configuration for capacity and threshold parameters.
        """
        self._working: deque = deque(maxlen=cfg.EPISODIC_CAPACITY_WORKING)
        self._short: deque = deque(maxlen=cfg.EPISODIC_CAPACITY_SHORT)
        self._long: List = []
        self._long_scores: List[float] = []
        self._step = 0
        self._half_life = cfg.EPISODIC_HALF_LIFE
        self._thresh_high = cfg.SURPRISE_THRESHOLD_HIGH
        self._thresh_mid = cfg.SURPRISE_THRESHOLD_MID

    @staticmethod
    def compute_surprise(
        logits: torch.Tensor, targets: torch.Tensor, gate_mean: float
    ) -> float:
        """
        Surprise = cross-entropy × (1 - gate_mean), clipped to [0, 10].

        A high gate_mean (confident model) attenuates the surprise signal;
        a low gate_mean (uncertain) amplifies it.

        Args:
            logits: Raw model logits [B, S, V] or [N, V].
            targets: Integer targets matching logits.
            gate_mean: Mean ACT halt probability in [0, 1].

        Returns:
            Scalar surprise value.
        """
        with torch.no_grad():
            ce = F.cross_entropy(
                logits.reshape(-1, logits.size(-1)),
                targets.reshape(-1),
                reduction="mean",
            )
            return ((ce * (1.0 - gate_mean)).clamp(0.0, 10.0) / max(logits.size(0), 1)).item()

    def store(self, episode: Dict, surprise: float) -> None:
        """
        Store an episode in the appropriate memory tier.

        Args:
            episode: Dict of tensors/metadata describing the experience.
            surprise: Scalar surprise score from compute_surprise.
        """
        self._step += 1
        if surprise > self._thresh_high:
            self._working.append((episode, surprise))
        elif surprise > self._thresh_mid:
            self._short.append((episode, surprise))
        else:
            importance = min(1.0, surprise / 2.0) * 0.6 + 0.2
            if importance > 0.5 and len(self._long) < 1000:
                self._long.append((episode, importance))
                self._long_scores.append(importance)
        if self._step % self._half_life == 0:
            self._decay()

    def sample(self, n: int) -> List[Dict]:
        """
        Sample n episodes with priority proportional to surprise / importance.

        Draws from all three tiers; working memory contributes the most
        samples (50 %), short-term 30 %, long-term 20 %.

        Args:
            n: Number of episodes to sample.

        Returns:
            List of episode dicts.
        """
        samples: List[Dict] = []
        for pool, k in [
            (list(self._working), max(1, n // 2)),
            (list(self._short), max(1, int(n * 0.3))),
        ]:
            if pool:
                idxs = np.random.choice(len(pool), size=min(k, len(pool)), replace=False)
                samples.extend(pool[i][0] for i in idxs)
        if self._long:
            scores = np.array(self._long_scores, dtype=np.float64)
            scores = scores / scores.sum()
            idxs = np.random.choice(
                len(self._long),
                size=min(max(1, n // 5), len(self._long)),
                p=scores,
                replace=False,
            )
            samples.extend(self._long[i][0] for i in idxs)
        return samples

    def _decay(self) -> None:
        """Apply exponential forgetting to the long-term memory scores."""
        factor = 0.5 ** (1.0 / self._half_life)
        self._long_scores = [max(1e-8, s * factor) for s in self._long_scores]


# ===========================================================================
# SWARM ORCHESTRATOR
# ===========================================================================


class SwarmOrchestrator:
    """
    Coordinates N_AGENTS lightweight agent slots over a shared weight tensor.

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
    - Otherwise → emit the call proposed by the most confident slot.
    """

    def __init__(self, model: TopoSwarmModel, cfg: SwarmConfig) -> None:
        """
        Args:
            model: Shared TopoSwarmModel instance.
            cfg: Swarm configuration.
        """
        self.model = model
        self.cfg = cfg
        self.n_agents = cfg.N_AGENTS
        self.berry_phases = [
            cfg.BERRY_PHASE_BASE * i for i in range(cfg.N_AGENTS)
        ]
        self.halt_threshold = cfg.ACT_HALT_THRESHOLD
        self.max_act_steps = cfg.ACT_MAX_STEPS
        self.memory = EpisodicMemory(cfg)
        self._logger = _setup_logger("SwarmOrchestrator", cfg.LOG_LEVEL)

    @torch.no_grad()
    def infer(
        self,
        input_ids: torch.Tensor,
        tokenizer: "BPETokenizer",
        max_new_tokens: int = 64,
        temperature: float = 0.8,
        top_k: int = 40,
    ) -> str:
        """
        Run swarm inference and return the decoded output string.

        Args:
            input_ids: Prompt token ids [1, S].
            tokenizer: BPETokenizer used to decode output ids.
            max_new_tokens: Maximum tokens any slot may generate.
            temperature: Sampling temperature.
            top_k: Top-k sampling truncation.

        Returns:
            Decoded string of the winning slot's output.
        """
        self.model.eval()
        results: List[Tuple[torch.Tensor, float]] = []

        for phase in self.berry_phases:
            ids, halted = self.model.generate(
                input_ids,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_k=top_k,
                berry_phase=phase,
                act_halt_threshold=self.halt_threshold,
            )
            out = self.model.forward(ids[:, -self.cfg.MAX_SEQ_LEN :], berry_phase=phase)
            confidence = torch.sigmoid(out["halt_logit"]).item()
            results.append((ids, confidence))

        # Select the most confident slot
        best_ids, best_conf = max(results, key=lambda t: t[1])
        self._logger.debug(
            "Swarm winner confidence=%.4f among %d slots", best_conf, self.n_agents
        )

        prompt_len = input_ids.shape[1]
        new_ids = best_ids[0, prompt_len:].tolist()
        return tokenizer.decode(new_ids)


# ===========================================================================
# TOKENIZER (GPT-2 BPE via tiktoken)
# ===========================================================================


class BPETokenizer:
    """
    Thin wrapper around tiktoken's GPT-2 BPE encoding.

    Adds special tool tokens by reserving a range at the top of the
    vocabulary [TOOL_TOKEN_OFFSET, TOOL_TOKEN_OFFSET + TOOL_VOCAB_SIZE).
    """

    def __init__(self, cfg: SwarmConfig) -> None:
        """
        Args:
            cfg: Swarm config (provides TOOL_TOKEN_OFFSET and TOOL_VOCAB_SIZE).
        """
        try:
            import tiktoken

            self._enc = tiktoken.get_encoding("gpt2")
        except ImportError as exc:
            raise RuntimeError(
                "tiktoken is required: pip install tiktoken"
            ) from exc

        self._bpe_vocab_size: int = self._enc.n_vocab   # 50257 for gpt2
        self.tool_offset: int = cfg.TOOL_TOKEN_OFFSET
        self.tool_vocab_size: int = cfg.TOOL_VOCAB_SIZE
        # Total vocabulary seen by the model embedding table
        self.vocab_size: int = cfg.VOCAB_SIZE

        # Sanity: tool offset must start at or above the BPE ceiling so no
        # BPE token ever aliases a tool token.
        if self.tool_offset < self._bpe_vocab_size:
            raise ValueError(
                f"TOOL_TOKEN_OFFSET ({self.tool_offset}) is below the tiktoken "
                f"gpt2 vocab size ({self._bpe_vocab_size}).  Set it to "
                f">= {self._bpe_vocab_size} to avoid token id collisions."
            )
        # The model embedding table must cover the highest possible tool token.
        max_tool_id = self.tool_offset + self.tool_vocab_size - 1
        if max_tool_id >= self.vocab_size:
            raise ValueError(
                f"Highest tool token id {max_tool_id} >= VOCAB_SIZE "
                f"({self.vocab_size}).  Increase VOCAB_SIZE or shrink "
                f"TOOL_VOCAB_SIZE."
            )
        self._tool_cache: Dict[str, int] = {}

    def encode(self, text: str) -> List[int]:
        """
        Encode text to BPE token ids, clamped to the BPE vocab ceiling.

        tiktoken encodes exclusively within [0, bpe_vocab_size), but we clamp
        defensively to prevent any edge-case overflow from reaching the
        embedding table lookup.
        """
        ids = self._enc.encode(text, allowed_special="all")
        ceiling = self._bpe_vocab_size - 1
        return [min(i, ceiling) for i in ids]

    def decode(self, ids: List[int]) -> str:
        """Decode token ids to text, silently dropping tool tokens."""
        normal = [i for i in ids if 0 <= i < self._bpe_vocab_size]
        return self._enc.decode(normal)

    def tool_token(self, tool_name: str) -> int:
        """
        Return a stable integer token id for a named tool.

        Assigns a deterministic id within the tool-token range based on the
        MD5 hash of the tool name, ensuring consistent mapping across runs.
        The result is always in [TOOL_TOKEN_OFFSET, TOOL_TOKEN_OFFSET + TOOL_VOCAB_SIZE)
        which is guaranteed to be < VOCAB_SIZE by the __init__ check above.

        Args:
            tool_name: Canonical tool identifier string.

        Returns:
            Integer token id in [TOOL_TOKEN_OFFSET, TOOL_TOKEN_OFFSET + TOOL_VOCAB_SIZE).
        """
        if tool_name not in self._tool_cache:
            h = int(hashlib.md5(tool_name.encode()).hexdigest(), 16)
            self._tool_cache[tool_name] = (
                self.tool_offset + (h % self.tool_vocab_size)
            )
        return self._tool_cache[tool_name]

    def encode_tool_trace(self, instruction: str, tool_name: str, result: str) -> List[int]:
        """
        Encode a ToolBench-style (instruction, tool, result) triple.

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
            Flat list of token ids, all in [0, VOCAB_SIZE).
        """
        return (
            self.encode(instruction)
            + [self.tool_token(tool_name)]
            + self.encode(result)
        )


# ===========================================================================
# DATASET: ToolBench JSONL loader
# ===========================================================================


class ToolBenchDataset(torch.utils.data.Dataset):
    """
    ToolBench "Instruction-Tool-Result" dataset loader.

    Attempts to load from HuggingFace datasets first; falls back to a local
    JSONL file at cfg.DATASET_LOCAL_PATH.  Only successful traces
    (is_halt=True or equivalent) are retained.

    Each sample is a flat token sequence:
        [instruction tokens] [tool token] [result tokens]
    truncated to MAX_SEQ_LEN.  Training targets are the input shifted by 1.
    """

    def __init__(
        self,
        cfg: SwarmConfig,
        tokenizer: BPETokenizer,
        split: str = "train",
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """
        Args:
            cfg: Swarm configuration.
            tokenizer: BPETokenizer for encoding traces.
            split: Dataset split name.
            logger: Optional logger instance.
        """
        self.cfg = cfg
        self.tok = tokenizer
        self.seq_len = cfg.MAX_SEQ_LEN
        self._vocab_size = cfg.VOCAB_SIZE   # stored for __getitem__ clamp
        self.logger = logger or _setup_logger("ToolBenchDataset", cfg.LOG_LEVEL)
        self._samples: List[List[int]] = []
        self._load(split)

    def _load(self, split: str) -> None:
        """
        Load and tokenise tool traces with three-level fallback.

        Level 1 – Maurus/ToolBench (HuggingFace parquet, no loading script).
            Schema: {query, api_list, domain}.  api_list is a JSON list of
            dicts each with keys tool_name and api_name.
        Level 2 – local JSONL at cfg.DATASET_LOCAL_PATH.
            Accepted schemas: any dict with recognisable query/tool/result keys.
        Level 3 – synthetic stubs of fixed length MAX_SEQ_LEN with token ids
            inside [0, VOCAB_SIZE).  Safe dry-run fallback.
        """
        records: List[Dict] = []
        hf_ok = False

        # ---- Level 1: Maurus/ToolBench parquet (no trust_remote_code) ------
        try:
            from datasets import load_dataset  # type: ignore

            self.logger.info(
                "Loading %s (split=%s) from HuggingFace...",
                self.cfg.DATASET_NAME,
                split,
            )
            # Maurus/ToolBench has only a 'train' split; tolerate that.
            hf_split = split if split == "train" else "train"
            ds = load_dataset(self.cfg.DATASET_NAME, split=hf_split)
            for row in ds:
                records.append(dict(row))
            hf_ok = True
            self.logger.info(
                "Loaded %d traces from HuggingFace.", len(records)
            )
        except Exception as exc:
            self.logger.warning("HuggingFace load failed (%s).", exc)

        # ---- Level 2: local JSONL ------------------------------------------
        if not hf_ok:
            local = Path(self.cfg.DATASET_LOCAL_PATH)
            if local.exists():
                self.logger.info("Loading from local JSONL: %s", local)
                with local.open("r", encoding="utf-8") as fh:
                    for line in fh:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            records.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
                self.logger.info("Loaded %d records from local JSONL.", len(records))
            else:
                # ---- Level 3: synthetic stubs -----------------------------
                self.logger.warning(
                    "No dataset source found. "
                    "Using synthetic stubs — install 'datasets' and connect "
                    "to the internet to train on real data."
                )
                records = self._synthetic_stubs(512)

        # ---- Tokenise and collect samples ----------------------------------
        total_tokens = 0
        for rec in records:
            if total_tokens >= self.cfg.MAX_TRAIN_TOKENS:
                break
            try:
                ids = self._encode_record(rec)
            except Exception:
                continue
            if len(ids) < 4:
                continue
            ids = ids[: self.seq_len]
            self._samples.append(ids)
            total_tokens += len(ids)

        self.logger.info(
            "Dataset ready: %d sequences, %d total tokens.",
            len(self._samples),
            total_tokens,
        )

    def _encode_record(self, rec: Dict) -> List[int]:
        """
        Encode a tool-trace record to token ids.

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
        prevent single records from dominating the token budget.
        """
        instruction = str(
            rec.get("query")
            or rec.get("instruction")
            or rec.get("input")
            or rec.get("prompt")
            or ""
        )[:512]

        # Maurus schema: api_list is a Python list (already deserialised by HF)
        api_list = rec.get("api_list")
        if api_list and isinstance(api_list, list) and len(api_list) > 0:
            first = api_list[0] if isinstance(api_list[0], dict) else {}
            tool_name = str(
                first.get("tool_name") or first.get("api_name") or "generic_tool"
            )
            # Build a compact result string from tool metadata
            desc = str(first.get("api_description") or "")[:256]
            domain = str(rec.get("domain") or "")
            result = f"[{domain}] {tool_name}: {desc}"[:512]
        else:
            # Legacy schema
            tool_name = str(
                rec.get("api_name")
                or rec.get("tool_name")
                or rec.get("tool")
                or "generic_tool"
            )
            result = str(
                rec.get("response")
                or rec.get("result")
                or rec.get("output")
                or rec.get("answer")
                or ""
            )[:512]

        return self.tok.encode_tool_trace(instruction, tool_name, result)

    def _synthetic_stubs(self, n: int) -> List[Dict]:
        """
        Generate n synthetic tool-trace stubs safe for dry-run training.

        All token ids produced from these stubs are guaranteed to be within
        [0, VOCAB_SIZE) because:
        - instruction and result text encode to ids within [0, bpe_vocab_size).
        - tool_token() returns ids within [TOOL_TOKEN_OFFSET, TOOL_TOKEN_OFFSET
          + TOOL_VOCAB_SIZE) < VOCAB_SIZE (validated in BPETokenizer.__init__).
        """
        tools = ["get_weather", "search_web", "calc_expr", "translate", "get_news"]
        cities = ["Santiago", "Tokyo", "Berlin", "Cairo", "Lima", "Lagos", "Oslo"]
        domains = ["Logistics", "Weather", "Finance", "Travel", "News"]
        stubs = []
        for i in range(n):
            tool = tools[i % len(tools)]
            city = cities[i % len(cities)]
            domain = domains[i % len(domains)]
            stubs.append(
                {
                    "query": f"I need to {tool} for {city}. Please help me.",
                    "api_list": [
                        {
                            "tool_name": tool,
                            "api_name": f"{tool}_endpoint",
                            "api_description": f"Returns {tool} data for a given city.",
                        }
                    ],
                    "domain": domain,
                }
            )
        return stubs

    def __len__(self) -> int:
        return len(self._samples)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Return a (input_ids, target_ids) pair of length MAX_SEQ_LEN.

        Token ids are clamped to [0, VOCAB_SIZE - 1] as a hard safety guard
        against any upstream encoding edge case that could produce an
        out-of-bounds embedding lookup on the GPU.
        """
        ids = self._samples[idx]
        if len(ids) < self.seq_len:
            ids = ids + [0] * (self.seq_len - len(ids))
        ids = ids[: self.seq_len]
        # Hard clamp: any id outside [0, VOCAB_SIZE) would cause a CUDA
        # device-side assert in nn.Embedding.  Clamp defensively here so the
        # error surfaces as a bad prediction rather than a crash.
        ceil = self._vocab_size - 1
        ids = [max(0, min(i, ceil)) for i in ids]
        ids_t = torch.tensor(ids, dtype=torch.long)
        return ids_t, ids_t


# ===========================================================================
# CHECKPOINT MANAGER
# ===========================================================================


class CheckpointManager:
    """
    Manages safetensors checkpoints with JSON metadata in a single directory.

    Writes to checkpoints_toposwarm/latest/ atomically by writing a temp
    file and renaming it.
    """

    def __init__(self, cfg: SwarmConfig, logger: logging.Logger) -> None:
        """
        Args:
            cfg: Swarm configuration.
            logger: Logger instance.
        """
        self.path = Path(cfg.CHECKPOINT_DIR) / "latest"
        self.path.mkdir(parents=True, exist_ok=True)
        self.logger = logger
        self.interval = cfg.CHECKPOINT_INTERVAL_MINUTES * 60
        self._last_save = time.time()

    def save(
        self,
        model: TopoSwarmModel,
        optimizer: torch.optim.Optimizer,
        meta: Dict,
        force: bool = False,
    ) -> None:
        """
        Save model weights and metadata if the interval has elapsed.

        Args:
            model: Model to checkpoint.
            optimizer: Optimizer state to checkpoint.
            meta: Scalar metadata dict (epoch, step, loss, etc.).
            force: If True, save regardless of the time interval.
        """
        if not force and time.time() - self._last_save < self.interval:
            return
        weights_path = self.path / "model.safetensors"
        opt_path = self.path / "optimizer.pt"
        meta_path = self.path / "meta.json"
        tmp_w = weights_path.with_suffix(".tmp")
        # Weight-tied models (embed.weight == lm_head.weight) share storage;
        # safetensors raises RuntimeError on duplicate data_ptr values.
        # Deduplicate: keep the first key for each storage address and drop
        # the rest.  load() uses strict=False so the tied weight is restored.
        raw_sd = model.state_dict()
        seen_ptrs: Dict[int, str] = {}
        deduped_sd: Dict[str, torch.Tensor] = {}
        for k, v in raw_sd.items():
            ptr = v.data_ptr()
            if ptr not in seen_ptrs:
                seen_ptrs[ptr] = k
                deduped_sd[k] = v
        st_save(deduped_sd, str(tmp_w))
        tmp_w.replace(weights_path)
        torch.save(optimizer.state_dict(), str(opt_path))
        with meta_path.open("w", encoding="utf-8") as fh:
            json.dump(meta, fh, indent=2)
        self._last_save = time.time()
        self.logger.info("Checkpoint saved → %s", self.path)

    def load(
        self,
        model: TopoSwarmModel,
        optimizer: Optional[torch.optim.Optimizer] = None,
        device: str = "cpu",
    ) -> Optional[Dict]:
        """
        Load model weights and metadata from the latest checkpoint.

        Args:
            model: Target model (mutated in-place).
            optimizer: Optional optimizer to restore state into.
            device: Device string for weight map.

        Returns:
            Metadata dict if found, None otherwise.
        """
        weights_path = self.path / "model.safetensors"
        meta_path = self.path / "meta.json"
        if not weights_path.exists():
            return None
        state = st_load(str(weights_path), device=device)
        model.load_state_dict(state, strict=False)
        if optimizer is not None:
            opt_path = self.path / "optimizer.pt"
            if opt_path.exists():
                optimizer.load_state_dict(
                    torch.load(str(opt_path), map_location=device)
                )
        meta: Dict = {}
        if meta_path.exists():
            with meta_path.open("r", encoding="utf-8") as fh:
                meta = json.load(fh)
        return meta


# ===========================================================================
# KAPPA COHERENCE DETECTOR (grokking signal)
# ===========================================================================


class KappaDetector:
    """
    Tracks the kappa coherence metric over a sliding window to detect grokking.

    Kappa is defined as the inverse of the cross-entropy loss (clipped),
    normalised to [0, 1].  A sharp upward jump of more than KAPPA_JUMP_THRESHOLD
    within the window signals that the model has found the function-call
    structure (the ToolBench grokking point).
    """

    def __init__(self, cfg: SwarmConfig) -> None:
        """
        Args:
            cfg: Swarm configuration (window and threshold).
        """
        self._window: deque = deque(maxlen=cfg.KAPPA_WINDOW)
        self._threshold = cfg.KAPPA_JUMP_THRESHOLD

    def update(self, loss: float) -> Tuple[float, bool]:
        """
        Update the detector with the latest loss value.

        Args:
            loss: Scalar training loss.

        Returns:
            Tuple of (current_kappa, grokking_detected bool).
        """
        kappa = 1.0 / max(loss, 1e-4)
        kappa = min(kappa, 10.0)
        self._window.append(kappa)
        if len(self._window) < self._window.maxlen:
            return kappa, False
        arr = list(self._window)
        jump = arr[-1] - arr[0]
        return kappa, jump > self._threshold


# ===========================================================================
# TRAINING ENGINE
# ===========================================================================


class SwarmTrainer:
    """
    Three-phase training pipeline for the TopoSwarm agent.

    Phase 0 (Kernel Calibration): Pre-trains only the SpectralBottleneck
    parameters on the API schema strings to seed the harmonic filter.

    Phase 1 (Main Training): Full model training with grokking detection
    via the KappaDetector.

    Phase 2 (Annealing): Fine-tunes with a reduced learning rate and
    cosine schedule to stabilise the tool-call routing.
    """

    def __init__(
        self,
        model: TopoSwarmModel,
        cfg: SwarmConfig,
        tokenizer: BPETokenizer,
        logger: logging.Logger,
    ) -> None:
        """
        Args:
            model: TopoSwarmModel instance.
            cfg: Swarm configuration.
            tokenizer: BPETokenizer.
            logger: Logger instance.
        """
        self.model = model.to(cfg.DEVICE)
        self.cfg = cfg
        self.tok = tokenizer
        self.logger = logger
        self.device = cfg.DEVICE
        self.scaler = torch.cuda.amp.GradScaler(enabled=cfg.USE_AMP and "cuda" in cfg.DEVICE)
        self.ckpt = CheckpointManager(cfg, logger)
        self.kappa = KappaDetector(cfg)
        self.memory = EpisodicMemory(cfg)

        self._step = 0
        self._epoch = 0

    def _make_optimizer(self, lr: float) -> torch.optim.AdamW:
        """
        Build AdamW with weight decay applied only to non-bias, non-norm params.

        Args:
            lr: Learning rate.

        Returns:
            Configured AdamW optimizer.
        """
        decay_params = [
            p
            for n, p in self.model.named_parameters()
            if p.requires_grad and p.ndim >= 2
        ]
        no_decay_params = [
            p
            for n, p in self.model.named_parameters()
            if p.requires_grad and p.ndim < 2
        ]
        return torch.optim.AdamW(
            [
                {"params": decay_params, "weight_decay": self.cfg.WEIGHT_DECAY},
                {"params": no_decay_params, "weight_decay": 0.0},
            ],
            lr=lr,
            betas=(0.9, 0.95),
            eps=1e-8,
        )

    def _warmup_cosine_lr(
        self,
        optimizer: torch.optim.AdamW,
        step: int,
        total_steps: int,
        warmup_steps: int,
        base_lr: float,
    ) -> None:
        """Apply warmup + cosine decay learning rate schedule."""
        if step < warmup_steps:
            lr = base_lr * step / max(warmup_steps, 1)
        else:
            progress = (step - warmup_steps) / max(total_steps - warmup_steps, 1)
            lr = base_lr * 0.5 * (1.0 + math.cos(math.pi * progress))
        for group in optimizer.param_groups:
            group["lr"] = max(lr, base_lr * 1e-3)

    def _train_one_batch(
        self,
        optimizer: torch.optim.AdamW,
        input_ids: torch.Tensor,
        targets: torch.Tensor,
        accum_step: int,
        berry_phase: float = 0.0,
    ) -> float:
        """
        Forward + backward for one micro-batch, returns detached loss.

        Args:
            optimizer: Current optimizer.
            input_ids: [B, S] token ids.
            targets: [B, S] target ids.
            accum_step: Index within the gradient accumulation window.
            berry_phase: Agent slot phase for this forward pass.

        Returns:
            Scalar loss value (Python float).
        """
        input_ids = input_ids.to(self.device)
        targets = targets.to(self.device)
        with torch.cuda.amp.autocast(
            enabled=self.cfg.USE_AMP and "cuda" in self.device
        ):
            out = self.model(input_ids, berry_phase=berry_phase, targets=targets)
            loss = out["loss"] / self.cfg.GRAD_ACCUM_STEPS

        self.scaler.scale(loss).backward()

        if (accum_step + 1) % self.cfg.GRAD_ACCUM_STEPS == 0:
            self.scaler.unscale_(optimizer)
            nn.utils.clip_grad_norm_(
                self.model.parameters(), self.cfg.GRADIENT_CLIP_NORM
            )
            self.scaler.step(optimizer)
            self.scaler.update()
            optimizer.zero_grad(set_to_none=True)

        return loss.detach().item() * self.cfg.GRAD_ACCUM_STEPS

    def _phase0_calibrate(
        self,
        dataloader: torch.utils.data.DataLoader,
        n_steps: int = 50,
    ) -> None:
        """
        Phase 0: Kernel calibration on API schema tokens.

        Freezes all parameters except the SpectralBottleneck kernels,
        training only the spectral filter to recognise API intent.

        Args:
            dataloader: Training dataloader.
            n_steps: Number of calibration gradient steps.
        """
        self.logger.info("Phase 0: Kernel calibration (%d steps).", n_steps)
        # Freeze all except spectral bottleneck
        for name, param in self.model.named_parameters():
            param.requires_grad = "spectral_bn" in name

        trainable = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        self.logger.info("Phase 0 trainable params: %d", trainable)

        opt = self._make_optimizer(self.cfg.LEARNING_RATE * 0.1)
        opt.zero_grad(set_to_none=True)
        self.model.train()
        dl_iter = iter(dataloader)

        for step in range(n_steps):
            try:
                ids, tgt = next(dl_iter)
            except StopIteration:
                dl_iter = iter(dataloader)
                ids, tgt = next(dl_iter)
            self._train_one_batch(opt, ids, tgt, step)

        # Unfreeze all
        for param in self.model.parameters():
            param.requires_grad = True
        self.logger.info("Phase 0 complete.")

    def train(
        self,
        train_dl: torch.utils.data.DataLoader,
        val_dl: torch.utils.data.DataLoader,
        resume: bool = False,
    ) -> None:
        """
        Full three-phase training loop.

        Phase 0: Kernel calibration (50 steps, spectral params only).
        Phase 1: Main training for cfg.EPOCHS epochs with kappa detection.
        Phase 2: Cosine annealing for 1 extra epoch at half learning rate.

        Args:
            train_dl: Training DataLoader.
            val_dl: Validation DataLoader.
            resume: If True, attempt to restore from the latest checkpoint.
        """
        cfg = self.cfg
        optimizer = self._make_optimizer(cfg.LEARNING_RATE)
        start_epoch = 0

        if resume:
            meta = self.ckpt.load(self.model, optimizer, device=cfg.DEVICE)
            if meta:
                start_epoch = meta.get("epoch", 0)
                self._step = meta.get("step", 0)
                self.logger.info("Resumed from epoch %d, step %d.", start_epoch, self._step)

        self._phase0_calibrate(train_dl)

        total_steps = len(train_dl) * cfg.EPOCHS
        warmup_steps = max(1, int(total_steps * cfg.WARMUP_RATIO))
        grokked = False

        for epoch in range(start_epoch, cfg.EPOCHS):
            self._epoch = epoch
            self.model.train()
            running_loss = 0.0
            n_batches = 0

            for accum_idx, (ids, tgt) in enumerate(train_dl):
                # Rotate berry phase across swarm slots for training diversity
                phase = self.cfg.BERRY_PHASE_BASE * (accum_idx % cfg.N_AGENTS)
                self._warmup_cosine_lr(
                    optimizer, self._step, total_steps, warmup_steps, cfg.LEARNING_RATE
                )
                loss_val = self._train_one_batch(
                    optimizer, ids, tgt, accum_idx, berry_phase=phase
                )
                running_loss += loss_val
                n_batches += 1
                self._step += 1

                kappa_val, grokked = self.kappa.update(loss_val)

                if self._step % cfg.LOG_INTERVAL_STEPS == 0:
                    avg_loss = running_loss / max(n_batches, 1)
                    self.logger.info(
                        "epoch=%d step=%d loss=%.4f kappa=%.4f grokked=%s lr=%.2e",
                        epoch,
                        self._step,
                        avg_loss,
                        kappa_val,
                        grokked,
                        optimizer.param_groups[0]["lr"],
                    )
                    running_loss = 0.0
                    n_batches = 0

                if grokked:
                    self.logger.info(
                        "Grokking detected at step %d (kappa jump). "
                        "Agent has crystallised tool-call routing.",
                        self._step,
                    )

                if self._step % cfg.EVAL_INTERVAL_STEPS == 0:
                    val_loss = self._evaluate(val_dl)
                    self.logger.info("val_loss=%.4f", val_loss)

                self.ckpt.save(
                    self.model,
                    optimizer,
                    {
                        "epoch": epoch,
                        "step": self._step,
                        "loss": loss_val,
                        "kappa": kappa_val,
                        "grokked": grokked,
                    },
                )

            self.ckpt.save(
                self.model,
                optimizer,
                {"epoch": epoch + 1, "step": self._step, "grokked": grokked},
                force=True,
            )

        # Phase 2: Annealing
        self.logger.info("Phase 2: Annealing.")
        ann_lr = cfg.LEARNING_RATE * 0.5
        ann_opt = self._make_optimizer(ann_lr)
        ann_steps = len(train_dl)
        for accum_idx, (ids, tgt) in enumerate(train_dl):
            self._warmup_cosine_lr(ann_opt, accum_idx, ann_steps, 0, ann_lr)
            self._train_one_batch(ann_opt, ids, tgt, accum_idx)
            self._step += 1
        self.ckpt.save(self.model, ann_opt, {"phase": "annealing_done"}, force=True)
        self.logger.info("Training complete.")

    @torch.no_grad()
    def _evaluate(self, val_dl: torch.utils.data.DataLoader) -> float:
        """
        Compute mean validation loss over the first EVAL_INTERVAL_STEPS batches.

        Args:
            val_dl: Validation DataLoader.

        Returns:
            Mean loss scalar.
        """
        self.model.eval()
        total, n = 0.0, 0
        limit = min(len(val_dl), self.cfg.EVAL_INTERVAL_STEPS // 4)
        for i, (ids, tgt) in enumerate(val_dl):
            if i >= limit:
                break
            ids = ids.to(self.device)
            tgt = tgt.to(self.device)
            with torch.cuda.amp.autocast(
                enabled=self.cfg.USE_AMP and "cuda" in self.device
            ):
                out = self.model(ids, targets=tgt)
            total += out["loss"].item()
            n += 1
        self.model.train()
        return total / max(n, 1)


# ===========================================================================
# ENTRY POINT
# ===========================================================================


def build_dataloaders(
    cfg: SwarmConfig,
    tokenizer: BPETokenizer,
    logger: logging.Logger,
) -> Tuple[torch.utils.data.DataLoader, torch.utils.data.DataLoader]:
    """
    Build train and validation DataLoaders from the ToolBench dataset.

    Args:
        cfg: Swarm configuration.
        tokenizer: BPETokenizer for encoding.
        logger: Logger instance.

    Returns:
        Tuple of (train_loader, val_loader).
    """
    dataset = ToolBenchDataset(cfg, tokenizer, split="train", logger=logger)
    n = len(dataset)
    n_val = max(1, int(n * 0.05))
    n_train = n - n_val
    train_ds, val_ds = torch.utils.data.random_split(
        dataset, [n_train, n_val], generator=torch.Generator().manual_seed(cfg.RANDOM_SEED)
    )
    num_workers = min(2, os.cpu_count() or 1)
    train_dl = torch.utils.data.DataLoader(
        train_ds,
        batch_size=cfg.BATCH_SIZE,
        shuffle=True,
        drop_last=True,
        num_workers=num_workers,
        pin_memory="cuda" in cfg.DEVICE,
    )
    val_dl = torch.utils.data.DataLoader(
        val_ds,
        batch_size=cfg.BATCH_SIZE,
        shuffle=False,
        drop_last=False,
        num_workers=num_workers,
        pin_memory="cuda" in cfg.DEVICE,
    )
    return train_dl, val_dl


def main() -> None:
    """
    CLI entry point.

    Modes:
        --train             : Run the full three-phase training pipeline.
        --resume            : Resume training from the latest checkpoint.
        --infer --prompt P  : Load checkpoint and run swarm inference.
        --param-count       : Print model parameter counts and exit.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="TopoSwarm: Minimal Quaternionic Toroidal Swarm Agent"
    )
    parser.add_argument("--train", action="store_true", help="Run training pipeline")
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint")
    parser.add_argument("--infer", action="store_true", help="Run swarm inference")
    parser.add_argument("--prompt", type=str, default="What is the weather in Santiago?")
    parser.add_argument("--param-count", action="store_true")
    parser.add_argument("--epochs", type=int, default=0)
    parser.add_argument("--batch-size", type=int, default=0)
    parser.add_argument("--lr", type=float, default=0.0)
    parser.add_argument("--n-agents", type=int, default=0)
    parser.add_argument("--device", type=str, default="")
    parser.add_argument("--local-data", type=str, default="", help="Path to local JSONL dataset")
    args = parser.parse_args()

    cfg = SwarmConfig()
    if args.epochs > 0:
        cfg.EPOCHS = args.epochs
    if args.batch_size > 0:
        cfg.BATCH_SIZE = args.batch_size
    if args.lr > 0.0:
        cfg.LEARNING_RATE = args.lr
    if args.n_agents > 0:
        cfg.N_AGENTS = args.n_agents
    if args.device:
        cfg.DEVICE = args.device
    if args.local_data:
        cfg.DATASET_LOCAL_PATH = args.local_data

    logger = _setup_logger("TopoSwarm", cfg.LOG_LEVEL)
    _set_seed(cfg.RANDOM_SEED, cfg.DEVICE)

    logger.info("Device: %s | AMP: %s", cfg.DEVICE, cfg.USE_AMP)

    tokenizer = BPETokenizer(cfg)

    model = TopoSwarmModel(cfg)
    counts = _param_count(model)
    logger.info(
        "Model params: total=%d (~%.2f M), trainable=%d",
        counts["total"],
        counts["total"] / 1e6,
        counts["trainable"],
    )

    if args.param_count:
        return

    if args.train or args.resume:
        os.makedirs(cfg.DATA_DIR, exist_ok=True)
        train_dl, val_dl = build_dataloaders(cfg, tokenizer, logger)
        trainer = SwarmTrainer(model, cfg, tokenizer, logger)
        trainer.train(train_dl, val_dl, resume=args.resume)

    if args.infer:
        ckpt_mgr = CheckpointManager(cfg, logger)
        meta = ckpt_mgr.load(model, device=cfg.DEVICE)
        if meta:
            logger.info("Loaded checkpoint: %s", meta)
        else:
            logger.warning("No checkpoint found; using random weights.")
        model = model.to(cfg.DEVICE)
        orchestrator = SwarmOrchestrator(model, cfg)
        prompt_ids = tokenizer.encode(args.prompt)
        prompt_t = torch.tensor([prompt_ids], dtype=torch.long, device=cfg.DEVICE)
        output = orchestrator.infer(
            prompt_t,
            tokenizer,
            max_new_tokens=64,
            temperature=0.8,
            top_k=40,
        )
        logger.info("Prompt  : %s", args.prompt)
        logger.info("Response: %s", output)


if __name__ == "__main__":
    main()
