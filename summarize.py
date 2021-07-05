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

# Fetch data from GitHub API via HTTPS request
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


# In[183]:


with open('./API_TOKEN.txt', 'r') as tokenfile:
    TOKEN = tokenfile.read()

def find_file(repo, filename, cache=True):
    title = repo['name']
    if cache and title in repo_trees and 'tree' in repo_trees[title]:
        tree = repo_trees[title]
    else:
#         Request the file tree of the repository's default branch (as of the latest commit)
        branch = repo['default_branch']
        request_path = '/'.join([repo['url']] + ['git', 'trees', f'{branch}?recursive=1'])
        print(f'Requesting data about repository {title} from {request_path}...')
        tree = requests.get(request_path, headers={'Authorization': 'token '+TOKEN}).json()
        repo_trees[title] = tree
#         Rate limit requests to avoid exceeding quota
        time.sleep(0.1)
    
#     Check if tree exists and a README file exists
    if 'tree' in tree and any(filename in f['path'] for f in tree['tree']):
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

# Convert NoneType and None/null string values to empty strings
def plain(x):
    return x if (x and x not in ['None', 'null']) else ''

# Convert a list of topic strings to a formatted list
def format_topics(r):
    topics, n = truncate(r['topics'])
    return ' '.join(f'`{t}`' for t in topics) + (f'*({n} more)*' if n else '')

# Shorten the repository description if it exceeds a set length
def format_description(r):
    desc = plain(r['description'])
    if len(desc) > 50:
        desc = desc[:50] + ('.'*3)
    return desc
    
columns = [
    ('Title', 'name', ''),
    ('Description', format_description),
    ('Topics', lambda r: format_topics(r)),
#     ('Issues', 'open_issues_count', 'issues'),
    ('Issues', lambda r: f'**[{r["open_issues_count"]}]({r["html_url"]+"/issues"})** [+]({r["html_url"]+"/issues/new"})'),
    ('README', lambda r: find_file(r, 'README.md')),
    ('License', lambda r: find_file(r, 'LICENSE')),
    ('Created', lambda r: datetime.datetime.strptime(r['created_at'], '%Y-%m-%dT%H:%M:%SZ').strftime('%b %Y')),
    ('Size', 'size', None, ' KB')
]
divider = ' | '.join(['---']*len(columns))
dash = '-'*3
header = ' | '.join([c[0] for c in columns]) + '\n' + ' | '.join(f':{dash}:' if c[0] in ['README', 'Issues', 'Created'] else dash for c in columns)
content = header



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


# In[184]:


# response.sort(reverse=True, key=lambda r: r['open_issues_count'])
for repo in response:
    repo['milliseconds'] = datetime.datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ').timestamp()
response.sort(reverse=True, key=lambda r: r['milliseconds'])
    
for repo in response[:]:
    if not repo['fork']:
        content += '\n' + ' | '.join([format_info(*col, r=repo) for col in columns])
with open('./output.md', 'w', encoding='UTF-8') as outputfile:
    outputfile.write(content)
        
with open(cache_path, 'w') as newcache:
    json.dump(repo_trees, newcache)
Markdown(content)


# In[182]:


x = [print(repo['name']) for repo in response]


# In[ ]:




