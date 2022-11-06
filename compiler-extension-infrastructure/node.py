from __future__ import annotations
from lib.pylist import List
import lark
from functools import reduce
import textwrap
from typing import Callable, Union

# from .token import Token
from . import token
# from .raise_error import raise_error
from . import raise_error
# from .resolve_names import resolve_names
from . import resolve_names


class Node:
    def __init__(self, source: lark.Tree = None, parent: Node = None,
                 depth: int = 0, root: Node = None,
                 children: Union[list[Node], List[Node]] = None,
                 type_: str = None, vtype: str = None,
                 names: dict[str, Node] = None, update: bool = True, **kwargs):

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

        for k, v in kwargs.items():
            setattr(self, k, v)
        if update:
            self.update_attrs()


    def from_lark(source: lark.Tree, *args, **kwargs):
        # self = Node.__init__(source=source, *args, **kwargs)
        self = Node(source=source, *args, **kwargs)

        self.meta = self.source.meta
        self.type = self.source.data
        for c in self.source.children:
            if isinstance(c, lark.Tree):
                self.children.append(
                    Node.from_lark(c, parent=self, depth=self.depth+1,
                         root=self.root if self.root else self))
            elif c is None:
                self.children.append(c)
            else:
                assert isinstance(c, lark.Token), c
                self.children.append(token.Token(c))
        self.update_attrs()

        return self

    def update_attrs(self):
        # for attr in 'arg name arguments signature type_params\
                # arguments return_type f args left right op'.split():
            # setattr(self, attr, None)

        self.data_attrs = set()
        # should we separate the AST representation from the IR?
        match self.type:
            case 'return':
                assert self.children.len() == 1, self
                self.alias_children('arg')
            case 'fn_signature':
                self.alias_children('name type_params arguments return_type',
                                    'name arguments return_type')
            case 'function_declaration':
                self.alias_children('signature body')
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
            case 'typed_name':
                self.alias_children('name ptype')

    def alias_children(self, *args, target=None):
        if target is None:
            target = self
        args = List(args).map(lambda x: x.split() if isinstance(x, str) else x)
        matches = args.filter(lambda x: len(x) == target.children.len())
        assert matches.len() > 0, f"At least one alias group must have as many elements as this node has children; got {args}, while node has children {target.children}; target is\n{target}"
        assert matches.len() == 1
        if target == self:
            setattr(self, 'child_aliases', matches[0])
        for name, node in zip(matches[0], target.children):
            if hasattr(self, name):
                print(f'Warning: overwriting existing attribute "{name}" with value {getattr(self, name)} (new value is {node}) -- this may not be the intended behavior. Use `update=False` to suppress this update.')
            setattr(self, name, node)
            self.data_attrs.add(name)

    def map(self, f: Callable[Node, Node],
            preserve_children: bool = False) -> Node:
        result = f(self)
        # if not preserve_children:
        # why did this work without the check before?
        if isinstance(result, Node):
            result = result.with_attr('children',
                                      result.children.map(lambda x: x.map(f)))
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
        return resolve_names.resolve_names(self, self.names if namespace is None else namespace)

    def clone(self, *args, **kwargs) -> Node:
        return Node(**{attr: getattr(self, attr) for attr in
                       set(['parent', 'depth', 'source', 'names',
                            'children', 'type', 'vtype']) | self.data_attrs},
                    **kwargs)

    def with_attr(self, k, v, update: bool = True,
                  propagate: bool = True) -> Node:
        nnode = self.clone(update=update)
        if propagate and k != 'children':
            assert isinstance(v, (Node, token.Token)), f'{k}, {v}'
            self.children[self.child_aliases.index(k)] = v
        setattr(nnode, k, v)
        if update:
            nnode.update_attrs()
        return nnode

    def infer_types(self) -> Node:
        if self.type == 'call':
            if self.f.vtype != 'function':
                print(self.f, self.f.vtype)
                try:
                    raise_error('type', f"""{self.f} is not a function; defined at
                    line {None}: \n\n{self.f.definition}""")
                except AttributeError as ex:
                    print(ex, '\n', self, '\n', self.f)
                    quit()

            if self.f.arity != len(self.args.children):
                raise_error('argument', f"""function call at line {None} has
                {len(self.args)} arguments, but function `{self.f.name}` takes
                {self.f.arity} arguments; `{self.f.name}` has signature:
                {self.f.signature}""")

            for x, y in zip(self.f.arguments.children, self.args.children):
                if x.ptype != y.vtype:
                    raise_error('argument', f"""
                    argument {y.source.meta} (for parameter {x.name.value}) in function
                    call at line {None} has invalid type `{y.vtype}`;
                    `{self.f.name.value}` has signature: {self.f.signature}""")

            return self.with_attr('vtype', self.f.return_type)

        self.children.map(lambda x: x.infer_types())

        if self.type in ['literal', 'expression']:
            assert self.children.len() == 1
            return self.with_attr('vtype',  self.children[0].vtype)

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
                if isinstance(self, token.Token):
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
