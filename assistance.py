from __future__ import annotations
import os
import math
from contextlib import contextmanager
from functools import partial
import torch
from torch import nn, LongTensor
from torch.utils.data import DataLoader
from fastcore.foundation import patch, store_attr, attrgetter, delegates
from fastai.callback.core import Callback
from fastai.learner import Learner
from fastai.data.load import DataLoaders, TfmdDL, _FakeLoader
from fastai.optimizer import OptimWrapper
from fastai.callback.progress import ProgressCallback
from accelerate import Accelerator
from torch.optim.lr_scheduler import ReduceLROnPlateau
import wandb

__all__ = [
    'ParallelTrainer', 'setup_distrib', 'teardown_distrib', 
    'DistributedDL', 'DistributedTrainer', 'rank0_first',
    'train_with_checkpointing'
]

# ==== Helper Functions ==== #

def _round_to_multiple(number, multiple):
    """Rounds `number` to the next multiple of `multiple`."""
    return int(math.ceil(number / multiple) * multiple)

# ==== Data Parallel Trainer ==== #

@patch
def reset(self: nn.DataParallel):
    if hasattr(self.module, 'reset'):
        self.module.reset()

class ParallelTrainer(Callback):
    run_after, run_before = ProgressCallback, None
    
    def __init__(self, device_ids): 
        self.device_ids = device_ids
    
    def before_fit(self):
        self.learn.model = nn.DataParallel(self.learn.model, device_ids=self.device_ids)
    
    def after_fit(self):
        self.learn.model = self.learn.model.module

@patch
def to_parallel(self: Learner, device_ids=None):
    self.add_cb(ParallelTrainer(device_ids))
    return self

@patch
def detach_parallel(self: Learner):
    self.remove_cb(ParallelTrainer)
    return self

# ==== Distributed Data Loader ==== #

class DistributedDL(TfmdDL):
    def __init__(self, dl, rank=None, world_size=None, device=None):
        if rank is None: rank = rank_distrib()
        if world_size is None: world_size = num_distrib()
        store_attr()
        if device is None: self.device = self.dl.device

    def _broadcast(self, t, rank):
        t = LongTensor(t).cuda()
        torch.distributed.broadcast(t, rank)
        return t.cpu().tolist()

    def get_idxs(self):
        idxs = list(self.dl.get_idxs())
        idxs = self._broadcast(idxs, 0)
        self.n = len(idxs)
        self.n_padded = _round_to_multiple(self.n, self.world_size)
        idxs += (idxs * (self.n_padded // self.n))[:self.n_padded - self.n]
        return idxs[self.rank * self.n_padded // self.world_size : (self.rank + 1) * self.n_padded // self.world_size]

# ==== Distributed Trainer with Checkpointing and Logging ==== #

class DistributedTrainer(Callback):
    order = 11
    
    @delegates(Accelerator)
    def __init__(self, sync_bn=True, log_with="wandb", log_dir="./logs", checkpoint_dir="./checkpoints", **kwargs):
        store_attr()
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        self.accelerator = Accelerator(**kwargs)
        if self.log_with == "wandb":
            wandb.init(project="RODAAI-Distributed", dir=self.log_dir)

    def before_fit(self):
        self.learn.model = self.accelerator.prepare(
            nn.SyncBatchNorm.convert_sync_batchnorm(self.learn.model) if self.sync_bn else self.learn.model
        )
        self.scheduler = ReduceLROnPlateau(self.learn.opt, patience=5, factor=0.5, verbose=True)

    def after_batch(self):
        if self.log_with == "wandb":
            wandb.log({"loss": self.learn.loss.item()})

    def after_epoch(self):
        checkpoint_path = os.path.join(self.checkpoint_dir, f"model_epoch_{self.learn.epoch}.pt")
        torch.save(self.learn.model.state_dict(), checkpoint_path)
        self.scheduler.step(self.learn.loss.item())

    def after_fit(self):
        if self.log_with == "wandb":
            wandb.finish()

@patch
@delegates(Accelerator)
def to_distributed(self: Learner, sync_bn=True, **kwargs):
    self.add_cb(DistributedTrainer(sync_bn, **kwargs))
    if rank_distrib(): self.remove_cb(ProgressCallback())
    return self

@patch
def detach_distributed(self: Learner):
    if num_distrib() <= 1: return self
    self.remove_cb(DistributedTrainer)
    if rank_distrib(): self.add_cb(ProgressCallback())
    return self

# ==== Training Loop with Checkpointing ==== #

def train_with_checkpointing(learner, epochs, checkpoint_dir="./checkpoints"):
    os.makedirs(checkpoint_dir, exist_ok=True)
    start_epoch = 0
    checkpoint_path = os.path.join(checkpoint_dir, "last_checkpoint.pt")

    if os.path.exists(checkpoint_path):
        checkpoint = torch.load(checkpoint_path)
        learner.model.load_state_dict(checkpoint['model_state'])
        learner.opt.load_state_dict(checkpoint['optimizer_state'])
        start_epoch = checkpoint['epoch']

    for epoch in range(start_epoch, epochs):
        try:
            learner.fit_one_cycle(1)
            torch.save({
                'epoch': epoch + 1,
                'model_state': learner.model.state_dict(),
                'optimizer_state': learner.opt.state_dict(),
            }, checkpoint_path)
        except KeyboardInterrupt:
            print("Training interrupted. Saving checkpoint...")
            torch.save({
                'epoch': epoch,
                'model_state': learner.model.state_dict(),
                'optimizer_state': learner.opt.state_dict(),
            }, checkpoint_path)
            break

# ==== Utilities ==== #

def setup_distrib(gpu=None):
    if gpu is None: return gpu
    torch.cuda.set_device(gpu)
    torch.distributed.init_process_group(backend='nccl', init_method='env://')

def teardown_distrib():
    if torch.distributed.is_initialized():
        torch.distributed.destroy_process_group()

def rank_distrib():
    return torch.distributed.get_rank() if torch.distributed.is_initialized() else 0

def num_distrib():
    return torch.distributed.get_world_size() if torch.distributed.is_initialized() else 1

def rank0_first(func, *args, **kwargs):
    if args or kwargs: func = partial(func, *args, **kwargs)
    dummy_l = Learner(DataLoaders(device='cpu'), nn.Linear(1,1), loss_func=lambda: 0)
    with dummy_l.distrib_ctx():
        if not rank_distrib(): res = func()
        torch.distributed.barrier()
        if rank_distrib(): res = func()
    return res
