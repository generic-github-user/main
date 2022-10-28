class Token:
    def __init__(self, content, ctype, parent=None, line=0, column=0):
        self.parent = parent
        self.content = content
        self.type = ctype

        self.line = line
        self.column = column

    def text(self): return self.content

    def print(self, depth=0):
        # print('  '*depth + type(self).__name__)
        print('  '*depth + self.content)

    def to_string(self, depth=0):
        return f'Token <{self.type}, {self.line}:{self.column}> {self.content}'

    def __eq__(self, other):
        return all(
            self.content == other.content,
            self.type == other.type
        )

    def __str__(self):
        return self.to_string(0)

    __repr__ = __str__
