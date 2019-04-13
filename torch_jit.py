import time

import numpy as np
import torch
from torchvision import models

from utils.apex_utils import get_dataloaders

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

dataloaders, dataset_sizes, class_names = get_dataloaders(data_dir='hymenoptera_data')
dataloader = dataloaders['train']
batch_size = 4

resnet = torch.jit.trace(models.resnet18(pretrained=True).to(device), torch.rand(batch_size, 3, 224, 224).to(device))


def resnet_infer(inputs):
    cuda_tensor = inputs.to(device)
    return resnet(cuda_tensor).argmax(1)


def process_set(model_infer, model_name):
    times = []
    for inputs, values in dataloader:
        time1 = time.time()
        model_infer(inputs)
        time2 = time.time()
        times.append(time2 - time1)
    print(f"Avegage FPS - {model_name}:", 4 / np.mean(times[1:]))


process_set(model_infer=resnet_infer, model_name='resnet_jit_fp32')
