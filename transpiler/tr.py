import ast
import argparse
import pathlib
import typing

parser = argparse.ArgumentParser()
parser.add_argument('source')


args = parser.parse_args()
content = pathlib.Path(args.source).read_text()
tree = ast.parse(content)
print(ast.dump(tree), '\n\n')
print(transpile(tree, 'js'))
