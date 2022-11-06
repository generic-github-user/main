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


def range_filter(node):
    """This filter handles desugaring of the ".." syntax, which is modelled
    loosely after Rust's. The operator is transformed into a call to the
    `range` function, which returns a particular kind of iterator. If the
    traits system and/or iterator trait/type are not used in the compilation
    process, it can be further rewritten into a standalone loop.

    This filter is also used as an example of a generic filter in `README.md`,
    and is helpful for demonstrating the purpose of the compiler extension
    infrastructure project."""

    # if isinstance(node, Node):
    #     print(node.type, node.op == '..')
    if node.type == 'bin_op' and node.op == '..':
        # we could also use string interpolation in combination with a parser
        # call, but this way is conceptually cleaner
        return Node(type_='call', children=[
            Token(type_='IDENTIFIER', value='range'),
            Node(type_='tuple', depth=node.depth+1, children=[
                node.left, node.right], parent=node.parent)
        ], depth=node.depth, parent=node.parent)
    return node


def resolve_names(node, namespace):
    """Replaces identifiers in particular kinds of locations ("evaluation
    contexts") with references to their values. This should generally happen
    before type inference is attempted."""

    if node.type == 'function_declaration':
        assert hasattr(node, 'signature') and node.signature is not None
        assert hasattr(node.signature, 'arguments') and\
            node.signature.arguments is not None
        fnode = Node(type_='function', vtype='function',
                     return_type=node.return_type,
                     definition=node,
                     name=node.signature.name,
                     signature=node.signature,
                     body=node.body,
                     arguments=node.signature.arguments,
                     arity=node.signature.arguments.children.len(),
                     parent=node.parent)
        namespace[node.name] = fnode
        for p in fnode.arguments.children:
            namespace[p.name] = None
        # breakpoint()
        result = node.with_attr('body', node.body.resolve_names(namespace))
        fnode.arguments.children.map(lambda x: namespace.pop(x.name))
        return result

    if node.type in ['start', 'program', 'form', 'block', 'statement',
                     'call', 'expression', 'declaration', 'expression']:
        print(f'Resolving names in {node.type}')
        return node.with_attr('children',
                              node.children.map(lambda x: x.resolve_names(namespace)))

    if node.type in ['operation', 'tuple', 'bin_op', 'literal']:
        print(f'Resolving names in {node.type}')
        return node.with_attr('children',
                              node.children.map(lambda x: x.resolve_names(namespace)))

    if node.type in ['OPERATOR', 'STRING', 'INT']:
        return node

    if node.type == 'IDENTIFIER':
        assert isinstance(node, Token)
        print(f'Dereferencing name {node.value}')
        if node.value not in namespace:
            raise_error('name resolution', f"""\
                        {node.value} not defined when used at line {node.line};
                        make sure that name is defined and in scope.""")
        # breakpoint()
        return namespace[node.value]

    raise NotImplementedError(node.type)
    # self.children.map(lambda x : x.infer_types())
    # return node


def raise_error(etype, message):
    wrapped = textwrap.dedent(message).replace("\n", " ")
    print(f'Compiler error ({etype} error): {wrapped}')
    quit()


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
