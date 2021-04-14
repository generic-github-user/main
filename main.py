import json
import time
import random
import datetime
from recurrent.event_parser import RecurringEvent
from dateutil import rrule


class Aliases:
    add = ['a', '.', 'add', 'create', 'make', 'new']
    find = ['f', 'list', 'find', 'show', 'search']
    all = ['e', '*', 'all', 'any', 'everything']
    exit = ['q', 'exit', 'quit', 'leave', 'stop', 'goodbye', 'shutdown', 'end', 'close', 'bye']

class Settings:
    markers = {
        'dates': '<>'
    }
    task_properties = ['name', 'content', 'created', 'modified', 'datestring', 'dateparse', 'dateparams', 'datesummary', 'next']
    task_props_short = ['n', 'c', 'tc', 'tm', 'ds', 'dp', 'dr', 'dv', 'nx']

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

        if self.datestring != None and len(self.datestring) > 0:
            try:
                now = datetime.datetime.now()
                # now = datetime.datetime(2010, 1, 1)
                r = RecurringEvent(now_date=now)
                self.dateparse = r.parse(self.datestring)
                self.dateparams = r.get_params()
                self.datesummary = r.format(self.dateparse)
                if r.is_recurring:
                    rr = rrule.rrulestr(r.get_RFC_rrule())
                    self.next = str(rr.after(now))

                    print(self.dateparse, self.dateparams, self.datesummary, self.next)
            except Exception as e:
                print(e)

    # is name dict reserved?
    def as_dict(self, compressed=True):
        task_dict = {}
        if compressed:
            for i, prop in enumerate(Settings.task_properties):
                short = Settings.task_props_short[i]
                if hasattr(self, prop):
                    # print(prop)
                    task_dict[short] = getattr(self, prop)
        else:
            for i, prop in enumerate(Settings.task_properties):
                short = Settings.task_props_short[i]
                if hasattr(self, prop):
                    task_dict[prop] = getattr(self, prop)
        return task_dict
    def stringify(self, compressed=True):
        return json.dump(self.as_dict(compressed))
    def from_dict(self, data, compressed=True):
        if compressed:
            for i, prop in enumerate(Settings.task_properties):
                short = Settings.task_props_short[i]
                # if hasattr(data, short):
                if short in data:
                    setattr(self, prop, data[short])
        else:
            pass

        return self

def load_data(path='cq_data.json'):
    try:
        with open(path, 'r') as json_file:
            loaded_data = json.loads(json_file.read())
    except:
        loaded_data = []
    return loaded_data

def save_data(data, path='cq_data.json'):
    with open(path, 'w') as save_file:
        json.dump(data, save_file)
    return True

session_data = [Task().from_dict(d) for d in load_data()]



greetings = ['Hey', 'Hello', 'Good morning', 'Buenos dias', 'Welcome back']
farewells = ['Bye', 'Goodbye', 'Until next time']

def run_command(text):
    cmd_parts = text.split(' ')
    first = cmd_parts[0]
    c = cmd_parts
    t = text

    if first in Aliases.add:
        a, b = Settings.markers['dates']
        if a in t:
            date_string = t[t.find(a)+1:t.find(b)]
        else:
            date_string = ''

        new_task = Task(content=c[1], datestring=date_string)
        session_data.append(new_task)
    elif first in Aliases.find:
        if c[1] in Aliases.all:
            for task in session_data:
                print(task.as_dict())
    elif first in Aliases.exit:
        print(random.choice(farewells))
        quit()
    else:
        print("I don't understand")

    save_buffer = []
    for task in session_data:
        save_buffer.append(task.as_dict(compressed=True))
    save_data(data=save_buffer)

print(random.choice(greetings)+'!')
for i in range(20):
    input_text = input()
    run_command(input_text)
