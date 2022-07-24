# OS/system utilities and file interaction
import os
import sys
import shutil
from pathlib import Path

# Serialization and other miscellaneous tools
import pickle
import time
import re
import itertools

# Logging
import warnings
import textwrap

# Monitoring
import psutil
import hashlib

# Utilities and internal modules
from utils import getsize, hashfile
from files import filenode, snapshot, catalog
# Configuration data
from config import *

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
