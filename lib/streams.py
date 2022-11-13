from lib.pystring import String


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

    # def windows(self, n):

    def __bool__(self):
        return not self.is_empty()

    def __iter__(self):
        return StreamIter(self)

    iter = __iter__
