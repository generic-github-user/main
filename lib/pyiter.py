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
