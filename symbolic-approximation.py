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
    [['E'], ['V']], #C
#     Grammar example; polynomial generation
#     [['V'], ['P']],
#     [['exp'], [['^', ['x', 'int']]]],
#     [['P'], [['+', ['term', 'term']]]],
#     [['term'], [['*', ['int', 'exp']]]],
    
#     [['E'], ['F']],
    [['V'], ['F'], 20],
    [['V'], ['x']],
    [['V'], ['y']],
    [['V'], ['int']],
#     [['O'], [lambda: random.choice(filter(lambda a: a[3]symbols['O']))[0]]],
#     [['V'], [lambda: random.choice(symbols['V'])()]],
    [['int'], [lambda: np.random.randint(-5, 5)], 2],
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
values = [
    ['constant', [lambda: np.random.randint(-5, 5)]]
]
symbols = {
    'O': functions,
    'V': values
}

expressions = [(e+[1] if len(e)==2 else e) for e in expressions]
expressions = [[a[0], b, c] for a, b, c in expressions]


# In[ ]:


# for s in symbols
# hierarchical regular expressions?
def generate(exp=None, level=1, iterations=10, max_levels=10, limit_complexity=True):
    if exp is None:
        exp = ['$']
#     elif isinstance(exp, str):
#         exp = [exp]
#     if level == 1:
#     exp = [e if isinstance(e, list) else [e] for e in exp]
#     print(exp)
    matches = None
    if level > (0.75 * max_levels) and limit_complexity:
#         'E Q'.split()
        exp = ['V' if e in ['E'] else e for e in exp]
    for i in range(iterations):
        for e in expressions:
            e_ = e[0]
#             j, k = e
#             print(e_, exp)
            if e[0] in exp:
                ie = exp.index(e_)
#                 print(len(exp), ie)
                matches = list(filter(lambda a: a[0]==e[0], expressions))
#                 matches = list(filter(lambda a: (a[0] in exp or a[0][0] in exp), expressions))
                if level > (0.75 * max_levels) and limit_complexity:
                    matches = list(filter(lambda z: not z[1] in [['F']], matches))
#                 print(matches, e[0], exp)
                if matches:
#                     [print(m) for m in matches]
#                     print(exp)
                    
#                     sub = random.choice(matches)[1]
                    sub = random.choices(matches, weights=[v[2] for v in matches], k=1)[0][1]
                    sub = [s() if callable(s) else s for s in sub]
                    exp = exp[:ie] + sub + exp[ie+1:]
            #     refactor?
#     print(exp)
                if level <= max_levels and matches:
#                         exp = [eg for eg in generate(exp=e, level=level+1) for e in exp]
                        exp = [generate(exp=e, level=level+1) if isinstance(e, (list, tuple)) else e for e in exp]
#                     exp = [generate(exp=e, level=level+1) for e in exp]
    return exp
# for i in range(5):
#     print(generate())
# In[ ]:


def safe_op(k, l):
    try:
        val = k(*l)
        if val > 10e30:
            val = 10e3
        return val
    except:
        return 0
