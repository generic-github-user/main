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

def load_data(self, path='cq_data.json'):
    with open(path, 'r') as json_file:
        loaded_data = json.loads(json_file.read())
    return loaded_data

def save_data(self, data, path='cq_data.json'):
    with open(path, 'w') as save_file:
        json.dump(data, save_file)
    return True
