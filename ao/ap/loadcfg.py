import os
import yaml
import argparse
from pathlib import Path
from box import Box

parser = argparse.ArgumentParser()
parser.add_argument('--dry-run', action='store_true',
                    help='Executes a "dry run"; will simulate updating \
                    the todo list but won\'t actually modify any files')
parser.add_argument('--flush', action='store_true')
parser.add_argument('--config', type=str)
args = parser.parse_args()
print(args)

todo_path = os.path.expanduser('~/Desktop/.todo')
config = Box(yaml.safe_load(Path(args.config).read_text()))
config.base = Path(config.base_path).expanduser()
for k, v in config.paths.items():
    # config[k] = os.path.expanduser(v)
    config.paths[k] = (Path(config.base) / Path(config.paths[k])).expanduser()
db_path = config.base / 'todo.pickle'
log_path = config.base / config.log
log_level = 0
config.replacements = {str(k): str(v) for k, v in config.replacements.items()}
