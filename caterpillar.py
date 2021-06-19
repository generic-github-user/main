# The following code is intended solely for educational and experimental purposes. I do not condone any unethical use of the code and disclaim responsibility from such use.

import ast
import random
import operator as ops
import string
import itertools
import re




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
    ],
    False: [
        [ast.And, True, False],
        [ast.Or, False, False],
        'True == False',
        'False == True',
    ]
}
# TODO: add boolean comparison operators
# TODO: add boolean to numerical/other comparison (string inequalities?)
# TODO: randomly use n // 1 instead of round
# TODO: map string length to integer
# TODO: randomize order in which transforms are applied to different node types
# TODO: use ord() and chr()
# TODO: get global variables as strings

def gen_string(n):
    return ''.join(random.choices(string.printable, k=n))

def remove_duplicates(x):
    # return [y for y in x if (x.count(y) == 1)]
    newlist = []
    [newlist.append(y) for y in x if y not in newlist]
    return newlist

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
            elif m == 2:
                node = ast.Call(ast.Name('len'), [ast.Constant(gen_string(node.value))], [])
            # Generate a shuffled list of characters and use an index method call to encode the integer
            elif m == 3:
                shuffled_chars = list(string.printable)
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
        elif type(node.value) is str:
            m = random.choice([1, 2, 3])
            if m == 1:
                pass
            elif m == 2:
                parts = segment(node.value)
                if len(parts) == 2:
                    parts = [ast.Constant(p) for p in parts]
                    node = ast.BinOp(parts[0], ast.Add(), parts[1])
                else:
                    node = ast.Call(
                        ast.Attribute(ast.Constant(''), 'join', ast.Load()),
                        [random.choice(ast_iterable)(elts=[ast.Constant(p) for p in parts], ctx=ast.Load())],
                        []
                    )
            elif m == 3:
                g = gen_string(3, charset=string.ascii_uppercase)
                if node.value and g not in node.value:
                    c = random.choice(node.value)
                    node.value = node.value.replace(c, g)
                    node = make_tree('{}.replace({}, {})', node, g, c)

        elif type(node.value) is bool:
            # print(node.value)
            ac = ast.Constant
            m = random.choice([1, 2, 3, 4, 5])
            # if random.random() < 1:
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
            elif m == 2:
                parts = random.choice(booleans[node.value])
                if type(parts) in iterable:
                    node = ast.BoolOp(parts[0](), [ac(p) for p in parts[1:]])
                else:
                    node = make_tree(parts)
            elif m == 3:
                node = ast.Call(ast.Name('bool'), [ac(random.randint(-50, 50)) if node.value else ac(0)], [])
            elif m == 4:
                node = ast.UnaryOp(ast.Not(), ac(not node.value))
            elif m == 5:
                pass

    return node

with open(__file__, 'r') as file:
    content = file.read()

parse = ast.parse(content)
# print(content, parse)
# for n in ast.walk(parse):
#     n = modify_node(n)

class NodeRewriter(ast.NodeTransformer):
    def visit_Constant(self, node):
        return modify_node(node)

    def visit_List(self, node):
        self.generic_visit(node)

        # print([a.value for a in node.elts if type(a) is ast.Constant])
        # print([type(a) for a in node.elts])
        if random.random() < 0.5:
            return ast.List([ast.List(a) for a in segment(node.elts)])
        else:
            return node

    def visit_Tuple(self, node):
        self.generic_visit(node)

        if random.random() < 0.5:
            return ast.Tuple([ast.Tuple(a) for a in segment(node.elts)])
        else:
            return node

    def visit_Attribute(self, node):
        if random.random() < 0.5:
            return ast.Call(ast.Name('getattr'), [node.value, ast.Constant(node.attr)], [])
        else:
            return node


    # def generic_visit(self, node):
    #     print('m')
    #     return modify_node(node)

def obfuscate(p, iterations=1):
    for i in range(iterations):
        p = NodeRewriter().visit(p)
    return p

parse = obfuscate(parse, 1)
result = ast.unparse(parse)
# result = ast.dump(parse)
# print(result)
with open('./butterfly.py', 'w') as file:
    file.write(result)
