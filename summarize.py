#!/usr/bin/env python
# coding: utf-8

# In[62]:


import requests
import datetime
import time
import json

from IPython.display import display, Markdown, JSON


# In[159]:


request_headers = {
    'Authorization': 'token '+TOKEN,
    'Accept': 'application/vnd.github.mercy-preview+json'
}

response = []
for p in range(1, 6):
    query = 'https://api.github.com/users/generic-github-user/repos?page='+str(p)
    data = requests.get(query, headers=request_headers).json()
#     print(data)
    response.extend(data)

print(len(response))
JSON(response[:5])


# In[42]:


requests.get('https://api.github.com/repos/generic-github-user/Alexandria/git/trees/master?recursive=1').json()


# In[79]:


repo_trees = {}


# In[158]:


JSON(response[:8])


# In[162]:


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

def truncate(x):
    x = [x_ for x_ in x]
    num = len(x)
    for i in range(len(x)):
        if sum(map(len, x)) < 30:
            break
        else:
            x.pop()
    return x, (num-len(x))
        
def format_topics(r):
    topics, n = truncate(r['topics'])
    return ' '.join(f'`{t}`' for t in topics) + (f'*({n} more)*' if n else '')
    
columns = [
    ('Title', 'name', ''),
    ('Description', 'description'),
    ('Topics', lambda r: format_topics(r)),
    ('Issues', 'open_issues_count', 'issues'),
    ('README', readme),
    ('Size', 'size', None, ' KB')
]
divider = ' | '.join(['---']*len(columns))
header = ' | '.join([c[0] for c in columns]) + '\n' + ' | '.join(['---', '---', ':---:', ':---:', ':---:'])
content = header

def plain(x):
    return x if (x and x not in ['None', 'null']) else ''

def format_info(x, y, z=None, w=None, r=None):
    if callable(y) and r:
        result = y(r)
    else:
        result = plain(str(repo[y]).strip())
    
    if z is not None:
        url = repo['html_url']
        link = url+'/'+z
        result = f'[{result}]({link})'
    if w:
        result += w
        
    return result

cache_path = './github-cache.json'
try:
    with open(cache_path, 'r') as cachefile:
        repo_trees = json.loads(cachefile.read())
except:
    print('No cache found')


# In[98]:


response.sort(reverse=True, key=lambda r: r['open_issues_count'])
for repo in response[:]:
    if not repo['fork']:
        content += '\n' + ' | '.join([format_info(*col, r=repo) for col in columns])

with open(cache_path, 'w') as newcache:
    json.dump(repo_trees, newcache)
Markdown(content)


# In[ ]:




