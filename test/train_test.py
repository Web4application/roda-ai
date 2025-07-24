# myapp/train_test.py

import torch
from fastai.vision.all import cnn_learner, resnet34, accuracy, ImageDataLoaders
from web4ai.distributed import train_with_checkpointing, setup_distrib, teardown_distrib
from web4ai.logger import Web4AILogger

def main():
    # Load Configuration
    checkpoint_dir = "./checkpoints/"
    task_name = "Distributed Training Test"
    
    # Initialize Dataset
    path = untar_data(URLs.PETS)
    dls = ImageDataLoaders.from_name_re(path, get_image_files(path/"images"), pat=r'(.+)_\d+.jpg', bs=32)

    # Initialize Model
    learner = cnn_learner(dls, resnet34, metrics=accuracy)

    # Distributed Training
    train_with_checkpointing(learner, epochs=5, task_name=task_name, checkpoint_dir=checkpoint_dir)

if __name__ == "__main__":
    # Set up distributed training
    setup_distrib(gpu=0)  # Adjust GPU ID as needed
    try:
        main()
    finally:
        teardown_distrib()
