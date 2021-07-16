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

colors = {}
# for i in range(len(operators)):
#     if operators[i][0] != '.':
#         colors.append(num_states + i)
#         colors[operators[i][0]] = (num_states + i)
#     else:
#         colors.append(None)
#         colors[operators[i][0]] = None

c=0
for op in operators:
    if op[0] in 'xajio':
        colors[op[0]] = (num_states + c)
        c += 1

repetitions = 5
S = np.array(list(filter(None, map(list, schematic.splitlines()))))
S = np.swapaxes(np.tile(S.T, repetitions), 0, 1)
values = np.full_like(S, -1, dtype=int)

inputs = [1,0,0]*repetitions
strict_inputs = True
directions = '<>^v'
history = []
