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
