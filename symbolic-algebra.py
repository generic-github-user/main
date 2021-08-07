#!/usr/bin/env python
# coding: utf-8

# In[3]:


import string

# In[217]:


class Expression:
#     def __init__(self, terms=None, *extra_terms):
    def __init__(self, *terms):
        if terms is None:
            terms = []
#         terms.extend(extra_terms)
        self.terms = terms
        self.group = True
