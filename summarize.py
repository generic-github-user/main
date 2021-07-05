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
