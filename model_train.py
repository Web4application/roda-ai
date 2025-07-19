# myapp/model_train.py
import argparse, os
import torch, torch.multiprocessing as mp, torch.distributed as dist
from fastai.vision.all import *
from datasets import mnist, cifar, imagenet, custom
from models.resnet_gray import get_resnet_model
from utils.save_load import save_checkpoint_if_master

def setup(rank, world_size):
    dist.init_process_group("nccl", init_method='env://', rank=rank, world_size=world_size)
    torch.cuda.set_device(rank)

def cleanup():
    dist.destroy_process_group()

def get_dataset(name):
    return {
        'mnist': mnist.get_dataloaders,
        'cifar': cifar.get_dataloaders,
        'imagenet': imagenet.get_dataloaders,
        'custom': custom.get_dataloaders
    }[name]

def train(rank, world_size, dataset_name, model_name, epochs):
    setup(rank, world_size)

    get_dls = get_dataset(dataset_name)
    dls = get_dls(rank, world_size)

    model = get_resnet_model(model_name, input_channels=dls.one_batch()[0].shape[1]).to(rank)
    model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[rank])

    learn = Learner(dls, model, loss_func=CrossEntropyLossFlat(), metrics=accuracy).to_fp32()
    learn.fit_one_cycle(epochs, 1e-2)

    save_checkpoint_if_master(learn, rank, f'{dataset_name}-{model_name}')

    cleanup()

def run_ddp(args):
    world_size = torch.cuda.device_count()
    mp.spawn(train, args=(world_size, args.dataset, args.model, args.epochs), nprocs=world_size, join=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, default='mnist', choices=['mnist', 'cifar', 'imagenet', 'custom'])
    parser.add_argument('--model', type=str, default='resnet18')
    parser.add_argument('--epochs', type=int, default=1)
    args = parser.parse_args()
    run_ddp(args)
