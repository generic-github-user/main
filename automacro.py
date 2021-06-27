#!/usr/bin/env python
# coding: utf-8

# In[47]:


import itertools

examples = [
    ['United States', 'US'],
    ['Continuous Integration', 'CI'],
    ['artificial intelligence', 'AI'],
    ['Machine learning', 'ML']
]
manipulations = [
    lambda x: x[0],
    lambda x: x[::-1],
    str.lower,
    str.upper,
    str.split,
    lambda x: ''.join(x)
]
