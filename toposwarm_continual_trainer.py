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
import torch.nn.functional as F

# ---------------------------------------------------------------------------
# Import sibling modules
# ---------------------------------------------------------------------------

_HERE = Path(__file__).parent.resolve()


def _import(name: str, filename: str):
    for candidate in [_HERE / filename, Path.cwd() / filename]:
        if candidate.exists():
            spec = importlib.util.spec_from_file_location(name, candidate)
            mod  = importlib.util.module_from_spec(spec)
            sys.modules[name] = mod
            spec.loader.exec_module(mod)
            return mod
    raise FileNotFoundError(f"{filename} not found")


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
    EWC_LAMBDA:        float = 400.0   # penalty strength; higher = less forgetting
    FISHER_N_SAMPLES:  int   = 512     # ToolBench samples to estimate Fisher diagonal
    FISHER_BATCH:      int   = 4       # batch size for Fisher estimation

    # ── Replay ───────────────────────────────────────────────────────────────
    REPLAY_RATIO:      float = 0.20    # fraction of each batch from replay buffer
    REPLAY_BUFFER_SIZE:int   = 600     # max ToolBench examples in memory

    # ── Training ─────────────────────────────────────────────────────────────
    EPOCHS:            int   = 2       # fine-tuning epochs (low to avoid forgetting)
    LEARNING_RATE:     float = 2e-5    # 15× lower than original 3e-4
    BATCH_SIZE:        int   = 4
    GRAD_ACCUM_STEPS:  int   = 4
    WARMUP_RATIO:      float = 0.10
    GRADIENT_CLIP:     float = 0.5    # tighter than original (1.0)
    WEIGHT_DECAY:      float = 0.05

    # ── Logging ───────────────────────────────────────────────────────────────
    LOG_INTERVAL:      int   = 10
    EVAL_INTERVAL:     int   = 50
    LOG_LEVEL:         str   = "INFO"


# ===========================================================================
# Logging
# ===========================================================================


def _setup_logger(level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger("TopoSwarmCL")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    if not logger.handlers:
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(logging.Formatter(
            "%(asctime)s %(name)-18s %(levelname)-8s %(message)s"
        ))
        logger.addHandler(h)
    return logger


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

    Uses the same format as BPETokenizer.encode_tool_trace() so the fine-tuning
    distribution exactly matches the original pretraining distribution.
    """
    try:
        api_list = record.get("api_list", [{}])
        tool_name = api_list[0].get("tool_name", "unknown") if api_list else "unknown"
        instruction = record.get("instruction", "")
        answer = record.get("answer", "")

        text = (
            f"query: {instruction}\n"
            f"api_list: {json.dumps(api_list)}\n"
            f"domain: {record.get('domain', 'General')}"
        )
        tool_token_id = tok.tool_token(tool_name)
        instruction_ids = tok.encode(text)
        result_ids      = tok.encode(answer)

        ids = instruction_ids + [tool_token_id] + result_ids
        ids = [min(i, cfg.VOCAB_SIZE - 1) for i in ids]

        if len(ids) < 4:
            return None

        ids = ids[-cfg.MAX_SEQ_LEN:]
        input_ids  = ids[:-1]
        target_ids = ids[1:]
        return input_ids, target_ids

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

    def _make_optimizer(self) -> torch.optim.AdamW:
        decay = [p for n, p in self.model.named_parameters()
                 if p.requires_grad and p.ndim >= 2]
        nodecay = [p for n, p in self.model.named_parameters()
                   if p.requires_grad and p.ndim < 2]
        return torch.optim.AdamW(
            [{"params": decay,   "weight_decay": self.cl_cfg.WEIGHT_DECAY},
             {"params": nodecay, "weight_decay": 0.0}],
            lr=self.cl_cfg.LEARNING_RATE,
            betas=(0.9, 0.95),
            eps=1e-8,
        )

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

    def train(self, lazyown_dataset: ToolBenchDataset) -> None:
        loader = torch.utils.data.DataLoader(
            lazyown_dataset,
            batch_size=self.cl_cfg.BATCH_SIZE,
            shuffle=True,
            collate_fn=_collate,
            drop_last=False,
            num_workers=0,
        )

        optimizer   = self._make_optimizer()
        total_steps = len(loader) * self.cl_cfg.EPOCHS
        warmup      = max(1, int(total_steps * self.cl_cfg.WARMUP_RATIO))
        step        = 0

        self.logger.info(
            "Continual fine-tuning: %d LazyOwn examples, %d replay buffer, "
            "λ_ewc=%.0f, replay_ratio=%.0f%%",
            len(lazyown_dataset),
            len(self.replay),
            self.cl_cfg.EWC_LAMBDA,
            self.cl_cfg.REPLAY_RATIO * 100,
        )

        for epoch in range(self.cl_cfg.EPOCHS):
            self.model.train()
            running_task = 0.0
            running_ewc  = 0.0
            n = 0

            for accum_idx, (ids, tgt) in enumerate(loader):
                ids = ids.to(self.device)
                tgt = tgt.to(self.device)

                # Mix in replay
                ids, tgt = self._merge_with_replay(ids, tgt)

                self._lr_schedule(optimizer, step, total_steps, warmup,
                                   self.cl_cfg.LEARNING_RATE)

                phase = self.cfg.BERRY_PHASE_BASE * (accum_idx % self.cfg.N_AGENTS)

                with torch.cuda.amp.autocast(
                    enabled=self.cfg.USE_AMP and "cuda" in self.device
                ):
                    out       = self.model(ids, berry_phase=phase, targets=tgt)
                    task_loss = out["loss"]
                    ewc_pen   = self.ewc.penalty()
                    loss      = (task_loss + ewc_pen) / self.cl_cfg.GRAD_ACCUM_STEPS

                self.scaler.scale(loss).backward()

                if (accum_idx + 1) % self.cl_cfg.GRAD_ACCUM_STEPS == 0:
                    self.scaler.unscale_(optimizer)
                    torch.nn.utils.clip_grad_norm_(
                        self.model.parameters(), self.cl_cfg.GRADIENT_CLIP
                    )
                    self.scaler.step(optimizer)
                    self.scaler.update()
                    optimizer.zero_grad()

                running_task += task_loss.item()
                running_ewc  += ewc_pen.item()
                n   += 1
                step += 1

                if step % self.cl_cfg.LOG_INTERVAL == 0:
                    self.logger.info(
                        "epoch=%d step=%d task_loss=%.4f ewc_pen=%.4f lr=%.2e",
                        epoch, step,
                        running_task / max(n, 1),
                        running_ewc  / max(n, 1),
                        optimizer.param_groups[0]["lr"],
                    )
                    running_task = running_ewc = 0.0
                    n = 0

            # Save after each epoch
            self.ckpt.save(self.model, optimizer, epoch, step, task_loss.item())
            self.logger.info("Epoch %d complete. Checkpoint saved.", epoch)

        self.logger.info("Continual fine-tuning complete.")


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
            enc = _encode_record(rec, tok, cfg)
            if enc is None:
                continue
            inp, _ = enc
            ids    = torch.tensor([inp[-cfg.MAX_SEQ_LEN:]], dtype=torch.long, device=cfg.DEVICE)
            with torch.no_grad():
                out    = model(ids, berry_phase=0.0)
                logits = out["logits"][0, -1, :]                # last position
                # Restrict to tool-token range
                tool_logits = logits[cfg.TOOL_TOKEN_OFFSET: cfg.TOOL_TOKEN_OFFSET + cfg.TOOL_VOCAB_SIZE]
                pred_offset = tool_logits.argmax().item()

            # Ground truth tool token
            api_list  = rec.get("api_list", [{}])
            tool_name = api_list[0].get("tool_name", "") if api_list else ""
            gt_token  = tok.tool_token(tool_name) - cfg.TOOL_TOKEN_OFFSET
            correct  += int(pred_offset == gt_token)
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
    fisher_path = Path(cl_cfg.FISHER_PATH)
    ewc = EWC(model, cfg, cl_cfg, tok, logger)

    if fisher_path.exists():
        logger.info("Loading pre-computed Fisher from %s", fisher_path)
        ewc.load(fisher_path)
    elif toolbench_records:
        ewc.compute(toolbench_records)
        ewc.save(fisher_path)
    else:
        logger.warning("No ToolBench data — EWC disabled (penalty will be 0)")

    # ── Step 4: Build replay buffer ───────────────────────────────────────────
    replay = ReplayBuffer(
        toolbench_records,
        cl_cfg.REPLAY_BUFFER_SIZE,
        tok, cfg,
    )
    logger.info("Replay buffer: %d samples", len(replay))

    # ── Step 5: Build dataset ─────────────────────────────────────────────────
    random.shuffle(lazyown_records)
    split = max(1, int(len(lazyown_records) * 0.9))
    train_records = lazyown_records[:split]
    val_records   = lazyown_records[split:]

    train_ds = ToolBenchDataset(train_records, tok, cfg)
    logger.info("Train: %d samples | Val: %d samples", len(train_ds), len(val_records))

    # ── Step 6: Fine-tune ─────────────────────────────────────────────────────
    trainer = ContinualTrainer(model, cfg, cl_cfg, tok, ewc, replay, logger)
    trainer.train(train_ds)

    # ── Step 7: Evaluate ──────────────────────────────────────────────────────
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
