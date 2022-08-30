import subprocess

# Run a shell command and return the output (i.e., stdout); assumes result is
# UTF-8 encoded text
def runcmd(command):
    return subprocess.run(command.split(), stdout=subprocess.PIPE).stdout.decode('UTF-8')

with open('README.src.md', 'r') as f: content = f.read()

content = content.replace('[[toc]]', runcmd('markdown-toc README.src.md'))
content = content.replace('[[stats]]', runcmd('cloc . --md'))
content = content.replace('[[tree]]', runcmd('tree'))

with open('README.md', 'w+') as f: f.write(content)

