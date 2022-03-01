import pickle
import string
import time
import json
import random
import sys
from customize import ratings
from collections import namedtuple
# from .. import giraffe

sys.path.insert(0, '../giraffe')
from giraffe import Graph

databasePath = './eva-db'
ignoredTypes = ['length', 'type', 'token', 'origin', 'label', 'group', 'rating']
debug = True


try:
    print('Loading database')
    with open(databasePath, 'rb') as fileRef:
        nodes = pickle.load(fileRef)
except:
    nodes = [];

nodeTemplate = namedtuple('node', 'id value members time')
nodes = list(map(lambda n: nodeTemplate(*n), nodes))


try:
    print('Loading reference lists')
    with open('./cache', 'rb') as cRef:
        references = pickle.load(cRef)
except:
    references = []
    if debug:
        print('Building reference lists')
    for n in nodes:
        references.append([m[0] for m in nodes if (n[0] in m[2])])
    if debug:
        print('Done')

# database = Graph()
# for n in nodes:
#     database.nodes.append(Node(
#         n[1], [database.nodes[i] for i in n[2]], graph=database,
#         dict(id=n[0], time=n[3])
#     ))

# for i in range(len(nodes)):

# print(references[-100:])
# use node hashes?

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
            references.append([])
            for m in members:
                references[m].append(newId)
    else:
            # return matches[0][1]
            return matches[0][0]
    return newId

def save():
    with open(databasePath, 'wb') as fileRef:
        nodeList = list(map(list, nodes))
        pickle.dump(nodeList, fileRef)
    with open('./cache', 'wb') as cRef:
        pickle.dump(references, cRef)

def nodeProperty(node, attr):
    # n[1]
    links = list(filter(lambda n: n[2][0]==node, getNodes(attr)))
    if len(links) == 0:
        return None
    destId = links[0][2][1]
    if isinstance(destId, str):
        destId = getNodes(destId)[0][0]
    return nodes[destId][1]

def getInfo():
    links = []
    for n in nodes:
        if n[2]:
            for rel in ['subset', 'member']:
                refSources = [nodes[x] for x in references[n[2][0]]]
                conditions = [
                    n[1] in ['are'],
                    len(n[2]) == 2,
                    # n[0]?
                    # (not list(filter(lambda m: m[1]==rel and m[2][0]==n[2][0], nodes)))
                    (not list(filter(lambda m: m[1]==rel and m[2][0]==n[2][0], refSources)))
                ]
                if all(conditions):
                    newLink = [n[0], rel, n[2], n[3]]
                    links.append(newLink)
                    # display(newLink)
                    # map(display, list(filter(lambda m: m[1]==rel and m[2][0]==n[2][0], nodes)))
    # for L in links:
        # display(L)
    # q = 'how are you'
    current_link = random.choice(links)
    q = f'Is {nodes[current_link[2][0]][1]} a {current_link[1]} of {nodes[current_link[2][1]][1]}?'
    # use closure?
    newId = addNode('intent', [addNode(q, [], True), addNode('question', [], False)])
    addNode('origin', [newId, addNode('eva_ouptut', [], False)])
    print(q)
    current_question = newId

def P(message):
    if debug:
        print(message)

def updateAll():
    if debug:
        print('Updating database')

    P('Consolidating identical nodes')
    for n in nodes:
        # print(f'Updating node {n[0]}: {n[1]}')
        duplicates = list(filter(lambda x: n[1]==x[1], nodes))
        exists = len(list(filter(lambda y: len(y[2])>0, duplicates))) > 0
        if len(duplicates) > 1 and not exists:
            addNode(n[1], [x[0] for x in duplicates])

    P('Extracting node data types')
    for n in nodes:
        if n[1] not in ignoredTypes:
            typeId = addNode(type(n[1]).__name__, [], False)
            # m = list(filter(lambda x: n[1]==x[1] and n[2]==x[2], nodes))
            refSources = [nodes[z] for z in references[n[0]]]
            m = list(filter(lambda x: x[2] and n[0]==x[2][0] and x[1]=='type', refSources))
            if (len(m) == 0):
                addNode('type', [n[0], typeId])

    P('Extracting lengths from string nodes')
    for n in nodes:
        if n[1] not in ignoredTypes and isinstance(n[1], str):
            lenId = addNode(len(n[1]), [], False)
            refSources = [nodes[z] for z in references[n[0]]]
            m = list(filter(lambda x: x[2] and n[0]==x[2][0] and x[1]=='length', refSources))
            if (len(m) == 0):
                addNode('length', [n[0], lenId])
        # if len(list(filter(lambda x: x[1]=='origin' and x[2]==[n[0], getNodes('user_input')[0][0]], nodes))) > 0:
        #     for t in n[1].split():
                # addNode()

    P('Marking rating nodes')
    # # TODO: move (some) input processing here
    for n in nodes:
        if n[1] not in ignoredTypes and isinstance(n[1], str) and len(n[1])==3 and n[1][1]=='.':
            for r in ratings:
                if r[0]==n[1][0]:
                    addNode('rating', [n[0], addNode(r, [], False)], False, True)
                    addNode('group', [n[0], addNode('ratings', [], False)], False, True)

    P('Extracting tokens from text nodes')
    for n in list(filter(lambda n: nodeProperty(n[0], 'origin')=='user_input' and n[1] not in ignoredTypes, nodes)):
        tokens = n[1].split()
        if len(tokens) > 1:
            for t in tokens:
                addNode('token', [addNode(t, [], False), n[0]], False, True)
    save()
    if debug:
        print('Done')

def display(n):
    print(f'{n[0]} {n[1]} {[nodes[i][1] for i in n[2]]}')

current_question = None
current_link = None
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
            display(n)
    elif newInput.startswith('find'):
        id = addNode(newInput, [], True)
        addNode('origin', [id, addNode('user_input', [], False)])
        results = list(filter(lambda x: isinstance(x[1], str) and (newInput[5:] in x[1]), nodes))
        for n in results:
            display(n)
            addNode('origin', [n[0], addNode('eva_output', [], False)])
    elif newInput.startswith('ask'):
        t = newInput.split()
        if len(t) > 1:
            num = int(t[1])
        else:
            num = 1
        for i in range(num):
            getInfo()
    elif newInput == 'breakpoint':
        breakpoint()
    elif newInput == 'remove':
        nodes.pop()
        save()
    elif newInput == 'restore':
        nodes = json.load(open('./prevdata.json'))
        save()
    elif newInput == 'uall':
        updateAll()
        save()
    elif newInput.startswith('list'):
        target = newInput.split()[1]
        # members = list(filter(lambda x: ))
        # could this be made more efficient by first locating the node corresponding to the keyword?
        members = list(filter(lambda x: nodeProperty(x[0], 'member')==target, nodes))
        for m in members:
            display(m)
        save()
    else:
        id = addNode(newInput, [])
        addNode('origin', [id, addNode('user_input', [], False)])
        if current_question is not None:
            addNode('response', [id, current_question], True)
            if current_link is not None:
                if newInput in ['yes']:
                    # check this
                    if debug:
                        print('Adding link to database')
                    J = addNode(current_link[1], [x for x in current_link[2]], False, True)
                    addNode('truth', [J, addNode(True, [], False)], True)
                elif newInput in ['no']:
                    if debug:
                        print('Adding link to database')
                    J = addNode(current_link[1], [x for x in current_link[2]], False, True)
                    addNode('truth', [J, addNode(False, [], False)], True)
                current_link = None
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
                        id_c = addNode(r, [id_a, id_b])
                        addNode('source', [id_c, id])
        save()
