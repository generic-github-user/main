import lark
from lark import Lark
from lark.indenter import Indenter
import pathlib


# Based on example at
# https://lark-parser.readthedocs.io/en/latest/examples/indented_tree.html
class TreeIndenter(Indenter):
    NL_type = '_NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8


grammar = pathlib.Path('python.lark').read_text()
parser = Lark(grammar, parser='lalr', postlex=TreeIndenter())
source = pathlib.Path('sample.py').read_text()


def test():
    print(parser.parse(source).pretty())


if __name__ == '__main__':
    test()
