#!/usr/bin/env python
# coding: utf-8

# In[11]:


import numpy as np
import matplotlib.pyplot as plt
import itertools


# In[12]:


# offsets = list(itertools.product([-1, 0, 1], repeat=2))
offsets = [[0, 1], [0, -1], [1, 0], [-1, 0]]
offsets = list(map(np.array, offsets))
print(offsets)
