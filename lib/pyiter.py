from lib.pystring import String
from lib.number import Number


class Number2(int):
    def __init__(self, x):
        super().__init__()
# breakpoint()

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
