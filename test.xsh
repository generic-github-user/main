def Echo (x : str):
    print(x)
    return x

Echo!(hello)

def Echo2 (x):
    print(x.split())
    return x
Echo2!(a b c)

def enum (name : str, variants : str):
    import ast
    print(name, variants)
    src = '\n'.join([
        f'class {name}:',
        '\n'.join(f'    {v} = {i}'
            for i, v in enumerate(variants.split())),
        f'    __variants__ = {variants.split()}'])
    print(src)
    return src

exec(enum!(Animal, cat dog fish))
print(Animal)
print(Animal.cat)

def fn (params : str, value : str):
    return eval(f'lambda {", ".join(params.split())}: {value}')

import lark
import textwrap
import pprint
class brace:
    __xonsh_block__ = str

    def __enter__ (self):
        pass

    def __exit__ (self, *args):
        # TODO: is there a cleaner way to do this?
        parser = lark.Lark("""
            other: /[^{}]+/
            pair: other block
            block: "{" (pair | block | other)* "}"
            start: (pair | block | other)*
            %import common.WS
            %ignore WS
        """)
        tree = parser.parse(self.macro_block)
        class Visitor(lark.visitors.Transformer):
            block = fn!(self args, '\n'.join(args))
            start = block
            other = fn!(self args, '\n'.join(x.strip()
                for x in args[0].splitlines()).strip())
            pair = fn!(self args, f'{args[0]}:\n{textwrap.indent(args[1], "    ")}')
        reshaped = Visitor().transform(tree)
        exec(reshaped)

class braces:
    __xonsh_block__ = str

    def __enter__ (self):
        pass

    def __exit__ (self, *args):
        result = ''
        for line in self.macro_block.splitlines():
            line = line.strip()
            for c in line:
                if c == '{':
                    result += ''
        return result

with! brace():
    def fib (n) {
        result = [0, 1]
        for i in range(n) {
            result.append(sum(result[-2:]))
        }
        return result[:max(0, len(result))]
    }
    print(fib(10))
