# The following code is intended solely for educational and experimental purposes. I do not condone any unethical use of the code and disclaim responsibility from such use.

import ast
import random
import operator as ops
import string

for i in range(2, 50):
    for j in range(2, i):
        if i % j == 0:
            break
    else:
        print(i)

a = 'This is a test string'
print(a)
q = True, False
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
    ],
    False: [
        [ast.And, True, False],
        [ast.Or, False, False],
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
            segments = random.randint(0, 8)
            chars = len(node.value)
            indices = [0] + [random.randint(0, chars) for x in range(segments)] + [chars]
            indices = list(set(indices))
            indices.sort(reverse=False)
            # print(indices)
            # print([(indices[i-1], j) for i, j in enumerate(indices[1:])])
            parts = [node.value[indices[i]:j] for i, j in enumerate(indices[1:])]
            # print(parts)
            if len(parts) == 2:
                parts = [ast.Constant(p) for p in parts]
                node = ast.BinOp(parts[0], ast.Add(), parts[1])
            else:
                node = ast.Call(
                    ast.Attribute(ast.Constant(''), 'join', ast.Load()),
                    [random.choice(ast_iterable)(elts=[ast.Constant(p) for p in parts], ctx=ast.Load())],
                    []
                )
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
                node = ast.BoolOp(parts[0](), [ac(p) for p in parts[1:]])
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
