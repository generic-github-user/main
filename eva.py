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

def getNodes(value):
    return list(filter(lambda n: n[1]==value, nodes))

# # TODO: search by pattern

def nodeMatch(node, info):
    for i in range(len(info)):
        if (info[i] != None and info[i] != node[i]):
            return False
    return True

def search(info):
    # results = []
    # for n in nodes:
    return list(filter(lambda n: nodeMatch(n, info), nodes))

def addNode(value, members=None, duplicate=True, useSearch=False):
    newId = getId()
    if useSearch:
        matches = search([None, value, members, None])
    else:
        matches = getNodes(value)
    if (duplicate or not matches):
            if members is None:
                members = []
            nodes.append([newId, value, members, time.time()])
    else:
            # return matches[0][1]
            return matches[0][0]
    return newId

def save():
    with open(databasePath, 'wb') as fileRef:
        pickle.dump(nodes, fileRef)

def nodeProperty(node, attr):
    # n[1]
    links = list(filter(lambda n: n[2][0]==node, getNodes(attr)))
    if len(links) == 0:
        return None
    destId = links[0][2][1]
    if isinstance(destId, str):
        destId = getNodes(destId)[0][0]
    return nodes[destId][1]

current_question = None
# graph compression?
relations = ['are', 'is a', 'has', 'have'];
for i in range(1000):
    # breakpoint()
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
    elif newInput.startswith('ask'):
        q = 'how are you'
        newId = addNode('intent', [addNode(q, [], True), addNode('question', [], False)])
        addNode('origin', [newId, addNode('eva_ouptut', [], False)])
        print(q)
        current_question = newId
    elif newInput == 'remove':
        nodes.pop()
        save()
    elif newInput == 'restore':
        nodes = json.load(open('./prevdata.json'))
        save()
    else:
        id = len(nodes)
        nodes.append([id, newInput, [], time.time()])
        if current_question is not None:
            addNode('response', [id, current_question], True)
        for r in relations:
            r2 = f' {r} '
            if r2 in newInput:
                rel = newInput.split(r2)
                if len(rel) == 2:
                    a, b = rel
                    for ai in a.split(','):
                        id_a = addNode(ai)
                        id_b = addNode(b)
                        id_c = len(nodes)
                        nodes.append([id_c, r, [id_a, id_b], time.time()])
                        nodes.append([len(nodes), 'source', [id_c, id], time.time()])
        save()
