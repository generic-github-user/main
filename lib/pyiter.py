from lib.python.pystring import String
from lib.python.number import Number


class Number2(int):
    def __init__(self, x):
        super().__init__()


class Range:
    def __init__(self, a, b):
        self.n = Number(a)
        self.bounds = (Number(a), Number(b))

    def __next__(self):
        if self.n < (self.bounds[1] - 1):
            self.n += 1
            return self.n
        return None

    def to_iter(self):
        return Iter(self, self.n, lambda S: self.__next__())

    def __str__(self):
        return f'Range [ {self.bounds[0]}..{self.bounds[1]} ]'


class Iter:
    def __init__(self, inner, init=None, next_=None):
        if next_ is None:
            next_ = lambda S: inner.__next__()

        self.value = init
        self.inner = inner

        self.next_ = next_
        # self.__next__ = next_
        # self.next = self.__next__

    def clone(self):
        return Iter(self.inner, self.value, self.next_)

    def __iter__(self):
        return self

    def __next__(self):
        self.value = self.next_(self)
        return self.value

    def next(self):
        self.value = self.__next__()
        return self.value

    def step(self):
        v = self.current()
        self.next()
        return v

    def stepped(self):
        self.next()
        return self

    def current(self):
        return self.value

    # TODO
    def filter(self, f):
        def nnext(S):
            while not f(self.step()):
                if S.current() is None:
                    return None
            return S.current()

        return Iter(self, self.current(), nnext)

    def take(self, n):
        i = 0

        def nnext(S):
            nonlocal i
            if i < n:
                i += 1
                return self.next()
            return None

        return Iter(self, self.current(), nnext)

    def windows(self, n):
        def nnext(S):
            # return S.stepped().clone().take(n)
            if self.next() is None:
                return None
            return S.clone().take(n)
        return Iter(self, self.current(), nnext)

    def all(self, f):
        while (x := self.step()) is not None:
            # if not f(self.current()):
            if not f(x):
                return False
        return True

    def any(self, f):
        while (x := self.step()) is not None:
            if f(x):
                return True
        return False

    def none(self, f):
        return not self.any(f)

    def map(self, f):
        def nnext(S):
            value = self.step()
            if value is None:
                return value
            else:
                return f(value)
        return Iter(self, self.current(), nnext)

    def join(self, delim):
        result = ''
        # TODO
        while (x := self.next()) is not None:
            if result:
                result += delim
            result += String.to_str_guard(x)
            # result += str(x)
        return result

    def to_list(self):
        result = []
        while (x := self.step()) is not None:
            result.append(x)
        return result

    def to_set(self):
        return set(self.to_list())

    def to_string(self):
        return self.map(String.to_str_guard).join(', ')

    def print(self):
        print(self.to_string())


def range(*args):
    return Range(*args).to_iter()
