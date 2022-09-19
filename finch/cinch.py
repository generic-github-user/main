import sys
import pathlib
# import ascii
import string


class ArgumentError(Exception):
    pass


class Token:
    def __init__(self, source, parent=None):
        self.parent = parent
        self.source = source
        for attr in 'type value line column'.split():
            setattr(self, attr, getattr(self.source, attr))
            self.length = len(self.source)

    def text(self): return self.value

    def __str__(self):
        return f'Token <{self.type}, {self.line}:{self.column}> {self.value}'


class Node:
    def __init__(self, source, parent=None, depth=0, root=None):
        self.parent = parent
        self.root = root if root else self
        self.children = []
        self.source = source

        self.meta = self.source.meta
        self.type = self.source.data
        self.depth = depth
        for c in self.source.children:
            if isinstance(c, lark.Tree): self.children.append(
                    Node(c, self, self.depth+1, root=self.root if self.root else self))
            elif c is None: self.children.append(c)
            else:
                assert isinstance(c, lark.Token), c
                self.children.append(Token(c))

    def text(self):
        return ''.join(c.text() for c in self.children)

    def __str__(self):
        return f'Node <{self.type}> ({self.depth})' + '\n' + '\n'.join('  '*self.depth + str(n) for n in self.children)


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
