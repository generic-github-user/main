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
