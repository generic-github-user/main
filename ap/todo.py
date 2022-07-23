import pickle
import datetime
import re
import time
import os
import dateparser

dbpath = os.path.expanduser('~/Desktop/todo.pickle')
todopath = os.path.expanduser('~/Desktop/.todo')

try:
    with open(dbpath, 'rb') as f:
        data = pickle.load(f)
except FileNotFoundError:
    data = []


class todo:
    def __init__(self, raw, content=''):
        self.raw = raw
        self.content = content
        self.done = False
        self.donetime = None
        self.snapshots = []
        self.tags = []
        self.created = time.time()
        self.importance = 0
        self.line = None
        self.location = ''
        self.sub = []
        self.parent = None

    def __str__(self):
        inner = [self.content, f'<{self.tags}>']
        inner = "\n\t".join(inner)
        return f'todo {{ {inner} }}'

def update():
    with open(todopath, 'r') as tfile:
        lines = tfile.readlines()
        for ln, l in enumerate(lines):
            snapshot = todo(l)
            snapshot.importance = l.count('*')
            l = l.replace('*', '')

            if '--' in l:
                snapshot.done = True
                l = l.replace('--', '')
            w = l.split()
            #for i, tag in (i, tag for i, tag in enumerate(w) if tag.startswith('#')):
            for i, tag in enumerate(w):
                if tag is None: continue

                if tag.startswith('#'):
                    snapshot.tags.append(tag[1:])
                    #del w[i]
                    w[i] = None
                    continue
                if tag.startswith(('-t', '-time')):
                    snapshot.time = dateparser.parse(w[i+1])
                    w[i:i+2] = [None] * 2
            snapshot.content = ' '.join(filter(None, w))
            snapshot.location = todopath
            snapshot.line = ln
            print(snapshot)

    with open(dbpath, 'wb') as f:
        pickle.dump(data, f)

update()
