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

def readme(repo, cache=True):
    title = repo['name']
    if cache and title in repo_trees and 'tree' in repo_trees[title]:
        tree = repo_trees[title]
    else:
        branch = repo['default_branch']
        request_path = '/'.join([repo['url']] + ['git', 'trees', f'{branch}?recursive=1'])
        print(f'Requesting data about repository {title} from {request_path}...')
        tree = requests.get(request_path, headers={'Authorization': 'token '+TOKEN}).json()
        repo_trees[title] = tree
        time.sleep(0.1)
    
    if 'tree' in tree and any(f['path'] == 'README.md' for f in tree['tree']):
        return '✅'
    else:
        return ''
