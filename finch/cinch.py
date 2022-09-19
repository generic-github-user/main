import sys
import pathlib
# import ascii
import string
from parse import parse


class ArgumentError(Exception):
    pass


if len(sys.argv) < 2:
    raise ArgumentError
path = pathlib.Path(sys.argv[1])
print(f'Loading source from {path}')
source = path.read_text()

tree = parse(tokens)
# print(tree)
tree.print()


