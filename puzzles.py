#!/usr/bin/env python
# coding: utf-8

# # Programming Puzzles
# 
# This is a list of (hopefully interesting) programming puzzles I created (mainly for my own enrichment) with solutions and brief explanations. I didn't want to place any unnecessary restrictions on how the problems are to be approached, but there will be some occasional suggestions about possible variants you might want to try (e.g., finding an answer with a certain time/space complexity, using a certain data structure, etc). Pull requests with better or more interesting solutions, as well as new problems, are welcome.

# Find the smallest palindromic positive integer greater than 100,000 which contains, in its sequence of digits, the floor of its own square root.

# In[1]:


base = ''
for d in range(4):
    for i in range(10):
        s = str(i)
        num = s+base+s
        root = int(num) ** (1/2)
        if str(root) in str(num):
            print(num)
            break
