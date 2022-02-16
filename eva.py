import pickle
import string
import time

databasePath = './eva-db';
try:
    with open(databasePath, 'rb') as fileRef:
        nodes = pickle.load(fileRef);
except:
    nodes = [];

relations = ['are', 'is a', 'has', 'have'];
for i in range(1000):
    newInput = input()
    if newInput == 'quit':
        quit()
    elif newInput == 'print':
        print(nodes)
    else:
        id = len(nodes)
        nodes.append([id, newInput, [], time.time()])
        for r in relations:
            r2 = f' {r} '
            if r2 in newInput:
                a, b = newInput.split(r2)
                for ai in a.split(','):
                    id_a = len(nodes)
                    nodes.append([id_a, ai, [], time.time()])
                    id_b = len(nodes)
                    nodes.append([id_b, b, [], time.time()])
                    id_c = len(nodes)
                    nodes.append([id_c, r, [id_a, id_b], time.time()])
                    nodes.append([len(nodes), 'source', [id_c, id], time.time()])
        with open(databasePath, 'wb') as fileRef:
            pickle.dump(nodes, fileRef)
