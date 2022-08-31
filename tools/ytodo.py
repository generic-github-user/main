import yaml
import json
import pathlib
import datetime
import os

path = '~/Desktop/todo.yaml'
path = os.path.expanduser(path)
source = pathlib.Path(path).read_text()
todos = yaml.safe_load(source)

pathlib.Path('./todo-backup').mkdir(exist_ok=True)
timestamp = datetime.datetime.now().strftime('%d-%m-%s_%H-%M-%S')
with open(f'./todo-backup/todo-{timestamp}.yaml', 'w') as bfile:
    bfile.write(source)
