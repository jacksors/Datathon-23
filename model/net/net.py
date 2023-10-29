import torch
from torch import nn
from torch.nn import functional as F
from torchvision.utils import save_image, make_grid
import numpy as np
from PIL import Image

class Block(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, downsample: bool):
        super().__init__()
        if downsample:
            self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=2, padding=1)
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=2),
                nn.BatchNorm2d(out_channels)
            )
        else:
            self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=1, padding=1)
            self.shortcut = nn.Sequential()
            
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
    def forward(self, x):
        shortcut = self.shortcut(x)
        x = nn.ReLU()(self.bn1(self.conv1(x)))
        x = nn.ReLU()(self.bn2(self.conv2(x)))
        x = x + shortcut
        return nn.ReLU()(x)

class Net(nn.Module):
    def __init__(self, num_classes: int = 10, save_images: bool = False):
        super().__init__()
        
        self.save_images = save_images
        
        self.layer0 = nn.Sequential(
            nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU()
        )

        self.layer1 = nn.Sequential(
            Block(64, 64, downsample=False),
            Block(64, 64, downsample=False)
        )

        self.layer2 = nn.Sequential(
            Block(64, 128, downsample=True),
            Block(128, 128, downsample=False)
        )

        self.layer3 = nn.Sequential(
            Block(128, 256, downsample=True),
            Block(256, 256, downsample=False)
        )


        self.layer4 = nn.Sequential(
            Block(256, 512, downsample=True),
            Block(512, 512, downsample=False)
        )

        self.gap = torch.nn.AdaptiveAvgPool2d(1)
        self.dropout = nn.Dropout(p=0.75)
        self.fc = torch.nn.Linear(512, num_classes)

    def forward(self, x):
        if self.save_images:
            activations = {}
        
        x = self.layer0(x)
        if self.save_images: activations[0] = x
        
        x = self.layer1(x)
        if self.save_images: activations[1] = x
        
        x = self.layer2(x)
        if self.save_images: activations[2] = x
        
        x = self.layer3(x)
        if self.save_images: activations[3] = x
        
        x = self.layer4(x)
        if self.save_images: activations[4] = x
        
        if self.save_images: self.activations = activations       
        
        x = self.gap(x)
        x = torch.flatten(x, start_dim=1)
        x = self.dropout(x)
        x = self.fc(x)

        return x
