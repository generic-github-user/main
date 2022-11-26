def Echo (x : str):
    print(x)
    return x

Echo!(hello)

# def Echo2 (x : list[str]):
# def Echo2 (*x : str):
def Echo2 (x):
    # print(list(x))
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
    # return ast.parse(src)
    # exec(src)

exec(enum!(Animal, cat dog fish))
print(Animal)
print(Animal.cat)

# def brace ()
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
        # print(tree.pretty())
        # pprint.pprint(tree)
        class Visitor(lark.visitors.Transformer):
            def block(self, args):
                # print(f'block: {args}')
                return '\n'.join(args)
            start = block
            def other(self, args):
                # return args[0].strip()
                return '\n'.join(x.strip() for x in args[0].splitlines()).strip()
            def pair(self, args):
                # print(f'pair: {args}')
                return f'{args[0]}:\n{textwrap.indent(args[1], "    ")}'
        # print(Visitor().transform(tree))
        # reshaped = Visitor().transform(tree).children[0]
        reshaped = Visitor().transform(tree)
        # print(reshaped)
        exec(reshaped)
        return

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
