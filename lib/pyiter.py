from lib.pystring import String
from lib.number import Number


class Number2(int):
    def __init__(self, x):
        super().__init__()
# breakpoint()


class Range:
    def __init__(self, a, b):
        self.n = Number(a)
        self.bounds = (Number(a), Number(b))

    def __next__(self):
        # print(self.n, self.bounds[1])
        # breakpoint()
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
        # if init is None: init = inner.value
        if next_ is None:
            next_ = lambda S: inner.__next__()

        self.value = init
        self.inner = inner

        self.next_ = next_
        # self.__next__ = next_
        # self.next = self.__next__

    def __iter__(self):
        return self

    def __next__(self):
        # return self.inner.__next__()
        self.value = self.next_(self)
        return self.value

    def next(self):
        self.value = self.__next__()
        return self.value

    def step(self):
        v = self.value
        self.next()
        return v

    # TODO
    def filter(self, f):
        def nnext(S):
            while not f(self.value):
                if self.inner.value is None:
                    return None
                pass
            return self.inner.value

        return Iter(self, self.value, nnext)

    def map(self, f):
        def nnext(S):
            # value = self.inner.__next__()
            value = self.step()
            if value is None:
                return value
            else:
                return f(value)
        return Iter(self, f(self.value), nnext)
    def to_list(self):
        result = []
        while (x := self.step()) is not None:
            # print(self.next_)
            result.append(x)
        return result

    def to_set(self):
        return set(self.to_list())

    def to_string(self):
        return self.map(lambda x: x.to_string()).join(', ')

    def print(self):
        print(self.to_string())


def range(*args):
    return Range(*args).to_iter()
