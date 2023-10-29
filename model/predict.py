import pandas as pd
from .net import net
import torch
from .utils.strokes_to_image import strokes_to_image
from torchvision import transforms
import typing as t
import csv
import numpy as np

def convert(strokes: pd.DataFrame) -> torch.Tensor:
    image = strokes_to_image(strokes)
    
    # convert the image to a tensor
    transform = transforms.Compose([
        transforms.ToTensor(),
    ])
    
    tensor_img: torch.Tensor = transform(image)
    
    return tensor_img

def predict(strokes: pd.DataFrame, weights: str, val_to_string_map: str) -> str:
    map = {}
    with open(val_to_string_map, "r") as f:
        reader = csv.reader(f)
        map = {int(rows[0]): rows[1] for rows in reader}
    
    model = net.Net()
    model.load_state_dict(torch.load(weights))
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    tensor_img = convert(strokes).to(device).unsqueeze(0)
    model.eval()
    
    with torch.no_grad():
        predictions = model(tensor_img)
        
        # Get the predicted class with the highest score
        prob, predicted = torch.max(predictions.data, 1)
        return map[predicted.item()], np.exp(prob.item())