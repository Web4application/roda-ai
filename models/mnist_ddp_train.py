import os
import torch
import torch.nn as nn
import torch.multiprocessing as mp
import torch.distributed as dist
from fastai.vision.all import *

# Modify ResNet18 for 1-channel (grayscale)
def get_grayscale_resnet18():
    model = resnet18()
    model.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
    return model

def setup(rank, world_size):
    dist.init_process_group(
        backend='nccl',  # Use 'gloo' for CPU
        init_method='env://',
        world_size=world_size,
        rank=rank
    )
    torch.cuda.set_device(rank)

def cleanup():
    dist.destroy_process_group()

def ddp_main(rank, world_size):
    setup(rank, world_size)

    # Load MNIST data
    path = untar_data(URLs.MNIST)
    items = get_image_files(path)
    splits = GrandparentSplitter(train_name='training', valid_name='testing')(items)

    # Dataloaders with DistributedSampler
    def build_dls():
        dsrc = Datasets(items, tfms=[[PILImageBW.create], [parent_label, Categorize()]], splits=splits)
        dls = dsrc.dataloaders(
            bs=256,
            after_item=[Resize(224), ToTensor(), IntToFloatTensor()],
            after_batch=[Normalize.from_stats(*imagenet_stats)],
            num_workers=2,
        )
        for dl in dls.loaders:
            dl.shuffle = False
            dl.drop_last = True
            dl.sampler = torch.utils.data.distributed.DistributedSampler(
                dl.dataset, num_replicas=world_size, rank=rank
            )
        return dls

    dls = build_dls()

    # Initialize model and wrap in DDP
    model = get_grayscale_resnet18().to(rank)
    ddp_model = nn.parallel.DistributedDataParallel(model, device_ids=[rank])

    # Train
    learn = Learner(dls, ddp_model, loss_func=CrossEntropyLossFlat(), metrics=accuracy).to_fp32()
    learn.fit_one_cycle(1, 1e-2)

    # Save model from rank 0 only
    if rank == 0:
        learn.save('mnist_ddp_model')
        learn.export('mnist_ddp_export.pkl')

    cleanup()

def run_ddp():
    world_size = torch.cuda.device_count()
    mp.spawn(ddp_main, args=(world_size,), nprocs=world_size, join=True)

if __name__ == '__main__':
    run_ddp()
