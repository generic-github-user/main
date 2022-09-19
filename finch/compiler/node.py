class Node:
    def __init__(self, children=None, parent=None, depth=0, root=None):
        # self.type = nodetype

        self.root = root if root else self
        self.parent = parent

        if children is None:
            children = []
        self.children = children

        self.depth = depth
        self.type = type(self).__name__

    def print(self, depth=0):
        print('  '*depth + str(self.type))
        for n in self.children:
            n.print(depth+1)

    def add(self, node):
        self.children.append(node)
        return self

    def __getitem__(self, i):
        return self.children[i]

    def __setitem__(self, i, value):
        self.children[i] = value

    def text(self):
        return ''.join(c.text() for c in self.children)

    def to_string(self, depth=0):
        return f'Node <{self.type}> ({self.depth})' +\
               '\n' +\
               '\n'.join('  '*depth + n.to_string(depth+1)
                         for n in self.children)

    def __str__(self):
        return self.to_string(0)

    __repr__ = __str__


class Expression(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Literal(Expression):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Int(Literal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Float(Literal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Tuple(Expression):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Array(Expression):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Symbol(Expression):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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


class Block(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def canonical(self):
        return '\n'.join(x.canonical() for x in self.children)


class Operator(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Comment(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def print(self, depth=0):
        print("  "*depth + "[Comment elided]")
