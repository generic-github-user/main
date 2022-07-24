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

# Represents a task or entry in a todo list, possibly with several sub-tasks
class todo:
    # Initialize a new todo item
    def __init__(self, raw, content=''):
        self.raw = raw
        self.content = content
        self.done = False
        self.donetime = None
        self.snapshots = []
        self.tags = []
        self.source = None
        self.created = time.time()
        self.importance = 0
        self.line = None # This might be used in the future but for now is just somewhat redundant metadata; if we incorporate positional context when analyzing lists we may as well be writing an entire version control system
        self.location = ''
        self.time = None
        self.duration = None
        self.sub = []
        self.parent = None

    # Generate a string summarizing this instance
    def __str__(self):
        inner = [self.content, f'<{self.tags}>']
        inner = "\n\t".join(inner)
        return f'todo {{ {inner} }}'

# Update the todo list(s) by parsing their members and comparing to the stored
# state (in a similar manner to file tracking, we can infer when entries are
# added, removed, or modified)
def update():
    with open(todopath, 'r') as tfile:
        newstate = []
        lines = tfile.readlines()
        for ln, l in enumerate(lines):
            snapshot = todo(l)
            snapshot.importance = l.count('*')
            l = l.replace('*', '')

            if '--' in l:
                snapshot.done = True
                snapshot.donetime = time.time()
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

            newstate.append(snapshot)
    pool = filter(lambda x: x.location == todopath)
    # for now we assume no duplicates (up to content and date equivalence)
    for s in newstate:
        matches = list(filter(lambda x: x.content == s.content and x.time == s.time, pool))
        if matches:
            assert(len(matches) == 1)
            matches[0].snapshots.append(s)
            matches[0].raw = s.raw
        else:
            data.append(s)

    with open(dbpath, 'wb') as f:
        pickle.dump(data, f)

update()
