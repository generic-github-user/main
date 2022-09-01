import ast
import argparse
import pathlib
import typing

parser = argparse.ArgumentParser()
parser.add_argument('source')


def transpile(source, target: str) -> str:
    match target:
        case 'js':
            match type(source):
                case ast.Module:
                    return '\n'.join(transpile(s, target) for s in source.body)
                case _ if isinstance(source, list):
                    return '\n'.join(transpile(s, target) for s in source)

                case _: raise NotImplementedError(source, type(source))
        case _: raise NotImplementedError


args = parser.parse_args()
content = pathlib.Path(args.source).read_text()
tree = ast.parse(content)
print(ast.dump(tree), '\n\n')
print(transpile(tree, 'js'))
