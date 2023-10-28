from predict import predict
import os
import pandas as pd
import csv
import numpy as np

df = pd.read_json("/home/jackson/Documents/Datathon-23/model/data/google/full_simplified_apple.ndjson", lines=True, nrows=1)['drawing']

map = {}
with open("/home/jackson/Documents/Datathon-23/model/classes.csv", "r") as f:
    reader = csv.reader(f)
    map = {int(rows[0]): rows[1] for rows in reader}
    

print(predict(df[0], '/home/jackson/Documents/Datathon-23/tut2-model.pt', map))