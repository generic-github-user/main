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


# In[5]:


w = 800
def clip(x):
    return x[:20]

c = random.choices(hamlet, k=w*2)
a = c[:w]
b = c[w:]

a, b = map(clip, a), map(clip, b)
pairs = []
limit = 1000
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
    
    def sample(self, n=1):
        return Graph(nodes=random.sample(self.nodes, k=n))
    
    def sample_nodes(self, n=1):
        return random.sample(self.nodes, k=n)
    
    def add_nodes(self, x, **kwargs):
        for xi in x:
            self.add_node(xi, **kwargs)
        return self
    
    def __getitem__(self, i):
        return self.nodes[i]
    
    def __bool__(self):
        return bool(self.nodes)
    
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
            
    def __str__(self):
        return str(self.value)
        
for cls in [Graph, Node]:
    setattr(cls, '__init__', getattr(cls, 'init'))
    

G = Graph()
G.add_nodes(pairs).nodes[0].value
G.visualize(width=800, height=800)

# Graph(rule=)


# In[87]:


G.nodes.__sizeof__()


# In[88]:


j


# In[199]:


list(map(str, G.nodes))


# In[90]:


G.find(cat='num').nodes


# In[91]:


# [c.cat for c in G.nodes]
for c in G.nodes:
#     if hasattr(c, 'cat'):
#         print(c.cat, c.value)
    print(c.value, list(map(str, c.grouped)), c.unique)


# In[ ]:


G.duplicate


# G.nodes[35].grouped
# G.nodes
sorted(list(map(str, [list(map(str, g.grouped)) for g in G.nodes])), reverse=True)


# In[109]:


JSON(G.nodes)


# In[ ]:




