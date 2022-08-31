#!/usr/bin/env python
# coding: utf-8

# # Alexandria

# In[253]:


from urllib.parse import urlparse, parse_qs
import randomcolor
import datetime
import matplotlib.pyplot as plt
import operator as ops
import requests
import time
import json
import zlib
import base64
import itertools
import random
from termcolor import colored
import networkx as nx
import numpy as np
import pprint
import webbrowser
from pyvis.network import Network
import uuid
import spacy
from spacy import displacy

rcolor = randomcolor.RandomColor()

def L(x, y):
    return lambda x: y


# ## Page

# In[237]:


class Page:
    def __init__(self, info, collection=None, unpack=False, lead='', extract_keywords=True, graph=None, **kwargs):
        if ' ' in info:
            parts = info.split(' | ')
        else:
            parts = info, ''
        self.url, self.title = parts[0], ''.join(parts[1:])
        self.parse = urlparse(self.url)
        self.params = parse_qs(self.parse.query)
        self.tags = []
        self.len = len(self.url)
        self.archives = []
        self.id = uuid.uuid4().hex
        self.collection = collection
        
        if unpack:
#             if 'url' in self.params and self.params['url'][0].startswith(lead):
            if self.url.startswith(lead):
                nested = Page(self.params['url'][0], collection=self.collection, graph=graph, **kwargs)
                self.url = nested.url
                self.parse = nested.parse
                self.params |= nested.params
        
        self.keywords = None
#         if extract_keywords:
#             self.get_keywords()
            
    def get_keywords(self):
        exclude = {'on', 'by', 'who', 'dont', 'was', 'without', 'when', 'http', 'https', 'www', 'com', 'an', 'in', 'the', 'with', 'and', 'org', 'a', 'as', 'en', 'of', 'to', 'at', 'all', 'for', 'we', 'how', 'it', 'do', 'why', 'be', 'have'}
        terms = list(itertools.chain.from_iterable(self.replace(attr.lower(), ' ').split() for attr in [self.parse.path[1:], self.title]))
#              and '&' not in t
        keywords = {t for t in terms if 3 < len(t) < 50 and not t.isnumeric() and not sum(c.isdigit() for c in t) > 5 and not t.isspace()} - exclude
        return keywords

    def add_keywords(self, keywords, graph=None):
        self.keywords = keywords
        for k in self.keywords:
            if k:
                self.tag(k[0]+' [{}]'.format(k[1]), g=graph, color='orange')
        return self
    
    def clear_tags(self):
        self.tags = []
        return self
    
#     either pass tag objects back up through the call stack or pass collection to constructor
    def tag(self, tags, g=None, **kwargs):
        if type(tags) is str:
            tags = Tag(tags, **kwargs)
        if type(tags) is Tag:
            tags = [tags]
        
#         self.tags.extend(tags)
        for tag in tags:
#             breakpoint()
            self.tags.append(tag.id)
            if self.collection:
                self.collection.tags[tag.id] = tag
            
            if tag.name and self.title:
                g.add_node(tag.name, color=tag.color)
                g.add_edge(self.title, tag.name, weight=1)
        
        return self
    
    def contains(self, term):
        return any(term in a for a in [self.url, self.title])
    
    def replace(self, s, n):
        punctuation = '.,/_-:?()[]'
        for p in punctuation:
            s = s.replace(p, n)
        return s
    
    def print(self):
        print(str(self))
        
    def as_dict(self):
        data = vars(self)
#         TODO
        if 'collection' in data:
            data.pop('collection')
        return data
        
    def __str__(self):
#         '; '.join(self.keywords)
        tag_info = [self.collection.tags[t] for t in self.tags]
        return ' | '.join([self.title, '; '.join(map(str, tag_info)), self.url[:100]])


# ## Tag

# In[89]:


class Tag:
    def __init__(self, name='', color=''):
        self.name = name
#         self.color = rcolor.generate()
        colors = [
            'grey',
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            'white'
        ]
        if not color or color not in colors:
            color = random.choice(colors)
        self.color = color
        self.created = str(datetime.datetime.now())
        self.id = uuid.uuid4().hex
        
    def as_dict(self):
        return vars(self)
        
    def __str__(self):
        return colored(self.name, self.color)
        


# ## Collection

# In[238]:


class Collection:
    def __init__(self, urls=None, source='', encoding='utf8'):
        self.urls = []
        self.graph = nx.Graph()
        self.id = uuid.uuid4().hex
        
        if source:
            with open(source, 'r', encoding=encoding) as file:
                text = file.read()
                text = text.encode(encoding)
                text = base64.b64decode(text)
                text = zlib.decompress(text)
                text = text.decode(encoding)
#             print(text[:500])

        self.tags = {}
        self.keywords = {}
        self.common_keywords = []
        
        if urls:
            self.add(urls)
    
    def load(self, path, limit=50, **kwargs):
        data = []
        with open(path, 'r', encoding='utf8') as file:
            l = 0
            for line in file:
                data.append(line)
                if l > limit:
                    break
                l += 1
        self.add(data, **kwargs)
    
    def add(self, urls, keywords=5, hide_labels=False, **kwargs):
        if type(urls) is str:
            urls = [urls]
        if type(urls) is list:
            for url in urls:
                if type(url) is str:
                    new = Page(url, collection=self, graph=self.graph, **kwargs)
                elif type(url) is Page:
                    new = url
                self.urls.append(new)
                label = ' ' if hide_labels else new.title
                self.graph.add_node(new.title, color='green', label=label, data='Page')
#                 print(new.url)
                for k in new.get_keywords():
                    if k in self.keywords:
                        self.keywords[k][0] += 1
                        self.keywords[k][1].append(new)
                    else:
                        self.keywords[k] = [1, [new]]
                        
        self.common_keywords = sorted(self.keywords.items(), key=lambda x: x[1][0], reverse=True)[:keywords]
        for word in self.common_keywords:
            for page in word[1][1]:
                page.add_keywords([[word[0], word[1][0]]], graph=self.graph)
                
    
    def find(self, attr, value=None):
        if not callable(attr):
            attr = lambda x: getattr(x, attr) == value
        return Collection(list(filter(attr, [p.clear_tags() for p in self.urls])))
    
    def tag(self, tags):
        if type(tags) is str:
            tags = Tag(tags)
        if type(tags) is Tag:
            tags = [tags]
        
        for u in self.urls:
            u.tags.extend(tags)
            for tag in tags:
#                 print(tag.name, u.title)
                self.graph.add_edge(u.title, tag.name, weight=1)
        
        return self
    
    def tag_if_in(self, tags):
        if type(tags) is str:
            tags = [tags]
        result = self
#         tags_ = [Tag(t) for t in tags]
        tags_ = []
        for t in tags:
            t_ = Tag(t)
            tags_.append(t_)
            self.graph.add_node(t_.name, color=t_.color, data='Tag')
        
        for t in tags_:
#             print(t.name)
#             result.find(lambda x: any(t.name.lower().replace(' ', '') in q for q in [x.title, x.url])).tag(t)
            for u in result.urls:
                if any(t.name.lower().replace(' ', '') in q for q in [u.title, u.url]):
                    u.tag(t, self.graph)
        
        return result
    
    def visualize(self, property='len'):
        summary = [getattr(u, property) for u in self.urls]
        plt.hist(summary, bins=100)
        return self
        
    def network(self, physics=False, display=0.5):
        self.vis = Network(width=800, height=800, notebook=True)
#         print(self.graph.nodes)
        vis_graph = self.graph.copy()
        nodes = [n for n, m in vis_graph.nodes.data('data') if m == 'Page']
        nodes = nodes[:round(len(nodes) * (1 - display))]
        vis_graph.remove_nodes_from(nodes)
        self.vis.from_nx(vis_graph)
#         self.vis.enable_physics(physics)
        self.vis.toggle_physics(physics)
        self.vis.repulsion(spring_length=400, spring_strength=0.01)
#         g.barnes_hut()
        output = self.vis.show('./library-network.html')
#         return net
        return output
        
        
    def download(self, limit=1, rate=1):
        for u in self.urls[:limit]:
            print('Archiving '+u.url)
            text = requests.get(u.url).text
            now = time.time()
            u.archives.append([now, text])
            time.sleep(1/rate)
        return self
            
    def save(self, path='./alexandria-library.txt', encoding='utf-8', compress=-1, base64_encode=True):
        if type(compress) is bool:
            compress = int(compress)
        
        attrs = ['urls', 'id', 'tags']
        data = {}
        for a in attrs:
            value = getattr(self, a)
            if type(value) is list:
#                 value = [v.as_dict() for v in value]
                value_ = []
                for v in value:
                    if type(v) in [Page, Tag]:
                        value_.append(v.as_dict())
                value = value_
            elif type(value) is dict:
                value = {k: v.as_dict() for k, v in value.items()}
            data[a] = value
#         text = json.dumps(self, default=vars)
        text = json.dumps(data)
        text = zlib.compress(text.encode(encoding), level=compress)
        if base64_encode:
            text = base64.b64encode(text).decode(encoding)
        else:
            text = str(text)
#             text = text.decode(encoding)
        with open(path, 'w') as f:
#             f.write(text.decode(encoding, 'ignore'))
            f.write(text)
#             f.write(text)
        return text
    
    def statistics(self):
        colors = [
            'red',
            'yellow',
            'green',
            'blue',
            'magenta',
            'cyan',
            'grey',
            'white'
        ]
        info = [
            ('Number of pages', len(self.urls)),
            ('Number of tags', len(self.common_keywords)),
            ('Average title length', round(np.mean([len(u.title) for u in self.urls]), 1)),
            ('Average URL length', round(np.mean([len(u.url) for u in self.urls]), 1)),
            ('Average number of tags', round(np.mean([len(u.tags) for u in self.urls]), 1))
        ]
        for i, s in enumerate(info):
            label, num = s
            print('{}: {}'.format(colored(label, colors[i]), num))
            
    def random(self):
        url = random.choice(self.urls).url
        webbrowser.open(url)
        return url
    
    def print(self, limit=100):
        print(colored('Collection '+self.id, 'blue'))
        for u in self.urls[:limit]:
            print(u)
    
    def __getitem__(self, i):
        return self.urls[i]


# In[6]:


class Rule:
    def __init__(self, z, op, value, action):
        if callable(z):
            self.when = z
        else:
            self.when = lambda x: op(getattr(x, z), value)


# ## Testing

# In[256]:


# c = Collection(source='./alexandria-library.txt')
c = Collection()
c.load(
    path='./may-28.txt',
    limit=10,
    keywords=5,
    hide_labels=True,
    unpack=True,
    lead='chrome-extension://fiabciakcmgepblmdkmemdbbkilneeeh/park.html'
)

# print(c.urls[100].parse)
# c.find(lambda x: len(x.url)>1000)[5]
# w = c.find(lambda x: 'Wikipedia' in x.title).tag('Wikipedia')
# w[0]
# t.created
# c.tag(t)[0].tags[0].name
# c[100].params
# c.find(lambda x: x.len < 600).visualize()

# c.tag_if_in(['Wikipedia', 'Google', 'Colab', 'Stack Overflow', 'GitHub', 'Twitter', 'YouTube', 'Stack Exchange', 'Physics', 'The New York Times', 'NumPy'])

# w.tag('Page')
# [([t.name for t in g.tags], g.url[-5:]) for g in w[:50]]

# r = Rule('url', ops.eq, 'wikipedia.org', None)
# c.download(limit=3)
# c.print()
# c.save(compress=9, base64_encode=True)
# w.graph.edges

# c.network(physics=True, display=0.2)
# c.statistics()
# c.keywords.items()
# c.random()

# TODO: central tag creation buffer?


# In[254]:


np.mean([len(x.title) for x in c.urls])


# In[545]:


net = Network(width=800, height=800, notebook=True)
net.from_nx(w.graph)
# net.show("./library-network.html")


# In[639]:


p = pprint.PrettyPrinter()
# p.pprint(list(c.graph.nodes))


# In[112]:


output = requests.get('https://stackoverflow.com/questions/2018026/what-are-the-differences-between-the-urllib-urllib2-urllib3-and-requests-modul')
output.text[:10]
int(True)


# In[252]:


query = 'Get all bookmarks containing python'
spacy.prefer_gpu()
nlp = spacy.load('en_core_web_sm')
doc = nlp(query)
action = None
parameters = []
aliases = {
    'find': ['get', 'list', 'find'],
    'with': ['with', 'containing', 'including']
}
def find_alias(term):
    a = [k for k,v in aliases.items() if term.lower() in v]
    if a:
        return a[0]
    
for token in doc:
    print(token.text, token.head, token.head.text, token.dep_, token.pos_)
    if token.dep_ == 'ROOT' and token.pos_ == 'VERB':
        action = find_alias(token.text)
    if token.dep_ == 'dobj' and token.head.dep_ == 'acl' and token.head.text in aliases['with']:
        parameters.append([find_alias(token.head.text), token.text])
print('\n')
for nc in doc.noun_chunks:
    print(nc.text, nc.root.text, nc.root.dep_, nc.root.head.text)

spacy.explain('acl')
displacy.render(doc, style='dep')
print(action, parameters)
c.find(lambda x: x.contains(parameters[0][1])).print()

