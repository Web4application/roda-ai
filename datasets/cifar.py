from fastai.vision.all import *

def get_dataloaders(rank, world_size):
    path = untar_data(URLs.CIFAR)
    items = get_image_files(path)
    splits = GrandparentSplitter()(items)

    dsrc = Datasets(items, [[PILImage.create], [parent_label, Categorize()]], splits=splits)
    dls = dsrc.dataloaders(bs=64, after_item=[Resize(224), ToTensor(), IntToFloatTensor()],
                           after_batch=[Normalize.from_stats(*imagenet_stats)])

    for dl in dls.loaders:
        dl.shuffle = False
        dl.drop_last = True
        dl.sampler = torch.utils.data.distributed.DistributedSampler(dl.dataset, num_replicas=world_size, rank=rank)
    return dls
