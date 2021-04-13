import json
import time

class Task:
    def __init__(self, content, name='', created=None, modified=None):
        current_time = time.time()

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
    # is name dict reserved?
    def as_dict(self, compressed=True):
        if compressed:
            task_dict = {
                'n': self.name,
                'c': self.content,
                'tc': self.created,
                'tm': self.modified
            }
        else:
            task_dict = {
                'name': self.name,
                'content': self.content,
                'created': self.created,
                'modified': self.modified
            }
        return task_dict

def load_data(self, path='cq_data.json'):
    with open(path, 'r') as json_file:
        loaded_data = json.loads(json_file.read())
    return loaded_data

def save_data(self, data, path='cq_data.json'):
    with open(path, 'w') as save_file:
        json.dump(data, save_file)
    return True
