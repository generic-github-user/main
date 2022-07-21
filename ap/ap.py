import os
import sys
import shutil

import pickle
import time
import re
import itertools

import warnings
import textwrap

import psutil
import hashlib

dbpath = '/home/alex/Desktop/ap.pickle'
timelimit = 20

loglevel = 0

from types import ModuleType, FunctionType
from gc import get_referents

# Custom objects know their class.
# Function objects seem to know way too much, including modules.
# Exclude modules as well.
BLACKLIST = type, ModuleType, FunctionType

# https://stackoverflow.com/a/30316760
def getsize(obj):
    """sum size of object & members."""
    if isinstance(obj, BLACKLIST):
        raise TypeError('getsize() does not take argument of type: '+ str(type(obj)))
    seen_ids = set()
    size = 0
    objects = [obj]
    while objects:
        need_referents = []
        for obj in objects:
            if not isinstance(obj, BLACKLIST) and id(obj) not in seen_ids:
                seen_ids.add(id(obj))
                size += sys.getsizeof(obj)
                need_referents.append(obj)
        objects = get_referents(*need_referents)
    return size

# Based on https://stackoverflow.com/a/44873382
def hashfile(path):
    # 256kb
    BUF_SIZE = 2 ** 18

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    with open(path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data: break
            md5.update(data)
            sha1.update(data)
    return (md5.hexdigest(), sha1.hexdigest())

#try:
#    with open(dbpath, 'rb') as f:
#        data = pickle.load(f)
#except Exception as E:
#    print(E)
#    data = {
#        'snapshots': [],
#        'files': []
#    }

if len(sys.argv) > 1 and sys.argv[1] == 'CLEAR':
    data = {
        'snapshots': [],
        'files': []
    }

def save(path=dbpath):
    with open(path, 'wb') as f:
        pickle.dump(data, f)

def log(content, level=0):
    n=60
    lines = [content[i:i+n] for i in range(0, len(content), n)]
    #print('  '*level+content)
    #print(lines[0])
    #print('\n~ '.join(lines))

    p='  ' * level # prefix
    print(p + f'\n{p}~ '.join(textwrap.wrap(content, n)))

# Very minimalist class for representing a file; aggregated from file
# snapshots, which represent a (possibly nonexistent) file at a particular
# point in time
class filenode:

    attrs = {'id': int, 'path': str, 'name': str, 'tags': list, 'size': int,
             'snapshots': list, 'ext': str}
    def __init__(self, **kwargs):
        self.id = 0
        self.path = ''
        self.ext = ''
        self.size = 0
        self.tags = []
        self.snapshots = []
        for k, v in kwargs.items():
            setattr(self, k, v)

    def validate(self):
        for k, v in filenode.attrs.items():
            if hasattr(self, k):
                if not isinstance(getattr(self, k), v):
                    warnings.warn(f'Attribute `{k}` should have type {v}')
            else:
                warnings.warn(f'filenode missing expected attribute: `{k}`')

    def __str__(self):
        return '\n'.join(f'{a}: {getattr(self, a) if hasattr(self, a) else None}' for a in 'path ext tags'.split())

    def print(self):
        print(self)

# Information about a file at a specific point in time (see above), similar to
# those used by Git; this approach enables highly accurate monitoring and
# versioning without having to continuously listen for file system events
class snapshot:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    # Integrate a file snapshot into The File Database
    def process(self):
        log('')
        print(f'Integrating snapshot: {self}')
        #print(len(data['files']))
        current = list(filter(lambda x: x.path == self.path, data['files']))
        if len(current) > 1:
            #raise BaseException('')
            warnings.warn('File database has more than one live file with the\
                          same path; this should not happen')
        #node = current.next()
        #hasn'tattr
        if not hasattr(self, 'ext'):
            _, self.ext = os.path.splitext(self.path)

        if current:
            log(f'Found corresponding node ({self.path})', 1)
            current[0].snapshots.append(self)
            #current[0].ext = self.ext
            current[0].ext = self.ext
            current[0].print()
        else:
            log(f'Adding file node for {self.path} ({len(data["files"])} total)', 1)
            newnode = filenode(
                id=len(data['files']),
                name=self.name, path=self.path, ext=self.ext,
                size=self.data.st_size,
                snapshots=[self],
                tags=[],
                processed=False,
                textproc=False
            )
            data['files'].append(newnode)
            newnode.print()
        self.processed=True
