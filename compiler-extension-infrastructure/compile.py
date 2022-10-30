import lark
import pathlib

# TODO: make diagram of type system(s) and related abstractions
# language/framework in which assignment is an assertion of equality?


class Token:
    def __init__(self, source=None, parent=None,
                 type_=None, value=None, line=None, column=None):
        self.parent = parent
        self.source = source
        self.type = type_
        self.value = value

        self.line = line
        self.column = column
        if self.source is not None:
            for attr in 'type value line column'.split():
                setattr(self, attr, getattr(self.source, attr))
                self.length = len(self.source)

    def text(self): return self.value

    def __str__(self):
        return f'Token <{self.type}, {self.line}:{self.column}> {self.value}'

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

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return self == other


def range_filter(node):
    # if isinstance(node, Node):
        # print(node.type, node.op == '..')
    if node.type == 'bin_op' and node.op == '..':
        # we could also use string interpolation in combination with a parser
        # call, but this way is conceptually cleaner
        return Node(type_='call', children=[
            Token(type_='IDENTIFIER', value='range'),
            Node(type_='tuple', depth=node.depth+1, children=[
                node.left, node.right])
        ], depth=node.depth)
    return node


class Node:
    def __init__(self, source=None, parent=None, depth=0, root=None,
                 children=None, type_=None):
        self.parent = parent
        self.root = root if root else self

        if children is None:
            children = List()
        self.children = children
        self.source = source

        if self.source is not None:
            self.meta = self.source.meta
            self.type = self.source.data
            self.depth = depth
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

    def text(self):
        return ''.join(c.text() for c in self.children)

    def __str__(self):
        return f'Node <{self.type}> ({self.depth})' + '\n' +\
            '\n'.join('  '*self.depth + str(n) for n in self.children)


grammar = pathlib.Path('grammar.lark').read_text()
parser = lark.Lark(grammar)

tree = Node(parser.parse(pathlib.Path('stdlib.z').read_text()))
# print(tree.pretty())
print(tree)
