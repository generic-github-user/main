#!/usr/bin/env python
# coding: utf-8

import nltk
from fuzzywuzzy import fuzz
import string
import random
import itertools
import pprint
import pyvis
from IPython.display import JSON
import numpy as np
import matplotlib.pyplot as plt

from graph import Graph
from randomgraph import RandomGraph
from completegraph import CompleteGraph
from gridgraph import GridGraph




R = RandomGraph(100, 100, weighted=True)
print(random.choice(R.nodes).weight)
# R.visualize(width=1000, height=1000, node_options={'shape': 'circle'})



# dynamic graphs/temporal analysis
# add advanced graph indexing syntax


# In[386]:


class Randomizer:
    def __init__(self, lower=0, upper=1, distribution='uniform', form='continuous'):
        self.lower = lower
        self.upper = upper
        self.distribution = distribution

    def sample(self):
        return getattr(random, self.distribution)(self.lower, self.upper)

    def __call__(self):
        return self.sample()


# R.visualize(width=1000, height=1000, node_options={'shape': 'circle'})


# In[233]:


# list(map(str,R.nodes))
[list(map(str,x.grouped)) for x in R.nodes]


# In[240]:





# In[241]:


for cls in [Graph, Node]:
    if hasattr(cls, 'init'):
        setattr(cls, '__init__', getattr(cls, 'init'))


# G = Graph()
# G.add_nodes(pairs, metadata=[dict(cat='similarity'), dict(cat='text')]).nodes[0].value
# G.visualize(width=1000, height=1000)


# In[244]:





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
