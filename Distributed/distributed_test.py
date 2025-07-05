# distributed/distributed_training.py

import torch
from fastai.vision.all import cnn_learner, resnet34, accuracy, ImageDataLoaders, untar_data, URLs, get_image_files
from web4ai.distributed import train_with_checkpointing, setup_distrib, teardown_distrib
from web4ai.logger import Web4AILogger

def initialize_dataloader(batch_size=32):
    """Initialize the dataset and dataloader."""
    path = untar_data(URLs.PETS)
    dls = ImageDataLoaders.from_name_re(
        path, 
        get_image_files(path/"images"), 
        pat=r'(.+)_\d+.jpg', 
        bs=batch_size
    )
    return dls

def initialize_model(dls):
    """Initialize the CNN learner model."""
    return cnn_learner(dls, resnet34, metrics=accuracy)

def train_model(checkpoint_dir, epochs=5, gpu_id=0):
    """Train the model with checkpointing and distributed training."""
    # Setup distributed training
    setup_distrib(gpu=gpu_id)
    
    try:
        # Logger
        logger = Web4AILogger()
        logger.info("Starting distributed training...")

        # Initialize data and model
        dls = initialize_dataloader()
        learner = initialize_model(dls)

        # Training with checkpointing
        train_with_checkpointing(
            learner, 
            epochs=epochs, 
            task_name="Distributed Training Test", 
            checkpoint_dir=checkpoint_dir
        )

    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise

    finally:
        teardown_distrib()

if __name__ == "__main__":
    train_model(checkpoint_dir="./checkpoints", epochs=5, gpu_id=0)
