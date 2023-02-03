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

    def midpoint(self) -> float:
        return (self.a + self.b) / 2

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

class OrderedSet:
    def __init__(self, data):
        self.data = data
        self.data_ = set(data)

    def __or__(a: OrderedSet, b: OrderedSet) -> OrderedSet:
        # return OrderedSet([x for x in a.data + b.data ])
        x = []
        for y in a.data + b.data:
            if not y in x: x.append(y)
        return OrderedSet(x)

    def __sub__(a: OrderedSet, b: OrderedSet) -> OrderedSet:
        return OrderedSet([x for x in a.data if x not in b.data_])

    def __iter__(self):
        return iter(self.data)

    def __contains__(self, x):
        return x in self.data_

    def __repr__(self):
        return repr(self.data)

class Rule:
    def __init__(self):
        pass

    def __mul__(self, n: int | Range[int]) -> Repeat:
        return Repeat(self, n)

    def __or__(a: Rule, b: Rule | str) -> Choice:
        if isinstance(b, str): b = Terminal(b)
        return Choice([a, b])

    def __and__(a: Rule, b: Rule) -> Sequence:
        return Sequence([a, b])

class Choice(Rule):
    def __init__(self, options: list[Rule]):
        super().__init__()
        self.options = options

    def sample(self) -> str:
        return unravel(random.choice(self.options)).sample()

    def iter(self) -> Iterator[str]:
        return itertools.chain.from_iterable(x.iter() for x in self.options)

    def length(self) -> int | Range[int]:
        return Range.join((Range.from_scalar(x.length()) if isinstance(x.length(), int) else x.length())
                          for x in self.options)

    def expected_length(self) -> float:
        if len(self.options) == 0: return 0
        return Mean([x.expected_length() for x in self.options])

    def __add__(self, b: Choice) -> Choice:
        return Choice(list(OrderedSet(self.options) | OrderedSet(b.options)))

    def __sub__(self, b: Choice) -> Choice:
        return Choice(list(OrderedSet(self.options) - OrderedSet(b.options)))

    def __repr__(self) -> str:
        return ' | '.join(map(repr, self.options))

    def __eq__(a, b) -> bool:
        return set(a.options) == set(b.options)

class Terminal(Rule):
    def __init__(self, value: str):
        super().__init__()
        self.value = value

    def sample(self) -> str:
        return self.value

    def iter(self) -> Iterator[str]:
        return [self.value]

    def length(self) -> int:
        return len(self.value)

    def expected_length(self) -> float:
        return len(self.value)

    def __repr__(self) -> str:
        return f'"{self.value}"'

    def __eq__(a, b):
        return a.value == b.value

    def __hash__(self):
        return hash(self.value)

def Terminals(source: Iterable[str], weights: Option[list[float]] = Option.none()) -> Choice:
    # if weights is None: weights = [1] * len(list(source))
    return Choice([Terminal(x) for x in source], weights=weights)

# TODO: "static" repetition (select before repeating)?
# analogues?
class Repeat(Rule):
    def __init__(self, rule: Rule, n: int | Range[int]):
        super().__init__()
        self.rule = rule
        self.n = n

    def sample(self) -> str:
        x = self.n if isinstance(self.n, int) else self.n.sample()
        # return sum(self.rule.sample() for i in range(x))
        return ''.join(unravel(self.rule).sample() for i in range(x))

    def iter(self) -> Iterator[str]:
        if isinstance(self.n, int):
            # TODO
            return Sequence([self.rule] * self.n).iter()
        return itertools.chain.from_iterable(Repeat(self.rule, x).iter()
                                             for x in self.n.iter())

    def __repr__(self) -> str:
        return f'{self.rule} {{ {self.n} }}'

    def __eq__(a, b) -> bool:
        return (a.rule == b.rule) and (a.n == b.n)

    def simplify(self) -> Repeat:
        # TODO
        return self

def Optional(source: Rule) -> Repeat:
    return Repeat(source, Range(0, 1))

def Star(source: Rule) -> Repeat:
    return Repeat(source, Range(0, math.inf))

class Sequence(Rule):
    def __init__(self, rules: list[Rule]) -> None:
        super().__init__()
        self.rules = rules

    def sample(self) -> str:
        return ''.join(unravel(x).sample() for x in self.rules)

    def iter(self) -> Iterator[str]:
        if len(self.rules) == 0:
            return []
        if len(self.rules) == 1:
            return self.rules[0].iter()
        return (a + b for a in self.rules[0].iter() for b in self[1:].iter()) # ?

    def __getitem__(self, i) -> Sequence:
        return Sequence(self.rules[i])

    def __repr__(self) -> str:
        return ' '.join(map(repr, self.rules))
