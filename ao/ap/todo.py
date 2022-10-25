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
from ...lib.pylist import List

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--dry-run', action='store_true',
                    help='Executes a "dry run"; will simulate updating \
                    the todo list but won\'t actually modify any files')
parser.add_argument('--flush', action='store_true')
args = parser.parse_args()
print(args)




todo_path = os.path.expanduser('~/Desktop/.todo')
config = Box(yaml.safe_load(Path('config.yaml').read_text()))
config.base = Path(config.base_path).expanduser()
for k, v in config.paths.items():
    # config[k] = os.path.expanduser(v)
    config.paths[k] = (Path(config.base) / Path(config.paths[k])).expanduser()
db_path = config.base / 'todo.pickle'
log_path = config.base / config.log
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
        # The original text from which this todo item was parsed
        self.raw = raw
        # The "text" or content of the todo item (excludes tags and other
        # metadata/markup)
        self.content = content
        # A boolean flag indicating whether the corresponding task is complete
        self.done = False
        # A timestamp indicating when this item was marked as complete
        # (actually reflects the first occasion on which the script was rerun
        # after the file was modified)
        self.donetime = None
        # A (chronologically ordered) set of "snapshots" reflecting every
        # processed todo item that was considered a match to the "canonical"
        # version of the task in the database (currently unused for efficiency
        # reasons)
        self.snapshots = []
        # Tags used to mark various properties about the task (item) -- these
        # are sometimes further processed into special attributes like
        # todo.done and todo.duration
        self.tags = []
        # unused
        self.source = None
        # The time at which the todo instance representing this item was first
        # created
        self.created = time.time()
        self.importance = 0
        # This might be used in the future but for now is just somewhat
        # redundant metadata; if we incorporate positional context when
        # analyzing lists we may as well be writing an entire version control
        # system
        self.line = None
        # The file (specific todo list) in which the item currently resides;
        # this is often modified during processing so that when the lists are
        # rewritten the item is moved to a new file
        self.location = ''
        self.time = None
        self.duration = None
        # Nested tasks/children of this item; currently unused due to parsing
        # limitations (the eventual goal is to integrate the zeal markup
        # parser, though the block indentation parser might be factored out
        # into a separate module)
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
        inner = [f'"{self.raw}"', f'<{self.tags}>']
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
            with open(log_path, 'a') as logfile:
                logfile.write(f'{datetime.datetime.now()} found completed task: {snapshot}\n')
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
        if 'ideas' in item.tags:
            item.location = config.paths.ideas
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
            with open(log_path, 'a') as logfile:
                logfile.write(f'{datetime.datetime.now()} found new task: {item}\n')

    for item in data:
        # if not any(a.content == item.content #and a.time == item.time
        # for a in new_state)\
        if all([new_state.none(lambda a: a.content == item.content),
                item.location == config.paths.main,
                path == config.paths.main]):
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


def save_list(path):
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


def backup_lists():
    backup_dir = config.base / 'todo-backup'
    backup_dir.mkdir(exist_ok=True)
    backup_path = backup_dir / f'archive-{time.time_ns()}.tar.gz'
    print(f'Backing up todo list and database to {backup_path}')

    with tarfile.open(backup_path, 'w:gz') as tarball:
        for path in set([db_path, todo_path] + list(config.paths.values())):
            print(path)
            try:
                tarball.add(path)
            except FileNotFoundError as ex:
                print(ex)


# Update the todo list(s) by parsing their members and comparing to the stored
# state (in a similar manner to file tracking, we can infer when entries are
# added, removed, or modified)
def update():
    if not args.dry_run:
        backup_lists()

    for todo_list, path in config.paths.items():
        update_list(todo_list, Path(path))

    for todo_list, path in config.paths.items():
        print(f'Writing output to list {todo_list} at {path}')
        if not args.dry_run:
            save_list(path)

        if config.git_commit and not args.dry_run:
            print('Committing updated todo files to git repository')
            os.chdir(config.base)
            os.system(f'git add {path}')
    # os.chdir(config.base)
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
