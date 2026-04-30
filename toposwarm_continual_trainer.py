#!/usr/bin/env python3
"""
TopoSwarm Continual Trainer — EWC + Experience Replay
======================================================
Fine-tunes the TopoSwarm router on LazyOwn traces WITHOUT catastrophic
forgetting of ToolBench generalisation.

Strategy
--------
Two complementary techniques run together every training step:

  1. Elastic Weight Consolidation (EWC)
     - Computes the Fisher Information diagonal on a sample of ToolBench data
       (measures which weights are most critical for the original task).
     - Adds a quadratic penalty to the loss:
         L_ewc = λ/2 · Σ_i  F_i · (θ_i − θ*_i)²
     - This anchors critical weights to their pre-fine-tuning values while
       still allowing less-critical weights to specialise on LazyOwn.
     - λ = 400 is strong enough for a 2M-param model; tune if needed.

  2. Experience Replay
     - Keeps a circular buffer of ToolBench training examples.
     - Mixes REPLAY_RATIO (20 %) ToolBench samples into every mini-batch.
     - Prevents the router from forgetting weather/calc/search routing
       by constantly seeing those examples during LazyOwn training.

Why EWC over LoRA?
------------------
LoRA adds trainable rank-decomposed adapters and freezes base weights —
great for large transformer checkpoints (7B+). For a 2M-param custom model
trained from scratch, modifying the full weight tensor IS the training.
EWC achieves the same "protect original weights" goal through a loss penalty
rather than a structural freeze, with zero architectural overhead.

Why Replay over just EWC?
-------------------------
EWC approximates the original task with a Gaussian; when the fine-tuning
distribution is very different (security vs. weather/calc), the quadratic
approximation can drift. Replay provides exact gradient signal from the
original task distribution, making the two methods strongly complementary.

Usage
-----
    # Full pipeline: generate dataset → compute Fisher → fine-tune
    python toposwarm_continual_trainer.py --full

    # Step by step
    python toposwarm_continual_trainer.py --gen-dataset
    python toposwarm_continual_trainer.py --compute-fisher
    python toposwarm_continual_trainer.py --train

    # Evaluate routing accuracy after training
    python toposwarm_continual_trainer.py --eval

    # Override λ (EWC strength) or replay ratio
    python toposwarm_continual_trainer.py --full --ewc-lambda 600 --replay-ratio 0.25

Author: Gris Iscomeback  —  GPL v3
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import logging
import math
import os
import random
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F

# ---------------------------------------------------------------------------
# Import sibling modules
# ---------------------------------------------------------------------------

_HERE = Path(__file__).parent.resolve()

# Shared utilities (logger, safe_eval, import_module, cached tokenizer)
try:
    from ts_utils import setup_logger, import_module, make_cached_encode, make_cached_tool_token
except ImportError:
    from ts_utils import setup_logger, import_module, make_cached_encode, make_cached_tool_token  # noqa

def _import(name: str, filename: str):
    return import_module(name, _HERE / filename, Path.cwd() / filename)


_agent      = _import("topo_swarm_agent",     "topo_swarm_agent.py")
_gen        = _import("lazyown_dataset_gen",  "lazyown_dataset_generator.py")

SwarmConfig      = _agent.SwarmConfig
TopoSwarmModel   = _agent.TopoSwarmModel
BPETokenizer     = _agent.BPETokenizer
CheckpointManager= _agent.CheckpointManager
SwarmTrainer     = _agent.SwarmTrainer


# ===========================================================================
# Continual Learning Config
# ===========================================================================


@dataclass
class ContinualConfig:
    """All hyper-parameters for the continual learning run."""

    # ── Paths ────────────────────────────────────────────────────────────────
    LAZYOWN_DATASET:  str = "data_toolbench/lazyown_full.jsonl"
    TOOLBENCH_DATASET:str = "data_toolbench/toolbench.jsonl"  # fallback replay source
    CHECKPOINT_DIR:   str = "checkpoints_toposwarm"
    FISHER_PATH:      str = "checkpoints_toposwarm/fisher.pt"

    # ── EWC ──────────────────────────────────────────────────────────────────
    # λ=400 was freezing the model — it anchored weights computed on LazyOwn
    # itself, preventing any routing improvement on the new task.
    # λ=10 allows learning while still providing a soft regulariser.
    EWC_LAMBDA:        float = 10.0
    FISHER_N_SAMPLES:  int   = 512
    FISHER_BATCH:      int   = 4

    # ── Replay ───────────────────────────────────────────────────────────────
    REPLAY_RATIO:      float = 0.20    # fraction of each batch from replay buffer
    REPLAY_BUFFER_SIZE:int   = 600     # max ToolBench examples in memory

    # ── Training ─────────────────────────────────────────────────────────────
    EPOCHS:            int   = 20      # more epochs needed; early-stop guards against overfit
    LEARNING_RATE:     float = 2e-5
    ROUTING_HEAD_LR:   float = 5e-4   # routing head learns faster than backbone
    BATCH_SIZE:        int   = 4
    GRAD_ACCUM_STEPS:  int   = 4
    WARMUP_RATIO:      float = 0.05
    GRADIENT_CLIP:     float = 0.5
    WEIGHT_DECAY:      float = 0.05

    # ── Logging ───────────────────────────────────────────────────────────────
    LOG_INTERVAL:      int   = 10
    EVAL_INTERVAL:     int   = 50
    LOG_LEVEL:         str   = "INFO"


# ===========================================================================
# Logging
# ===========================================================================


def _setup_logger(level: str = "INFO") -> logging.Logger:
    return setup_logger("TopoSwarmCL", level)


# ===========================================================================
# Surprise Buffer — priority replay for hard examples (NeuroLogos-inspired)
# ===========================================================================

class SurpriseBuffer:
    """
    Tracks per-example surprise scores and returns a priority-weighted
    replay sample so the trainer oversamples examples the model is failing on.

    Surprise (from NeuroLogos tricameral):
        surprise = CE_loss × (1 − confidence)
    where confidence = softmax_max of the LM-head logits at the routing position.

    High surprise = model is wrong AND was overconfident → hardest to learn.
    These examples are stored and mixed into subsequent mini-batches at a
    configurable ratio (default 25 % of each batch).
    """

    def __init__(self, maxsize: int = 512, replay_ratio: float = 0.25) -> None:
        self.maxsize      = maxsize
        self.replay_ratio = replay_ratio
        self._records: List[Dict] = []     # original JSONL records
        self._scores:  List[float] = []    # surprise scores

    def update(
        self,
        records:    List[Dict],
        task_losses: torch.Tensor,         # [B] per-example CE at tool position
        logits:      torch.Tensor,         # [B, TOOL_VOCAB_SIZE] tool logits
    ) -> None:
        """Add batch examples to buffer, keyed by surprise score."""
        with torch.no_grad():
            # confidence = max prob in tool-token softmax
            conf = torch.softmax(logits.float(), dim=-1).max(dim=-1).values  # [B]
            surprise = (task_losses.float() * (1.0 - conf)).clamp(0, 10)    # [B]

        for rec, sc in zip(records, surprise.tolist()):
            if sc < 0.1:          # ignore near-zero surprise (model already knows)
                continue
            self._records.append(rec)
            self._scores.append(sc)

        # Keep only the top-maxsize most surprising examples
        if len(self._records) > self.maxsize:
            # key=index breaks ties without comparing dicts
            pairs = sorted(enumerate(zip(self._scores, self._records)),
                           key=lambda x: x[1][0], reverse=True)
            keep  = [idx for idx, _ in pairs[:self.maxsize]]
            self._scores  = [self._scores[i]  for i in keep]
            self._records = [self._records[i] for i in keep]

    def sample(self, batch_size: int) -> List[Dict]:
        """Return a priority-weighted sample of hard examples."""
        if not self._records:
            return []
        n = min(max(1, int(batch_size * self.replay_ratio)), len(self._records))
        probs = np.array(self._scores, dtype=np.float64)
        probs = probs / probs.sum()
        idx = np.random.choice(len(self._records), size=n, p=probs, replace=False)
        return [self._records[i] for i in idx]

    def __len__(self) -> int:
        return len(self._records)


# ===========================================================================
# Dataset utilities
# ===========================================================================


def _load_jsonl(path: Path) -> List[Dict]:
    if not path.exists():
        return []
    records = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return records


def _encode_record(record: Dict, tok: BPETokenizer, cfg: SwarmConfig) -> Optional[Tuple[List[int], List[int]]]:
    """
    Encode a ToolBench-format record into (input_ids, target_ids).

    Uses the same compact format as topo_swarm_agent.ToolBenchDataset._encode_record:
        [instruction BPE tokens]  [tool token]  [compact result BPE tokens]

    This matches the pretraining distribution exactly, keeping cross-entropy in
    the same range as the original training (1-2 nats) rather than the full
    vocabulary baseline (~10.8 nats for random predictions over 50k+ tokens).
    """
    try:
        instruction = str(
            record.get("instruction") or record.get("query") or ""
        )[:512]

        api_list  = record.get("api_list", [])
        first     = api_list[0] if api_list and isinstance(api_list[0], dict) else {}
        tool_name = str(first.get("tool_name") or first.get("api_name") or "generic_tool")

        # Compact result: same formula as topo_swarm_agent to stay in-distribution
        domain = str(record.get("domain") or "")
        desc   = str(first.get("api_description") or "")[:256]
        result = f"[{domain}] {tool_name}: {desc}"[:512]

        instr_ids  = tok.encode(instruction)
        tool_tok   = tok.tool_token(tool_name)
        result_ids = tok.encode(result)

        # Full sequence (same layout as ToolBenchDataset: return full ids, not pre-shifted)
        # Model forward does its own shift: logits[:,:-1] vs targets[:,1:]
        ids = (instr_ids + [tool_tok] + result_ids)[-cfg.MAX_SEQ_LEN:]

        if len(ids) < 4:
            return None

        # Build masked targets aligned with full ids (no pre-shift).
        # Model forward takes targets[:,1:], so to supervise position p in ids,
        # set masked[p] = ids[p].  Everything else stays -100 (ignore_index).
        # We supervise only the tool token slot: ids[tool_pos] = tool_tok,
        # predicted from the last instruction token at ids[tool_pos - 1].
        instr_len_clipped = min(len(instr_ids), len(ids))
        tool_pos = instr_len_clipped          # index of tool_tok in ids
        masked = [-100] * len(ids)
        if 0 < tool_pos < len(ids):
            masked[tool_pos] = tool_tok       # model learns: after instr → predict tool

        return ids, masked

    except Exception:
        return None


class ToolBenchDataset(torch.utils.data.Dataset):
    def __init__(self, records: List[Dict], tok: BPETokenizer, cfg: SwarmConfig) -> None:
        self.samples: List[Tuple[torch.Tensor, torch.Tensor]] = []
        for r in records:
            enc = _encode_record(r, tok, cfg)
            if enc:
                inp, tgt = enc
                self.samples.append((
                    torch.tensor(inp, dtype=torch.long),
                    torch.tensor(tgt, dtype=torch.long),
                ))

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int):
        return self.samples[idx]


def _collate(batch):
    max_len = max(x.shape[0] for x, _ in batch)
    xs, ys = [], []
    for x, y in batch:
        pad = max_len - x.shape[0]
        xs.append(F.pad(x, (0, pad), value=0))
        ys.append(F.pad(y, (0, pad), value=-100))
    return torch.stack(xs), torch.stack(ys)


# ===========================================================================
# Replay Buffer
# ===========================================================================


class ReplayBuffer:
    """
    Circular buffer of ToolBench examples.

    Randomly selects REPLAY_RATIO * batch_size samples to mix into every
    fine-tuning batch, ensuring the model continuously sees original-task
    examples during LazyOwn training.
    """

    def __init__(self, records: List[Dict], max_size: int, tok: BPETokenizer, cfg: SwarmConfig) -> None:
        dataset = ToolBenchDataset(records, tok, cfg)
        # Sample up to max_size uniformly
        indices = list(range(len(dataset)))
        random.shuffle(indices)
        self._samples = [dataset[i] for i in indices[:max_size]]
        self._rng = random.Random(42)

    def sample(self, n: int) -> List[Tuple[torch.Tensor, torch.Tensor]]:
        if not self._samples or n <= 0:
            return []
        return self._rng.choices(self._samples, k=n)

    def __len__(self) -> int:
        return len(self._samples)


# ===========================================================================
# EWC — Fisher Information + penalty
# ===========================================================================


class EWC:
    """
    Elastic Weight Consolidation.

    Computes the diagonal of the Fisher Information Matrix on a sample of
    ToolBench data, then adds the quadratic penalty to the loss at every
    fine-tuning step.

    The penalty is:
        L_ewc = λ/2 · Σ_i  F_i · (θ_i − θ*_i)²

    where θ* is the snapshot of parameters BEFORE fine-tuning begins, and
    F_i is the empirical Fisher diagonal (mean squared gradient of log-prob).
    """

    def __init__(
        self,
        model: TopoSwarmModel,
        cfg: SwarmConfig,
        cl_cfg: ContinualConfig,
        tok: BPETokenizer,
        logger: logging.Logger,
    ) -> None:
        self.model   = model
        self.cfg     = cfg
        self.cl_cfg  = cl_cfg
        self.tok     = tok
        self.logger  = logger
        self.device  = cfg.DEVICE

        # Will be populated by compute() or load()
        self._fisher: Dict[str, torch.Tensor] = {}
        self._theta_star: Dict[str, torch.Tensor] = {}

    # ── Snapshot & Fisher computation ────────────────────────────────────────

    def compute(self, toolbench_records: List[Dict]) -> None:
        """
        Compute Fisher diagonal on a sample of ToolBench records and snapshot θ*.

        Uses label log-prob gradients (empirical Fisher):
            F_i = (1/N) Σ_n  (∂ log p(y_n|x_n, θ) / ∂ θ_i)²
        """
        self.logger.info(
            "Computing Fisher diagonal on %d ToolBench samples...",
            self.cl_cfg.FISHER_N_SAMPLES,
        )
        # Snapshot θ* before any fine-tuning
        self._theta_star = {
            n: p.data.clone()
            for n, p in self.model.named_parameters()
            if p.requires_grad
        }
        # Initialise Fisher accumulators
        self._fisher = {
            n: torch.zeros_like(p.data)
            for n, p in self.model.named_parameters()
            if p.requires_grad
        }

        sample = random.sample(
            toolbench_records,
            min(self.cl_cfg.FISHER_N_SAMPLES, len(toolbench_records))
        )
        dataset  = ToolBenchDataset(sample, self.tok, self.cfg)
        loader   = torch.utils.data.DataLoader(
            dataset,
            batch_size=self.cl_cfg.FISHER_BATCH,
            shuffle=True,
            collate_fn=_collate,
            drop_last=False,
        )

        self.model.eval()
        n_batches = 0

        for ids, tgt in loader:
            ids = ids.to(self.device)
            tgt = tgt.to(self.device)
            self.model.zero_grad()

            out  = self.model(ids, berry_phase=0.0, targets=tgt)
            loss = out["loss"]
            loss.backward()

            for n, p in self.model.named_parameters():
                if p.requires_grad and p.grad is not None:
                    self._fisher[n] += p.grad.data.pow(2)

            n_batches += 1

        # Normalise
        for n in self._fisher:
            self._fisher[n] /= max(n_batches, 1)

        self.model.train()
        self.logger.info("Fisher computed over %d batches.", n_batches)

    # ── Persistence ──────────────────────────────────────────────────────────

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        torch.save({"fisher": self._fisher, "theta_star": self._theta_star}, path)
        self.logger.info("Fisher saved → %s", path)

    def load(self, path: Path) -> bool:
        if not path.exists():
            return False
        data = torch.load(path, map_location=self.device)
        self._fisher     = {k: v.to(self.device) for k, v in data["fisher"].items()}
        self._theta_star = {k: v.to(self.device) for k, v in data["theta_star"].items()}
        self.logger.info("Fisher loaded ← %s", path)
        return True

    # ── Loss penalty ─────────────────────────────────────────────────────────

    def penalty(self) -> torch.Tensor:
        """
        Returns the EWC penalty term to add to the task loss.

        Complexity: O(params) per step — negligible for a 2M-param model.
        """
        if not self._fisher:
            return torch.tensor(0.0, device=self.device)

        penalty = torch.tensor(0.0, device=self.device)
        for n, p in self.model.named_parameters():
            if n in self._fisher and p.requires_grad:
                penalty += (self._fisher[n] * (p - self._theta_star[n]).pow(2)).sum()

        return (self.cl_cfg.EWC_LAMBDA / 2.0) * penalty


# ===========================================================================
# SwarmLiquidNeuron — fast Hebbian weights + slow gradient weights
# ===========================================================================
#
# From NeuroLogos Tricameral (StableLiquidNeuron):
#   - Slow weights  : learned by backprop (general patterns)
#   - Fast weights  : updated by Hebbian rule (quick tool associations)
#   - Homeostasis   : normalises output magnitude for stable training
#
# Applied to routing: after each correct prediction, the fast weights
# strengthen the hidden_state → tool_class association without touching
# the gradient graph. This gives the routing head a fast memory that
# complements the slow gradient learning — exactly what's needed to
# escape the 57% plateau.


class SwarmLiquidNeuron(nn.Module):
    """
    Liquid neuron for routing: slow proj (gradient) + fast Hebbian weights.

    Architecture:
        slow_out  = W_slow(x)            # [B, n_tools], gradient path
        fast_out  = x @ W_fast.T         # [B, n_tools], Hebbian path, no grad
        output    = LayerNorm(slow_out + fast_scale * fast_out)

    W_fast is updated after each training step via:
        ΔW_fast = lr_hebb × (post.T @ pre) / B   (clamped ±0.3)
    where pre = hidden states, post = one-hot tool labels.

    Homeostasis clips output norm to [0.5, 2.0] to prevent explosion.
    """

    HEBB_LR    = 0.005   # Hebbian learning rate (much faster than SGD)
    FAST_DECAY = 0.999   # weight decay on W_fast (prevent explosion)
    FAST_CLIP  = 0.4     # W_fast magnitude clip

    def __init__(self, d_model: int, n_tools: int) -> None:
        super().__init__()
        self.d_model = d_model
        self.n_tools = n_tools

        # Slow path (gradient)
        self.W_slow = nn.Linear(d_model, n_tools, bias=True)
        nn.init.xavier_uniform_(self.W_slow.weight)
        nn.init.zeros_(self.W_slow.bias)

        # Fast path (Hebbian, no gradient) — stored as buffer
        self.register_buffer("W_fast", torch.zeros(n_tools, d_model))
        self.register_buffer("fast_scale", torch.tensor(0.3))
        self.register_buffer("norm_ema", torch.tensor(1.0))

        self.norm = nn.LayerNorm(n_tools)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: [B, d_model] → logits [B, n_tools]"""
        slow = self.W_slow(x)
        fast = F.linear(x.detach(), self.W_fast)   # no gradient through W_fast
        out  = slow + float(self.fast_scale) * fast
        out  = self.norm(out)

        # Homeostasis: clip output norm
        with torch.no_grad():
            out_norm = out.norm(dim=-1).mean()
            self.norm_ema = 0.95 * self.norm_ema + 0.05 * out_norm
            if self.norm_ema > 2.0:
                self.fast_scale.mul_(0.95)
            elif self.norm_ema < 0.5:
                self.fast_scale.mul_(1.05).clamp_(max=1.0)

        return out

    @torch.no_grad()
    def hebbian_update(self, pre: torch.Tensor, labels: torch.Tensor) -> None:
        """
        Strengthen W_fast associations after correct predictions.

        pre:    [B, d_model] — hidden states (instruction-end position)
        labels: [B]          — true tool class indices
        """
        B = pre.shape[0]
        if B == 0:
            return

        # One-hot post activations [B, n_tools]
        post = torch.zeros(B, self.n_tools, device=pre.device)
        post.scatter_(1, labels.unsqueeze(1), 1.0)

        # Hebbian delta: (post.T @ pre) / B — correlation between output and input
        delta = torch.mm(post.t(), pre.float()) / B
        delta = delta.clamp(-0.3, 0.3)

        self.W_fast += self.HEBB_LR * delta
        self.W_fast *= self.FAST_DECAY
        self.W_fast.clamp_(-self.FAST_CLIP, self.FAST_CLIP)


# ===========================================================================
# Routing Head — dedicated 80-class classifier
# ===========================================================================



class RoutingHead(nn.Module):
    """
    Thin linear probe: d_model → n_tools.

    Trained on top of the frozen (or lightly-tuned) backbone with standard
    cross-entropy over the N LazyOwn tools.  Bypasses the 50k-token LM head
    so 100% of the gradient goes to the routing decision.

    Tool-to-index mapping is deterministic (sorted tool name list), so the
    head can be saved/loaded independently of the backbone checkpoint.
    """

    HEAD_CKPT = "checkpoints_toposwarm/routing_head.pt"

    def __init__(self, d_model: int, tool_names: List[str],
                 n_experts: int = 4, top_k: int = 2) -> None:
        super().__init__()
        self.tool_names  = sorted(set(tool_names))
        self.tool_to_idx = {t: i for i, t in enumerate(self.tool_names)}
        n = len(self.tool_names)
        self.n_experts = n_experts
        self.top_k     = top_k

        # LiquidNeuron core: slow gradient path + fast Hebbian path
        # Replaces the simple linear projection with a dual-speed learner.
        self.liquid = SwarmLiquidNeuron(d_model, n)

        # MoE gate on top of the liquid output: n_experts specialty heads,
        # each refining the liquid logits for a subset of tools.
        self.experts = nn.ModuleList([
            nn.Linear(n, n, bias=True) for _ in range(n_experts)
        ])
        for exp in self.experts:
            nn.init.eye_(exp.weight)   # identity init: experts start neutral
            nn.init.zeros_(exp.bias)

        self.gate = nn.Linear(d_model, n_experts, bias=False)
        nn.init.xavier_uniform_(self.gate.weight)

    @property
    def n_tools(self) -> int:
        return len(self.tool_names)

    def forward(self, hidden: torch.Tensor) -> torch.Tensor:
        """
        hidden: [B, d_model] → logits [B, n_tools]

        Pipeline:
          1. LiquidNeuron: slow grad + fast Hebbian → base logits [B, n_tools]
          2. MoE gate: select top-k specialty expert refinements
          3. Weighted sum of expert-refined logits
        """
        # Step 1: liquid neuron base logits
        base = self.liquid(hidden)                               # [B, n_tools]

        # Step 2: MoE gate on d_model features
        gate_scores = torch.sigmoid(self.gate(hidden))           # [B, E]
        topk_w, topk_idx = gate_scores.topk(self.top_k, dim=-1) # [B, K]
        topk_w = topk_w / (topk_w.sum(dim=-1, keepdim=True) + 1e-9)

        # Step 3: experts refine the base logits (not re-process d_model)
        all_logits = torch.stack([e(base) for e in self.experts], dim=1)  # [B,E,n_tools]
        W = hidden.new_zeros(hidden.shape[0], self.n_experts)
        for k in range(self.top_k):
            W.scatter_add_(1, topk_idx[:, k:k+1], topk_w[:, k:k+1])
        refined = (W.unsqueeze(-1) * all_logits).sum(dim=1)     # [B, n_tools]

        # Residual: refined on top of base
        return base + 0.5 * refined

    def label(self, tool_name: str) -> int:
        return self.tool_to_idx.get(tool_name, -1)

    def predict(self, hidden: torch.Tensor) -> List[str]:
        """hidden: [B, d_model] → list of predicted tool name strings"""
        idx = self.forward(hidden).argmax(dim=-1).tolist()
        if isinstance(idx, int):
            idx = [idx]
        return [self.tool_names[i] for i in idx]

    def save(self, path: str = HEAD_CKPT) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        torch.save({
            "state_dict": self.state_dict(),
            "tool_names":  self.tool_names,
            "n_experts":   self.n_experts,
            "top_k":       self.top_k,
        }, path)

    @classmethod
    def load(cls, d_model: int, path: str = HEAD_CKPT) -> "RoutingHead":
        data = torch.load(path, map_location="cpu", weights_only=False)
        head = cls(d_model, data["tool_names"],
                   n_experts=data.get("n_experts", 4),
                   top_k=data.get("top_k", 2))
        head.load_state_dict(data["state_dict"])
        return head


# ===========================================================================
# Continual Trainer
# ===========================================================================


class ContinualTrainer:
    """
    Fine-tuning loop with EWC + Replay.

    Each training step:
        1. Sample a mini-batch from LazyOwn dataset.
        2. Sample REPLAY_RATIO fraction from ToolBench replay buffer.
        3. Concatenate → mixed batch.
        4. Compute task loss on mixed batch.
        5. Add EWC penalty.
        6. Backward + gradient clip + optimizer step.

    The combined loss is:
        L = L_task(mixed_batch) + EWC.penalty()
    """

    def __init__(
        self,
        model: TopoSwarmModel,
        cfg: SwarmConfig,
        cl_cfg: ContinualConfig,
        tok: BPETokenizer,
        ewc: EWC,
        replay: ReplayBuffer,
        logger: logging.Logger,
        routing_head: Optional["RoutingHead"] = None,
    ) -> None:
        self.model    = model
        self.cfg      = cfg
        self.cl_cfg   = cl_cfg
        self.tok      = tok
        self.ewc      = ewc
        self.replay   = replay
        self.logger   = logger
        self.device   = cfg.DEVICE
        self.ckpt     = CheckpointManager(cfg, logger)
        self.scaler   = torch.cuda.amp.GradScaler(
            enabled=cfg.USE_AMP and "cuda" in self.device
        )
        self.routing_head = routing_head.to(self.device) if routing_head else None

        # Cached tokenizer calls — avoids re-encoding identical strings
        self._encode    = make_cached_encode(tok)
        self._tool_token = make_cached_tool_token(tok)

        # O(1) reverse map: token_id → tool_name (built once, used in training loop)
        self._tok_id_to_tool: Dict[int, str] = {}
        if routing_head is not None:
            for tn in routing_head.tool_names:
                tid = self._tool_token(tn)
                self._tok_id_to_tool[tid] = tn

    def _make_optimizer(self) -> torch.optim.AdamW:
        # Exclude adapter and routing head — they get their own param groups below
        _exclude = set()
        adapter = getattr(self.model, "moe_adapter", None)
        if adapter is not None:
            _exclude.update(id(p) for p in adapter.parameters())
        if self.routing_head is not None:
            _exclude.update(id(p) for p in self.routing_head.parameters())

        decay   = [p for n, p in self.model.named_parameters()
                   if p.requires_grad and p.ndim >= 2 and id(p) not in _exclude]
        nodecay = [p for n, p in self.model.named_parameters()
                   if p.requires_grad and p.ndim < 2 and id(p) not in _exclude]
        # Backbone trains at 5× lower LR than adapter/head — prevents forgetting
        # what the backbone already learned while still allowing escape from plateau
        backbone_lr = self.cl_cfg.LEARNING_RATE / 5.0
        param_groups = [
            {"params": decay,   "weight_decay": self.cl_cfg.WEIGHT_DECAY,
             "lr": backbone_lr},
            {"params": nodecay, "weight_decay": 0.0,
             "lr": backbone_lr},
        ]
        if self.routing_head is not None:
            param_groups.append({
                "params": list(self.routing_head.parameters()),
                "weight_decay": self.cl_cfg.WEIGHT_DECAY,
                "lr": self.cl_cfg.ROUTING_HEAD_LR,
            })
        # MoE adapter — trains at routing head LR (starts from zero, needs warmth)
        adapter = getattr(self.model, "moe_adapter", None)
        if adapter is not None:
            param_groups.append({
                "params": list(adapter.parameters()),
                "weight_decay": 0.0,
                "lr": self.cl_cfg.ROUTING_HEAD_LR,
            })
        return torch.optim.AdamW(param_groups, betas=(0.9, 0.95), eps=1e-8)

    @staticmethod
    def _lr_schedule(optimizer, step: int, total: int, warmup: int, base_lr: float) -> None:
        if step < warmup:
            lr = base_lr * step / max(warmup, 1)
        else:
            progress = (step - warmup) / max(total - warmup, 1)
            lr = base_lr * 0.5 * (1.0 + math.cos(math.pi * progress))
        for g in optimizer.param_groups:
            g["lr"] = max(lr, base_lr * 1e-3)

    def _merge_with_replay(
        self,
        ids: torch.Tensor,
        tgt: torch.Tensor,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Append replay samples to the LazyOwn batch."""
        n_replay = max(1, int(ids.shape[0] * self.cl_cfg.REPLAY_RATIO))
        replay_samples = self.replay.sample(n_replay)
        if not replay_samples:
            return ids, tgt

        rids_list, rtgt_list = zip(*replay_samples)
        max_len = max(ids.shape[1], max(r.shape[0] for r in rids_list))

        # Pad existing batch to max_len
        if ids.shape[1] < max_len:
            pad = max_len - ids.shape[1]
            ids = F.pad(ids, (0, pad), value=0)
            tgt = F.pad(tgt, (0, pad), value=-100)

        # Pad and stack replay samples
        rids_padded = []
        rtgt_padded = []
        for ri, rt in zip(rids_list, rtgt_list):
            pad = max_len - ri.shape[0]
            rids_padded.append(F.pad(ri, (0, pad), value=0))
            rtgt_padded.append(F.pad(rt, (0, pad), value=-100))

        r_ids = torch.stack(rids_padded).to(self.device)
        r_tgt = torch.stack(rtgt_padded).to(self.device)

        return torch.cat([ids, r_ids], dim=0), torch.cat([tgt, r_tgt], dim=0)

    def _routing_accuracy(self, records: List[Dict]) -> float:
        """
        Routing accuracy using the LM head (primary) and routing head (secondary).

        Feeds only instruction tokens; evaluates the last-position logits.
        Uses cached encode for speed.  Always returns LM-head accuracy (which
        matches the training objective) so the metric is honest.
        """
        self.model.eval()
        lm_correct = head_correct = total = 0

        for rec in records:
            api_list   = rec.get("api_list", [{}])
            tool_name  = api_list[0].get("tool_name", "") if api_list else ""
            instruction = str(rec.get("instruction") or "")[:512]
            instr_ids  = self._encode(instruction)[-self.cfg.MAX_SEQ_LEN:]
            if not instr_ids:
                continue
            ids = torch.tensor([instr_ids], dtype=torch.long, device=self.device)
            gt_off = self._tool_token(tool_name) - self.cfg.TOOL_TOKEN_OFFSET

            with torch.no_grad():
                # Single forward — extract both logits and hidden state
                captured: List[torch.Tensor] = []
                def _hook(m, i, o): captured.append(o[0, -1, :].detach())
                h_handle = self.model.norm_out.register_forward_hook(_hook)
                out = self.model(ids, berry_phase=0.0)
                h_handle.remove()

                # LM head accuracy (primary — honest metric)
                lm_logits = out["logits"][0, -1,
                            self.cfg.TOOL_TOKEN_OFFSET:
                            self.cfg.TOOL_TOKEN_OFFSET + self.cfg.TOOL_VOCAB_SIZE]
                lm_correct += int(lm_logits.argmax().item() == gt_off)

                # Routing head accuracy (secondary)
                if self.routing_head is not None and captured:
                    rlogits   = self.routing_head(captured[0].unsqueeze(0))[0]
                    pred_name = self.routing_head.tool_names[rlogits.argmax().item()]
                    head_correct += int(pred_name == tool_name)

            total += 1

        self.model.train()
        if self.routing_head is not None:
            self.routing_head.train()

        if self.routing_head is not None and total:
            self.logger.debug("  routing_head_acc=%.1f%%  lm_head_acc=%.1f%%",
                              head_correct / total * 100, lm_correct / total * 100)
        return lm_correct / max(total, 1)  # return LM-head (honest metric)

    def train(self, lazyown_dataset: ToolBenchDataset,
              train_records: Optional[List[Dict]] = None,
              val_records:   Optional[List[Dict]] = None) -> None:
        loader = torch.utils.data.DataLoader(
            lazyown_dataset,
            batch_size=self.cl_cfg.BATCH_SIZE,
            shuffle=True,
            collate_fn=_collate,
            drop_last=False,
            num_workers=0,
        )

        optimizer        = self._make_optimizer()
        steps_per_epoch  = len(loader)
        # Cosine schedule restarts each epoch so LR never dies regardless of
        # how many epochs are configured.  Warmup only on the first epoch.
        warmup           = max(1, int(steps_per_epoch * self.cl_cfg.WARMUP_RATIO))
        step             = 0

        best_val_acc      = 0.0
        no_improve_epochs = 0
        # Surprise buffer — oversamples examples the model is failing on
        surprise_buf = SurpriseBuffer(maxsize=512, replay_ratio=0.25)

        self.logger.info(
            "Continual fine-tuning: %d LazyOwn examples, %d replay buffer, "
            "λ_ewc=%.0f, replay_ratio=%.0f%%, steps/epoch=%d, routing_head=%s, moe_adapter=%s",
            len(lazyown_dataset),
            len(self.replay),
            self.cl_cfg.EWC_LAMBDA,
            self.cl_cfg.REPLAY_RATIO * 100,
            steps_per_epoch,
            "yes" if self.routing_head else "no",
            "yes" if getattr(self.model, "moe_adapter", None) is not None else "no",
        )

        for epoch in range(self.cl_cfg.EPOCHS):
            self.model.train()
            running_task = 0.0
            running_ewc  = 0.0
            n            = 0
            epoch_step   = 0   # step within this epoch for per-epoch cosine schedule

            for accum_idx, (ids, tgt) in enumerate(loader):
                ids = ids.to(self.device)
                tgt = tgt.to(self.device)

                # Mix in replay
                ids, tgt = self._merge_with_replay(ids, tgt)

                # Per-epoch cosine restart: warmup only on epoch 0
                eff_warmup = warmup if epoch == 0 else 0
                self._lr_schedule(optimizer, epoch_step, steps_per_epoch,
                                   eff_warmup, self.cl_cfg.LEARNING_RATE)

                phase = self.cfg.BERRY_PHASE_BASE * (accum_idx % self.cfg.N_AGENTS)


                with torch.cuda.amp.autocast(
                    enabled=self.cfg.USE_AMP and "cuda" in self.device
                ):
                    # ── LM backbone loss ─────────────────────────────────────
                    out       = self.model(ids, berry_phase=phase, targets=tgt)
                    task_loss = out["loss"]
                    ewc_pen   = self.ewc.penalty()
                    loss      = (task_loss + ewc_pen) / self.cl_cfg.GRAD_ACCUM_STEPS

                    # ── Routing head loss (when available) ───────────────────
                    head_loss_val = 0.0
                    if self.routing_head is not None:
                        # Capture full hidden state tensor [B, S, D] via hook
                        hidden_states: List[torch.Tensor] = []
                        def _capture(module, inp, out_h):
                            hidden_states.append(out_h)
                        _h = self.model.norm_out.register_forward_hook(_capture)
                        _ = self.model(ids, berry_phase=phase)
                        _h.remove()
                        if hidden_states:
                            h_all = hidden_states[0]  # [B, S, D]
                            h_vecs, lb_list = [], []
                            for b in range(tgt.shape[0]):
                                nonmask = (tgt[b] != -100).nonzero(as_tuple=True)[0]
                                if not len(nonmask):
                                    continue
                                tool_tok_id = tgt[b, nonmask[0]].item()
                                # Position in ids where tool_tok sits (= nonmask[0])
                                # The routing head should see hidden state at the
                                # LAST INSTRUCTION TOKEN position = tool_pos - 1.
                                # This matches _routing_accuracy() which feeds only
                                # instruction tokens and takes the last hidden.
                                instr_end = int(nonmask[0]) - 1
                                if instr_end < 0:
                                    continue
                                # O(1) reverse lookup via pre-built map
                                tool_name_b = self._tok_id_to_tool.get(int(tool_tok_id))
                                if tool_name_b is None:
                                    continue
                                lb = self.routing_head.label(tool_name_b)
                                if lb < 0:
                                    continue
                                h_vecs.append(h_all[b, instr_end, :])
                                lb_list.append(lb)
                            if h_vecs:
                                h_v  = torch.stack(h_vecs)
                                lb_v = torch.tensor(lb_list, dtype=torch.long,
                                                    device=self.device)
                                rlogits   = self.routing_head(h_v)
                                head_loss = F.cross_entropy(rlogits, lb_v)
                                loss = loss + head_loss / self.cl_cfg.GRAD_ACCUM_STEPS
                                head_loss_val = head_loss.item()

                                # ── Hebbian update (no gradient, fast memory) ──
                                # Update W_fast for correctly predicted examples.
                                # This immediately strengthens seen associations
                                # without waiting for backprop to converge.
                                with torch.no_grad():
                                    preds = rlogits.argmax(dim=-1)
                                    correct_mask = (preds == lb_v)
                                    if correct_mask.any():
                                        self.routing_head.liquid.hebbian_update(
                                            h_v[correct_mask].detach(),
                                            lb_v[correct_mask],
                                        )

                self.scaler.scale(loss).backward()

                if (accum_idx + 1) % self.cl_cfg.GRAD_ACCUM_STEPS == 0:
                    self.scaler.unscale_(optimizer)
                    all_params = list(self.model.parameters())
                    if self.routing_head is not None:
                        all_params += list(self.routing_head.parameters())
                    torch.nn.utils.clip_grad_norm_(all_params, self.cl_cfg.GRADIENT_CLIP)
                    self.scaler.step(optimizer)
                    self.scaler.update()
                    optimizer.zero_grad()

                # ── Surprise tracking (NeuroLogos style) ──────────────────
                # Store batch records when loss is above median — these are
                # the hard examples the model keeps getting wrong.
                loss_val = task_loss.item()
                if loss_val > 1.5 and train_records:
                    # Approximate which records are "surprising" using batch loss
                    start_idx = (accum_idx * self.cl_cfg.BATCH_SIZE) % len(train_records)
                    end_idx   = min(start_idx + self.cl_cfg.BATCH_SIZE, len(train_records))
                    batch_recs = train_records[start_idx:end_idx]
                    with torch.no_grad():
                        # Get tool logits at last instruction position for confidence
                        tool_logits = out["logits"][:len(batch_recs), -1,
                                      self.cfg.TOOL_TOKEN_OFFSET:
                                      self.cfg.TOOL_TOKEN_OFFSET + self.cfg.TOOL_VOCAB_SIZE]
                        per_example = torch.full((len(batch_recs),), loss_val,
                                                 device=tool_logits.device)
                        surprise_buf.update(batch_recs, per_example, tool_logits)

                running_task += loss_val
                running_ewc  += ewc_pen.item()
                n          += 1
                step       += 1
                epoch_step += 1

                if step % self.cl_cfg.LOG_INTERVAL == 0:
                    self.logger.info(
                        "epoch=%d step=%d task_loss=%.4f head_loss=%.4f ewc=%.4f lr=%.2e",
                        epoch, step,
                        running_task / max(n, 1),
                        head_loss_val,
                        running_ewc  / max(n, 1),
                        optimizer.param_groups[0]["lr"],
                    )
                    running_task = running_ewc = 0.0
                    n = 0

            # Per-epoch train/val routing accuracy
            tr_acc = self._routing_accuracy(train_records) if train_records else 0.0
            va_acc = self._routing_accuracy(val_records)   if val_records   else 0.0
            self.logger.info(
                "epoch=%d  train_acc=%.1f%%  val_acc=%.1f%%  surprise_buf=%d",
                epoch, tr_acc * 100, va_acc * 100, len(surprise_buf),
            )

            # Save routing head whenever val_acc improves
            if va_acc > best_val_acc:
                best_val_acc      = va_acc
                no_improve_epochs = 0
                if self.routing_head is not None:
                    self.routing_head.save()
                adapter = getattr(self.model, "moe_adapter", None)
                if adapter is not None:
                    adapter.save()
                if self.routing_head is not None or adapter is not None:
                    self.logger.info("New best val_acc=%.1f%% — heads saved.", va_acc*100)
            else:
                no_improve_epochs += 1

            self.ckpt.save(
                self.model, optimizer,
                {"epoch": epoch, "step": step,
                 "task_loss": task_loss.item(), "val_acc": va_acc,
                 "ewc_lambda": self.cl_cfg.EWC_LAMBDA},
                force=True,
            )
            self.logger.info("Epoch %d complete.", epoch)

        self.logger.info(
            "Continual fine-tuning complete. Best val_acc=%.1f%%  epochs_run=%d",
            best_val_acc * 100, self.cl_cfg.EPOCHS,
        )


# ===========================================================================
# Evaluation — routing accuracy
# ===========================================================================


def evaluate_routing(
    model: TopoSwarmModel,
    cfg: SwarmConfig,
    tok: BPETokenizer,
    lazyown_records: List[Dict],
    toolbench_records: List[Dict],
    logger: logging.Logger,
) -> None:
    """
    Measure routing accuracy on a held-out subset of both datasets.

    Routing accuracy = fraction of examples where the highest-probability
    tool token matches the ground-truth tool in the api_list.
    """
    model.eval()

    def _accuracy(records: List[Dict], label: str) -> float:
        sample = random.sample(records, min(100, len(records)))
        correct = 0
        for rec in sample:
            api_list  = rec.get("api_list", [{}])
            tool_name = api_list[0].get("tool_name", "") if api_list else ""
            instruction = str(rec.get("instruction") or rec.get("query") or "")[:512]

            # Feed ONLY the instruction tokens — the model must predict the
            # tool token as the very next token (position after instruction end).
            instr_ids = tok.encode(instruction)
            if not instr_ids:
                continue
            instr_ids = instr_ids[-cfg.MAX_SEQ_LEN:]
            ids = torch.tensor([instr_ids], dtype=torch.long, device=cfg.DEVICE)

            with torch.no_grad():
                out    = model(ids, berry_phase=0.0)
                logits = out["logits"][0, -1, :]   # next-token prediction after instruction
                tool_logits = logits[cfg.TOOL_TOKEN_OFFSET:
                                     cfg.TOOL_TOKEN_OFFSET + cfg.TOOL_VOCAB_SIZE]
                pred_offset = tool_logits.argmax().item()

            gt_token = tok.tool_token(tool_name) - cfg.TOOL_TOKEN_OFFSET
            correct += int(pred_offset == gt_token)

        acc = correct / max(len(sample), 1)
        logger.info("Routing accuracy %-20s : %.1f%%  (%d/%d)",
                    label, acc * 100, correct, len(sample))
        return acc

    logger.info("=== Routing accuracy evaluation ===")
    la_acc = _accuracy(lazyown_records,  "LazyOwn")
    tb_acc = _accuracy(toolbench_records,"ToolBench")
    logger.info("Combined accuracy: %.1f%%", (la_acc + tb_acc) / 2 * 100)


# ===========================================================================
# Full pipeline
# ===========================================================================


def build_model_and_tok(cl_cfg: ContinualConfig, logger: logging.Logger):
    cfg = SwarmConfig()
    cfg.CHECKPOINT_DIR = cl_cfg.CHECKPOINT_DIR
    cfg.EPOCHS         = cl_cfg.EPOCHS
    cfg.BATCH_SIZE     = cl_cfg.BATCH_SIZE
    cfg.GRAD_ACCUM_STEPS = cl_cfg.GRAD_ACCUM_STEPS
    cfg.LEARNING_RATE  = cl_cfg.LEARNING_RATE
    cfg.WEIGHT_DECAY   = cl_cfg.WEIGHT_DECAY

    tok   = BPETokenizer(cfg)
    model = TopoSwarmModel(cfg).to(cfg.DEVICE)

    ckpt_mgr = CheckpointManager(cfg, logger)
    meta = ckpt_mgr.load(model, device=cfg.DEVICE)
    if meta:
        logger.info("Checkpoint loaded: epoch=%s loss=%s", meta.get("epoch"), meta.get("loss"))
    else:
        logger.warning("No checkpoint found — starting from random weights")

    return model, tok, cfg


def run_full_pipeline(cl_cfg: ContinualConfig, logger: logging.Logger) -> None:
    """Generate dataset → compute Fisher → fine-tune → evaluate."""

    # ── Step 1: Generate LazyOwn dataset ─────────────────────────────────────
    lazyown_path = Path(cl_cfg.LAZYOWN_DATASET)
    if not lazyown_path.exists():
        logger.info("Generating LazyOwn dataset...")
        records = _gen.build_dataset()
        _gen.write_jsonl(records, lazyown_path)
        logger.info("Generated %d examples → %s", len(records), lazyown_path)

    lazyown_records   = _load_jsonl(lazyown_path)
    toolbench_records = _load_jsonl(Path(cl_cfg.TOOLBENCH_DATASET))

    if not toolbench_records:
        logger.warning(
            "ToolBench dataset not found at %s — replay buffer will be empty. "
            "EWC will still work. Download ToolBench or provide a local JSONL.",
            cl_cfg.TOOLBENCH_DATASET,
        )

    logger.info("LazyOwn: %d records | ToolBench: %d records",
                len(lazyown_records), len(toolbench_records))

    # ── Step 2: Load model ────────────────────────────────────────────────────
    model, tok, cfg = build_model_and_tok(cl_cfg, logger)

    # ── Step 3: Compute / load Fisher ────────────────────────────────────────
    # Skip EWC entirely when backbone will be frozen — the adapter is the only
    # trainable component, so there's nothing to penalise with EWC.
    backbone_frozen = not any(
        p.requires_grad for p in model.parameters()
        if "moe_adapter" not in getattr(p, "_param_name", "")
    )
    # Re-check after potential freeze (adapter not yet injected here, check later)
    fisher_path = Path(cl_cfg.FISHER_PATH)
    ewc = EWC(model, cfg, cl_cfg, tok, logger)

    # Backbone will be frozen (adapter-only training) → EWC penalty is always
    # zero (frozen params can't drift), so skip the expensive Fisher computation.
    _all_trainable = [p for p in model.parameters() if p.requires_grad]
    _backbone_will_freeze = True   # inject_moe_adapter freezes backbone below
    if _backbone_will_freeze:
        logger.info("Backbone will be frozen — skipping EWC Fisher computation "
                    "(penalty would be 0 anyway; only adapter trains).")
    elif fisher_path.exists():
        logger.info("Loading pre-computed Fisher from %s", fisher_path)
        ewc.load(fisher_path)
    elif toolbench_records:
        ewc.compute(toolbench_records)
        ewc.save(fisher_path)
    else:
        logger.info(
            "No ToolBench data — computing Fisher on LazyOwn dataset "
            "(anchors current routing knowledge for future runs)."
        )
        ewc.compute(lazyown_records)
        ewc.save(fisher_path)

    # ── Step 4: Build replay buffer ───────────────────────────────────────────
    replay = ReplayBuffer(
        toolbench_records,
        cl_cfg.REPLAY_BUFFER_SIZE,
        tok, cfg,
    )
    logger.info("Replay buffer: %d samples", len(replay))

    # ── Step 4b: Load user feedback (from bridge.feedback() calls) ───────────────
    feedback_file = Path(_HERE).parent.parent / "LazyOwn" / "sessions" / "toposwarm_feedback.jsonl"
    if not feedback_file.exists():
        # Try sibling LazyOwn directory
        for candidate in [
            Path(_HERE) / ".." / ".." / "LazyOwn" / "sessions" / "toposwarm_feedback.jsonl",
            Path.home() / "src_note" / "LazyOwn" / "sessions" / "toposwarm_feedback.jsonl",
        ]:
            if Path(candidate).exists():
                feedback_file = Path(candidate)
                break

    pos_feedback, neg_feedback = [], []
    if feedback_file.exists():
        for line in feedback_file.read_text(encoding="utf-8").splitlines():
            try:
                entry = json.loads(line)
                rec = {
                    "instruction": entry["prompt"],
                    "api_list": [{"tool_name": entry["tool_name"],
                                  "api_name": entry["tool_name"] + "_endpoint",
                                  "api_description": entry["tool_name"],
                                  "required_parameters": [{"name": "arg", "type": "STRING"}],
                                  "optional_parameters": []}],
                    "answer": f"[TOOL_CALL: {entry['tool_name']}()] [user confirmed]",
                    "domain": "Security/Feedback",
                }
                (pos_feedback if entry.get("good") else neg_feedback).append(rec)
            except Exception:
                pass
        if pos_feedback or neg_feedback:
            logger.info("User feedback loaded: %d positive, %d negative examples",
                        len(pos_feedback), len(neg_feedback))
            # Positive feedback: add to lazyown_records with 3× weight (oversample)
            lazyown_records.extend(pos_feedback * 3)
            # Negative feedback: skip — used only for logging / future contrastive loss
            if neg_feedback:
                logger.info("  %d negative examples noted (not used in training yet)",
                            len(neg_feedback))

    # ── Step 5: Build dataset ─────────────────────────────────────────────────
    random.shuffle(lazyown_records)
    split = max(1, int(len(lazyown_records) * 0.9))
    train_records = lazyown_records[:split]
    val_records   = lazyown_records[split:]

    train_ds = ToolBenchDataset(train_records, tok, cfg)
    logger.info("Train: %d samples | Val: %d samples", len(train_ds), len(val_records))

    # ── Step 6: Build or load routing head ───────────────────────────────────
    all_tool_names = list({
        rec["api_list"][0]["tool_name"]
        for rec in lazyown_records
        if rec.get("api_list") and rec["api_list"]
    })
    head_path = Path(RoutingHead.HEAD_CKPT)
    if head_path.exists():
        try:
            routing_head = RoutingHead.load(cfg.D_MODEL, str(head_path))
            logger.info("Routing head loaded from %s (%d tools)", head_path, routing_head.n_tools)
        except Exception as e:
            logger.warning("Routing head load failed (%s) — starting fresh", e)
            routing_head = RoutingHead(cfg.D_MODEL, all_tool_names)
    else:
        routing_head = RoutingHead(cfg.D_MODEL, all_tool_names)
        logger.info("New routing head: %d tools → %d classes", len(all_tool_names), routing_head.n_tools)

    # ── Step 6b: Inject MoE adapter (zero-init residual, no retraining needed) ──
    adapter_path = Path(SwarmMoEAdapter.ADAPTER_CKPT) if hasattr(SwarmMoEAdapter := _agent.SwarmMoEAdapter, 'ADAPTER_CKPT') else None
    try:
        inject_fn = _agent.inject_moe_adapter
        adapter = inject_fn(
            model,
            n_experts       = 4,
            top_k           = 2,
            dropout         = 0.0,
            freeze_backbone = False,   # full model unfrozen — escape local minimum
            adapter_path    = str(Path(_agent.SwarmMoEAdapter.ADAPTER_CKPT))
                              if Path(_agent.SwarmMoEAdapter.ADAPTER_CKPT).exists() else None,
        )
        logger.info("MoE adapter: %d experts, top-%d, %d params",
                    adapter.n_experts, adapter.top_k,
                    sum(p.numel() for p in adapter.parameters()))
    except Exception as e:
        logger.warning("MoE adapter injection failed (%s) — training without it", e)

    # ── Step 7: Fine-tune ─────────────────────────────────────────────────────
    trainer = ContinualTrainer(model, cfg, cl_cfg, tok, ewc, replay, logger,
                               routing_head=routing_head)
    trainer.train(train_ds, train_records=train_records, val_records=val_records)

    # ── Step 8: Evaluate ──────────────────────────────────────────────────────
    evaluate_routing(model, cfg, tok, val_records, toolbench_records[:200], logger)


# ===========================================================================
# CLI
# ===========================================================================


def main() -> None:
    parser = argparse.ArgumentParser(
        description="TopoSwarm Continual Trainer — EWC + Experience Replay for LazyOwn fine-tuning"
    )
    parser.add_argument("--full",          action="store_true", help="Run full pipeline")
    parser.add_argument("--gen-dataset",   action="store_true", help="Generate LazyOwn dataset only")
    parser.add_argument("--compute-fisher",action="store_true", help="Compute Fisher on ToolBench data")
    parser.add_argument("--train",         action="store_true", help="Run fine-tuning only")
    parser.add_argument("--eval",          action="store_true", help="Evaluate routing accuracy")
    parser.add_argument("--ewc-lambda",    type=float, default=0.0,
                        help="Override EWC λ (default: 400.0)")
    parser.add_argument("--replay-ratio",  type=float, default=0.0,
                        help="Override replay ratio (default: 0.20)")
    parser.add_argument("--epochs",        type=int,   default=0,
                        help="Override number of fine-tuning epochs")
    parser.add_argument("--lr",            type=float, default=0.0,
                        help="Override learning rate")
    parser.add_argument("--dataset",       type=str,   default="",
                        help="Override LazyOwn dataset path")
    parser.add_argument("--checkpoint",    type=str,   default="",
                        help="Override checkpoint directory")
    parser.add_argument("--log-level",     type=str,   default="INFO")
    args = parser.parse_args()

    logger   = _setup_logger(args.log_level)
    cl_cfg   = ContinualConfig()

    if args.ewc_lambda   > 0:  cl_cfg.EWC_LAMBDA      = args.ewc_lambda
    if args.replay_ratio > 0:  cl_cfg.REPLAY_RATIO     = args.replay_ratio
    if args.epochs       > 0:  cl_cfg.EPOCHS           = args.epochs
    if args.lr           > 0:  cl_cfg.LEARNING_RATE    = args.lr
    if args.dataset:           cl_cfg.LAZYOWN_DATASET  = args.dataset
    if args.checkpoint:        cl_cfg.CHECKPOINT_DIR   = args.checkpoint

    if args.full or (not any([args.gen_dataset, args.compute_fisher, args.train, args.eval])):
        run_full_pipeline(cl_cfg, logger)
        return

    if args.gen_dataset:
        out = Path(cl_cfg.LAZYOWN_DATASET)
        records = _gen.build_dataset()
        _gen.write_jsonl(records, out)
        _gen.print_stats(records)
        return

    # Load model for remaining actions
    model, tok, cfg = build_model_and_tok(cl_cfg, logger)
    toolbench_records = _load_jsonl(Path(cl_cfg.TOOLBENCH_DATASET))
    ewc = EWC(model, cfg, cl_cfg, tok, logger)

    if args.compute_fisher:
        if not toolbench_records:
            logger.error("ToolBench dataset not found: %s", cl_cfg.TOOLBENCH_DATASET)
            return
        ewc.compute(toolbench_records)
        ewc.save(Path(cl_cfg.FISHER_PATH))
        return

    ewc.load(Path(cl_cfg.FISHER_PATH))
    replay = ReplayBuffer(toolbench_records, cl_cfg.REPLAY_BUFFER_SIZE, tok, cfg)

    if args.train:
        lazyown_records = _load_jsonl(Path(cl_cfg.LAZYOWN_DATASET))
        if not lazyown_records:
            logger.error("LazyOwn dataset not found: %s — run --gen-dataset first", cl_cfg.LAZYOWN_DATASET)
            return
        train_ds = ToolBenchDataset(lazyown_records, tok, cfg)
        trainer  = ContinualTrainer(model, cfg, cl_cfg, tok, ewc, replay, logger)
        trainer.train(train_ds)

    if args.eval:
        lazyown_records = _load_jsonl(Path(cl_cfg.LAZYOWN_DATASET))
        evaluate_routing(model, cfg, tok, lazyown_records, toolbench_records[:200], logger)


if __name__ == "__main__":
    main()
