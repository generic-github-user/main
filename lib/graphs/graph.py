import pyvis
import itertools
import numpy as np
import random

from node import Node

class Graph:
    def __init__(self, nodes=None, duplicate=False, u=False, **kwargs):
        if nodes is None:
            nodes = []
#         self.nodes = nodes
        self.nodes = []
        self.duplicate = duplicate
        if nodes:
            self.add_nodes(nodes, duplicate=u, **kwargs)

class Graph(Graph):
    def visualize(self, node_options={}, edge_options={}, **kwargs):
        self.visualization = pyvis.network.Network(notebook=True, **kwargs)
        added_nodes = []
        for node in self.nodes:
            text = node.value
            if not node.grouped:
#                 print(node.degree())


#                 deg = node.value

                if type(node.value) is str:
                    metric = len(node.value)
                else:
                    metric = node.value

#                 metric = node.degree()
                deg = f'hsl({metric*6}, 80%, 50%)'

                if not text:
                    text = ' '
                self.visualization.add_node(id(node), label=text, group=deg, **node_options)#, color=deg)#, size=deg**(1/4)*10)
#             for g in node.grouped:
#                 self.visualization.add_edge(text, g.value)
        for node in self.nodes:
#             print([list(map(str, n.grouped)) for n in self.nodes])
            defaults = {
                'smooth': True
            }
            edge_options = defaults | edge_options
            if len(node.grouped) == 2:
                if type(node.value) in [int, float]:
#                     d = int(10e2*1/(node.value*0.1))

                    try:
                        self.visualization.add_edge(*[id(x) for x in node.grouped], label=node.value, **edge_options)
                    except:
                        pass
                else:
                    try:
                        self.visualization.add_edge(*[id(x) for x in node.grouped], label=node.value, **edge_options)
                    except:
                        pass
        return self.visualization.show('./visualization.html')

class Graph(Graph):
    def find(self, **kwargs):
        defaults = dict(unique=True)
        kwargs |= defaults
#         return list(filter(lambda n: n.value == x and n.unique, self.nodes))
        results = list(filter(lambda n: all((k in vars(n) and getattr(n, k) == v) for k, v in kwargs.items()), self.nodes))
        return Graph(nodes=results, duplicate=self.duplicate)

class Graph(Graph):
    def add_node(self, data, duplicate=False, return_node=True, metadata=None):
        new_node = None
#         if hasattr(self, 'duplicate'):
#         print(vars(self))
#         if duplicate is None:
#             duplicate = self.duplicate

        if type(data) in [list, tuple]:
            matches = self.find(value=data[0])
            if (not matches) or duplicate:# or data[0] in '+':
                connecting_node = Node(data[0], data[1:], graph=self, metadata=metadata, duplicate=duplicate)
    #             self.nodes.append(connecting_node)
#                 self.add_node(connecting_node)
                self.add_node(connecting_node, metadata=metadata, duplicate=duplicate)
                new_node = connecting_node
            elif matches:
                new_node = matches[0]
        elif type(data) in [Node]:
            matches = self.find(value=data.value)
#             print(matches, data.value)
            if (not matches) or duplicate:# or data.unique:
#             if not matches or type(data.value) is int:
                self.nodes.append(data)
                new_node = data
            elif matches:
                new_node = matches[0]
        elif type(data) in [str, int, float, bool]:
            matches = self.find(value=data)
            if (not matches) or (duplicate and str(data) == '   '):
#                 print(data, matches.nodes, Node(data).value)
                new_node = Node(data, graph=self, metadata=metadata, duplicate=duplicate)
            elif matches:
                new_node = matches[0]

        if return_node == 'inner':
            return new_node.grouped
        elif return_node:
            return new_node
        else:
            return self

class Graph(Graph):
    def sample(self, n=1):
        return Graph(nodes=random.sample(self.nodes, k=n))

    def sample_nodes(self, n=1):
        return random.sample(self.nodes, k=n)

    def add_nodes(self, x, **kwargs):
        for xi in x:
            self.add_node(xi, **kwargs)
        return self

    def join(self, x, q='s'):
        lx = len(x.nodes)
        for i in range(lx):
            val = x.nodes[i].value
            if 'e' not in val:
                self.nodes[i].extend(x.nodes[i].value+str(i)+q, f'e{val}{i}'+q, duplicate=True)
        return self

class Graph(Graph):
    def __getitem__(self, i):
        return self.nodes[i]

    def __bool__(self):
        return bool(self.nodes)

# semi-toroidal graphs

class Graph(Graph):
    def AdjacencyMatrix(self, use_weights=True, weight_prop='weight'):
        matrix = np.zeros([len(self.nodes)//2+2]*2)
        for a, b in itertools.product(self.nodes, repeat=2):
            if a in b.adjacent():
                connecting_node = list(filter(lambda x: all(y in x.grouped for y in [a, b]), self.nodes))[0]
                if use_weights and hasattr(connecting_node, weight_prop):
                    value = getattr(connecting_node, weight_prop)
                else:
                    value = 1
                matrix[self.nodes.index(a), self.nodes.index(b)] = value
        return matrix
