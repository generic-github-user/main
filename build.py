# This script performs various tasks that apply to this repository at the top
# level and potentially lower levels. Most notably, it builds README.md from
# README.src.md and the metadata stored in projects.yaml and
# substitutions.yaml. It should be periodically executed on the /master branch
# and other long-lived branches to generate updated code statistics.

import subprocess
import yaml
import json
from box import Box
import textwrap

# Run a shell command and return the output (i.e., stdout); assumes result is
# UTF-8 encoded text
def runcmd(command):
    print(f'Executing command: {command}')
    return subprocess.run(command.split(), stdout=subprocess.PIPE).stdout.decode('UTF-8')

print(f'Loading source files')
with open('README.src.md', 'r') as f: content = f.read()
with open('substitutions.yaml', 'r') as f: subs = yaml.safe_load(f.read())
with open('projects.yaml', 'r') as f: projects = Box(yaml.safe_load(f.read()), default_box=True)

with open('branches.yaml', 'r') as f: branches = yaml.safe_load(f.read())
# ref https://stackoverflow.com/a/3495395
B = {}
for b in branches: B |= b
branches = Box(B)

print(json.dumps(subs, indent=4))

# projects.projects.sort()
# branches.sort()

projects.projects = dict(sorted(projects.projects.items(), key=lambda x: x[0].casefold()))
branches = dict(sorted(branches.items(), key=lambda x: x[0].casefold()))

for k, v in subs.items():
    print(f'Replacing template: {k}')
    content = content.replace(f'[[{k}]]', runcmd(v))
content = content.replace('[[projects]]', '\n'.join(
    f'- {k} {"".join(f" `{t}`" for t in v.labels)}' for k, v in projects.projects.items()))
content = content.replace('[[branches]]', '\n'.join(
    f'- `{k}`: {v.strip()}' for k, v in branches.items()))

msg = """This file was automatically generated from README.src.md; you should
edit that file instead. Any changes made to this file will be overwritten the
next time build.py is executed."""
w = 50
content = '\n'.join(f'<!--  {line}{" "*(w-len(line))}  -->' for line in textwrap.wrap(msg, w)) + ('\n' * 5) + content

print(f'Writing output file')
with open('README.md', 'w+') as f: f.write(content)

print('Done')
