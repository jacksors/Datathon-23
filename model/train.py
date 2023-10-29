import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data as data

import torchvision.transforms as transforms
import torchvision.datasets as datasets

from sklearn import decomposition
from sklearn import manifold
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import classification_report
from tqdm import tqdm, trange
import matplotlib.pyplot as plt
import numpy as np

import copy
import random
import time

import dataset

import net.net as net

def train(strokes_dir = "/home/jackson/Documents/Datathon-23/model/data/datathon/", batch_size = 32, learning_rate = 0.001, epochs = "auto", samples_per_class = None):
    SEED = np.random.randint(0, 10000)

    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    torch.cuda.manual_seed(SEED)
    torch.backends.cudnn.deterministic = True

    all_data = None
    if samples_per_class is None:
        all_data = dataset.Dataset(strokes_dir, limit_samples=False)
    else:
        all_data = dataset.Dataset(strokes_dir, limit_samples=True, samples_per_class=samples_per_class)

    train_data, validation_data, test_data = data.random_split(all_data, [0.7, 0.2, 0.1])

    BATCH_SIZE = batch_size

    train_iterator = data.DataLoader(train_data, shuffle=True, batch_size=BATCH_SIZE)
    valid_iterator = data.DataLoader(validation_data, batch_size=BATCH_SIZE)
    test_iterator = data.DataLoader(test_data, batch_size=BATCH_SIZE)

    print(f"Number of training examples: {len(train_data)}")
    print(f"Number of validation examples: {len(validation_data)}")
    print(f"Number of testing examples: {len(test_data)}")

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = net.Net(num_classes=len(all_data.unique_classes)).to(device)


    def count_parameters(model):
        return sum(p.numel() for p in model.parameters() if p.requires_grad)

    print(f'The model has {count_parameters(model):,} trainable parameters')

    optimizer = optim.Adam(model.parameters())

    critereon = nn.CrossEntropyLoss()

    critereon = critereon.to(device)

    def calculate_accuracy(y_pred, y):
        top_pred = y_pred.argmax(1, keepdim=True)
        correct = top_pred.eq(y.view_as(top_pred)).sum()
        acc = correct.float() / y.shape[0]
        return acc

    def train(model: nn.Module, iterator, optimizer, critereon, device):
        
        epoch_loss = 0
        epoch_acc = 0
        
        model.train()
        
        for x, y in tqdm(iterator, desc="Training", leave=False):
            x = x.to(device)
            y = y.to(device)
            
            optimizer.zero_grad()
            
            y_pred = model(x)
            
            loss = critereon(y_pred, y)

            acc = calculate_accuracy(y_pred, y)

            loss.backward()

            optimizer.step()

            epoch_loss += loss.item()
            epoch_acc += acc.item()

        return epoch_loss / len(iterator), epoch_acc / len(iterator)

    def evaluate(model: nn.Module, iterator, criterion, device):

        epoch_loss = 0
        epoch_acc = 0

        model.eval()

        with torch.no_grad():

            for (x, y) in tqdm(iterator, desc="Evaluating", leave=False):

                x = x.to(device)
                y = y.to(device)

                y_pred = model(x)

                loss = criterion(y_pred, y)

                acc = calculate_accuracy(y_pred, y)

                epoch_loss += loss.item()
                epoch_acc += acc.item()

        return epoch_loss / len(iterator), epoch_acc / len(iterator)

    def epoch_time(start_time, end_time):
        elapsed_time = end_time - start_time
        elapsed_mins = int(elapsed_time / 60)
        elapsed_secs = int(elapsed_time - (elapsed_mins * 60))
        return elapsed_mins, elapsed_secs

    # Epochs is number of samples / batch size    
    best_valid_loss = float('inf')

    no_improvement_counter = 0

    for epoch in trange(epochs if epochs != "auto" else 1000, desc="Epochs"):

        start_time = time.monotonic()

        train_loss, train_acc = train(model, train_iterator, optimizer, critereon, device)
        valid_loss, valid_acc = evaluate(model, valid_iterator, critereon, device)

        if valid_loss < best_valid_loss:
            best_valid_loss = valid_loss
            torch.save(model.state_dict(), 'tut2-model.pt')
        elif epochs == "auto":
            no_improvement_counter += 1
            if no_improvement_counter >= 10:
                print(f"ending early, no improvement in {no_improvement_counter} epochs")
                break

        end_time = time.monotonic()

        epoch_mins, epoch_secs = epoch_time(start_time, end_time)

        print(f'Epoch: {epoch+1:02} | Epoch Time: {epoch_mins}m {epoch_secs}s')
        print(f'\tTrain Loss: {train_loss:.3f} | Train Acc: {train_acc*100:.2f}%')
        print(f'\t Val. Loss: {valid_loss:.3f} |  Val. Acc: {valid_acc*100:.2f}%')
        
    # create arrays to save all y and y_hat values
    ys = []
    y_hats = []    
    # calculate final metrics on test data
    for (x, y) in tqdm(test_iterator, desc="Testing", leave=False):
        x = x.to(device)
        y = y.to(device)
        
        # Get predictions
        with torch.no_grad():  # No need for gradients in the testing phase
            y_hat = model(x)
        
        # Move y_pred and y to CPU, and convert them to NumPy arrays or Python lists before using them with sklearn
        y_hat = y_hat.argmax(dim=1).cpu().numpy()  # Taking the index of the highest prediction if y_pred is one-hot encoded
        y = y.cpu().numpy()
        
        ys.append(y)
        y_hats.append(y_hat)
        
    # Flatten the lists
    ys = np.concatenate(ys, axis=0)
    y_hats = np.concatenate(y_hats, axis=0)

    # Now you can use sklearn's functions like classification_report
    print(classification_report(ys, y_hats))

if __name__ == "__main__":
    train(batch_size=64, samples_per_class=500, learning_rate=0.01)