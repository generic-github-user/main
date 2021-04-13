import json
import time
import random

class Task:
    def __init__(self, content='', name='', created=None, modified=None, datestring=None):
        current_time = round(time.time())

        self.name = name
        self.content = content

        if created:
            self.created = created
        else:
            self.created = current_time

        if modified:
            self.modified = modified
        else:
            self.modified = current_time

        self.datestring = datestring
    # is name dict reserved?
    def as_dict(self, compressed=True):
        if compressed:
            task_dict = {
                'n': self.name,
                'c': self.content,
                'tc': self.created,
                'tm': self.modified,
                'ds': self.datestring
            }
        else:
            task_dict = {
                'name': self.name,
                'content': self.content,
                'created': self.created,
                'modified': self.modified
            }
        return task_dict
    def stringify(self, compressed=True):
        return json.dump(self.as_dict(compressed))
    def from_dict(self, data, compressed=True):
        # prop_names = []
        self.name = data['n']
        self.content = data['c']
        self.created = data['tc']
        self.modified = data['tm']
        # self.datestring = data['ds']
        
        return self

def load_data(path='cq_data.json'):
    try:
        with open(path, 'w') as json_file:
            loaded_data = json.loads(json_file.read())
    except:
        loaded_data = []
    return loaded_data

def save_data(data, path='cq_data.json'):
    with open(path, 'w') as save_file:
        json.dump(data, save_file)
    return True

session_data = [Task().from_dict(d) for d in load_data()]

class Aliases:
    add = ['add', 'create', 'make', 'new']

class Settings:
    markers = {
        'dates': '<>'
    }

greetings = ['Hello', 'Good morning', 'Buenos dias', 'Welcome back']

def run_command(text):
    cmd_parts = text.split(' ')
    first = cmd_parts[0]
    c = cmd_parts
    t = text

    if first in Aliases.add:
        a, b = Settings.markers['dates']
        date_string = t[t.find(a)+1:t.find(b)]

        new_task = Task(content=c[1], datestring=date_string)
        session_data.append(new_task)

    save_buffer = []
    for task in session_data:
        save_buffer.append(task.as_dict(compressed=True))
    save_data(data=save_buffer)

print(random.choice(greetings)+'!')
for i in range(20):
    input_text = input()
    run_command(input_text)
