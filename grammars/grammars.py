from __future__ import annotations

import string
import random
import itertools
import math
import functools

from typing import TypeVar, Generic, Any, Iterable, Iterator
T = TypeVar('T')

def unravel(z):
    if callable(z): return z()
    return z

class Range(Generic[T]):
    def __init__(self: Range[T], a: T, b: T) -> None:
        assert b >= a
        self.a = a
        self.b = b

    @staticmethod
    def from_scalar(x: T) -> Range[T]:
        return Range(x, x)

    def contains(self, x: T) -> bool:
        return x >= self.a and x <= self.b

    def sample(self) -> int:
        assert isinstance(self.a, int)
        return random.randint(self.a, self.b)

    def iter(self):
        return range(self.a, self.b+1)

    def join_(self: Range[T], x: T | Range[T]) -> Range[T]:
        if isinstance(x, int):
            return Range(min(self.a, x), max(self.b, x))
        # ?
        return Range(min(self.a, x.a), max(self.b, x.b))

    @staticmethod
    def join(ranges: Iterable[T | Range[T]]) -> Range[T]:
        # return Range(min(x.a for x in ranges), max(x.b for x in ranges))
        return functools.reduce(Range.join_, ranges)

    def __next__(self):
        if self.n < (self.bounds[1] - 1):
            self.n += 1
            return self.n
        return None

    def to_iter(self):
        return Iter(self, self.n, lambda S: self.__next__())

    def __str__(self):
        return f'Range [ {self.a}..{self.b} ]'

    def __repr__(self):
        return f'{self.a}..{self.b}'

    def __add__(x, y):
        return Range(x.a + y.a, x.b + y.b)

    def __radd__(x, y):
        if isinstance(y, int):
            return Range(x.a + y, x.b + y)
        raise NotImplementedError

    def __mul__(x, y):
        return Range(x.a * y.a, x.b * y.b)
