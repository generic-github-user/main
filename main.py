import json

def load_data(self, path='cq_data.json'):
    with open(dictionary, 'r') as dictionary_file:
        loaded_data = json.loads(dictionary_file.read())
    return loaded_data

def save_data(self, data, path='cq_data.json'):
    with open(path, 'w') as savefile:
        json.dump(data, savefile)
    return True
