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
    [['O2'], ['+']],
    [['O2'], ['-']],
    [['O2'], ['*']],
    [['O2'], ['/']],
    [['O2'], ['^'], 3],
    [['O2'], ['frac']],
    [['O1'], ['sqrt']],
    [['O1'], ['abs']],
    [['O1'], ['trig'], 1],
    [['O1'], ['fact']],
#     identity/input
#     [['$'], ['I']],
]
functions = [
    ['+', operator.add, '+', 2],
    ['-', operator.sub, '-', 2],
    ['*', operator.mul, '\cdot', 2],
    ['/', operator.truediv, '\div', 2],
    ['^', lambda a, b: (a ** b), '^', 2],
    ['frac', operator.truediv, r'\frac', 2],
    ['sqrt', lambda a: (a ** (1/2)), '\sqrt', 1],
    ['abs', abs, '|$|', 1],
    ['fact', math.factorial, '$!', 1],
#     ['sqrt', lambda a: math.factorial(a), '', 1]
]
trig_funcs = 'sin cos tan csc sec cot'.split()
for t in trig_funcs:
    functions.append([t, lambda a: math.sin(a), f'\\{t}'])
    expressions.append([['trig'], [t], 1])
# In[ ]:


def safe_op(k, l):
    try:
        val = k(*l)
        if val > 10e30:
            val = 10e3
        return val
    except:
        return 0
