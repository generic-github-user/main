import pickle
import string
import time

databasePath = './eva-db';
try:
    with open(databasePath, 'rb') as fileRef:
        nodes = pickle.load(fileRef);
except:
    nodes = [];
