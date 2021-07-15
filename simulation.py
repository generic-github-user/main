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


# In[14]:




schematic = """
              v                                 
              v                                 
    i>>->>x>->x>>>>>>>>>>>>>>>>>>>>>>>>>>>>>j   
       v  ^ v |                                 
  i>>>> />- ->a                                 
       | v    v                                 
       ->a>>>>o                                 
              v                                 
              v       ??????                    
"""


num_states = 2

# TODO: generate directed graph of components/oeprators
chr(172)
# xor = (1-np.max(q))*np.max(q)
xor = lambda q: np.sum(q) % 2
operators = [
    ['i', 'input', '#', None, True],
    ['.', 'identity', '.', np.max, True],
    ['-', 'identity', '-', np.max, True],
    ['o', 'or', 'o', np.max, True],
#     ['?', 'random', '?', lambda q: np.random.randint(num_states), True],
    ['j', 'output', '.', np.max, True],
    ['a', 'and', '∧', np.min, True],
    ['x', 'xor', '⊻', xor, True],
    ['|', 'vpull', '|', lambda x, y: (x-2, y), False],
    ['/', 'hpull', '/', lambda x, y: (x, y-2), False],
#     double-check these
    ['<', 'left', '<', lambda x, y: (x, y+1), False],
    ['>', 'right', '>', lambda x, y: (x, y-1), False],
    ['^', 'up', '^', lambda x, y: (x+1, y), False],
    ['v', 'down', 'v', lambda x, y: (x-1, y), False],
]
