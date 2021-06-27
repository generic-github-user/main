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
