#!/usr/bin/env python
# coding: utf-8

# In[3]:


import string


# In[53]:


def dynamic_var(X):
    if X in globals():
        return globals()[X]
    else:
        globals()[X] = Symbol(X)
        return globals()[X]
# globals().__getitem__ = dynamic_var


# In[217]:


class Expression:
#     def __init__(self, terms=None, *extra_terms):
    def __init__(self, *terms):
        if terms is None:
            terms = []
#         terms.extend(extra_terms)
        self.terms = terms
        self.group = True
    def stringify(self, level=0):
        result = ' '.join([(T.stringify(level+1) if isinstance(T, Expression) else str(T)) for T in self.terms])
        if all([self.group, level!=0, self.terms]):
            result = f'({result})'
        return result
    def __str__(self):
#         return ' '.join(map(str, self.terms))
        return self.stringify()
    def __repr__(self):
        return str(self)


# In[218]:


class Operator(Expression):
    def __init__(self, symbol, *inputs, **kwargs):
        super().__init__(*inputs, **kwargs)
        self.symbol = symbol
        self.inputs = self.terms
