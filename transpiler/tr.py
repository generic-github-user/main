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

                case ast.Name:
                    return source.id

                case ast.UnaryOp:
                    return ' '.join([
                        transpile(source.op, target),
                        transpile(source.operand, target)
                    ])
                case ast.UAdd: return '+'
                case ast.USub: return '-'
                case ast.Not | ast.Invert: return '!'

                case ast.Assign:
                    targets = ', '.join(transpile(t, target) for t in source.targets)
                    return f'{targets} = {transpile(source.value, target)}'

                case ast.BinOp:
                    return ' '.join([
                        transpile(source.left, target),
                        transpile(source.op, target),
                        transpile(source.right, target)
                    ])
                case ast.BoolOp:
                    return f' {transpile(source.op, target)} '.join(transpile(v, target) for v in source.values)
                case ast.Or: return '||'
                case ast.And: return '&&'
                case ast.Eq: return '=='
                case ast.NotEq: return '=='
                case ast.Gt: return '>'
                case ast.GtE: return '>='
                case ast.Compare:
                    # ref https://stackoverflow.com/a/7946825
                    tail = [val for pair in zip(source.ops, source.comparators) for val in pair]
                    return ' '.join(transpile(x, target) for x in [source.left] + tail)

                case ast.Add: return '+'
                case ast.Sub: return '-'
                case ast.Mult: return '*'
                case ast.Div: return '/'
                case ast.Mod: return '%'

                case ast.JoinedStr:
                    return f'`{"".join(transpile(x, target) for x in source.values)}`'
                case ast.FormattedValue:
                    return f'${{{transpile(source.value, target)}}}'

                case ast.Subscript:
                    return f'{transpile(source.value, target)}[{transpile(source.slice, target)}]'
                case ast.Slice:
                    return transpile(source.lower, target)

                case ast.If:
                    NL = '\n'
                    return f'if ({transpile(source.test, target)}) {{{transpile(source.body, target)}}}'

                case ast.Constant:
                    #match source.kind:
                    match type(source.value).__name__:
                        case 'str': return f'"{source.value}"'
                        case 'NoneType': return 'null'
                        case 'int' | 'float': return str(source.value)
                        case 'bool': return str(source.value).lower()
                        case _: raise NotImplementedError(source.value, source.kind)
                #case ast.NameConstant:
                    #match source.value:
                case ast.Expr:
                    return transpile(source.value, target)
                #case _ if isinstance(source, NoneType):
                case _ if source is None:
                    return 'null'

                case _: raise NotImplementedError(source, type(source))
        case _: raise NotImplementedError


args = parser.parse_args()
content = pathlib.Path(args.source).read_text()
tree = ast.parse(content)
print(ast.dump(tree), '\n\n')
print(transpile(tree, 'js'))
