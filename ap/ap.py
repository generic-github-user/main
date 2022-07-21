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
