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
