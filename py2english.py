#!/usr/bin/env python
# coding: utf-8

# # py2english

# This program parses a Python program into an abstract syntax tree, then generates a natural language description of what it does and how it does it. This is just an experiment, but if it works well as a proof-of-concept the system could be refined and aid in understanding and analyzing large codebases.

# In[1]:


import ast


# In[2]:


sample_code = """
for i in range(2, 50):
    for j in range(2, round(i**(1/2))):
        if i % j == 0:
            break
    else:
        print(i)
"""
