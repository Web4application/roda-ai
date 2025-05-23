from torchvision.models import resnet18, resnet34, resnet50
import torch.nn as nn

def get_resnet_model(name='resnet18', input_channels=3):
    model_fn = {
        'resnet18': resnet18,
        'resnet34': resnet34,
        'resnet50': resnet50
    }[name]
    model = model_fn()

    if input_channels != 3:
        model.conv1 = nn.Conv2d(input_channels, 64, kernel_size=7, stride=2, padding=3, bias=False)

    return model
