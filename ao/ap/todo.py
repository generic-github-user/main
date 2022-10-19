import pickle
import yaml

import datetime
import re
import time
import os
from pathlib import Path
import dateparser
import tarfile
from box import Box

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--dry-run', action='store_true',
                    help='Executes a "dry run"; will simulate updating \
                    the todo list but won\'t actually modify any files')
args = parser.parse_args()
print(args)

todo_path = os.path.expanduser('~/Desktop/.todo')
config = Box(yaml.safe_load(Path('config.yaml').read_text()))
config.base = Path(config.base_path).expanduser()
for k, v in config.paths.items():
    # config[k] = os.path.expanduser(v)
    config.paths[k] = (Path(config.base) / Path(config.paths[k])).expanduser()
db_path = config.base / 'todo.pickle'
config.replacements = {str(k): str(v) for k, v in config.replacements.items()}


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
        # This might be used in the future but for now is just somewhat
        # redundant metadata; if we incorporate positional context when
        # analyzing lists we may as well be writing an entire version control
        # system
        self.line = None
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
        return self.content + ' ' + ' '.join('#'+t for t in self.tags)\
            + f' {config.complete_symbol}' * self.done

    # Generate a string summarizing this instance
    def __str__(self):
        inner = [f'"{self.content}"', f'<{self.tags}>']
        # inner = "\n\t".join(inner)
        inner = ' '.join(inner)
        return f'todo {{ {inner} }}'


try:
    with open(db_path, 'rb') as f:
        data = pickle.load(f)
except FileNotFoundError:
    data = []


def parse_todos(path):
    try:
        with open(path.expanduser(), 'r') as tfile:
            lines = [line for line in tfile.readlines()
                     if line not in ['', '\n']]
    except FileNotFoundError:
        lines = []

    newstate = []
    for ln, line in enumerate(lines):
        snapshot = todo(line)

        if config.complete_symbol in line:
            snapshot.done = True
            snapshot.donetime = time.time()
            line = line.replace(config.complete_symbol, '')
        words = line.split()
        for i, tag in enumerate(words):
            if tag is None:
                continue

            if tag.startswith('#'):
                snapshot.tags.append(tag[1:])
                words[i] = None
                continue

            if tag.startswith(('-t', '-time')):
                snapshot.time = dateparser.parse(words[i+1])
                words[i:i+2] = [None] * 2

        if 'raw' not in snapshot.tags:
            snapshot.importance = line.count('*')
            line = line.replace('*', '')

        snapshot.content = ' '.join(filter(None, words))
        snapshot.location = path
        snapshot.line = ln

        newstate.append(snapshot)
        print(snapshot)
    return newstate


def update_list(tlist, path):
    print(f'Parsing todo list {tlist} at {path}')
    newstate = parse_todos(path)

    print('Updating todo item metadata')
    for s in newstate:
        if 'onhold' in s.tags:
            s.location = config.paths.hold
        if s.done:
            s.location = config.paths.complete

    print(f'Reconciling {len(data)} items')
    pool = list(filter(lambda x: x.location == path, data))
    # for now we assume no duplicates (up to content and date equivalence)
    for s in newstate:
        print(s)
        matches = list(filter(lambda x: x.content == s.content
                              and x.time == s.time, pool))
        if matches:
            # if path == config.paths['main']:
                # assert len(matches) == 1, f'Duplicates for: {s}'
            matches[0].snapshots.append(s)
            matches[0].raw = s.raw
            matches[0].location = s.location
        else:
            data.append(s)

    for item in data:
        if not any(a.content == item.content #and a.time == item.time
                   for a in newstate):
            print(item.content)
            item.done = True
            item.donetime = time.time()
            # item.location = config.paths.complete

    for item in data:
        for x, y in config.replacements.items():
            if y.lower() not in item.content.lower():
                item.content = item.content.replace(x, y)



# Update the todo list(s) by parsing their members and comparing to the stored
# state (in a similar manner to file tracking, we can infer when entries are
# added, removed, or modified)
def update():
    backup_dir = config.base / 'todo-backup'
    backup_dir.mkdir(exist_ok=True)
    backup_path = backup_dir / f'archive-{time.time_ns()}.tar.gz'
    print(f'Backing up todo list and database to {backup_path}')
    if not args.dry_run:
        with tarfile.open(backup_path, 'w:gz') as tarball:
            for path in set([db_path, todo_path] + list(config.paths.values())):
                print(path)
                try:
                    tarball.add(path)
                except FileNotFoundError as ex:
                    print(ex)

    for tlist, path in config.paths.items():
        update_list(tlist, Path(path))

    for tlist, path in config.paths.items():
        print(f'Writing output to list {tlist} at {path}')
        if not args.dry_run:
            with open(path, 'w') as tfile:
                tfile.write('\n'.join(z.content for z in sorted(
                    filter(lambda x: x.location == path, data),
                    key=lambda y: (
                        # (0 if 'raw' in y.tags else -y.content.count('*')),
                        -y.importance,
                        (datetime.timedelta.max if y.time is None
                            else datetime.datetime.now()-y.time),
                        y.content.casefold()
                    ))))

        if config.git_commit and not args.dry_run:
            print('Committing updated todo files to git repository')
            os.chdir(config.base)
            os.system(f'git add {path}')
            os.system('git commit -m "Update todo list"')

    if not args.dry_run:
        with open(db_path, 'wb') as f:
            pickle.dump(data, f)


update()
