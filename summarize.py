#!/usr/bin/env python
# coding: utf-8

# In[62]:


import requests
import datetime
import time
import json

from IPython.display import display, Markdown, JSON


# In[61]:


response = []
for p in range(1, 6):
    query = 'https://api.github.com/users/generic-github-user/repos?page='+str(p)
    data = requests.get(query).json()
#     print(data)
    response.extend(data)

print(len(response))
JSON(response[:5])


# In[42]:


requests.get('https://api.github.com/repos/generic-github-user/Alexandria/git/trees/master?recursive=1').json()


# In[79]:


repo_trees = {}


# In[95]:


with open('./API_TOKEN.txt', 'r') as tokenfile:
    TOKEN = tokenfile.read()
