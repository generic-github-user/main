import subprocess
import yaml
import json

# Run a shell command and return the output (i.e., stdout); assumes result is
# UTF-8 encoded text
def runcmd(command):
    print(f'Executing command: {command}')
    return subprocess.run(command.split(), stdout=subprocess.PIPE).stdout.decode('UTF-8')

print(f'Loading source files')
with open('README.src.md', 'r') as f: content = f.read()
with open('substitutions.yaml', 'r') as f: subs = yaml.safe_load(f.read())
print(json.dumps(subs, indent=4))

for k, v in subs.items():
    print(f'Replacing template: {k}')
    content = content.replace(f'[[{k}]]', runcmd(v))

print(f'Writing output file')
with open('README.md', 'w+') as f: f.write(content)

print('Done')
