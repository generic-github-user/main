import pickle
import yaml
import json

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
parser.add_argument('--flush', action='store_true')
args = parser.parse_args()
print(args)


class List:
    def __init__(self, items=None):
        if items is None:
            items = []
        self.items = items

    def map(self, f):
        return List(map(f, self.items))

    def filter(self, p):
        return List(list(filter(p, self.items)))

    def filter_by(self, attr, value):
        return self.filter(lambda x: getattr(x, attr) == value)

    def remove(self, *args):
        return self.filter(lambda x: x not in args)

    def get(self, attr):
        return self.map(lambda x: getattr(x, attr))

    def sorted(self, f):
        return List(list(sorted(self.items, key=f)))

    def all(self, p):
        return all(p(i) for i in self.items)

    def any(self, p):
        return any(p(i) for i in self.items)

    def none(self, p):
        return not self.any(p)

    def len(self):
        return len(self.items)

    def append(self, x):
        return self.items.append(x)

    def join(self, s): return s.join(self.items)

    def __iter__(self):
        return self.items.__iter__()

    def __len__(self):
        return self.len()

    def __getitem__(self, i):
        return self.items[i]


todo_path = os.path.expanduser('~/Desktop/.todo')
config = Box(yaml.safe_load(Path('config.yaml').read_text()))
config.base = Path(config.base_path).expanduser()
for k, v in config.paths.items():
    # config[k] = os.path.expanduser(v)
    config.paths[k] = (Path(config.base) / Path(config.paths[k])).expanduser()
db_path = config.base / 'todo.pickle'
config.replacements = {str(k): str(v) for k, v in config.replacements.items()}

if args.flush:
    archive_dir = config.base / Path('old')
    archive_dir.mkdir(exist_ok=True)
    config.paths.complete.rename(archive_dir / config.paths.complete)
    config.paths.cancelled.rename(archive_dir / config.paths.cancelled)
    db_path.rename(archive_dir / db_path)
    quit()


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
        data = List(pickle.load(f))
except FileNotFoundError:
    data = List()


# Opens the todo list file at `path`, parses its entries (one per line), and
# returns a plain list of `todo` objects corresponding to the items in the
# source -- these are the "snapshots" processed by update_list, which attempts
# to infer the temporal relationship between the current and saved states and
# modify the list accordingly
def parse_todos(path):
    try:
        with open(path.expanduser(), 'r') as tfile:
            lines = List(tfile.readlines()).remove('', '\n')
    except FileNotFoundError:
        lines = List()

    new_state = List()
    for ln, line in enumerate(lines):
        print(f'Parsing line: {line}')
        snapshot = todo(line)
        snapshot.location = path

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
                continue

            if tag == '-cc':
                snapshot.location = config.paths.cancelled
                # TODO: refactor this to improve separation of concerns
                words[i] = None
                continue

        if 'raw' not in snapshot.tags:
            snapshot.importance = line.count('*')
            line = line.replace('*', '')

        snapshot.content = ' '.join(filter(None, words))
        snapshot.line = ln

        new_state.append(snapshot)
        print(snapshot)
    return new_state


def update_list(todo_list, path):
    print(f'Updating todo list {todo_list} ({path})')
    print(f'Parsing todo list {todo_list} at {path}')
    new_state = parse_todos(path)

    print('Updating todo item metadata')
    for item in new_state:
        # Some tags and todo item attributes should cause the representation of
        # the task to be moved to a different list
        if 'onhold' in item.tags:
            item.location = config.paths.hold
        if item.done:
            item.location = config.paths.complete

    # Compare parsed todo list data with previous state and update accordingly
    print(f'Reconciling {len(data)} items')
    pool = data.filter(lambda x: x.location == path)
    # for now we assume no duplicates (up to content and date equivalence)
    for item in new_state:
        print(item)
        # matches = pool.filter(lambda x: x.content == item.content,
        matches = pool.filter_by('content', item.content)
        # and x.time == item.time, pool
        if matches:
            # if path == config.paths['main']:
            #    assert len(matches) == 1, f'Duplicates for: {item}'
            # matches[0].snapshots.append(item)
            matches[0].raw = item.raw
            matches[0].location = item.location
        else:
            data.append(item)

    for item in data:
        # if not any(a.content == item.content #and a.time == item.time
        # for a in new_state)\
        if all(new_state.none(lambda a: a.content == item.content),
                item.location == config.paths.main,
                path == config.paths.main):
            print(f'No matching item in new state: {item.content}')
            # breakpoint()
            item.done = True
            item.donetime = time.time()
            item.location = config.paths.complete

    # Substitute abbreviations listed in config file with their expanded forms
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

    for todo_list, path in config.paths.items():
        update_list(todo_list, Path(path))

    for todo_list, path in config.paths.items():
        print(f'Writing output to list {todo_list} at {path}')
        if not args.dry_run:
            with open(path, 'w') as tfile:
                tfile.write(
                    data.filter(lambda x: x.location == path)
                        .sorted(lambda y: (
                            # (0 if 'raw' in y.tags else -y.content.count('*')),
                            -y.importance,
                            (datetime.timedelta.max if y.time is None
                                else datetime.datetime.now()-y.time),
                            y.content.casefold()
                        ))
                        .get('content')
                        .join('\n'))

        if config.git_commit and not args.dry_run:
            print('Committing updated todo files to git repository')
            os.chdir(config.base)
            os.system(f'git add {path}')
            os.system('git commit -m "Update todo list"')

    print(f'Persisting database ({db_path})')
    if not args.dry_run:
        with open(db_path, 'wb') as f:
            pickle.dump(data, f)
        with open('debug.yaml', 'w') as f:
            yaml.dump(data[:5], f)
        # with open('debug.json', 'w') as f:
            # json.dump(data, f, indent=4)


update()
