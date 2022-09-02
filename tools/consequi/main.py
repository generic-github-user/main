import json
import time
import random
import datetime
from recurrent.event_parser import RecurringEvent
from dateutil import rrule
import uuid
from pathlib import Path
import zlib
import base64

import termtables as tt

from task import *
from settings import *
from tag import *

def load_data(path='cq_data.json'):
    try:
        with open(path, 'r') as json_file:
            loaded_data = json.loads(json_file.read())
    except:
        loaded_data = {}
    return loaded_data

def save_data(data, path='cq_data.json'):
    with open(path, 'w') as save_file:
        json.dump(data, save_file)
    return True

class session_data:
    ld = load_data()
    tasks = [Task().from_dict(d) for d in ld['tasks']]

    if 'tags' in ld:
        tags = [Tag().from_dict(v) for v in ld['tags']]
    else:
        tags = []

    if 'settings' not in ld:
        settings = {
            'backup_dir': 'cq_backup'
        }
    else:
        settings = ld['settings']

    # are these local?

def jsonify():
    save_buffer = {
        'tasks': [],
        'tags': [],
        'settings': {}
    }
    # Loop through all tasks in memory
    for task in session_data.tasks:
        save_buffer['tasks'].append(task.as_dict(compressed=True))
    for tag in session_data.tags:
        save_buffer['tags'].append(tag.as_dict(compressed=True))
    save_buffer['settings'] = session_data.settings

    return save_buffer

def save_all():
    # moved this out of the loop
    save_data(data=jsonify())

save_all()

greetings = ['Hey', 'Hello', 'Good morning', 'Buenos dias', 'Welcome back']
farewells = ['Bye', 'Goodbye', 'Until next time']

def get_random_task():
    return random.choice(session_data.tasks)

# Abbreviation
def z(x):
    return x.importance['calculated']

def rank():
    # Get two random tasks
    a = get_random_task()
    b = get_random_task()
    if a.id == b.id:
        b = get_random_task()

    print('Which is more important?\n')
    print('1. '+a.content+'\n')
    print('2. '+b.content+'\n')

    a_prev = z(a)
    b_prev = z(b)

    response = input()
    # The formula for computing each task's score change (inverted for the losing item)
    delta = (z(b) - z(a)) / 2. + 20.
    delta = round(delta)
    # First one wins matchup
    if response == '1':
        a.importance['calculated'] += delta
        b.importance['calculated'] -= delta
    # Second one wins
    elif response == '2':
        a.importance['calculated'] -= delta
        b.importance['calculated'] += delta

    def reverse():
        a.importance['calculated'] = a_prev
        b.importance['calculated'] = b_prev
        print('Reversed ranking change')

    save_all()
    return reverse

command_buffer = []

class Session:
    selection = []
    context = []

def store_command(undo_function):
    command_buffer.append(undo_function)
    if len(command_buffer) > Settings.command_buffer_size:
        command_buffer.pop(0)

def add_task(task):
    session_data.tasks.append(task)
    Session.context = [task]
    save_all()

    def reverse():
        session_data.tasks.remove(task)
        print('Reverted add task')

    return reverse

def remove_tasks(task_list):
    for task in task_list:
        session_data.tasks.remove(task)
    print('Removed {} tasks'.format(len(task_list)))
    save_all()

    def reverse():
        for task in task_list:
            session_data.tasks.append(task)
        print('Action undone')

    return reverse

def add_tag(tag):
    session_data.tags.append(tag)
    Session.context = [tag]
    save_all()

    def reverse():
        session_data.tags.remove(tag)
        print('Reverted tag creation')

    return reverse

def undo():
    # command_buffer[-1].reverse()
    command_buffer[-1]()
    command_buffer.pop()
    save_all()

def get_arg(command, labels):
    p = command
    a, b = labels
    if a in p:
        a_ = p.find(a)
        b_ = p.find(b)
        arg_string = p[a_+1:b_]
        p = p[:a_] + p[b_+1:]
    else:
        arg_string = ''

    return p, arg_string

def search(search_func):
    return list(filter(search_func, session_data.tasks))

def not_archived():
    return search(lambda t: not t.archived_())

def print_tasks(tasks):
    task_info = []
    for i, task in enumerate(tasks):
        task_info.append([(i+1), task.name, task.content])

    if len(task_info) > 0:
        table_header = ('#', 'Name', 'Content')
        tt.print(
            task_info,
            header=table_header,
            padding=(0, 1)
        )
    else:
        print('Nothing is selected')

def backup(compress=False, compress_level=6):
    # Dump the current session's data to a string
    backup_data = json.dumps(jsonify()).encode('utf-8')
    original_length = len(backup_data)
    if compress:
        # Compress the text data with zlib and encode in base 64
        backup_data = base64.b64encode(zlib.compress(backup_data, level=compress_level))
        compressed_length = len(backup_data)
        # If compressed, store data in txt file
        extension = 'txt'
    else:
        # Use json file if saving raw data
        extension = 'json'

    # Get backup directory from settings
    bd = session_data.settings['backup_dir']
    # Make the backup directory if it doesn't exist
    Path('./'+bd).mkdir(parents=True, exist_ok=True)
    # timestamp = str(datetime.datetime.now())
    # Current time formatted in a string (that is an acceptable Windows file name)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')
    # Relative file path where backup data will be stored
    backup_path = './{}/{}.{}'.format(bd, timestamp, extension)

    # save_data(backup_data, path=backup_path)

    # Write the data
    with open(backup_path, 'w') as save_file:
        save_file.write(str(backup_data))
    # Print backup info
    print('Backup saved to '+backup_path)
    if compress:
        print('{} characters; compressed to {} characters ({}%)'.format(original_length, compressed_length, round(compressed_length / original_length * 100)))
    else:
        print('{} characters written'.format(original_length))

def run_command(text):
    cmd_parts = text.split()
    first = cmd_parts[0]
    c = cmd_parts
    t = text
    arg_num = len(cmd_parts)

    # Add a new task
    if first in Aliases.add:
        if c[1] in Aliases.task:
            content = ' '.join(c[2:])

            # Handle date tag in task content
            content, date_string = get_arg(command=content, labels=Settings.markers['dates'])
            content, duration_string = get_arg(content, Settings.markers['durations'])

            new_task = Task(content=content, datestring=date_string, durationstring=duration_string)
            store_command(add_task(new_task))
        elif c[1] in Aliases.tag:
            tag_name = ' '.join(c[2:])
            new_tag = Tag(name=tag_name)
            store_command(add_tag(new_tag))
    # Search for certain tasks
    elif first in Aliases.find:
        search_results = []
        if arg_num == 1 or c[1] in Aliases.select:
            sr = Session.selection
            # search_results = not_archived()
            for i, task in enumerate(sr):
                search_results.append(task)
        elif c[1] in Aliases.all:
            for i, task in enumerate(not_archived()):
                search_results.append(task)
            Session.context = search_results

        print_tasks(search_results)
    elif first in Aliases.select:
        if arg_num == 1:
            Session.selection = Session.context
        elif c[1] in Aliases.all:
            for t in session_data.tasks:
                Session.selection.append(t)
        else:
            def sf(task):
                search_term = c[1].lower()
                return (search_term in task.content.lower()) or (search_term in task.name.lower()) and (not task.archived_())
            results = search(sf)
            Session.selection = results
            Session.context = results

        print_tasks(Session.selection)
    elif first in Aliases.deselect:
        print('Deselected {} tasks'.format(len(Session.selection)))
        Session.selection = []
    elif first in Aliases.archive:
        for task in Session.selection:
            task.archived = True
        print('Archived {} tasks'.format(len(Session.selection)))
        save_all()
    elif first in Aliases.backup:
        if arg_num == 1:
            backup()
        elif c[1] == 'true':
            backup(compress=True)
    elif first in Aliases.remove:
        store_command(remove_tasks(Session.selection))
    # Spend some time sorting tasks to rank their importance/other properties
    elif first in Aliases.rank:
        for i in range(int(c[1])):
            store_command(rank())
    elif first in Aliases.undo:
        undo()
    # Close the program
    elif first in Aliases.exit:
        print(random.choice(farewells))
        quit()
    # Unclear command
    else:
        print("I don't understand")

print(random.choice(greetings)+'!')
for i in range(20):
    input_text = input()
    run_command(input_text)
