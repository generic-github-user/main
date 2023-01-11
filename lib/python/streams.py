from lib.pystring import String
from macropy.experimental.tco import macros, tco
# from macropy.core.hquotes import hq, u


# one day I will pay for my sins
def If(p, x, y):
    if p:
        return x()
    else:
        return y()


class SEmpty:
    def is_empty():
        return True

    def __iter__():
        return StreamIter(SEmpty)
    iter = __iter__

    def to_list():
        return []

    def all(f):
        return True

    def nth(i):
        raise IndexError(i)


for m in ['map', 'filter']:
    setattr(SEmpty, m, lambda S: SEmpty)


def memo(f):
    def memoized(*args, **kwargs):
        return f(*args, **kwargs)
    return memoized


class Stream:
    def __init__(self, head, tail):
        self.head = head
        self.tail = memo(tail)

    def is_empty(self):
        return False

    def to_list(self):
        return If(self, lambda: [self.head] + self.tail().to_list(),
                  lambda: [])

    def to_set(self):
        return set(self.to_list())

    def to_string(self):
        return f'<{", ".join(self.map(str).iter())}>'

    def print(self):
        print(self.to_string())

    def map(self, f):
        return If(self, lambda: Stream(f(self.head),
                                       lambda: self.tail().map(f)), SEmpty)

    def filter(self, f):
        # print(self.head)
        return If(f(self.head),
                  lambda: Stream(self.head, lambda: self.tail().filter(f)),
                  lambda: self.tail().filter(f))

    # def reduce(self, f, init):
        # return

    # @with_continuations()
    # def all(self, f, self=None):
    @tco
    def all(self, f):
        return f(self.head) and self.tail().all(f)
        # return f(self.head) and

    def nth(self, i):
        if i == 0:
            return self.head
        else:
            return self.tail().nth(i - 1)

    def take(self, n):
        if n == 0:
            return SEmpty
        else:
            return Stream(self.head, lambda: self.tail().take(n - 1))

    # def windows(self, n):

    def __bool__(self):
        return not self.is_empty()

    def __iter__(self):
        return StreamIter(self)

    iter = __iter__


class StreamIter:
    def __init__(self, S):
        self.S = S

    def __iter__(self):
        return self

    def __next__(self):
        if self.S.is_empty():
            raise StopIteration
        v = self.S.head
        self.S = self.S.tail()
        return v


def range(a, b):
    return If(
        a < b,
        lambda: Stream(
            a,
            lambda: range(
                a + 1,
                b)),
        lambda: SEmpty)
