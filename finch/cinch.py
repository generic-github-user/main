import sys
import pathlib
# import ascii
import string


class ArgumentError(Exception):
    pass


class Token:
    def __init__(self, content, ctype, parent=None, line=0, column=0):
        self.parent = parent
        self.content = content
        self.type = ctype

        self.line = line
        self.column = column

    def text(self): return self.content

    def to_string(self, depth=0):
        return f'Token <{self.type}, {self.line}:{self.column}> {self.content}'

    def __str__(self):
        return self.to_string(0)

    __repr__ = __str__


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


if len(sys.argv) < 2:
    raise ArgumentError
path = pathlib.Path(sys.argv[1])
print(f'Loading source from {path}')
source = path.read_text()


class CharType:
    Letter = 0
    Digit = 1
    Whitespace = 2
    Newline = 3
    Punctuation = 4
    Quote = 5


tokens = []
line = 0
col = 0
for c in source:
    chartype = None
    if c in string.ascii_letters:
        chartype = CharType.Letter
    elif c in string.digits:
        chartype = CharType.Digit
    elif c in string.whitespace:
        chartype = CharType.Whitespace
    elif c == '\n':
        chartype = CharType.Newline
    elif c == '"':
        chartype = CharType.Quote
    elif c in string.punctuation:
        chartype = CharType.Punctuation
    else:
        raise SyntaxError(f'Unknown character type: {c}')

    if not tokens or chartype != tokens[-1].type:
        tokens.append(Token(c, chartype, line=line, column=col))
    else:
        tokens[-1].content += c

    col += 1
    if c == '\n':
        line += 1
        col = 0
# print(tokens)


# class NodeType:
#    Int = 0
#    Float = 1
#    String = 2


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


class Call(Expression):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class String(Literal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Block(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Operator(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Comment(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def print(self, depth=0):
        print("  "*depth + "[Comment elided]")


tree = Block()
stack = [tree]
current = tree
depth = 0
for token in tokens:
    current = stack[-1]
    depth = len(stack)
    if isinstance(current, String) and token.type != CharType.Quote:
        current.add(token)
        continue
    match token.type:
        case CharType.Quote:
            if isinstance(current, String):
                stack.pop()
            else:
                nnode = String()
                current.add(nnode)
                stack.append(nnode)

        case CharType.Punctuation:
            match token.content:
                case "(":
                    nnode = Tuple()
                    if isinstance(current[-1], Expression):
                        nnode_inner = Call(
                            [current[-1], nnode],
                            depth=depth
                        )
                        current[-1] = nnode_inner
                        stack.append(nnode_inner)

                    current.add(nnode)
                    stack.append(nnode)

                case ")":
                    stack.pop()

                case "#":
                    nnode = Comment()
                    current.add(nnode)
                    stack.append(nnode)
        case _:
            print(tree)
            print(token)
            raise SyntaxError
print(tree)
