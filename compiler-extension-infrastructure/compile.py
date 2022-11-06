from __future__ import annotations
import lark
import pathlib
import sys
from lib.pylist import List
from functools import reduce
import textwrap
from typing import Callable, Union

from token import Token
from node import Node

from filters import range_filter
# from resolve_names import resolve_names

# TODO: make diagram of type system(s) and related abstractions
# language/framework in which assignment is an assertion of equality?


def lift_tuples(node):
    if (node.type == 'tuple' and
            node.children.len() == 1 and
            node.children[0].type == 'list'):
        node.children = node.children[0].children
    return node


def lift_nodetype(a, b):
    def lifter(node):
        if (node.type == a and
                node.children.len() == 1 and
                node.children[0].type == b):
            node.children = node.children[0].children
        return node
    return lifter


def lift_outer(a, b):
    def lifter(node):
        if node.type == a and node.children[0].type == b:
            assert node.children.len() == 1
            return node.children[0]
        return node
    return lifter


def label_assignments(node):
    if node.type == 'bin_op' and node.op == '=':
        return Node(type_='assignment', children=[node.left, node.right],
                    names=node.names)
    return node


# def implicit_return(node):
    # if node.type == 'function':


class IRNode:
    pass


grammar_path = 'compiler-extension-infrastructure/grammar.lark'
grammar = pathlib.Path(grammar_path).read_text()
parser = lark.Lark(grammar)

tree = Node.from_lark(parser.parse(pathlib.Path(sys.argv[1]).read_text()),
                      names=dict())
# print(tree.pretty())

tree = tree.map(lift_tuples).map(range_filter)
tree = tree.map(lift_outer('expression', 'IDENTIFIER'))
tree = tree.map(label_assignments)
tree = tree.resolve_names()
print(tree)
# breakpoint()
tree = tree.infer_types()
# tree = tree.map_each([lift_tuples, range_filter,
# lift_nodetype('expression', 'literal')])
# breakpoint()
# print(tree.emit_code())
