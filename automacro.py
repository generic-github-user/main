#!/usr/bin/env python
# coding: utf-8

# In[38]:


import itertools
manipulations = [
    lambda x: x[0],
    lambda x: x[::-1],
    str.lower,
    str.upper,
    str.split,
    lambda x: ''.join(x)
]
