from collections import namedtuple
import pickle

class Graph:
    def __init__(self, nodes=None, hashmap=None, savePath='./saved_graph', fields='id value members time', references=None, parent=None):
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
        for n in self.nodes:
            self.hashmap[n.id] = n
        return self

    def getNodes(self, value):
        return Graph(list(filter(lambda n: n[1]==value, self.nodes)), parent=self.parent)
        # return Graph(hashmap={k: v for k, v in self.hashmap.items() if v.value==value})

    def search(self, info):
        return Graph(list(filter(lambda n: nodeMatch(n, info), self.nodes)), parent=self.parent)
        # return Graph(hashmap={k: v for k, v in self.hashmap.items() if nodeMatch(v, info)})

    def filter(self, condition):
        # return Graph(list(filter(condition, self.nodes)))
        say(f'Searching {len(self)} nodes')
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
            if (x % 10000 == 0):
                say(f'Checked {x}/{len(self)} nodes')
        return Graph(result, references=newrefs, parent=self.parent)
        # return outGraph

    def nodeFilter(self, condition):
        return self.filter(lambda n: condition(Node(n.id, self.parent, n)))

    def updateNode(self, node, level=0):
        assert(isinstance(node, int))

        if self[node].value not in ignoredTypes:
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
            say(f'Found {numAdj} adjacent nodes', level=level+1)
            self.addNode('num_adjacent', [node, self.addNode(numAdj, [], False)], False, True, level=level+1)
            markType(self[node], level=level+1)
            markLength(self[node], level=level+1)
            tokenize(self[node], level=level+1)
            markSubstrings(self[node], level=level+1)

            current = self[node]
            if current.value not in ignoredTypes and isinstance(current.value, str):
                if isinstance(current.value, str):
                    est = estimateEntropy(bytes(current.value, 'UTF-8'))
                else:
                    est = estimateEntropy(bytes(current.value))
                say(f'Estimated entropy of {current.value} is {est}', level=level+1)
                entId = self.addNode(est, [], False, level=level+1)
                m = list(filter(lambda x: x.members and current.id == x.members[0] and x.value=='entropy_estimate', current.referrers()))
                if (len(m) == 0):
                    self.addNode('entropy_estimate', [current.id, entId], level=level+1)

        return node

    def addNode(self, value, members=None, duplicate=True, useSearch=False, update=False, level=0):
        assert(isinstance(members, list) or members is None)
        assert(isinstance(duplicate, bool))
        assert(isinstance(useSearch, bool))
        assert(isinstance(update, bool))

        newId = getId()
        if useSearch:
            matches = self.search([None, value, members, None])
        else:
            matches = self.getNodes(value)
        if Eva.debugInfo:
            say(f'Search results: {matches}', level=level+1)
        if (duplicate or not matches):
                say(f'Creating node {value} with members [{"; ".join(str(m) for m in members)}]', level=level+1)
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
        if Eva.debugInfo:
            say('Updating node', level=level+1)
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
