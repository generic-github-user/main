from __future__ import annotations

import string
import random
import itertools

from typing import TypeVar, Generic, Any, Iterable, Iterator
T = TypeVar('T')

class Range(Generic[T]):
    def __init__(self: Range[T], a: T, b: T) -> None:
        assert b >= a
        self.a = a
        self.b = b

    def contains(self, x: T) -> bool:
        return x >= self.a and x <= self.b

    def sample(self) -> int:
        assert isinstance(self.a, int)
        return random.randint(self.a, self.b)

    def iter(self):
        return range(self.a, self.b+1)

    def __next__(self):
        if self.n < (self.bounds[1] - 1):
            self.n += 1
            return self.n
        return None

    def to_iter(self):
        return Iter(self, self.n, lambda S: self.__next__())

    def __str__(self):
        return f'Range [ {self.a}..{self.b} ]'
