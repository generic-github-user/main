import pickle
import string
import time
from datetime import datetime
import json
import random
import sys
from customize import ratings
from collections import namedtuple
import os
from itertools import chain
import zlib
import string
# from .. import giraffe

from types import ModuleType, FunctionType
from gc import get_referents

# Custom objects know their class.
# Function objects seem to know way too much, including modules.
# Exclude modules as well.
BLACKLIST = type, ModuleType, FunctionType

sys.path.insert(0, '../giraffe')
# from giraffe import Graph

databasePath = './eva-db'
importDir = '../../Downloads/'
ignoredTypes = ['length', 'type', 'token', 'origin', 'label', 'group', 'rating', 'processed_flag', 'source', 'name', 'size', 'accessed', 'modified', 'size', 'unit']
debug = True
buffer = None
# snails.adjacent
# todo = []
# inferences = 0
# graph matching
# infinite node chains
# construct heuristics

# An OOP-style interface for working with the graph database
# The efficient array-based implementation is still used but this wrapper allows for method chaining and more literate code
# This class is largely functional and tightly intertwined with the Graph class (i.e., not encapsulated)
# Instances of this class are not meant to be processed in large numbers - it is intended for convenient access to
# functions on graphs
class Node:
    def __init__(self, nid, graph):
        self.id = nid
        self.graph = graph

class Graph:
    def __init__(self, nodes):
        self.nodes = nodes

    def search(self, info):
        return list(filter(lambda n: nodeMatch(n, info), self.nodes))

    def updateNode(self, node):
        if self.nodes[node][1] not in ignoredTypes:
            self.addNode(
                'processed_flag',
                [node],
                False, True
            )

        return node

    def addNode(self, value, members=None, duplicate=True, useSearch=False):
        newId = getId()
        if useSearch:
            matches = self.search([None, value, members, None])
        else:
            matches = getNodes(value)
        if (duplicate or not matches):
                if members is None:
                    members = []
                nodeData = [newId, value, members, time.time()]
                nodes.append(nodeTemplate(*nodeData))
                references.append([])
                for m in members:
                    if m is not None:
                        references[m].append(newId)
        else:
                return matches[0].id
        self.updateNode(newId)
        return newId

# https://stackoverflow.com/a/30316760
def getsize(obj):
    if isinstance(obj, BLACKLIST):
        raise TypeError('getsize() does not take argument of type: '+ str(type(obj)))
    seen_ids = set()
    size = 0
    objects = [obj]
    while objects:
        need_referents = []
        for obj in objects:
            if not isinstance(obj, BLACKLIST) and id(obj) not in seen_ids:
                seen_ids.add(id(obj))
                size += sys.getsizeof(obj)
                need_referents.append(obj)
        objects = get_referents(*need_referents)
    return size



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

database = Graph(nodes)
# TODO: use tensorflow models
# meta-inference


def parseExpression(ex):
    frame = []
    valueType = None
    value = None
    for c in ex:
        if c in string.digits:
            if valueType == 'num':
                value += c
            else:
                # last = frame
                frame.append(value)
                value = c
                valueType = 'num'
        elif (c in '+-*/^'):
            if valueType == 'op':
                value += c
            else:
                frame.append(value)
                value = c
                valueType = 'op'

def getId():
    return len(nodes)

def getNodes(value):
    return list(filter(lambda n: n[1]==value, nodes))

def nodeMatch(node, info):
    for i in range(len(info)):
        if (info[i] != None and info[i] != node[i]):
            return False
    return True

def save():
    with open(databasePath, 'wb') as fileRef:
        nodeList = list(map(list, nodes))
        pickle.dump(nodeList, fileRef)
    with open('./cache', 'wb') as cRef:
        pickle.dump(references, cRef)

def nodeProperty(node, attr):
    # n[1]
    # getNodes(attr)
    refs = list(filter(lambda n: n.value==attr, [database.nodes[x] for x in references[node]]))
    links = list(filter(lambda n: n.members[0]==node, refs))
    if len(links) == 0:
        return None
    destId = links[0].members[1]
    if isinstance(destId, str):
        destId = getNodes(destId)[0].id
    return database.nodes[destId].value

def getReferrers(node):
    return [database.nodes[x] for x in references[node]]

# TODO: direct database indexing
def getAdjacent(node, value=None, directional=False):
    # return filter(lambda n: n!=node and any(n in m.members for m in getReferrers(node)), )
    # return [m for n in getReferrers(node) for m in .n.members]

    # adjacent = list(filter(lambda n: n != node, chain.from_iterable(m.members for m in getReferrers(node))))
    # if value is not None:
    #     adjacent = list(filter(lambda n: database.nodes[n].value == value, adjacent))

    adjacent = []
    for m in getReferrers(node):
        for ref in m.members:
            if (ref != node) and (value is None or m.value == value) and ((not directional) or m.members.index(node)==0):
                adjacent.append(ref)
    return adjacent
def getInfo():
    links = []
    for n in nodes:
        if len(n.members) > 0 and False:
            for rel in ['subset', 'member']:
                refSources = [nodes[x] for x in references[n.members[0]]]
                conditions = [
                    n[1] in ['are'],
                    len(n[2]) == 2,
                    # n[0]?
                    # (not list(filter(lambda m: m[1]==rel and m[2][0]==n[2][0], nodes)))
                    (not list(filter(lambda m: m.value == rel and m.members[0]==n.members[0], refSources)))
                ]
                if all(conditions):
                    newLink = [n[0], rel, n[2], n[3]]
                    links.append(nodeTemplate(*newLink))
        # if len(n.members) > 0:
        #     for R in relations:
        #         refs = getReferrers(n)
    # q = 'how are you'
    current_link = random.choice(links)
    q = f'Is {nodes[current_link[2][0]].value} a {current_link.value} of {nodes[current_link[2][1]].value}?'
    # use closure?
    newId = database.addNode('intent', [database.addNode(q, [], True), database.addNode('question', [], False)])
    database.addNode('origin', [newId, database.addNode('eva_ouptut', [], False)])
    print(q)
    # current_question = newId
    return newId, current_link

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
            database.addNode(n[1], [x[0] for x in duplicates])

    P('Extracting node data types')
    for n in nodes:
        if n.value not in ignoredTypes:
            typeId = database. addNode(type(n[1]).__name__, [], False)
            # m = list(filter(lambda x: n[1]==x[1] and n[2]==x[2], nodes))
            refSources = [nodes[z] for z in references[n[0]]]
            m = list(filter(lambda x: x[2] and n[0]==x[2][0] and x.value=='type', refSources))
            if (len(m) == 0):
                database.addNode('type', [n[0], typeId])

    P('Extracting lengths from string nodes')
    for n in nodes:
        if n.value not in ignoredTypes and isinstance(n.value, str):
            lenId = database.addNode(len(n.value), [], False)
            refSources = [nodes[z] for z in references[n[0]]]
            m = list(filter(lambda x: x[2] and n[0]==x[2][0] and x.value=='length', refSources))
            if (len(m) == 0):
                database.addNode('length', [n[0], lenId])
        # if len(list(filter(lambda x: x[1]=='origin' and x[2]==[n[0], getNodes('user_input')[0][0]], nodes))) > 0:
        #     for t in n[1].split():
                # addNode()

    P('Marking rating nodes')
    # TODO: move (some) input processing here
    for n in nodes:
        if n.value not in ignoredTypes and isinstance(n.value, str) and len(n.value)==3 and n.value[1]=='.':
            for r in ratings:
                if r[0]==n[1][0]:
                    database.addNode('rating', [n.id, database.addNode(r, [], False)], False, True)
                    database.addNode('group', [n.id, database.addNode('ratings', [], False)], False, True)

    P('Extracting tokens from text nodes')
    for n in list(filter(lambda n: nodeProperty(n.id, 'origin')=='user_input' and n.value not in ignoredTypes, nodes)):
        tokens = n[1].split()
        if len(tokens) > 1:
            for t in tokens:
                database.addNode('token', [database.addNode(t, [], False), n.id], False, True)
    save()
    if debug:
        print('Done')

def display(n):
    print(f'{n[0]} {n[1]} {[nodes[i][1] for i in n[2]]}')

def scanDir(DB, parent, dir, count, scanId):
    fId = DB.addNode(dir.path, [], False)
    DB.addNode('source', [fId, scanId], False, True)
    DB.addNode('name', [fId, DB.addNode(dir.name, [], False)], False, True)
    DB.addNode('size', [fId, DB.addNode(os.stat(dir).st_size, [], False)], False, True)
    DB.addNode('accessed', [fId, DB.addNode(os.stat(dir).st_atime, [], False)], False, True)
    DB.addNode('modified', [fId, DB.addNode(os.stat(dir).st_mtime, [], False)], False, True)
    DB.addNode('parent', [fId, parent], False, True)
    if dir.is_dir() and (count < 100):
        for item in os.scandir(dir):
            count = scanDir(DB, fId, item, count, scanId)
    return count+1

current_question = None
current_link = None
relations = ['are', 'is a', 'has', 'have']
for i in range(1000):
    newInput = input()
    if newInput == 'quit':
        quit()
    elif newInput == 'print':
        print('100 most recent nodes:')
        for n in nodes[-100:]:
            display(n)
    elif newInput.startswith('find'):
        nodeId = database.addNode(newInput, [], True)
        database.addNode('origin', [nodeId, database.addNode('user_input', [], False)])
        results = list(filter(lambda x: isinstance(x.value, str) and (newInput[5:] in x.value), nodes))
        for n in results:
            display(n)
            database.addNode('origin', [n.id, database.addNode('eva_output', [], False)])
    elif newInput.startswith('ask'):
        t = newInput.split()
        if len(t) > 1:
            num = int(t[1])
        else:
            num = 1
        for i in range(num):
            current_question, current_link = getInfo()
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
    elif newInput.startswith('json'):
        database.addNode(
            'origin',
            [database.addNode(newInput, []), database.addNode('user_input', [], False)]
        )
        jsonPath = importDir+newInput[5:]
        database.addNode(jsonPath, [], False)
        with open(jsonPath) as f:
            newData = json.load(f)
        print(newData)
    elif newInput.startswith('crawl'):
            database.addNode(
                'origin',
                [database.addNode(newInput, []), database.addNode('user_input', [], False)]
            )
            scan = database.addNode('file_scan', [], True)
            c = 0
            for d in os.scandir(newInput[6:]):
                scanDir(database, None, d, c, scan)
    elif newInput.startswith('list'):
        target = newInput.split()[1]
        # members = list(filter(lambda x: ))
        # could this be made more efficient by first locating the node corresponding to the keyword?
        members = list(filter(lambda x: nodeProperty(x.id, 'member')==target, nodes))
        for m in members:
            display(m)
        save()
    # elif newInput == 'undo':
    elif newInput == 'backup':
        date_format = '%m_%d_%Y, %H_%M_%S'
        backupPath = f'./eva_{datetime.now().strftime(date_format)}.evab'
        with open(backupPath, 'wb') as fileRef:
            nodeList = list(map(list, nodes))
            B = zlib.compress(pickle.dumps(nodeList))
            fileRef.write(B)
    elif newInput.startswith('$'):
        database.addNode(
            'origin',
            [database.addNode(newInput, []), database.addNode('user_node', [], False)]
        )
        symbols = {
            '<': 'subset'
        }
        for s in symbols:
            if s in newInput:
                A, B = newInput[1:].split(s)
                for Ai in A.split(','):
                    for Bi in B.split(','):
                        database.addNode(
                            symbols[s],
                            [
                                database.addNode(Ai, [], False),
                                database.addNode(Bi, [], False)
                            ],
                            False,
                            True
                        )
            break
        save()
    else:
        nodeId = database.addNode(newInput, [])
        database.addNode('origin', [nodeId, database.addNode('user_input', [], False)])
        if current_question is not None:
            database.addNode('response', [nodeId, current_question], True)
            if current_link is not None:
                if newInput in ['yes']:
                    # check this
                    if debug:
                        print('Adding link to database')
                    J = database.addNode(current_link.value, [x for x in current_link.members], False, True)
                    database.addNode('truth', [J, database.addNode(True, [], False)], True)
                elif newInput in ['no']:
                    if debug:
                        print('Adding link to database')
                    J = database.addNode(current_link.value, [x for x in current_link.members], False, True)
                    database.addNode('truth', [J, database.addNode(False, [], False)], True)
                current_link = None
            current_question = None
        for r in relations:
            r2 = f' {r} '
            if r2 in newInput:
                rel = newInput.split(r2)
                if len(rel) == 2:
                    a, b = rel
                    for ai in a.split(','):
                        id_a = database.addNode(ai)
                        id_b = database.addNode(b)
                        id_c = database.addNode(r, [id_a, id_b])
                        database.addNode('source', [id_c, id])
        save()


# TODO: mark time node/neighborhood was last updated
# TODO: search by pattern
# TODO: graph compression
# TODO: node hashes
# TODO: HCI language
