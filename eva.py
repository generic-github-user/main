print('Importing libraries')

import pickle
import json
import zlib

import string
from customize import ratings

from datetime import datetime
import time

import numpy as np
import random

from collections import namedtuple
from itertools import chain

from getsize import *
from hash_file import *

import sys
import os

import pyparsing

from PIL import Image
import pytesseract

print('Done')


# def stringEntropy

sys.path.insert(0, '../giraffe')
# from giraffe import Graph

importDir = '../../Downloads/'
ignoredTypes = ['length', 'type', 'token', 'origin', 'label', 'group', 'rating', 'processed_flag', 'source', 'name', 'size', 'accessed', 'modified', 'unit', 'byte', 'importance_heuristic', 'num_adjacent', 'entropy_estimate']
debug = True
buffer = None
# snails.adjacent
# todo = []
# inferences = 0

timeLimit = 5
opLimit = 10

logical_relations = [
    ('subset', 'subset', 'subset'),
    ('member', 'subset', 'member'),
    ('member', 'use', 'use'),
    ('member', 'can', 'can'),
    ('member', 'melt', 'melt'),
    ('member', 'contain', 'contain'),
    ('contain', 'contain', 'contain'),
]
# graph matching
# infinite node chains
# construct heuristics
# define concepts analogous to adjacency using grammars?

# An OOP-style interface for working with the graph database
# The efficient array-based implementation is still used but this wrapper allows for method chaining and more literate code
# This class is largely functional and tightly intertwined with the Graph class (i.e., not encapsulated)
# Instances of this class are not meant to be processed in large numbers - it is intended for convenient access to
# functions on graphs
class Node:
    def __init__(self, nid, graph, rep):
        assert(isinstance(nid, int))
        assert(isinstance(graph, Graph))
        self.id = nid
        self.graph = graph
        self.rep = rep
        self.references = []

    def referrers(self, update=True):
        return Graph([self.graph.get(x, update) for x in self.graph.references[self.id]])

    def adjacent(self, value=None, directional=False, return_ids=True):
        assert(isinstance(directional, bool))
        assert(isinstance(return_ids, bool))

        adjacent = []
        for m in self.referrers().nodes:
            for ref in m.members:
                if (ref != self.id) and (value is None or m.value == value) and ((not directional) or m.members.index(self.id)==0):
                    adjacent.append(ref)
        if return_ids:
            return adjacent
        else:
            return Graph([self.graph[x] for x in adjacent])

    def __getattr__(self, attr):
        # return getattr(self.graph.nodes[self.id], attr)
        return getattr(self.rep, attr)

# TODO: handle graphs sharing nodes

class Graph:
    def __init__(self, nodes=None, savePath='./saved_graph', fields='id value members time'):
        self.savePath = savePath
        self.nodes = nodes
        self.fields = fields
        self.nodeTemplate = namedtuple('node', fields)
        if self.nodes is None:
            self.nodes = []
            self.load()

    def load(self):
        try:
            print('Loading database')
            with open(self.savePath, 'rb') as fileRef:
                self.nodes = pickle.load(fileRef)
        except Exception as error:
            print(error)
            self.nodes = []

        self.nodes = list(map(lambda n: self.nodeTemplate(*n), self.nodes))
        return self

    def getNodes(self, value):
        return Graph(list(filter(lambda n: n[1]==value, self.nodes)))

    def search(self, info):
        return Graph(list(filter(lambda n: nodeMatch(n, info), self.nodes)))

    def filter(self, condition):
        # return Graph(list(filter(condition, self.nodes)))
        say(f'Searching {len(self)} nodes')
        result = []
        for x in range(len(self)):
            # node = self.get(x, False)
            node = self.nodes[x]
            if condition(node):
                result.append(node)
            if (x % 10000 == 0):
                say(f'Checked {x}/{len(self)} nodes')
        return Graph(result)

    def updateNode(self, node):
        assert(isinstance(node, int))

        if self[node].value not in ignoredTypes:
            self.addNode(
                'processed_flag',
                [node],
                False, True
            )
            self.addNode(
                'unit',
                [
                    self.addNode('size', [node, self.addNode(getsize(self[node]), [], False)], False, True),
                    self.addNode('byte', [], False)
                ]
            )
            # self.addNode('neighborhood_size', [node, self.addNode(len())])
            numAdj = len(self[node].adjacent())
            say(f'Found {numAdj} adjacent nodes')
            self.addNode('num_adjacent', [node, self.addNode(numAdj, [], False)], False, True)
            markType(self[node])
            markLength(self[node])
            current = self[node]
            if current.value not in ignoredTypes and isinstance(current.value, str):
                if isinstance(current.value, str):
                    est = estimateEntropy(bytes(current.value, 'UTF-8'))
                else:
                    est = estimateEntropy(bytes(current.value))
                say(f'Estimated entropy of {current.value} is {est}')
                entId = self.addNode(est, [], False)
                m = list(filter(lambda x: x.members and current.id == x.members[0] and x.value=='entropy_estimate', current.referrers()))
                if (len(m) == 0):
                    self.addNode('entropy_estimate', [current.id, entId])

        return node

    def addNode(self, value, members=None, duplicate=True, useSearch=False, update=False):
        assert(isinstance(members, list) or members is None)
        assert(isinstance(duplicate, bool))
        assert(isinstance(useSearch, bool))
        assert(isinstance(update, bool))

        newId = getId()
        if useSearch:
            matches = self.search([None, value, members, None])
        else:
            matches = self.getNodes(value)
        if (duplicate or not matches):
                if members is None:
                    members = []
                nodeData = [newId, value, members, time.time()]
                self.nodes.append(self.nodeTemplate(*nodeData))
                database.references.append([])
                for m in members:
                    if m is not None:
                        database.references[m].append(newId)
        else:
                return matches[0].id
        if update:
            self.updateNode(newId)
        return newId

    def save(self):
        if len(self) > 80000:
            with open(self.savePath, 'wb') as fileRef:
                nodeList = list(map(list, self.nodes))
                pickle.dump(nodeList, fileRef)
            with open('./cache', 'wb') as cRef:
                pickle.dump(database.references, cRef)
        else:
            say('Database integrity check failed; terminating save')
        return self

    def random(self, weighted=True):
        # W = [0.9 if nodeProperty(n.id, 'origin')=='user_input' else 0.1 for n in self]
        W = [0.9 if (n.value not in ignoredTypes and isinstance(n.value, str)) else 0.1 for n in self.nodes]
        if weighted:
            node = random.choices(self.nodes, weights=W, k=1)[0]
        else:
            node = random.choice(self.nodes)
        node = Node(node.id, self.parent, node)
        assert(isinstance(node, Node))
        return node

    def get(self, i, update=True):
        assert(isinstance(i, int))
        assert(isinstance(update, bool))

        if isinstance(i, int):
            if update:
                self.addNode('accessed', [i, self.addNode(time.time(), [], False)])
            return Node(self.nodes[i].id, self, self.nodes[i])
        elif isinstance(i, slice):
            return Graph(self.nodes[i], self.savePath)
        else:
            print(i)
            raise Exception

    def __getitem__(self, i):
        return self.get(i)

    def __bool__(self):
        return len(self.nodes) > 0

    def __len__(self):
        return len(self.nodes)

    # TODO
    def __iter__(self):
        # def nodeWrapper(node):
        #     def wrapNode(rep):
        #         return Node(nid, graph, rep)
        def nodeWrapper(node):
            return Node(node.id, self, node)
        return map(nodeWrapper, self.nodes)




# database = Graph()
# for n in nodes:
#     database.nodes.append(Node(
#         n[1], [database.nodes[i] for i in n[2]], graph=database,
#         dict(id=n[0], time=n[3])
#     ))

database = Graph(savePath='./eva-db')
# TODO: use tensorflow models
# meta-inference


try:
    print('Loading reference lists')
    with open('./cache', 'rb') as cRef:
        database.references = pickle.load(cRef)
except:
    database.references = []
    if debug:
        print('Building reference lists')
    for n in database.nodes:
        database.references.append([m.id for m in nodes if (n.id in m[2])])
    if debug:
        print('Done')


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
    return len(database.nodes)

def estimateEntropy(value):
    return getsize(zlib.compress(value))/getsize(value)

def nodeMatch(node, info):
    for i in range(len(info)):
        if (info[i] != None and info[i] != node[i]):
            return False
    return True

def nodeProperty(node, attr, update=True):
    # n[1]
    # getNodes(attr)
    refs = list(filter(lambda n: n.value==attr, database.get(node, update).referrers(update=update)))
    links = list(filter(lambda n: n.members[0]==node, refs))
    if len(links) == 0:
        return None
    destId = links[0].members[1]
    if isinstance(destId, str):
        destId = database.getNodes(destId)[0].id
    return database.get(destId, update).value


# related_to
def say(content, source=None, intent='information', record=False):
    assert(isinstance(content, str))
    assert(isinstance(source, int) or source is None)

    if record:
        newId = database.addNode('intent', [database.addNode(content, [], True), database.addNode(intent, [], False)])
        database.addNode('origin', [newId, database.addNode('eva_output', [], False)])
        if source is not None:
            database.addNode('source', [newId, source])
    print(content)
    # return newId

# logical_relations / relations
# why was getsize working before?
# expected_usefulness
# "hanging" nodes (with intermediary inferences deleted)

def timeFunc(F, level=0):
    def timed(*args, **kwargs):
        start = time.time()
        say('Executing function', level=level+1)
        fOut = F(*args, **kwargs)
        end = time.time()
        elapsed = end - start

        src = [fOut] if (fOut is not None) else []
        database.addNode('start_time', src + [database.addNode(start, [], False)], False, True, level=level+1)
        database.addNode('end_time', src + [database.addNode(end, [], False)], False, True, level=level+1)
        database.addNode('duration', src + [database.addNode(elapsed, [], False)], False, True, level=level+1)

        say(f'Finished execution in {elapsed} seconds', level=level)

        return fOut
    return timed

def think(node=None):
    start = time.time()
    if node is None:
        node = database.random()
    else:
        node = database[node]
    name = node.value
    say(f'Pondering {name}')

    database.updateNode(node.id)

    inferences = []
    for R in logical_relations:
        # inferences.extend(filter(lambda m: self.nodes[m], getAdjacent(node, R[0])))
        adj = node.adjacent(R[0], True)
        say(f'{len(adj)} nodes adjacent to {name} via {R[0]}')
        for m1 in adj:
            for m2 in database[m1].adjacent(R[1], True):
                inferences.append(([R[2], [node.id, m2]], [m1, m2]))
    if len(inferences) > 0:
        inf = random.choice(inferences)
        newNode = database.addNode(*inf[0], False, True)
        database.addNode(
            'origin',
            [newNode, database.addNode('eva_inference', [], False)],
            False,
            True
        )
        database.addNode('sources', [newNode]+inf[1], False, True)
        say(
            f'Inferred relationship {database[inf[0][1][0]].value} -- {inf[0][0]} -- {database[inf[0][1][1]].value}',
            newNode, 'information'
        )
    else:
        say('No viable inferences found')
    database.save()

def getInfo():
    links = []
    for n in nodes:
        if len(n.members) > 0 and False:
            for rel in ['subset', 'member']:
                refSources = [nodes[x] for x in database.references[n.members[0]]]
                conditions = [
                    n[1] in ['are'],
                    len(n[2]) == 2,
                    # n[0]?
                    # (not list(filter(lambda m: m[1]==rel and m[2][0]==n[2][0], nodes)))
                    (not list(filter(lambda m: m.value == rel and m.members[0]==n.members[0], refSources)))
                ]
                if all(conditions):
                    newLink = [n[0], rel, n[2], n[3]]
                    links.append(database.nodeTemplate(*newLink))
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


def markType(node):
    assert(isinstance(node, Node))
    if node.value not in ignoredTypes:
        typeId = database.addNode(type(node.value).__name__, [], False)
        # m = list(filter(lambda x: n[1]==x[1] and n[2]==x[2], nodes))
        m = list(filter(lambda x: x.members and node.id == x.members[0] and x.value=='type', node.referrers()))
        if (len(m) == 0):
            database.addNode('type', [node.id, typeId])
    return node

def markLength(node):
    assert(isinstance(node, Node))
    if node.value not in ignoredTypes and isinstance(node.value, str):
        lenId = database.addNode(len(node.value), [], False)
        m = list(filter(lambda x: x.members and node.id == x.members[0] and x.value=='length', node.referrers()))
        if (len(m) == 0):
            database.addNode('length', [node.id, lenId])

def updateAll():
    if debug:
        say('Updating database')

    say('Consolidating identical nodes')
    for n in nodes:
        # print(f'Updating node {n[0]}: {n[1]}')
        duplicates = list(filter(lambda x: n[1]==x[1], database.nodes))
        exists = len(list(filter(lambda y: len(y[2])>0, duplicates))) > 0
        if len(duplicates) > 1 and not exists:
            database.addNode(n[1], [x[0] for x in duplicates])

    say('Extracting node data types')
    for n in nodes:
        markType(n)

    say('Extracting lengths from string nodes')
    for n in nodes:
        markLength(n)
        # if len(list(filter(lambda x: x[1]=='origin' and x[2]==[n[0], getNodes('user_input')[0][0]], nodes))) > 0:
        #     for t in n[1].split():
                # addNode()

    say('Marking rating nodes')
    # TODO: move (some) input processing here
    for n in nodes:
        if n.value not in ignoredTypes and isinstance(n.value, str) and len(n.value)==3 and n.value[1]=='.':
            for r in ratings:
                if r[0]==n[1][0]:
                    database.addNode('rating', [n.id, database.addNode(r, [], False)], False, True)
                    database.addNode('group', [n.id, database.addNode('ratings', [], False)], False, True)

    say('Extracting tokens from text nodes')
    for n in list(filter(lambda n: nodeProperty(n.id, 'origin')=='user_input' and n.value not in ignoredTypes, nodes)):
        tokens = n[1].split()
        if len(tokens) > 1:
            for t in tokens:
                database.addNode('token', [database.addNode(t, [], False), n.id], False, True)
    database.save()
    if debug:
        print('Done')

def display(n):
    print(f'{n.id} {n.value} {[database[i].value for i in n.members]}')

def scanDir(DB, parent, dir, count, scanId):
    say(f'Scanning {dir.path}')
    fId = DB.addNode(dir.path, [], False)
    DB.addNode('source', [fId, scanId], False, True)
    DB.addNode('name', [fId, DB.addNode(dir.name, [], False)], False, True)
    DB.addNode('size', [fId, DB.addNode(os.stat(dir).st_size, [], False)], False, True)
    DB.addNode('accessed', [fId, DB.addNode(os.stat(dir).st_atime, [], False)], False, True)
    DB.addNode('modified', [fId, DB.addNode(os.stat(dir).st_mtime, [], False)], False, True)
    DB.addNode('parent', [fId, parent], False, True)
    if dir.is_dir() and (count < 100):
        say(f'Scanning directory')
        for item in os.scandir(dir):
            count = scanDir(DB, fId, item, count, scanId)
    if dir.is_file():
        DB.addNode('md5_hash', [fId, DB.addNode(hash_file(dir.path), [], False)])
    return count+1

def backup():
    date_format = '%m_%d_%Y, %H_%M_%S'
    backupPath = f'./eva_{datetime.now().strftime(date_format)}.evab'
    with open(backupPath, 'wb') as fileRef:
        nodeList = list(map(list, database.nodes))
        B = zlib.compress(pickle.dumps(nodeList))
        fileRef.write(B)
        say(f'Backup saved to {backupPath} [{getsize(B)} bytes]')
    return backupPath

commands = {}
def command(prefix):
    def command_decorator(func):
        # commands.append(func)
        commands[prefix] = func
        return func
    return command_decorator

@command('quit')
def quitCommand(newInput):
    quit()

@command('ask')
def askCommand(newInput):
    t = newInput.split()
    if len(t) > 1:
        num = int(t[1])
    else:
        num = 1
    for i in range(num):
        current_question, current_link = getInfo()

@command('clear')
def clearCommand(newInput):
    for i in range(50):
        print('')

@command('crawl')
def crawlCommand(newInput):
    p = newInput[6:]
    say(f'Scanning {p}')
    scan = database.addNode('file_scan', [], True)
    c = 0
    for d in os.scandir(p):
        scanDir(database, None, d, c, scan)
    say('Done')

@command('backup')
def backupCommand(newInput):
    backup()

@command('think')
def thinkCommand(newInput):
    before = time.time()
    for j in range(opLimit):
        think()
        if time.time()-before>timeLimit:
            break

@command('list')
def listCommand(newInput):
    target = newInput.split()[1]
    # members = list(filter(lambda x: ))
    # could this be made more efficient by first locating the node corresponding to the keyword?
    members = database.filter(lambda x: nodeProperty(x.id, 'member', False)==target)
    for m in members:
        display(m)

ppc = pyparsing.pyparsing_common
pyparsing.ParserElement.enablePackrat()
# sys.setrecursionlimit(3000)

integer = ppc.integer
variable = pyparsing.Word(pyparsing.alphas)
operand = pyparsing.Literal('*') | variable | integer

adjOp = pyparsing.Literal(".")
# signop = pyparsing.oneOf("+ -")
# multop = pyparsing.oneOf("* /")
# plusop = pyparsing.oneOf("+ -")
# factop = pyparsing.Literal("!")

expr = pyparsing.infixNotation(
    operand,
    [
        # ("^", 2, pyparsing.opAssoc.RIGHT),
        (".", 2, pyparsing.opAssoc.LEFT),
        (";", 2, pyparsing.opAssoc.LEFT),
        ("/", 2, pyparsing.opAssoc.LEFT),
        (">", 2, pyparsing.opAssoc.LEFT),
        ("^", 2, pyparsing.opAssoc.LEFT),
        ("?", 2, pyparsing.opAssoc.LEFT),
        # (signop, 1, pyparsing.opAssoc.RIGHT),
        # (multop, 2, pyparsing.opAssoc.LEFT),
        # (plusop, 2, pyparsing.opAssoc.LEFT),
    ],
)
# def mapCommand

current_question = None
current_link = None
relations = ['are', 'is a', 'has', 'have']
for i in range(1000):
    newInput = input()
    inputId = database.addNode(newInput, [], True)
    # breakpoint()
    # why isn't quit command recorded?
    database.addNode(
        'origin',
        [inputId, database.addNode('user_input', [], False)]
    )
    database.save()

    for prefix, f in commands.items():
        if newInput.startswith(prefix):
            f(newInput)

    if newInput == 'print':
        print('10 most recent nodes:')
        # for n in database[-10:]:
        N = len(database.nodes)
        for x in range(N-10, N):
            display(database[x])
    elif newInput.startswith('find'):
        start = time.time()
        # TODO: clean this up
        searchNode = database.addNode('search_cmd', [], True)
        database.addNode('source', [searchNode, inputId])
        results = list(filter(lambda x: isinstance(x.value, str) and (newInput[5:] in x.value), database.nodes))
        for n in results:
            display(n)
            database.addNode('origin', [n.id, database.addNode('eva_output', [], False)])
        end = time.time()
        elapsed = end-start
        database.addNode('start_time', [searchNode, database.addNode(start, [], False)], False, True)
        database.addNode('end_time', [searchNode, database.addNode(end, [], False)], False, True)
        database.addNode('duration', [searchNode, database.addNode(elapsed, [], False)], False, True)
    elif newInput.startswith('adj'):
        N = list(filter(lambda x: isinstance(x.value, str) and (newInput[4:] == x.value), database.nodes))[0]
        results = [database[i] for i in N.adjacent()]
        for n in results:
            display(n)
            database.addNode('origin', [n.id, database.addNode('eva_output', [], False)])
    elif newInput == 'breakpoint':
        breakpoint()
    elif newInput.startswith('refresh'):
        print(database.getNodes(newInput[8:]))
        think(database.getNodes(newInput[8:])[0].id)
    elif newInput == 'remove':
        database.nodes.pop()
    elif newInput == 'restore':
        database.nodes = json.load(open('./prevdata.json'))
    elif newInput == 'loadbackup':
        with open('eva_03_10_2022, 15_22_15.evab', 'rb') as fileRef:
            database.nodes = pickle.loads(zlib.decompress(fileRef.read()))
            database.nodes = list(map(lambda n: database.nodeTemplate(*n), database.nodes))

            database.references = []
            print('Building reference lists')
            for n in database.nodes:
                database.references.append([m.id for m in database.nodes if (n.id in m.members)])
            print('Done')
        database.save()
    elif newInput == 'uall':
        updateAll()
    elif newInput.startswith('json'):
        jsonPath = importDir+newInput[5:]
        database.addNode(jsonPath, [], False)
        with open(jsonPath) as f:
            newData = json.load(f)
        print(newData)
    # elif newInput == 'undo':
    elif newInput.startswith('$'):
        symbols = {
            '<': 'subset',
            '{': 'member',
            '[use]': 'use',
            '[melt]': 'melt',
            '[can]': 'can',
            '[contain]': 'contain',
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
    else:
        if current_question is not None:
            database.addNode('response', [inputId, current_question], True)
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
        # for r in relations:
        #     r2 = f' {r} '
        #     if r2 in newInput:
        #         rel = newInput.split(r2)
        #         if len(rel) == 2:
        #             a, b = rel
        #             for ai in a.split(','):
        #                 id_a = database.addNode(ai)
        #                 id_b = database.addNode(b)
        #                 id_c = database.addNode(r, [id_a, id_b])
        #                 database.addNode('source', [id_c, inputId])
    database.save()
