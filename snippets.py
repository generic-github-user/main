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
