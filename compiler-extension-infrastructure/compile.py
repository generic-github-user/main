import lark
import pathlib

grammar = pathlib.Path('grammar.lark').read_text()
parser = lark.Lark(grammar)

tree = parser.parse(pathlib.Path('stdlib.z').read_text())
print(tree.pretty())
