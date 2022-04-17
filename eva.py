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
from functools import partial
from itertools import chain

from getsize import getsize
from hash_file import hash_file

import sys
import os

import pyparsing
from arithmetic_parser import arith
import spacy
import graphbrain
from graphbrain.parsers import create_parser

from PIL import Image
import pytesseract

import requests
from bs4 import BeautifulSoup

from node import Node
from graph import Graph
from settings import Settings
from entropy import estimateEntropy

from timefunc import timeFunc
from say import say

print('Done')


sys.path.insert(0, '../giraffe')
# from giraffe import Graph

debug = True
buffer = None
class Eva:
    genericFunctions = dict(
        sum=sum,
        mul=lambda a, b: a*b
    )
    modelName = 'en_core_web_sm'
    nlp = spacy.load(modelName)
    gbParser = create_parser(lang='en')
    selection = None

# snails.adjacent
# todo = []
# inferences = 0


logical_relations = [
    ('subset', 'subset', 'subset'),
    ('member', 'subset', 'member'),
    ('member', 'use', 'use'),
    ('member', 'can', 'can'),
    ('subset', 'can', 'can'),
    ('member', 'must', 'must'),
    ('member', 'need', 'need'),
    ('member', 'melt', 'melt'),
    ('member', 'contain', 'contain'),
    ('contain', 'contain', 'contain'),
]

def importList(data):
    for i, item in enumerate(data):
        if isinstance(item, data):
            importList(data)
        else:
            database.addNode(item, [], True)
    return data

database = Graph(savePath='./eva-db', logger=None)
timeFunc = partial(timeFunc, database)
say = partial(say, database)

# TODO: handle graphs sharing nodes
# TODO: use tensorflow models
# TODO: meta-inference


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

def nodeProperty(node, attr, update=False):
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

# logical_relations / relations
# why was getsize working before?
# expected_usefulness
# "hanging" nodes (with intermediary inferences deleted)
# time_limit wrapper function



# == length of *

def updater(node, level):
    markType(node, level=level+1)
    markLength(node, level=level+1)
    tokenize(node, level=level+1)
    markSubstrings(node, level=level+1)

def think(node=None):
    infNode = None
    start = time.time()
    if node is None:
        # weights=
        node = database.random()
    else:
        node = database[node]
    name = node.value
    say(f'Pondering {name}', level=0)

    database.updateNode(node.id, level=1, callback=updater)
    callNode = database.addNode('func_call', [database.addNode('think', [], False)], True, level=1)

    inferences = []
    random.shuffle(logical_relations)
    for R in logical_relations:
        # inferences.extend(filter(lambda m: self.nodes[m], getAdjacent(node, R[0])))
        adj = node.adjacent(R[0], True)
        # say(f'{len(adj)} nodes adjacent to {name} via {R[0]}: {adj}', level=2)
        for m1 in adj:
            for m2 in database[m1].adjacent(R[1], True):
                inferences.append(([R[2], [node.id, m2]], [m1, m2]))
    if len(inferences) > 0:
        inf = random.choice(inferences)
        newNode = database.addNode(*inf[0], False, True, level=1)
        infNode = database.addNode(
            'origin',
            [newNode, database.addNode('eva_inference', [], False)],
            False,
            True,
            level=1
        )
        database.addNode('sources', [newNode]+inf[1], False, True, level=1)
        say(
            f'Inferred relationship {database[inf[0][1][0]].value} -- {inf[0][0]} -- {database[inf[0][1][1]].value}',
            newNode, 'information', level=1
        )
    else:
        say('No viable inferences found', level=1)
    database.save()
    return callNode

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


def makePropertyBuilder():
    def builder(node, **kwargs):
        assert(isinstance(node, Node))
        if node.value not in Settings.ignoredTypes:
            typeId = database.addNode(type(node.value).__name__, [], False, **kwargs)
            m = list(filter(lambda x: x.members and node.id == x.members[0] and x.value=='type', node.referrers()))
            if (len(m) == 0):
                database.addNode('type', [node.id, typeId], **kwargs)
        return node
    return builder

def markSubstrings(node, **kwargs):
    say(f'Searching for nodes of which {node} is a substring')
    if node.value not in Settings.ignoredTypes:
        for node2 in database:
            conditions = [
                lambda: node.id != node2.id,
                lambda: node.value != node2.value,
                lambda: all(isinstance(n.value, str) for n in [node, node2]),
                lambda: node.value in node2.value,
            ]
            if  all(c() for c in conditions):
                if Settings.debugInfo:
                    say(f'{node} is a substring of {node2}')
                database.addNode('substring', [node.id, node2.id], False, True)
    return node



def markType(node, **kwargs):
    assert(isinstance(node, Node))
    if node.value not in Settings.ignoredTypes:
        typeId = database.addNode(type(node.value).__name__, [], False, **kwargs)
        # m = list(filter(lambda x: n[1]==x[1] and n[2]==x[2], nodes))
        m = list(filter(lambda x: x.members and node.id == x.members[0] and x.value=='type', node.referrers()))
        if (len(m) == 0):
            database.addNode('type', [node.id, typeId], **kwargs)
    return node

def markLength(node, **kwargs):
    assert(isinstance(node, Node))
    if node.value not in Settings.ignoredTypes and isinstance(node.value, str):
        lenId = database.addNode(len(node.value), [], False, **kwargs)
        m = list(filter(lambda x: x.members and node.id == x.members[0] and x.value=='length', node.referrers()))
        if (len(m) == 0):
            database.addNode('length', [node.id, lenId], **kwargs)
    return node

def tokenize(node, **kwargs):
    assert(isinstance(node, Node))
    say(f'Tokenizing {node}')
    if nodeProperty(node.id, 'origin')=='user_input' and (node.value not in Settings.ignoredTypes):
        tokens = node.value.split()
        if len(tokens) > 1:
            for t in tokens:
                database.addNode('token', [database.addNode(t, [], False, **kwargs), node.id], False, True, **kwargs)
    return node

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
        if n.value not in Settings.ignoredTypes and isinstance(n.value, str) and len(n.value)==3 and n.value[1]=='.':
            for r in ratings:
                if r[0]==n[1][0]:
                    database.addNode('rating', [n.id, database.addNode(r, [], False)], False, True)
                    database.addNode('group', [n.id, database.addNode('ratings', [], False)], False, True)

    say('Extracting tokens from text nodes')
    for n in nodes:
        tokenize(n)
    database.save()
    if debug:
        print('Done')

def display(n):
    print(f'{n.id} {n.value} {[database[i].value for i in n.members]}')

def hasExt(path, E):
    return any(path.endswith(ext) for ext in E.split())

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
        # if any(dir.path.endswith('.'+ext) for ext in ['png', 'jpg']):
        if hasExt(dir.path, 'png jpg PNG JPG JPEG'):
            try:
                say(f'Running Tesseract OCR on {dir.path}')
                tesseractParse = pytesseract.image_to_string(Image.open(dir.path))
                DB.addNode('tesseract_parse', [fId, DB.addNode(tesseractParse, [], False)], False, True)
            except Exception as ex:
                print(ex)
        if hasExt(dir.path, 'py js txt java md ipynb tex'):
            try:
                say(f'Reading lines from text file {dir.path}')
                with open(dir.path, 'r') as txtFile:
                    lines = txtFile.readlines()
                    if len(lines) <= 1000:
                        for line in lines:
                            DB.addNode('line_from', [DB.addNode(line, [], False), fId], False, True)
            except Exception as ex:
                print(ex)
    return count+1

# start = 'https://en.wikipedia.org/wiki/Branching_random_walk'
def html_archive(start, node):
    requested = time.time()
    text = requests.get(start).text
    parsed = BeautifulSoup(text)
    links = parsed.find_all('a')
    links = [L.get('href') for L in links]
    startNode = DB.addNode(start, [], True)
    # page_name = start.split('/')[-1]

    DB.addNode('text', [startNode, DB.addNode(text, [], True)], False, True)

    for link in links:
        # link_name = link.split('/')[-1]
        DB.addNode('links_to', [startNode, DB.addNode(link, [], True)])
    time.sleep(0.1)

def backup():
    date_format = '%m_%d_%Y, %H_%M_%S'
    backupPath = f'./eva_{datetime.now().strftime(date_format)}.evab'
    with open(backupPath, 'wb') as fileRef:
        nodeList = list(map(list, database.nodes))
        B = zlib.compress(pickle.dumps(nodeList))
        fileRef.write(B)
        say(f'Backup saved to {backupPath} [{getsize(B)} bytes]')
    # return backupPath

    callNode = database.addNode('backup', [], True)
    return callNode

commands = {}
def command(prefix):
    if not isinstance(prefix, str):
        raise TypeError

    def command_decorator(func):
        # commands.append(func)
        commands[prefix] = func
        return func
    return command_decorator

@command('quit')
def quitCommand(newInput):
    if not isinstance(newInput, str):
        raise TypeError
    say('Goodbye')
    quit()

@command('ask')
def askCommand(newInput):
    if not isinstance(newInput, str):
        raise TypeError
    t = newInput.split()
    if len(t) > 1:
        num = int(t[1])
    else:
        num = 1
    for i in range(num):
        current_question, current_link = getInfo()

@command('clear')
def clearCommand(newInput):
    if not isinstance(newInput, str):
        raise TypeError
    for i in range(50):
        print('')

@command('webcrawl')
def webcrawlCommand(newInput):
    if not isinstance(newInput, str):
        raise TypeError
    def webcrawlWrapper():
        p = newInput[9:]
        say(f'Scanning URL {p}')
        scanNode = database.addNode('web_scan', [], True)
        html_archive(p, scanNode)
        say('Done')
        return scanNode
    timeFunc(webcrawlWrapper)()


@command('crawl')
def crawlCommand(newInput):
    def crawlWrapper():
        p = newInput[6:]
        say(f'Scanning {p}')
        scan = database.addNode('file_scan', [], True)
        c = 0
        for d in os.scandir(p):
            scanDir(database, None, d, c, scan)
        say('Done')
        # !
        return scan
    timeFunc(crawlWrapper)()

@command('backup')
def backupCommand(newInput):
    timeFunc(backup)()

@command('think')
def thinkCommand(newInput):
    before = time.time()
    say(f'Current selection: {Eva.selection}')
    if Eva.selection is None:
        for j in range(Settings.opLimit):
            timeFunc(think)()
            if time.time()-before>Settings.timeLimit:
                break
    else:
        for n in Eva.selection:
            timeFunc(think)(n.id)
            if time.time()-before>Settings.timeLimit:
                break

@command('list')
def listCommand(newInput):
    target = newInput.split()[1]
    # members = list(filter(lambda x: ))
    # could this be made more efficient by first locating the node corresponding to the keyword?
    members = database.filter(lambda x: nodeProperty(x.id, 'member', False)==target)
    for m in members:
        print(m)

@command('label')
def labelCommand(newInput):
    z = random.randint(1000, 1000000)
    database.addNode(
        database.addNode('{:x}'.format(int(z)))
    )

@command('#')
def nlpCommand(newInput):
    doc = Eva.nlp(newInput[1:])
    parseNode = database.addNode('spacy_parse', [], True)
    database.addNode('source', [parseNode, inputId])
    for token in doc:
        tokenNode = database.addNode(token.text, [], True)
        database.addNode('token', [tokenNode, parseNode], True)
        database.addNode('dep', [tokenNode, database.addNode(token.dep_, [], False)], True)
        database.addNode('pos', [tokenNode, database.addNode(token.pos_, [], False)], True)
        database.addNode('head', [tokenNode, database.addNode(token.head.text, [], False)], True)

@command('find')
def findCommand(newInput):
    start = time.time()
    # TODO: clean this up
    searchNode = database.addNode('search_cmd', [], True)
    database.addNode('source', [searchNode, inputId])
    results = list(filter(lambda x: isinstance(x.value, str) and (newInput[5:] in x.value), database.nodes))
    for n in results:
        print(n)
        database.addNode('origin', [n.id, database.addNode('eva_output', [], False)])
    end = time.time()
    elapsed = end-start
    database.addNode('start_time', [searchNode, database.addNode(start, [], False)], False, True)
    database.addNode('end_time', [searchNode, database.addNode(end, [], False)], False, True)
    database.addNode('duration', [searchNode, database.addNode(elapsed, [], False)], False, True)

@command('loadbackup')
def loadbackupCommand(newInput):
    with open('eva_03_17_2022, 11_41_04.evab', 'rb') as fileRef:
        database.nodes = pickle.loads(zlib.decompress(fileRef.read()))
        database.nodes = list(map(lambda n: database.nodeTemplate(*n), database.nodes))

        database.references = []
        print(f'Building reference lists for {len(database.nodes)} nodes')
        for i, n in enumerate(database.nodes):
            if (i % 1000 == 0):
                say(f'Processed {i} nodes')
            if n.value not in ['origin', 'accessed', 'source', 'type']:
                database.references.append([m.id for m in database.nodes if (n.id in m.members)])
            else:
                database.references.append([])
        print('Done')
    database.save()

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
        (".", 2, pyparsing.opAssoc.LEFT),
        (";", 2, pyparsing.opAssoc.LEFT),
        ("/", 2, pyparsing.opAssoc.LEFT),
        (">", 2, pyparsing.opAssoc.LEFT),
        ("^", 2, pyparsing.opAssoc.LEFT),
        ("?", 2, pyparsing.opAssoc.LEFT),
    ],
)


@command('@')
def queryCommand(newInput):
    parsed = expr.parseString(newInput[1:])
    print('Parsed as:')
    print(parsed)
    def queryGenerator(query):
        def newQuery():
            output = database.filter(lambda n: n.value==query[0][0])[0]
            for ci in range((len(query[0])-1)//2):
                # A, op, B = cond
                op, B = query[0][ci*2+1:ci*2+3]
                if op == '/':
                    func = lambda n: n.adjacent(B, return_ids=False)
                elif op == '^':
                    func = lambda n: n.referrers()
                # elif op == ';':
                #     func = lambda g: [think(n.id) for n in g]
                # output = output.nodeFilter(func)
                output = func(output)

                # database.addNode('user_selection')
            # selection = output
            return output
        return newQuery

    Q = queryGenerator(parsed)
    results = Q()
    say(f'Found {len(results)} matching nodes')
    say('Updating selection')
    Eva.selection = results
    print(results)
    for r in results:
        print(r)
    return results

@command('adj')
def adjCommand(newInput):
    N = list(filter(lambda x: isinstance(x.value, str) and (newInput[4:] == x.value), database))[0]
    results = [database[i] for i in N.adjacent()]
    for n in results:
        print(n)
        database.addNode('origin', [n.id, database.addNode('eva_output', [], False)])

@command('breakpoint')
def breakpointCommand(newInput):
    breakpoint()

@command('$')
def relationCommand(newInput):
    symbols = {
        '<': 'subset',
        '{': 'member',
        '[use]': 'use',
        '[melt]': 'melt',
        '[can]': 'can',
        '[contain]': 'contain',
        '[must]': 'must',
        '[need]': 'need',
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

@command('json')
def jsonCommand(newInput):
    jsonPath = Settings.importDir + newInput[5:]
    database.addNode(jsonPath, [], False)
    with open(jsonPath) as f:
        newData = json.load(f)
    print(newData)

@command('remove')
def removeCommand(newInput):
    database.nodes.pop()

@command('restore')
def restoreCommand(newInput):
    database.nodes = json.load(open('./prevdata.json'))

@command('print')
def printCommand(newInput):
    print('10 most recent nodes:')
    N = len(database)
    for x in range(N-10, N):
        say(str(database[x]))

@command('refresh')
def refreshCommand(newInput):
    print(database.getNodes(newInput[8:]))
    think(database.getNodes(newInput[8:])[0].id)

@command('uall')
def updateCommand(newInput):
    updateAll()

# def mapCommand

current_question = None
current_link = None
relations = ['are', 'is a', 'has', 'have']
for i in range(1000):
    newInput = input()
    inputId = database.addNode(newInput, [], True)
    database.addNode(
        'origin',
        [inputId, database.addNode('user_input', [], False)]
    )
    database.save()

    for prefix, f in commands.items():
        if newInput.startswith(prefix):
            f(newInput)

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
    database.save()
