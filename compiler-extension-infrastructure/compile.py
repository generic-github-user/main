import lark
import pathlib
import sys
from lib.pylist import List
from functools import reduce

# TODO: make diagram of type system(s) and related abstractions
# language/framework in which assignment is an assertion of equality?


class Token:
    def __init__(self, source=None, parent=None,
                 type_=None, value=None, line=None, column=None):
        self.parent = parent
        self.source = source
        self.type = type_
        self.value = value

        self.vtype = None

        self.line = line
        self.column = column
        if self.source is not None:
            for attr in 'type value line column'.split():
                setattr(self, attr, getattr(self.source, attr))
                self.length = len(self.source)

    def text(self): return self.value

    def __str__(self):
        return f'Token <{self.type}, {self.line}:{self.column}> {self.value}'

    def resolve_names(self, namespace):
        return resolve_names(self, namespace)

    def infer_types(self):
        match self.type:
            case 'INT':
                self.vtype = 'int'
            case 'FLOAT':
                self.vtype = 'float'

    def emit_code(self):
        return self.value

    def map(self, f):
        return f(self)

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return self == other


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


def range_filter(node):
    # if isinstance(node, Node):
        # print(node.type, node.op == '..')
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
    if node.type == 'function_declaration':
        namespace[node.name] = Node(type_='function', vtype='function',
                                    return_type=node.return_type,
                                    definition=node, body=node.body, parent=node.parent)
        return node
    if node.type in ['start', 'program', 'form', 'block', 'statement',
                     'call', 'expression', 'declaration', 'expression']:
        # TODO: rework this to be functional (match style of rest of code)
        node.children = node.children.map(lambda x : x.resolve_names(namespace))
    if node.type == 'IDENTIFIER':
        print(f'Dereferencing name {node.value}')
        if node.value not in namespace:
            print(f'Compiler error: {node.value} not defined when used at line {node.line}; make sure that name is defined and in scope.')
            quit()
        # breakpoint()
        return namespace[node.value]
    # self.children.map(lambda x : x.infer_types())
    return node


class Node:
    def __init__(self, source=None, parent=None, depth=0, root=None,
                 children=None, type_=None, vtype=None, names=None, **kwargs):
        self.parent = parent
        self.root = root if root else self
        self.depth = depth

        if children is None:
            children = List()
        elif isinstance(children, list):
            children = List(children)
        self.children = children
        for node in self.children:
            if node.parent is None:
                node.parent = self
                node.depth = self.depth + 1

        self.type = type_
        self.source = source

        self.vtype = vtype

        if names is None:
            # names = dict()
            assert parent is not None, self
            names = parent.names
        self.names = names

        if self.source is not None:
            self.meta = self.source.meta
            self.type = self.source.data
            for c in self.source.children:
                if isinstance(c, lark.Tree):
                    self.children.append(
                        Node(c, self, self.depth+1,
                             root=self.root if self.root else self))
                elif c is None:
                    self.children.append(c)
                else:
                    assert isinstance(c, lark.Token), c
                    self.children.append(Token(c))

        for k, v in kwargs.items():
            setattr(self, k, v)

        for attr in 'arg name arguments signature type_params\
                arguments return_type f args left right op'.split():
            setattr(self, attr, None)

        # should we separate the AST representation from the IR?
        match self.type:
            case 'return':
                assert self.children.len() == 1, self
                self.arg = self.children[0]
            case 'fn_signature':
                self.name, self.type_params,\
                    self.arguments, self.return_type = self.children
            case 'function_declaration':
                self.signature, self.body = self.children
                self.name, self.type_params,\
                    self.arguments, self.return_type = self.signature.children
            case 'call':
                self.f, self.args = self.children
            case 'list' | 'tuple':
                self.items = self.children
            # case 'tuple':
                # self.items = self.children[0].items
            case 'bin_op':
                self.left, self.op, self.right = self.children

    def map(self, f, preserve_children=False):
        result = f(self)
        # if not preserve_children:
        # why did this work without the check before?
        if isinstance(result, Node):
            result.children = result.children.map(lambda x : x.map(f))
            for node in result.children:
                if node.parent is None:
                    node.parent = result
        # print(self)
        return result

    def map_each(self, fs):
        return reduce(lambda a, b: b(a), fs, self)

    def text(self):
        return ''.join(c.text() for c in self.children)

    def __str__(self):
        return f'Node <{self.type}> ({self.depth})' + '\n' +\
            '\n'.join('  '*self.depth + str(n) for n in self.children)

    # def validate(self):

    def resolve_names(self, namespace=None):
        # return self.map(lambda n : resolve_names(n, self.names))
        return resolve_names(self, self.names)

    def infer_types(self):
        if self.type == 'call':
            if self.f.vtype != 'function':
                print(self.f, self.f.vtype)
                print(f'Compile error: {self.f} is not a function; defined at line {None}: \n\n{self.f.definition}')
            if self.f.arity != len(self.args):
                print(f'Compile error (arity mismatch): function call at line {None} has {len(self.args)} arguments, but function `{self.f.name}` takes {self.f.arity} arguments; `{self.f.name}` has signature: {self.f.signature}')
                quit()
            for x, y in zip(self.f.args, self.args):
                if x.argtype != y.vtype:
                    print(f'Compile error (argument error): argument {y} in function call at line {None} has invalid type `{y.vtype}`; `{self.f.name}` has signature: {self.f.signature}')
                    quit()

            self.vtype = self.f.return_type

        self.children.map(lambda x : x.infer_types())

        return self
parser = lark.Lark(grammar)

tree = Node(parser.parse(pathlib.Path('stdlib.z').read_text()))
# print(tree.pretty())
print(tree)
