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
# from ...lib.pylist import List
# from main.lib.pylist import List
# from main.lib import pylist
# print(pylist.List)

# TODO: include presence/absence of previously stored snapshot in todo list
# resolution
# TODO: store images/snapshot groups created by a single run of the script

from lib.pylist import List
from .todoitem import todo
from .loadcfg import args, config, db_path, log_path, todo_path, log_level


if args.flush:
    archive_dir = config.base / Path('old')
    archive_dir.mkdir(exist_ok=True)
    config.paths.complete.rename(archive_dir / config.paths.complete)
    config.paths.cancelled.rename(archive_dir / config.paths.cancelled)
    db_path.rename(archive_dir / db_path)
    quit()


def log(content):
    content = '  ' * log_level + str(content)
    if log_level <= config.verbosity:
        print(content)
    with open(log_path, 'a') as logfile:
        logfile.write(f'{datetime.datetime.now()} {content}\n')


if config.stateful:
    try:
        with open(db_path, 'rb') as f:
            data = List(pickle.load(f))
    except FileNotFoundError:
        data = List()
else:
    data = List()


# Opens the todo list file at `path`, parses its entries (one per line), and
# returns a plain list of `todo` objects corresponding to the items in the
# source -- these are the "snapshots" processed by update_list, which attempts
# to infer the temporal relationship between the current and saved states and
# modify the list accordingly
def parse_todos(path):
    global log_level
    try:
        with open(path.expanduser(), 'r') as tfile:
            lines = List(tfile.readlines()).remove('', '\n')
    except FileNotFoundError:
        lines = List()

    new_state = List()
    for ln, line in enumerate(lines):
        log(f'Parsing line: {line}')
        log_level += 1
        snapshot = todo(line, config=config)
        snapshot.location = path

        if config.complete_symbol in line:
            snapshot.done = True
            snapshot.donetime = time.time()
            line = line.replace(config.complete_symbol, '')
            log(f'found completed task: {snapshot}')

        # if 'raw' not in snapshot.tags:
        snapshot.importance = line.count('*')
        line = line.replace('*', '')

        brackets = re.compile('\[([0-9-]+?)\]')
        words = line.split()
        for i, tag in enumerate(words):
            if tag is None:
                continue

            if (M := brackets.match(tag)):
                snapshot.time = datetime.datetime.strptime(M.group(1), config.date_format)\
                                                 .replace(datetime.datetime.now().year)
                words[i] = None
                continue

            if tag.startswith('#'):
                snapshot.tags.append(tag[1:])
                words[i] = None
                continue

            if tag.startswith('-'):
                tag = tag[1:]
                if tag in ['daily', 'cc']:
                    snapshot.flags[tag] = None
                    words[i] = None
                else:
                    snapshot.flags[tag] = words[i+1]
                    words[i:i+2] = [None] * 2

                if tag in ['t', 'time']:
                    snapshot.time = dateparser.parse(words[i+1])
                    words[i:i+2] = [None] * 2

        content = ' '.join(filter(None, words))
        snapshot.content = content
        snapshot.line = ln

        if 'daily' in snapshot.flags:
            snapshot.frequency = 1
            snapshot.flags['f'] = 'd'
        if 'cc' in snapshot.flags:
            snapshot.location = config.paths.cancelled
            # TODO: refactor this to improve separation of concerns

        new_state.append(snapshot)
        log(snapshot)
        log_level -= 1
    return new_state


def merge_state(new_state, path):
    # Compare parsed todo list data with previous state and update
    # accordingly
    log(f'Reconciling {len(data)} items')
    pool = data.filter(lambda x: x.location == path)
    # for now we assume no duplicates (up to content and date equivalence)
    for item in new_state:
        log(item)
        # matches = pool.filter(lambda x: x.content == item.content,
        matches = pool.filter_by('content', item.content)
        # and x.time == item.time, pool
        if matches:
            # if path == config.paths['main']:
            #    assert len(matches) == 1, f'Duplicates for: {item}'
            matches[0].snapshots.append(item)
            matches[0].raw = item.raw
            matches[0].location = item.location
        else:
            data.append(item)
            log(f'found new task: {item}')

    for item in data:
        # if not any(a.content == item.content #and a.time == item.time
        # for a in new_state)\
        if all([new_state.none(lambda a: a.content == item.content),
                item.location == config.paths.main,
                path == config.paths.main]):
            log(f'No matching item in new state: {item.content}')
            item.done = True
            item.donetime = time.time()
            item.location = config.paths.complete


def update_list(todo_list, path):
    global log_level, data

    log(f'Updating todo list {todo_list} ({path})')
    log_level += 1
    log(f'Parsing todo list {todo_list} at {path}')
    new_state = parse_todos(path)

    log('Updating todo item metadata')
    for item in new_state:
        # Some tags and todo item attributes should cause the representation of
        # the task to be moved to a different list
        if 'onhold' in item.tags:
            item.location = config.paths.hold
        if 'ideas' in item.tags:
            item.location = config.paths.ideas
        if item.done:
            item.location = config.paths.complete

    if config.stateful:
        merge_state(new_state, path)
    else:
        data.extend(new_state)

    # Substitute abbreviations listed in config file with their expanded forms
    for item in data:
        for x, y in config.replacements.items():
            if y.lower() not in item.content.lower():
                item.content = item.content.replace(x, y)

    log_level -= 1
    return data


def save_list(path):
    with open(path, 'w') as tfile:
        now = datetime.datetime.now()
        tfile.write(
            data.filter(lambda x: x.location == path)
                .sorted(lambda y: (
                    (datetime.timedelta.max if y.time is None
                        else now-y.time),
                    -y.importance,
                    y.content.casefold()
                ))
                .map(todo.toraw)
                .join('\n'))


def backup_lists():
    global log_level

    backup_dir = config.base / 'todo-backup'
    backup_dir.mkdir(exist_ok=True)
    backup_path = backup_dir / f'archive-{time.time_ns()}.tar.gz'
    log(f'Backing up todo list and database to {backup_path}')
    log_level += 1

    targets = set([todo_path] + list(config.paths.values()))
    if config.backup_db and config.stateful:
        targets.add(db_path)
    with tarfile.open(backup_path, 'w:gz') as tarball:
        for path in targets:
            log(path)
            try:
                tarball.add(path)
            except FileNotFoundError as ex:
                log(ex)
    log_level -= 1


def update_recurring():
    append_buffer = List()
    for item in data.filter_by('location', config.paths.recur)\
                    .filter(lambda x: x.frequency is not None):
        now = datetime.datetime.now()
        if data.none(lambda x: x.content == item.content and
                     x.time is not None and
                     now - x.time <= datetime.timedelta(days=item.frequency)):
            append_buffer.append(item.with_attr('time', datetime.datetime.today())
                                 .with_attr('location', config.paths.main))
    # still not entirely sure why this is necessary...
    data.extend(append_buffer)
    return data


# Update the todo list(s) by parsing their members and comparing to the stored
# state (in a similar manner to file tracking, we can infer when entries are
# added, removed, or modified)
def update():
    global log_level
    start = time.time()
    if not args.dry_run:
        backup_lists()

    for todo_list, path in config.paths.items():
        data = update_list(todo_list, Path(path))
    update_recurring()

    log_level += 1
    for todo_list, path in config.paths.items():
        log(f'Writing output to list {todo_list} at {path}')
        if not args.dry_run:
            save_list(path)

        if config.git_commit and not args.dry_run:
            os.chdir(config.base)
            os.system(f'git add {path}')
    # os.chdir(config.base)
    log('Committing updated todo files to git repository')
    os.system('git commit -m "Update todo list"')
    log_level -= 1

    if config.stateful:
        log(f'Persisting database ({db_path})')
        if not args.dry_run:
            with open(db_path, 'wb') as f:
                pickle.dump(data, f)
            # with open('debug.json', 'w') as f:
                # json.dump(data, f, indent=4)
    if config.debug_dump and not args.dry_run:
        with open('debug.yaml', 'w') as f:
            yaml.dump(data[:50], f)
    end = time.time()
    log(f'Finished in {end - start} seconds')


update()
