import sys
import pathlib
# import ascii
import string


class ArgumentError(Exception):
    pass


class Token:
    def __init__(self, content, ctype, parent=None):
        self.parent = parent
        self.content = content
        self.type = ctype

        self.line = 0
        self.column = 0

    def text(self): return self.content

    def __str__(self):
        return f'Token <{self.type}, {self.line}:{self.column}> {self.content}'

    __repr__ = __str__


class Node:
    def __init__(self, nodetype, parent=None, depth=0, root=None):
        self.type = nodetype

        self.root = root if root else self
        self.parent = parent
        self.children = []

        self.depth = depth

    def text(self):
        return ''.join(c.text() for c in self.children)

    def __str__(self):
        return f'Node <{self.type}> ({self.depth})' +\
               '\n' +\
               '\n'.join('  '*self.depth + str(n) for n in self.children)


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


tokens = []
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
    elif c in string.punctuation:
        chartype = CharType.Punctuation
    else:
        raise SyntaxError(f'Unknown character type: {c}')

    if not tokens or chartype != tokens[-1].type:
        tokens.append(Token(c, chartype))
    else:
        tokens[-1].content += c
print(tokens)
