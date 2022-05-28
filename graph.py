from collections import namedtuple
import pickle
import time
import random
from functools import partial

from helpers.getsize import getsize
from helpers.entropy import estimateEntropy

from node import Node
# import node
# Node = node.Node

from settings import Settings
from globals import Eva

# say = partial(say, Eva.database)

# A generic graph data structure (more specifically, a metagraph, which does not distinguish between nodes and edges)
class Graph:
    def __init__(self, nodes=None, hashmap=None, savePath='./saved_graph', fields='id value members time', references=None, parent=None, logger=None):
        if not (parent is None or isinstance(parent, Graph)):
            raise TypeError

        self.savePath = savePath
        self.nodes = nodes
        self.fields = fields
        self.nodeTemplate = namedtuple('node', fields)
        if references is None:
            references = []
        self.references = references

        if parent is None:
            parent = self
        self.parent = parent

        if hashmap is None:
            hashmap = {}
        self.hashmap = hashmap

        if self.nodes is None:
            self.nodes = []
            self.load()
        else:
            for n in self.nodes:
                self.hashmap[n.id] = n

        if logger is None:
            def L(*args, **kwargs):
                print(*args)
            logger = L
        self.logger = logger

    def getId(self):
        return len(self.nodes)

    def load(self):
        try:
            print('Loading database')
            with open(self.savePath, 'rb') as fileRef:
                self.nodes = pickle.load(fileRef)
        except Exception as error:
            print(error)
            self.nodes = []
            self.hashmap = {}

        self.nodes = list(map(lambda n: self.nodeTemplate(*n), self.nodes))
        for n in self.nodes:
            self.hashmap[n.id] = n
        return self

    # Returns a new graph containing only the nodes for which condition evaluates to true
    def filter(self, condition, log=False):
        if log:
            self.logger(f'Searching {len(self)} nodes')
        Eva.loglevel += 1
        result = []
        newrefs = []
        # outGraph = Graph()
        for x in range(len(self)):
            # node = self.get(x, False)
            node = self.nodes[x]
            if condition(node):
                result.append(node)
                # outGraph.addNode()
                newrefs.append(self.references[x])
            if (x % 10000 == 0) and log:
                self.logger(f'Checked {x}/{len(self)} nodes')
        Eva.loglevel -= 1
        return Graph(result, references=newrefs, parent=self.parent)
        # return outGraph

    def nodeFilter(self, condition):
        return self.filter(lambda n: condition(Node(n.id, self.parent, n)))

    def search(self, **kwargs):
#        return self.filter(lambda n: n.value == value)
        return self.filter(lambda n: all(getattr(n, k) == v for k, v in kwargs.items()))

    def map(self, f):
        return Graph(map(f, self.nodes), parent=self.parent)

    # A callback used when a graph update needs to be propagated to a node; updates information such as adjacency lists
    def updateNode(self, node, level=0, callback=None):
        assert(isinstance(node, int))
        self.logger(f'Updating node {node}')
        Eva.loglevel += 1

        if self[node].value not in Settings.ignoredTypes:
            self.addNode(
                'processed_flag',
                [node],
                False, True, level=level+1
            )
            self.addNode(
                'unit',
                [
                    self.addNode('size', [node, self.addNode(getsize(self[node]), [], False)], False, True, level=level+1),
                    self.addNode('byte', [], False, level=level+1)
                ], level=level+1
            )
            # self.addNode('neighborhood_size', [node, self.addNode(len())])
            numAdj = len(self[node].adjacent())
            self.logger(f'Found {numAdj} adjacent nodes', level=level+1)
            self.addNode('num_adjacent', [node, self.addNode(numAdj, [], False)], False, True, level=level+1)
            if callback is not None:
                callback(self[node], level+1)

            current = self[node]
            if current.value not in Settings.ignoredTypes and isinstance(current.value, str):
                if isinstance(current.value, str):
                    est = estimateEntropy(bytes(current.value, 'UTF-8'))
                else:
                    est = estimateEntropy(bytes(current.value))
                self.logger(f'Estimated entropy of {current.value} is {est}', level=level+1)
                entId = self.addNode(est, [], False, level=level+1)
                m = list(filter(lambda x: x.members and current.id == x.members[0] and x.value=='entropy_estimate', current.referrers()))
                if (len(m) == 0):
                    self.addNode('entropy_estimate', [current.id, entId], level=level+1)

        Eva.loglevel -= 1
        return node

    # Add a node to the graph
    def addNode(self, value, members=None, duplicate=True, useMembers=False, update=False, level=0):
        assert(isinstance(members, list) or members is None)
        assert(isinstance(duplicate, bool))
        assert(isinstance(useMembers, bool))
        assert(isinstance(update, bool))

        newId = self.getId()
        if not duplicate:
            if useMembers:
                matches = self.search(value=value, members=members)
            else:
                matches = self.search(value=value)
            if Settings.debugInfo:
                self.logger(f'Search results: {matches}', level=level+1)

        if (duplicate or not matches):
                self.logger(f'Creating node {value} with members [{"; ".join(str(m) for m in members)}]', level=level+1)
                if members is None:
                    members = []
                nodeData = [newId, value, members, time.time()]
                self.nodes.append(self.nodeTemplate(*nodeData))
                self.references.append([])
                for m in members:
                    if m is not None:
                        self.references[m].append(newId)
        else:
                return matches[0].id
        if Settings.debugInfo:
            self.logger('Updating node', level=level+1)
        if update:
            # TODO: pass callback
            self.updateNode(newId)
        return newId

    # Write the graph to a local file to be reused later
    def save(self):
        if len(self) > 80000:
            with open(self.savePath, 'wb') as fileRef:
                nodeList = list(map(list, self.nodes))
                pickle.dump(nodeList, fileRef)
            with open('./cache', 'wb') as cRef:
                pickle.dump(self.references, cRef)
        else:
            self.logger('Database integrity check failed; terminating save')
        return self

    # Select a random node from this graph
    def random(self, weighted=True):
        if not isinstance(weighted, bool):
            raise TypeError

        # W = [0.9 if nodeProperty(n.id, 'origin')=='user_input' else 0.1 for n in self]
        W = [0.9 if (n.value not in Settings.ignoredTypes and isinstance(n.value, str)) else 0.1 for n in self.nodes]
        if weighted:
            node = random.choices(self.nodes, weights=W, k=1)[0]
        else:
            node = random.choice(self.nodes)
        node = Node(node.id, self.parent, node)
        assert(isinstance(node, Node))
        return node

    def get(self, i, update=False):
        # assert(isinstance(i, (int, slice)))
        assert(isinstance(update, bool))

        if isinstance(i, int):
            # todo: call updateNode?
            if update:
                self.addNode('accessed', [i, self.addNode(time.time(), [], False)])
            return Node(self.nodes[i].id, self.parent, self.nodes[i])
        elif isinstance(i, slice):
            return Graph(self.nodes[i], self.savePath, parent=self.parent)
        elif (i is None):
            return None
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
            return Node(node.id, self.parent, node)
        return map(nodeWrapper, self.nodes)
