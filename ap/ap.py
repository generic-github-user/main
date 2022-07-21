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

from utils import getsize, hashfile
from files import filenode, snapshot, catalog

dbpath = '/home/alex/Desktop/ap.pickle'
timelimit = 20

loglevel = 0

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

