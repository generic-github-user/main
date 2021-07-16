#!/usr/bin/env python
# coding: utf-8

# In[108]:


import nltk
from fuzzywuzzy import fuzz
import string
import random
import itertools
import pprint
import pyvis
from IPython.display import JSON


# In[8]:


hamlet = nltk.corpus.gutenberg.sents('shakespeare-hamlet.txt')
def words_to_sent(w):
    s = w[0]
    s += ''.join([t if t in string.punctuation else ' '+t for t in w[1:]])
    return s
hamlet = list(map(words_to_sent, hamlet))
hamlet = list(filter(lambda l: len(l) >= 10, hamlet))


# In[96]:


pyvis.network.Network.add_node


# In[225]:


w = 200
def clip(x):
    return x[:20]
a = random.choices(hamlet, k=w)
b = random.choices(hamlet, k=w)
a, b = map(clip, a), map(clip, b)
pairs = []
limit = 400
for x, y in itertools.product(a, b):
    dist = fuzz.token_set_ratio(x, y)
    if dist > 60:
        pairs.append([dist, x, y])
    if len(pairs) >= limit:
        break

pprinter = pprint.PrettyPrinter()
pprinter.pprint(pairs[:5])
print(len(pairs))


# In[218]:


G.find(random.choice(G.nodes).value)


# In[226]:


class Graph:
    def init(self, nodes=None):
        if nodes is None:
            nodes = []
        self.nodes = nodes
        
    def visualize(self, **kwargs):
        self.visualization = pyvis.network.Network(notebook=True, **kwargs)
        added_nodes = []
        for node in self.nodes:
            text = node.value
            if not node.grouped:
#                 print(node.degree())
                deg = node.degree()
                self.visualization.add_node(text, group=deg, size=10)#, size=deg**(1/4)*10)
#             for g in node.grouped:
#                 self.visualization.add_edge(text, g.value)
        for node in self.nodes:
            if len(node.grouped) == 2:
                d = int(10e2*1/(node.value*0.1))
#                 print([n.grouped for n in self.nodes])
                self.visualization.add_edge(*[x.value for x in node.grouped], length=d, label=node.value)
        return self.visualization.show('./visualization.html')
    
    def find(self, x):
        return list(filter(lambda n: n.value == x and n.unique, self.nodes))
    
    def add_node(self, data, duplicate=False, return_node=True):
        new_node = None
        if type(data) in [list, tuple]:
            matches = self.find(data[0])
            if (not matches) or duplicate:
                connecting_node = Node(data[0], data[1:], graph=self)
    #             self.nodes.append(connecting_node)
                self.add_node(connecting_node)
                new_node = connecting_node
            elif matches:
                new_node = matches[0]
        elif type(data) in [Node]:
            matches = self.find(data.value)
#             print(matches, data.value)
            if (not matches) or duplicate:
#             if not matches or type(data.value) is int:
                self.nodes.append(data)
                new_node = data
            elif matches:
                new_node = matches[0]
        elif type(data) in [str, int, float, bool]:
            matches = self.find(data)
            if (not matches) or duplicate:
                new_node = Node(data, graph=self)
            elif matches:
                new_node = matches[0]
        
        if return_node:
            return new_node
        else:
            return self
    
    def add_nodes(self, x):
        for xi in x:
            self.add_node(xi)
        return self
            
class Node:
    def init(self, value, grouped=None, graph=None):
        self.value = value
        if grouped is None:
            grouped = []
#         self.grouped = [g if type(g) is Node else Node(g, graph=graph) for g in grouped]
        self.graph = graph
        self.grouped = [g if type(g) is Node else self.graph.add_node(g) for g in grouped]
        self.unique = not (type(self.value) is int)
        if graph:
            graph.add_node(self)
            
    def degree(self):
        self.deg = None
        if self.graph:
#             self.deg = sum(int(self in x.grouped) for x in self.graph.nodes)
#             self.deg = sum(map(bool, self.graph.find(self.value)))
            self.deg = sum(self in x.grouped for x in self.graph.nodes)
#             print(self.deg)
        return self.deg
        
for cls in [Graph, Node]:
    setattr(cls, '__init__', getattr(cls, 'init'))
    
