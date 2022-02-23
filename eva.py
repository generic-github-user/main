import pickle
import string
import time

databasePath = './eva-db';
try:
    with open(databasePath, 'rb') as fileRef:
        nodes = pickle.load(fileRef);
except:
    nodes = [];

def getId():
    return len(nodes)

def addNode(value, members=None):
def nodeMatch(node, info):
    for i in range(len(info)):
        if (info[i] != None and info[i] != node[i]):
            return False
    return True

def search(info):
    # results = []
    # for n in nodes:
    return list(filter(lambda n: nodeMatch(n, info), nodes))
    newId = getId()
    if members is None:
        members = []
    nodes.append([getId, value, members, time.time()])
    return newId

def save():
    with open(databasePath, 'wb') as fileRef:
        pickle.dump(nodes, fileRef)

# graph compression?
relations = ['are', 'is a', 'has', 'have'];
for i in range(1000):
    newInput = input()
    if newInput == 'quit':
        quit()
    elif newInput == 'print':
        for n in nodes:
            print(n)
    elif newInput.startswith('find'):
        id = addNode(newInput, [], True)
        addNode('origin', [id, addNode('user_input', [], False)])
        results = list(filter(lambda x: isinstance(x[1], str) and (newInput[5:] in x[1]), nodes))
        for n in results:
            print(n)
            addNode('origin', [n[0], addNode('eva_output', [], False)])
    else:
        id = len(nodes)
        nodes.append([id, newInput, [], time.time()])
        for r in relations:
            r2 = f' {r} '
            if r2 in newInput:
                a, b = newInput.split(r2)
                for ai in a.split(','):
                    id_a = addNode(ai)
                    id_b = addNode(b)
                    id_c = len(nodes)
                    nodes.append([id_c, r, [id_a, id_b], time.time()])
                    nodes.append([len(nodes), 'source', [id_c, id], time.time()])
        save()
