from __future__ import annotations
import lark
import pathlib
import sys
from lib.pylist import List
from functools import reduce
import textwrap
from typing import Callable, Union

# TODO: make diagram of type system(s) and related abstractions
# language/framework in which assignment is an assertion of equality?


class Token:
    def __init__(self, source: lark.Token = None, parent: Node = None,
                 type_: str = None, value: str = None, line: int = None,
                 column: int = None):
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

    def text(self) -> str:
        return self.value

    def __str__(self) -> str:
        return f'Token <{self.type}, {self.line}:{self.column}> {self.value}'

    def resolve_names(self, namespace):
        return resolve_names(self, namespace)

    def infer_types(self):
        match self.type:
            case 'INT':
                self.vtype = 'int'
            case 'FLOAT':
                self.vtype = 'float'

    def emit_code(self) -> str:
        return self.value

    def map(self, f) -> Token:
        return f(self)

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other) -> bool:
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
        namespace[node.name] = Node(type_='function', vtype='function',
                                    return_type=node.return_type,
                                    definition=node, body=node.body,
                                    parent=node.parent)
        return node

    if node.type in ['start', 'program', 'form', 'block', 'statement',
                     'call', 'expression', 'declaration', 'expression']:
        # TODO: rework this to be functional (match style of rest of code)
        node.children = node.children.map(lambda x: x.resolve_names(namespace))

    if node.type == 'function_declaration':
        node.body = node.body.resolve_names(namespace)

    if node.type in ['operation', 'tuple']:
        node.children = node.children.map(lambda x: x.resolve_names(namespace))

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
    def __init__(self, source: lark.Tree = None, parent: Node = None,
                 depth: int = 0, root: Node = None,
                 children: Union[list[Node], List[Node]] = None,
                 type_: str = None, vtype: str = None,
                 names: dict[str, Node] = None, **kwargs):

        self.parent: Node = parent
        self.root: Node = root if root else self
        self.depth: int = depth

        if children is None:
            children = List()
        elif isinstance(children, list):
            children = List(children)
        self.children = children
        for node in self.children:
            if node.parent is None:
                node.parent = self
                node.depth = self.depth + 1

        self.type: str = type_
        self.source: lark.Tree = source

        self.vtype: str = vtype

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
                self.alias_children('name type_params arguments return_type',
                                    'name arguments return_type')
            case 'function_declaration':
                self.signature, self.body = self.children
                self.alias_children('name type_params arguments return_type',
                                    'name arguments return_type',
                                    target=self.signature)
            case 'call':
                self.alias_children('f args')
            case 'list' | 'tuple':
                self.items = self.children
            # case 'tuple':
                # self.items = self.children[0].items
            case 'bin_op':
                self.alias_children('left op right')
            case 'assignment':
                self.alias_children('left right')

    def alias_children(self, *args, target=None):
        if target is None:
            target = self
        args = List(args).map(lambda x: x.split() if isinstance(x, str) else x)
        matches = args.filter(lambda x: len(x) == target.children.len())
        assert matches.len() > 0, f"At least one alias group must have as many elements as this node has children; got {args}, while node has children {target.children}"
        assert matches.len() == 1
        for name, node in zip(matches[0], target.children):
            setattr(self, name, node)

    def map(self, f: Callable[Node, Node],
            preserve_children: bool = False) -> Node:
        result = f(self)
        # if not preserve_children:
        # why did this work without the check before?
        if isinstance(result, Node):
            result.children = result.children.map(lambda x: x.map(f))
            for node in result.children:
                if node.parent is None:
                    node.parent = result
        # print(self)
        return result

    def map_each(self, fs: list[Callable[Node, Node]]) -> Node:
        return reduce(lambda a, b: b(a), fs, self)

    def text(self) -> str:
        return ''.join(c.text() for c in self.children)

    def __str__(self) -> str:
        return f'Node <{self.type} ~ {self.vtype}> ({self.depth})' + '\n' +\
            '\n'.join('  '*self.depth + str(n) for n in self.children)

    # def validate(self):

    def resolve_names(self, namespace: dict[str, Node] = None) -> Node:
        # return self.map(lambda n : resolve_names(n, self.names))
        return resolve_names(self, self.names)

    def infer_types(self) -> Node:
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

        self.children.map(lambda x: x.infer_types())

        if self.type in ['literal', 'expression']:
            assert self.children.len() == 1
            self.vtype = self.children[0].vtype

        return self

    def emit_code(self) -> str:
        """Generates semantically equivalent code for the target
        platform/compiler (not guaranteed to be formatted or comply with
                           typical style conventions). Currently, only C is
        supported. This method works recursively on a "C-like" syntax tree and
        is analogous to the inverse function of that represented by the parser.
        It is assumed that by now, all higher-level constructs have been
        "lowered" to canonical forms appropriate for the target; if this is not
        the case, an error may be thrown here or when the generated code is
        passed off to gcc/g++ for translation to an object file."""

        match self.type:
            case 'program':
                # TODO: handle outer function generation using tree rewriting
                body = self.children.map(Node.emit_code).join('\n')
                return '\n'.join(['int main () {', body, '}'])

            case 'start' | 'form':
                return self.children.map(Node.emit_code).join('\n')

            case 'block':
                return '{\n' + self.children.map(Node.emit_code).join('\n') + '\n}'

            case 'statement':
                return f'{self.children[0].emit_code()};'

            case 'expression' | 'declaration' | 'operation' | 'literal':
                # this is a hotfix to handle "wrapped" AST nodes; a single form
                # in the source code can sometimes produce several nested
                # statement, expression, block, etc. nodes
                return self.children.map(Node.emit_code).join('')

            case 'return':
                return f'return {self.arg.emit_code()}'

            case 'function_declaration':
                return List([self.return_type.emit_code(),
                             self.name.emit_code(),
                             '()',
                             self.body.emit_code()]).join(' ')

            case 'type':
                return ''

            case 'tuple':
                return self.children.map(Node.emit_code).join(', ')

            case 'list':
                return self.children.map(Node.emit_code).join(', ')

            case 'call':
                return f'{self.f.emit_code()}({self.args.emit_code()})'

            case 'bin_op':
                # prior to this translation, nonstandard operators like ".."
                # must have been lowered; in the future an error will be thrown
                # if they are present in the input tree
                return List([
                    self.left, self.op, self.right
                ]).map(Node.emit_code).join(' ')

            case 'INT':
                # one of the few lucky cases where the parse output is always
                # (?) equivaent to its native form (an exception may be methods
                # called on number/string literals, but this should be handled
                # during the rewriting stage)
                return self.value

            case 'assignment':
                assert self.right.vtype is not None
                return textwrap.dedent(f'{self.right.vtype} {self.left.emit_code()} = {self.right.emit_code()}')

            case _:
                if isinstance(self, Token):
                    return self.emit_code()
                raise NotImplementedError(self)

    class Expression:
        def __init__(self, *args, **kwargs):
            Node.__init__(*args, **kwargs)

    class Literal(Expression):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    class Int(Literal):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def compile(self):
            return self[0].content

    class Float(Literal):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def compile(self):
            return self[0].content

    class Tuple(Expression):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def compile(self):
            return ", ".join(x.compile() for x in self.children)

    class Array(Expression):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    class Symbol(Expression):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def compile(self):
            return self[0].content

    class Operation(Expression):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # assert len(self.children) == 3, self
            # self.left, self.op, self.right = self.children

    class Call(Expression):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    class String(Literal):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    class Block:
        def __init__(self, *args, **kwargs):
            Node.__init__(*args, **kwargs)

        def canonical(self):
            return '\n'.join(x.canonical() for x in self.children)

    class Operator:
        def __init__(self, *args, **kwargs):
            Node.__init__(*args, **kwargs)

    class Comment:
        def __init__(self, *args, **kwargs):
            Node.__init__(*args, **kwargs)

        def print(self, depth=0):
            print("  "*depth + "[Comment elided]")


class IRNode:
    pass


grammar_path = 'compiler-extension-infrastructure/grammar.lark'
grammar = pathlib.Path(grammar_path).read_text()
parser = lark.Lark(grammar)

tree = Node(parser.parse(pathlib.Path(sys.argv[1]).read_text()),
            names=dict())
# print(tree.pretty())

print(tree)
tree = tree.map(lift_tuples).map(range_filter)
tree = tree.map(lift_outer('expression', 'IDENTIFIER'))
tree = tree.map(label_assignments)
tree = tree.resolve_names()
print(tree)
tree.infer_types()
# tree = tree.map_each([lift_tuples, range_filter,
# lift_nodetype('expression', 'literal')])
print(tree)
# breakpoint()
print(tree.emit_code())
