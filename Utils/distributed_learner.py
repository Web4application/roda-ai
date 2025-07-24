from distributed_learner import ParallelTrainer, DistributedTrainer, distrib_ctx

# Updated FastAI Distributed Learner Helper
from fastai.callback.core import Callback
from fastai.learner import Learner
from fastai.data.load import TfmdDL
from torch.nn.parallel import DataParallel, DistributedDataParallel
from accelerate import Accelerator
import torch, os
from contextlib import contextmanager

def setup_distrib():
    if not torch.distributed.is_initialized():
        torch.distributed.init_process_group(backend='nccl', init_method='env://')

def teardown_distrib():
    if torch.distributed.is_initialized():
        torch.distributed.destroy_process_group()

def rank0_first(func):
    def wrapper(*args, **kwargs):
        if torch.distributed.get_rank() == 0:
            result = func(*args, **kwargs)
        torch.distributed.barrier()
        if torch.distributed.get_rank() != 0:
            result = func(*args, **kwargs)
        return result
    return wrapper

class ParallelTrainer(Callback):
    def before_fit(self):
        if torch.cuda.device_count() > 1:
            self.learn.model = DataParallel(self.learn.model)

class DistributedTrainer(Callback):
    def before_fit(self):
        self.accel = Accelerator()
        self.learn.model, self.learn.opt = self.accel.prepare(self.learn.model, self.learn.opt)
        self.learn.dls.train = self.accel.prepare(self.learn.dls.train)
        self.learn.dls.valid = self.accel.prepare(self.learn.dls.valid)

    def after_fit(self):
        self.accel.end_training()

class DistributedDL(TfmdDL):
    def __iter__(self):
        for batch in super().__iter__():
            yield batch

Learner.to_parallel = lambda self: self.add_cb(ParallelTrainer())
Learner.to_distributed = lambda self: self.add_cb(DistributedTrainer())
Learner.detach_parallel = lambda self: self.remove_cb(ParallelTrainer)
Learner.detach_distributed = lambda self: self.remove_cb(DistributedTrainer)

@contextmanager
def distrib_ctx():
    setup_distrib()
    try:
        yield
    finally:
        teardown_distrib()
