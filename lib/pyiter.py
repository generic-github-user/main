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
        # TODO: allow proper cloning of range objects
        return Iter(self, self.n, lambda S: self.__next__())
        # RangeIterator = Iter.make_iterator_wrapper()

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
        class taker(Iter):
            def __init__(inner, i=0):
                super().__init__(inner, None, inner.__next__)
                inner.i = i

            def __next__(inner):
                # nonlocal i
                if inner.i < n:
                    inner.i += 1
                    return self.next()
                return None

            def clone(inner):
                return taker(i=inner.i)

        # return Iter(self, self.current(), nnext)
        return taker()

    def windows(self, n, size_hint=None):
        i = 0

        def nnext(S):
            nonlocal i
            # return S.stepped().clone().take(n)
            if self.next() is None or (size_hint is not None
                                       and i >= size_hint() - n - 1):
                return None
            return self.clone().take(n)
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
            value = self.next()
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
        while (x := self.next()) is not None:
            result.append(x)
        return result

    def to_set(self):
        return set(self.to_list())

    def to_string(self):
        return self.map(String.to_str_guard).join(', ')

    def print(self):
        print(self.to_string())

    @staticmethod
    def make_iterator_wrapper(origin, wrapper_next, attributes):
        class Wrapper(Iter):
            def __init__(inner, *args, **kwargs):
                super().__init__(inner, None, inner.__next__, *args, **kwargs)

            def __next__(inner):
                return wrapper_next(inner)

            def clone(inner):
                attrs = {k: getattr(inner, k) for k in attributes.keys()}
                return Wrapper(**attrs)
        return Wrapper


def range(*args):
    return Range(*args).to_iter()
