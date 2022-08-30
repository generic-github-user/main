import yaml
import json
import pathlib
import sys

content = yaml.safe_load(pathlib.Path(sys.argv[1]).read_text())
encoded = json.dumps(content, indent=4)
print(encoded)
