# The following code is intended solely for educational and experimental purposes. I do not condone any unethical use of the code and disclaim responsibility from such use.

import ast
import random
import operator as ops
import string
import itertools
import re
from pyvis.network import Network


for i in range(2, 50):
    for j in range(2, i):
        if i % j == 0:
            break
    else:
        print(i)

test1 = 'appleb6>b6>b6>b6>b6>b6>b6>b6>b6>b6>b6>b6>b6>pear'
test2 = 'g5g5g5g5g5g5g5g5g5testing'
test3 = 'helloworld121212121212121212'

a = 'This is a test string'
print(a)
q = True, False
t = True
# r = list(range(0, 30, 4))
r = [5, 7, 9, 2, 3, 5, 7, 5, 2, 6, 4]
v = '1m0r4ghp3qosjl5ifcd2n76eat98kbl9pm36n8fe05s14d2iq7thkjbrcago'

# TODO: random string replacements + string repetition
# TODO: visualize program as graph of nodes


transforms = [
    [ops.add, ast.Sub],
    [ops.sub, ast.Add],
    [ops.mul, ast.Div],
    [ops.truediv, ast.Mult],
]
# TODO: add other math operations (sqrt, modulo, trig functions, etc.)
# TODO: add bit shift operators
iterable = [list, tuple]
ast_iterable = [ast.List, ast.Tuple]
booleans = {
    True: [
        [ast.And, True, True],
        [ast.Or, True, False],
        'True == True',
        'False == False',
        'True != False',
        'False != True',
    ],
    False: [
        [ast.And, True, False],
        [ast.Or, False, False],
        'True == False',
        'False == True',
        'True != True',
        'False != False',
    ]
}
# TODO: add boolean comparison operators
# TODO: add boolean to numerical/other comparison (string inequalities?)
# TODO: randomly use n // 1 instead of round
# TODO: map string length to integer
# TODO: randomize order in which transforms are applied to different node types
# TODO: use ord() and chr()
# TODO: get global variables as strings

def gen_string(n, charset=string.printable):
    return ''.join(random.choices(charset, k=n))

def remove_duplicates(x):
    # return [y for y in x if (x.count(y) == 1)]
    newlist = []
    [newlist.append(y) for y in x if y not in newlist]
    return newlist

# https://stackoverflow.com/a/29489919/10940584
def principal_period(s):
    i = (s+s).find(s, 1, -1)
    return None if i == -1 else s[:i]

print(principal_period('0.6666666666666666'))

# https://stackoverflow.com/a/9079897/10940584
def repetitions(s):
   r = re.compile(r"(.+?)\1+")
   for match in r.finditer(s):
       yield (match.group(1), len(match.group(0))/len(match.group(1)))
print(list(repetitions('0.6666666666666666')))
print(list(repetitions('762e380mkf94dljrip1catnbsqohg5')))

def segment(sequence, num=None):
    chars = len(sequence)
    if not num:
        num = round(random.uniform(0, 0.1) * chars)
    indices = [0] + [random.randint(0, chars) for x in range(num)] + [chars]
    print(indices)
    indices = remove_duplicates(indices)
    indices.sort(reverse=False)
    # print(indices)
    # print([(indices[i-1], j) for i, j in enumerate(indices[1:])])
    parts = [sequence[indices[i]:j] for (i, j) in enumerate(indices[1:])]
    # print(parts)
    return parts

primitives = [str, int, float, bool]
def make_tree(source, *nested):
    if nested:
        nested = [ast.Constant(n) if type(n) in primitives else n for n in nested]
        return ast.parse(source.format(*[ast.unparse(n) for n in nested]))
    else:
        # print(source, ast.dump(ast.parse(source)))
        return ast.parse(source)

def modify_node(node):
    if type(node) is ast.Constant:
        if type(node.value) is int:
            m = random.choice([1, 2, 3, 4])
            # Generate a mathematical expression that produces the number
            if m == 1:
                equ_expr = random.randint(-50, 50)
                # if random.random() < 0.5:
                #     val, op = node.value+equ_expr, ast.Sub()
                # else:
                #     val, op = node.value-equ_expr, ast.Add()
                inv, op = random.choice(transforms)

                # Avoid division by 0 by switching the inverse operation
                if inv == ops.truediv and equ_expr == 0:
                    inv = ops.mul
                val = inv(node.value, equ_expr)

                a, b = ast.Constant(val), ast.Constant(equ_expr)
                # a = str(a)
                a = ast.Call(ast.Name(type(val).__name__), [ast.Constant(str(a.value))], [])

                node_int = type(node.value) == int
                node = ast.BinOp(a, op(), b)
                # Round nodes that might produce float values if the node originally stored an integer
                if inv in [ops.mul, ops.truediv] and node_int:
                    node = ast.Call(ast.Name('round'), [node], [])
            # Generate a random string with len == value and encode the integer as the length of the string
            elif m == 2 and node.value <= 10:
                node = ast.Call(ast.Name('len'), [ast.Constant(gen_string(node.value))], [])
            # Generate a shuffled list of characters and use an index method call to encode the integer
            elif m == 3:
                shuffled_chars = list(string.printable[:30])
                random.shuffle(shuffled_chars)
                shuffled_chars = ''.join(shuffled_chars)
                # print(shuffled_chars)
                if 0 <= node.value < len(shuffled_chars):
                    node = ast.Call(ast.Attribute(ast.Constant(shuffled_chars), 'index', ast.Load()), [ast.Constant(shuffled_chars[node.value])], [])
            # Leave the node unchanged
            elif m == 4:
                pass

            # Randomly wrap the node in a lambda function and a function call that executes it
            if random.random() < 0.5:
                node = ast.Call(ast.Lambda([], body=node), [], [])
        # Rewrite strings (string literals/constants)
        elif type(node.value) is str:
            # Randomly select a transformation
            m = random.choice([1, 2, 3, 4])

            # Apply no transform
            if m == 1:
                pass
            # Split the string into random segments and represent it as the concatenation of these segments
            elif m == 2:
                parts = segment(node.value)
                if random.random() < 0.5:
                    parts = [ast.Constant(p) for p in parts]
                    # node = ast.BinOp(parts[0], ast.Add(), parts[1])
                    node = make_tree(' + '.join(['{}']*len(parts)), *parts)
                else:
                    node = ast.Call(
                        ast.Attribute(ast.Constant(''), 'join', ast.Load()),
                        [random.choice(ast_iterable)(elts=[ast.Constant(p) for p in parts], ctx=ast.Load())],
                        []
                    )
            # Rewrite the string as the (equivalent) result of replacing a sequence of characters
            elif m == 3:
                g = gen_string(3, charset=string.ascii_uppercase)
                if node.value and g not in node.value:
                    c = random.choice(node.value)
                    node.value = node.value.replace(c, g)
                    node = make_tree('{}.replace({}, {})', node, g, c)
            # "Compress" the string by finding a repeated pattern/substring and encoding this part of the string as a repeated string literal (e.g., "0.6666666" might become something like "0." + "6" * 7)
            elif m == 4:
                reps = list(repetitions(node.value))
                if reps:
                    selected = max(reps, key=lambda s: len(s[0]) * s[1])
                    pattern, num = selected
                    start = node.value.find(pattern)
                    end = node.value.rfind(pattern)+len(pattern)
                    a = node.value[:start]
                    b = make_tree('{} * {}', pattern, round(num))
                    c = node.value[end:]
                    h = [g for g in [a, b, c] if g]
                    # node = make_tree('{} + {} + {}', a, b, c)
                    node = make_tree(' + '.join(['{}']*len(h)), *h)


            # TODO: use detected patterns for replacements

        # Encode booleans
        elif type(node.value) is bool:
            # print(node.value)
            ac = ast.Constant
            m = random.choice([1, 2, 3, 4, 5])
            # if random.random() < 1:

            # Rewrite boolean as a comparison between numerical values that is guaranteed to evaluate to the original True/False value
            if m == 1:
                x = random.randint(-50, 50)
                y = random.randint(1, 100)
                if node.value:
                    z = x - y
                    node = ast.Compare(ac(x), [ast.Gt()], [ac(z)])
                else:
                    z = x - y
                    node = ast.Compare(ac(x), [ast.Lt()], [ac(z)])
                node = ast.Expr(node)
            # Rewrite the boolean as a logical operation on other boolean values
            # e.g., True might become (True or False) or False might become (False and True)
            elif m == 2:
                parts = random.choice(booleans[node.value])
                if type(parts) in iterable:
                    node = ast.BoolOp(parts[0](), [ac(p) for p in parts[1:]])
                elif type(parts) is str:
                    node = make_tree(parts)
            # Encode the boolean as a casting from a numerical value to a bool; 0 will become False and anything else will evaluate as True
            elif m == 3:
                node = ast.Call(ast.Name('bool'), [ac(random.randint(-50, 50)) if node.value else ac(0)], [])
            # Rewrite as boolean inverse ("not" operator)
            elif m == 4:
                node = ast.UnaryOp(ast.Not(), ac(not node.value))
            elif m == 5:
                pass

    return node

# TODO: add eval() based rewrites

with open(__file__, 'r') as file:
    content = file.read()

parse = ast.parse(content)
# print(content, parse)
# for n in ast.walk(parse):
#     n = modify_node(n)

names = {}

class NodeRewriter(ast.NodeTransformer):
    def visit_alias(self, node):
        # for i, n in enumerate(node.names):
        if node.name not in names:
            newname = gen_string(5, charset=string.ascii_letters)
            names[node.name] = newname
            if node.asname:
                names[node.asname] = newname
            # node.names[i].asname = newname
            return ast.alias(node.name, newname)
        else:
            return node

    def visit_Constant(self, node):
        return modify_node(node)

    def visit_List(self, node):
        self.generic_visit(node)

        # print([a.value for a in node.elts if type(a) is ast.Constant])
        # print([type(a) for a in node.elts])
        if random.random() < 0.5 and len(node.elts) > 3:
            nested = ast.List([ast.List(a) for a in segment(node.elts)])
            return ast.parse('list(itertools.chain(*{}))'.format(ast.unparse(nested)))
        else:
            return node

    def visit_Tuple(self, node):
        self.generic_visit(node)

        if random.random() < 0.5 and len(node.elts) > 3:
            return ast.Tuple([ast.Tuple(a) for a in segment(node.elts)])
        else:
            return node

    def visit_Attribute(self, node):
        if random.random() < 0.5 and type(node.ctx) == ast.Load:
            return ast.Call(ast.Name('getattr'), [node.value, ast.Constant(node.attr)], [])
        else:
            return node

    # def visit_Name(self, node):
        # if random.random() < 1 and node.id in globals():
        #     return ast.Subscript(ast.Call(ast.Name('globals'), [], []), ast.Constant(node.id))
        # else:
        #     return node


    # def generic_visit(self, node):
    #     print('m')
    #     return modify_node(node)

class NameRewriter(ast.NodeTransformer):
    def visit_Name(self, node):
        if node.id in names:
            # node.id = names[node.id]
            return ast.Name(names[node.id], node.ctx)
        else:
            return node

def obfuscate(p, iterations=1):
    """
    Obfuscate source code by applying logical transformations that convert abstract syntax tree nodes into other nodes (or combinations of nodes) that are semantically equivalent

    Params:
        iterations: The number of times to apply the obfuscation
    """
    for i in range(iterations):
        p = NodeRewriter().visit(p)
        p = NameRewriter().visit(p)
    return p

def attrstring(a, b):
    result = a
    # if '.' in b:
    b = b.split('.')
    for p in b:
        if hasattr(result, p):
            result = getattr(result, p)
        else:
            return None
    return result

def firstavailable(m, *props):
    for p in props:
        # if hasattr(m, p):
            # return getattr(m, p)
        value = attrstring(m, p)
        if value:
            return value
    return 'None'

uniques = ast_iterable + [ast.BinOp, ast.Assign, ast.Dict, ast.BoolOp, ast.Call, ast.Compare, ast.Constant]
from pyvis.utils import check_html
class NetworkVis(Network):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def show(self, name):
        check_html(name)
        if self.template is not None:
            return self.write_html(name, notebook=True)
        else:
            self.write_html(name)

vis = NetworkVis(directed=True)
# vis.toggle_physics(False)
# def add_node(node)
descriptors = {
    ast.Constant: 'value',
    ast.Name: 'id',
    ast.Starred: lambda x: 'starred',
    # ast.Call: lambda x: x.func.id if type(x.func) is ast.Name else
    # ast.Compare: lambda x: ast.unparse(x.ops[0]),
    ast.Compare: lambda x: type(x.ops[0]).__name__,
    ast.FunctionDef: 'name',
    ast.BinOp: lambda x: type(x.op).__name__,
}
parse = obfuscate(parse, 1)
result = ast.unparse(parse)
fix = '=+'
for c in fix:
    # result = result.replace(f'{c} \n', '= ')
    result = result.replace('{} \n'.format(c), '= ')
# result = ast.dump(parse)
# print(result)


with open('./butterfly.py', 'w') as file:
    file.write(result)
