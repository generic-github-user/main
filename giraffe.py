#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk
from fuzzywuzzy import fuzz
import string
import random
import itertools
import pprint
import pyvis
from IPython.display import JSON


# In[2]:


hamlet = nltk.corpus.gutenberg.sents('shakespeare-hamlet.txt')
def words_to_sent(w):
    s = w[0]
    s += ''.join([t if t in string.punctuation else ' '+t for t in w[1:]])
    return s
hamlet = list(map(words_to_sent, hamlet))
hamlet = list(filter(lambda l: len(l) >= 10, hamlet))


# In[3]:


len(hamlet)


# In[4]:


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
    dist = fuzz.token_sort_ratio(x, y)
    if 60 < dist < 97:
        pairs.append([dist, x, y])
    if len(pairs) >= limit:
        break

pprinter = pprint.PrettyPrinter()
pprinter.pprint(pairs[:5])
print(len(pairs))


# In[6]:


G.find(random.choice(G.nodes).value)


# In[323]:


class Graph:
    def __init__(self, nodes=None, duplicate=False, u=False, **kwargs):
        if nodes is None:
            nodes = []
#         self.nodes = nodes
        self.nodes = []
        self.duplicate = duplicate
        if nodes:
            self.add_nodes(nodes, duplicate=u, **kwargs)
        
    def visualize(self, node_options={}, edge_options={}, **kwargs):
        self.visualization = pyvis.network.Network(notebook=True, **kwargs)
        added_nodes = []
        for node in self.nodes:
            text = node.value
            if not node.grouped:
#                 print(node.degree())
                
#                 deg = node.degree()
#                 deg = node.value

                if type(node.value) is str:
                    metric = len(node.value)
                else:
                    metric = node.value
                deg = f'hsl({metric*6}, 80%, 50%)'
                if not text:
                    text = ' '
                self.visualization.add_node(id(node), label=text, group=deg, **node_options)#, color=deg)#, size=deg**(1/4)*10)
#             for g in node.grouped:
#                 self.visualization.add_edge(text, g.value)
        for node in self.nodes:
#             print([list(map(str, n.grouped)) for n in self.nodes])
            if len(node.grouped) == 2:
                if type(node.value) in [int, float]:
                    d = int(10e2*1/(node.value*0.1))
                    
                    self.visualization.add_edge(*[id(x) for x in node.grouped], length=d, label=node.value, **edge_options)
                else:
                    try:
                        self.visualization.add_edge(*[id(x) for x in node.grouped], label=node.value, smooth=True, **edge_options)
                    except:
                        pass
        return self.visualization.show('./visualization.html')
    
    def find(self, **kwargs):
        defaults = dict(unique=True)
        kwargs |= defaults
#         return list(filter(lambda n: n.value == x and n.unique, self.nodes))
        results = list(filter(lambda n: all((k in vars(n) and getattr(n, k) == v) for k, v in kwargs.items()), self.nodes))
        return Graph(nodes=results, duplicate=self.duplicate)
    
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
    
    def adjacent(self, exclude=None):
        grouping_nodes = [x for x in self.graph.nodes if (self in x.grouped)]
        return Graph(nodes=[n for gn in grouping_nodes for n in gn.grouped if (n is not self and (not exclude or n not in exclude.nodes))])
    
    def extend(self, z, w, **kwargs):
        self.graph.add_node([w, self, z], **kwargs)
        return self
    
    def __str__(self):
        return str(self.value)
        
for cls in [Graph, Node]:
    if hasattr(cls, 'init'):
        setattr(cls, '__init__', getattr(cls, 'init'))
    

# G = Graph()
# G.add_nodes(pairs, metadata=[dict(cat='similarity'), dict(cat='text')]).nodes[0].value
# G.visualize(width=1000, height=1000)


# In[330]:


symbols = '++--'
num = [dict(cat='num')]
op = [dict(unique=False), dict(unique=False)]
# G = Graph(nodes=[1, 1], duplicate=True, metadata=num)

L = 6
#     start_values = [2, 12, 4, 32, 7]
start_values = [random.randint(-10, 10) for i in range(6)]
G = Graph(start_values, False, False, metadata=num)


# graph lambda
# rule class/strings?
# Graph(rule=)


# In[326]:


S = 'know'
G = Graph([S], False, False)
# for t in range(2):
#     B = G.nodes[t]
f = 0
done = []
for B in G.nodes:
    v = B.value
    if ' ' not in v:
        for i in range(len(v)):
            R = v[:i]+v[i+1:]
            if len(R)>0:
                B.extend(R, '   ', metadata=num, duplicate=True)
                f += 1
    if f > 200:
        break

# options = {'font': {'background': 'white'}}
options = {}
G.visualize(node_options={'shape': 'circle'}, edge_options=options, width=1000, height=1000, directed=True)


# In[267]:


G.nodes.__sizeof__()


# In[280]:


len(G.nodes)


# In[88]:


j


# In[282]:


# list(map(str, G.nodes))


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


# In[ ]:


# G.add_node([5], return_node=False).nodes
list(map(str,G.nodes))
# add callbacks


# In[ ]:


r = G.find(cat='text').sample_nodes()[0]
visited = Graph()
for i in range(20):
    print(r.value)
    visited.add_node(r)
    neighbors = r.adjacent(exclude=visited).nodes
    if neighbors:
        r = neighbors[0]
    else:
        break


# In[ ]:


r[0].cat


# In[284]:


# G.nodes[35].grouped
# G.nodes
# sorted(list(map(str, [list(map(str, g.grouped)) for g in G.nodes])), reverse=True)
sorted(list(map(lambda x: (str(x.value)), G.nodes)))


# In[ ]:


JSON(G.nodes)


# In[ ]:




