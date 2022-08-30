#!/usr/bin/env python
# coding: utf-8

# # Project Summary
# 
# This is a small tool to compile a formatted list of information about a user's GitHub repositories. It includes relevant links and can summarize the completion of tasks across many repositories (for example, adding a README or license file).
# 
# ## Usage
# 
# If (a) you want to include branch-level data like specific files included in a repository **and** (b) more than 50 or so repositories are being queried, you will need to add an API key/token since GitHub places fairly restrictive rate limits on API calls; making authenticated calls raises this limit from ~60 to 5000 calls per hour (depending on which service is being requested). To do this, [generate a personal access token](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token) then either input it into the command-line prompt when the script requests it, or create a file named `API_TOKEN.txt` containing the token inside the repo's main directory (the same one as `summarize.ipynb`).

# In[1]:


import requests
import datetime
import time
import json

from IPython.display import display, Markdown, JSON


# In[3]:


with open('./API_TOKEN.txt', 'r') as tokenfile:
    TOKEN = tokenfile.read()

request_headers = {
    'Authorization': 'token '+TOKEN,
    'Accept': 'application/vnd.github.mercy-preview+json'
}

def get_repos():
    # Fetch data from GitHub API via HTTPS request
    response = []
    for p in range(1, 6):
        query = 'https://api.github.com/users/generic-github-user/repos?page='+str(p)
        data = requests.get(query, headers=request_headers).json()
    #     print(data)
        response.extend(data)
    return response

response = get_repos()
print(len(response))
JSON(response[:5])


# In[4]:


repo_trees = {}


# In[8]:


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

def format_info(x, y, z=None, w=None, r=None):
    if callable(y) and r:
        result = y(r)
    else:
        result = plain(str(r[y]).strip())
    
    if z is not None:
        url = r['html_url']
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


# In[9]:


sum(map(bool, ['test']))


# In[10]:


def count_prop(c):
#     return sum([(p in repo and repo[p]) for repo in response])
    return sum(map(bool, [format_info(*c, r=r) for r in response if not r['fork']]))

def generate_table():
    """
    Produce a table summarizing selected attributes of each retrieved repository
    """
    
    response = get_repos()
    divider = ' | '.join(['---']*len(columns))
    dash = '-'*3
#     Build the header from the column titles and alignments
    header = ' | '.join([c[0] for c in columns]) + '\n' + ' | '.join(f':{dash}:' if c[0] in ['README', 'Issues', 'Created'] else dash for c in columns)
    content = header

    # response.sort(reverse=True, key=lambda r: r['open_issues_count'])
#     Convert the timestamp to a human-readable string
    for repo in response:
        repo['milliseconds'] = datetime.datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ').timestamp()
#     Sort repos
    response.sort(reverse=True, key=lambda r: r['milliseconds'])

#     Columns to ignore when calculating totals/counting attributes
    exclude_cols = ['Title', 'Issues', 'Created', 'Size']
    content += '\n' + ' | '.join(
        map(str, [str(round(count_prop(col) / len(response) * 100))+'%' if col[0] not in exclude_cols else ' ' for col in columns])
    )

#     Loop through repositories and generate rows
    for repo in response[:]:
#         Exclude forked repos
        if not repo['fork']:
            content += '\n' + ' | '.join([format_info(*col, r=repo) for col in columns])
    
#     Write output to file
    with open('./output.md', 'w', encoding='UTF-8') as outputfile:
        outputfile.write(content)
#     Cache data requested from GitHub API
    with open(cache_path, 'w') as newcache:
        json.dump(repo_trees, newcache)
        
    return content
    
content = generate_table()
Markdown(content)


# In[ ]:


x = [print(repo['name']) for repo in response]


# In[ ]:




