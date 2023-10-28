import os
import pandas as pd
from torchvision.io import read_image
import torch.utils.data
import typing as t
import torchvision.transforms as transforms
import csv

from utils.strokes_to_image import strokes_to_image

class Dataset(torch.utils.data.Dataset):
    def __init__(self, strokes_dir: str, limit_samples: bool = True, samples_per_class: int = 100, img_transform: t.Callable[[torch.Tensor], torch.Tensor] = None, label_transform: t.Callable[[int], int] = None):
        data = {}
        for file in os.listdir(strokes_dir):
            fname = os.fsdecode(file)
            df = pd.read_json("/home/jackson/Documents/Datathon/model/data/google/" + fname, lines=True, nrows=100)[['word', 'drawing']]
            if df.shape[0] == 100:
                data[fname] = df
                
        data = pd.concat(data, ignore_index=True)
        self.df = data
        self.img_transform = img_transform
        self.label_transform = label_transform
        unique_classes = self.df['word'].unique()

        # Create a dictionary of classes and their corresponding index
        self.class_to_idx = {unique_classes[i]: i for i in range(len(unique_classes))}
        
        # Save to a csv for later use
        with open("classes.csv", "w+") as f:
            writer = csv.writer(f)
            for key, value in self.class_to_idx.items():
                writer.writerow([value, key])
              
    def __len__(self):
        return self.df.shape[0]
    
    def __getitem__(self, idx) -> t.Tuple[torch.Tensor, str]:
        image = strokes_to_image(self.df.iloc[idx, 1])
        
        transform = transforms.Compose([
            transforms.ToTensor(),
        ])
        
        tensor_img: torch.Tensor = transform(image)
        
        label = self.df.iloc[idx, 0]
        
        if self.img_transform:
            tensor_img = self.img_transform(image)
            
        if self.label_transform:
            label = self.label_transform(label)
            
        return tensor_img, torch.tensor(self.class_to_idx[label], dtype=torch.long)