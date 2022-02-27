import pickle
import string
import time
import json
debug = True

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
        print('100 most recent nodes:')
        for n in nodes[-100:]:
            print(f'{n[0]} {n[1]} {[nodes[i][1] for i in n[2]]}')
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
        addNode('origin', [id, addNode('user_input', [], False)])
        if current_question is not None:
            addNode('response', [id, current_question], True)
            current_question = None
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
        if debug:
            print('Updating database')
        for n in nodes:
            # print(f'Updating node {n[0]}: {n[1]}')
            duplicates = list(filter(lambda x: n[1]==x[1], nodes))
            exists = len(list(filter(lambda y: len(y[2])>0, duplicates))) > 0
            if len(duplicates) > 1 and not exists:
                addNode(n[1], [x[0] for x in duplicates])

            if n[1] not in ['length', 'type', 'token']:
                typeId = addNode(type(n[1]).__name__, [], False)
                # m = list(filter(lambda x: n[1]==x[1] and n[2]==x[2], nodes))
                m = list(filter(lambda x: x[2] and n[0]==x[2][0] and x[1]=='type', nodes))
                if (len(m) == 0):
                    addNode('type', [n[0], typeId])
            if n[1] not in ['length', 'type', 'token'] and isinstance(n[1], str):
                lenId = addNode(len(n[1]), [], False)
                m = list(filter(lambda x: x[2] and n[0]==x[2][0] and x[1]=='length', nodes))
                if (len(m) == 0):
                    addNode('length', [n[0], lenId])
            # if len(list(filter(lambda x: x[1]=='origin' and x[2]==[n[0], getNodes('user_input')[0][0]], nodes))) > 0:
            #     for t in n[1].split():
                    # addNode()
        for n in list(filter(lambda n: nodeProperty(n[0], 'origin')=='user_input' and n[1] not in ['length', 'type', 'token'], nodes)):
            tokens = n[1].split()
            if len(tokens) > 1:
                for t in tokens:
                    addNode('token', [addNode(t, [], False), n[0]], False, True)
        save()
        if debug:
            print('Done')
