import lark
import pathlib

# TODO: make diagram of type system(s) and related abstractions
# language/framework in which assignment is an assertion of equality?

grammar = pathlib.Path('grammar.lark').read_text()
parser = lark.Lark(grammar)

tree = parser.parse(pathlib.Path('stdlib.z').read_text())
print(tree.pretty())
