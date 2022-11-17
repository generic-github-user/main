from lib.pyiter import Iter


class StringIter(Iter):
    def __init__(self, string):
        self.i = 0
        self.string = string

    def current(self):
        return self.string[self.i]

    def __next__(self):
        if self.n < (self.string.len() - 1):
            self.n += 1
            return self.n
        return None

    def to_iter(self):
        return Iter(self, self.n, lambda S: self.__next__())

    def __str__(self):
        return f'StringIter <i = {self.i}>'


class String:
    def __init__(self, s=''):
        if isinstance(s, String):
            s = s.s
        self.s = s

    def to_string(self):
        return self

    def iter(self):
        return StringIter(self)

    def len(self):
        return len(self.s)

    def __iadd__(self, other):
        if isinstance(other, String):
            other = other.s
        return String(self.s + other)

    def __bool__(self):
        return bool(len(self.s))

    def __str__(self):
        return f'"{self.s}"'
