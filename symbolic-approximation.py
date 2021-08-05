#!/usr/bin/env python
# coding: utf-8

# In[989]:


import numpy as np
import operator
import random
from IPython.display import Latex, Math
import IPython.display as display
import math
import matplotlib.pyplot as plt


# In[624]:


# Math()


# In[2]:


X = np.arange(10)
Y = np.random.randint(0, 20, 10)


# In[3935]:


# string rewriting?
expressions = [
    [['$'], ['F'], 1],
#     [['$'], ['E']],
#     [['F'], [[lambda: random.choice(functions[:3])[0], ['E', 'E']]]],
#     [['F'], [[lambda: random.choice(functions[3:])[0], ['E']]]],
    [['F'], [['O2', ['E', 'E']]], 3],
    [['F'], [['O1', ['E']]]],
#     identity/input
#     [['$'], ['I']],
]
