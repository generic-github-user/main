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

                case ast.arguments:
                    arglist = ', '.join(transpile(a, target) for a in source.args)
                    return arglist
                case ast.arg:
                    return source.arg

                case ast.FunctionDef:
                    #arglist = ', '.join(transpile(a, target) for a in source.args)
                    arglist = transpile(source.args, target)
                    return f'function {source.name} ({arglist}) {{{transpile(source.body, target)}}}'
                case ast.Call:
                    return f'{transpile(source.func, target)}({", ".join(transpile(a, target) for a in source.args)})'
                case ast.Return:
                    return f'return {transpile(source.value, target)}'
                case _: raise NotImplementedError(source, type(source))
        case _: raise NotImplementedError


args = parser.parse_args()
content = pathlib.Path(args.source).read_text()
tree = ast.parse(content)
print(ast.dump(tree), '\n\n')
print(transpile(tree, 'js'))
