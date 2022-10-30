import lark
import pathlib
import sys
from lib.pylist import List
from functools import reduce
import textwrap

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
    if node.type == 'function_declaration':
        node.body = node.body.resolve_names(namespace)
    if node.type == 'IDENTIFIER':
        print(f'Dereferencing name {node.value}')
        if node.value not in namespace:
            raise_error('name', f"""Compiler error: {node.value} not defined
                        when used at line {node.line}; make sure that name is
                        defined and in scope.""")
        # breakpoint()
        return namespace[node.value]
    # self.children.map(lambda x : x.infer_types())
    return node


def raise_error(etype, message):
    print(f'Compiler error ({etype} error): {textwrap.dedent(message)}')
    quit()


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
                raise_error('type', f"""{self.f} is not a function; defined at
                line {None}: \n\n{self.f.definition}""")
            if self.f.arity != len(self.args):
                raise_error('argument', f"""function call at line {None} has
                {len(self.args)} arguments, but function `{self.f.name}` takes
                {self.f.arity} arguments; `{self.f.name}` has signature:
                {self.f.signature}""")
            for x, y in zip(self.f.args, self.args):
                if x.argtype != y.vtype:
                    raise_error('argument', f"""argument {y} in function call
                    at line {None} has invalid type `{y.vtype}`;
                    `{self.f.name}` has signature: {self.f.signature}""")

            self.vtype = self.f.return_type

        self.children.map(lambda x : x.infer_types())

        return self

    def emit_code(self):
        match self.type:
            case 'program':
                body = self.children.map(Node.emit_code).join('\n')
                return '\n'.join(['int main () {', body, '}'])
            case 'start' | 'block' | 'form':
                return self.children.map(Node.emit_code).join('\n')
            case 'statement':
                return f'{self.children[0].emit_code()};'
            case 'expression' | 'declaration' | 'operation' | 'literal':
                return self.children.map(Node.emit_code).join('')
            case 'return':
                return f'return {self.arg.emit_code()}'
            case 'function_declaration':
                return f'{self.return_type.emit_code()} {self.name.emit_code()} () {self.body.emit_code()}'
            case 'type':
                return ''
            case 'tuple':
                return self.children.map(Node.emit_code).join(', ')
            case 'list':
                return self.children.map(Node.emit_code).join(', ')
            case 'call':
                return f'{self.f.emit_code()}({self.args.emit_code()})'
            case 'bin_op':
                return List([
                    self.left, self.op, self.right
                ]).map(Node.emit_code).join(' ')
            case 'INT':
                return self.value
            case _:
                if isinstance(self, Token):
                    return self.emit_code()
                raise NotImplementedError(self)


class IRNode:
    pass


grammar = pathlib.Path('compiler-extension-infrastructure/grammar.lark').read_text()
parser = lark.Lark(grammar)

tree = Node(parser.parse(pathlib.Path(sys.argv[1]).read_text()),
            names=dict())
# print(tree.pretty())

print(tree)
tree = tree.map(lift_tuples).map(range_filter)
tree = tree.map(lift_outer('expression', 'IDENTIFIER'))
tree = tree.resolve_names()
print(tree)
tree.infer_types()
# tree = tree.map_each([lift_tuples, range_filter,
                      # lift_nodetype('expression', 'literal')])
print(tree)
# breakpoint()
print(tree.emit_code())
