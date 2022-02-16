import pickle
import string
import time

databasePath = './eva-db';
try:
    with open(databasePath, 'rb') as fileRef:
        nodes = pickle.load(fileRef);
except:
    nodes = [];

for i in range(1000):
    newInput = input()
    if newInput == 'quit':
        quit()
    elif newInput == 'print':
        print(nodes)
    else:
        id = len(nodes)
        nodes.append([id, newInput, [], time.time()])
        with open(databasePath, 'wb') as fileRef:
            pickle.dump(nodes, fileRef)
