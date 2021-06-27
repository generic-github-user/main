#!/usr/bin/env python
# coding: utf-8

# In[2]:


import ast
import re
import string
import time


# This is a simple Python preprocessor designed to improve concision when using some common operators and functions. It parses the file with a series of regular expressions and replaces abbreviations and various syntactical sugar with their normal Python formats. The tweaks are mostly centered around data access and operations involving higher-order functions.

# In[91]:


sample = """
[52]**3
[6]***4
xy::xy+5
5~[3,3,3]
4:90
1:100:5
dictionary..key
a..b..c
F$G
A$B$C$x
F^6(x)
C ++
"""
# a...c?

# (20??100) ?? (200??1000)
# """
types = {
    'NAT': r'(\d+)',
    'NUM': r'([+-]?\d+\.?\d*)',
    'DIV': r'(\,?[ ]*)',
    'LIST': r'(\[ (?: VAL DIV?){1,}? \])',
    'TUPLE': r'(\((?:NUM(?:,+|\s?)){1,}\))',
    'NAME': r'([a-zA-Z]+)',
    'EXPR': r'(\((?:OP|NAME|VAL)+?\))',
    'OP': r'((?:NAME|VAL)(?:[\+\-\*/] | \?{2})(?:NAME|VAL))',
    'VAL': r'(NAT|NUM)',
    'LETTER': r'([a-zA-Z])',
    'LRANGE': r'(LETTER)[.]{3}(LETTER)',
    'STRING': r'(\"LETTER+?\")',
#     'COM': '(#.*\n)'
}
def iterate(f, g, n):
    h = '{}({})'.format(f, g)
    for i in range(n):
        h = '{}({})'.format(f, h)
    return h

def tile(n, m):
    print(n, m)
    s = f'[{n}]'
    for i in ast.literal_eval(m):
        s = f'[{s} * {i}]'
    return s
