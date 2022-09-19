import sys
import pathlib


class ArgumentError(Exception):
    pass


if len(sys.argv) < 2:
    raise ArgumentError
path = pathlib.Path(sys.argv[1])
print(f'Loading source from {path}')
source = path.read_text()
