import pickle
import datetime
import re
import time
import os
import dateparser
import tarfile

dbpath = os.path.expanduser('~/Desktop/todo.pickle')
todopath = os.path.expanduser('~/Desktop/.todo')


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

    # Convert this item to a string representation of the form used in the todo
    # files (i.e., `content [*] #tag1 #tag2 -t [date] [--]`)
    def toraw(self):
        # don't blame me, blame whoever decided that overloading the
        # multiplication operator was okay
        return self.content + ' ' + ' '.join('#'+t for t in self.tags) +  ' --' * self.done

    # Generate a string summarizing this instance
    def __str__(self):
        inner = [f'"{self.content}"', f'<{self.tags}>']
        inner = "\n\t".join(inner)
        return f'todo {{ {inner} }}'

try:
    with open(dbpath, 'rb') as f:
        data = pickle.load(f)
except FileNotFoundError:
    data = []

# Update the todo list(s) by parsing their members and comparing to the stored
# state (in a similar manner to file tracking, we can infer when entries are
# added, removed, or modified)
def update():
    backuppath = os.path.expanduser(f'~/Desktop/ao/ap/todo-backup/archive-{time.time_ns()}.tar.gz')
    print(f'Backing up todo list and database to {backuppath}')
    with tarfile.open(backuppath, 'w:gz') as tarball:
        for path in [dbpath, todopath]:
            try:
                tarball.add(path)
            except FileNotFoundError as ex:
                print(ex)

    with open(todopath, 'r') as tfile:
        newstate = []
        lines = [l for l in tfile.readlines() if l not in ['', '\n']]
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
            #print(snapshot)
            if snapshot.content == '':
                print(snapshot.toraw())
                print(l)

            newstate.append(snapshot)
    print(f'Reconciling {len(data)} items')
    #pool = filter(lambda x: x.location == todopath, data)
    #breakpoint()
    pool = list(filter(lambda x: x.location == todopath, data))
    # for now we assume no duplicates (up to content and date equivalence)
    for s in newstate:
        matches = list(filter(lambda x: x.content == s.content and x.time == s.time, pool))
        #print(f'{s.toraw()} ... {len(matches)} matches')
        #print(s)
        if matches:
            assert len(matches) == 1, f'Duplicates for: {s}'
            matches[0].snapshots.append(s)
            matches[0].raw = s.raw
        else:
            # why were entries duplicated (in the database) originally?
            data.append(s)

    print(f'Writing output to {todopath}')
    with open(todopath, 'w') as tfile:
        tfile.write(''.join(z.raw for z in sorted(filter(lambda x: x.location == todopath, data), key=lambda y: y.content.casefold())))

    with open(dbpath, 'wb') as f:
        pickle.dump(data, f)

update()
