#!/usr/bin/env python
# coding: utf-8

# ### Prime Number Generator
# 
# Prints out a list of prime numbers in the specified range.

# In[2]:


for i in range(2, 50):
    for j in range(2, round(i**(1/2))):
        if i % j == 0:
            break
    else:
        print(i)


# ### Flatten Nested List
# 
# Convert an irregular ordered list of lists and/or values to a shallow sequence of values.
# 
# Source: https://stackoverflow.com/a/14491059/10940584

# In[3]:


def flatten(L):
    for item in L:
        try:
            yield from flatten(item)
        except TypeError:
            yield item

list(flatten([[[1, 2, 3], [4, 5]], 6]))
