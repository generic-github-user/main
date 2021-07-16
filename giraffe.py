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
        return self.visualization.show('./visualization.html')
