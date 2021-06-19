# The following code is intended solely for educational and experimental purposes. I do not condone any unethical use of the code and disclaim responsibility from such use.

import ast
import random
import operator as ops

for i in range(2, 50):
    for j in range(2, i):
        if i % j == 0:
            break
    else:
        print(i)

a = 'This is a test string'
print(a)
q = True, False

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
