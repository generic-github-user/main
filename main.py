import json

def load_data(self, path='cq_data.json'):
    with open(path, 'r') as json_file:
        loaded_data = json.loads(json_file.read())
    return loaded_data

def save_data(self, data, path='cq_data.json'):
    with open(path, 'w') as save_file:
        json.dump(data, save_file)
    return True
