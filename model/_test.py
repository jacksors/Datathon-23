from _predict import predict
import os
import pandas as pd
import csv
import numpy as np
import pickle
    
# loop through all of the files in the directory
for filename in os.listdir("/home/jackson/Documents/Datathon-23/model"):
    if filename.startswith("newcase"):
        df = pd.read_pickle("/home/jackson/Documents/Datathon-23/model/" + filename)
        print(filename)
        input()
        try:
            print(predict(df, '/home/jackson/Documents/Datathon-23/tut2-model.pt', "/home/jackson/Documents/Datathon-23/model/classes.csv"))
        except Exception as e:
            raise(e)
    
