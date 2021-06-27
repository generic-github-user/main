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
    [lambda x: x[0], 'First char'],
    [lambda x: x[::-1], 'Reverse'],
    [str.lower, 'Lowercase'],
    [str.upper, 'Capitalize'],
    [str.split, 'Split'],
    [lambda x: ''.join(x), 'Join'],
]
