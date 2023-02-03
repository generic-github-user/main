from __future__ import annotations

from lib.python.option import Option

import string
import random
import itertools
import math
import functools

import typing
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

    def __contains__(self, x) -> bool:
        return self.a <= x <= self.b

    def __str__(self):
        return f'Range [ {self.a}..{self.b} ]'

    def __repr__(self):
        return f'{self.a}..{self.b}'

    def __add__(x, y):
        if isinstance(y, int): return Range(x.a + y, x.b + y)
        return Range(x.a + y.a, x.b + y.b)

    def __radd__(x, y):
        if isinstance(y, int):
            return Range(x.a + y, x.b + y)
        raise NotImplementedError

    def __sub__(x, y):
        if isinstance(y, int): return Range(x.a - y, x.b - y)
        return Range(x.a - y.a, x.b - y.b)

    def __mul__(x, y):
        return Range(x.a * y.a, x.b * y.b)

    def __lt__(self, x):
        return self.b < x

    def __gt__(self, x):
        return self.a > x

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

    def match(self, x: str) -> bool:
        return any(rule.match(x) for rule in self.options)

    def partial_match(self, x: str) -> set[int]:
        return set.union(*[rule.partial_match(x) for rule in self.options])

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

    def match(self, x: str) -> bool:
        return self.value == x

    def partial_match(self, x: str) -> set[int]:
        if x.startswith(self.value):
            # return set([len(x)])
            return set([len(self.value)])
        return set()

    def __repr__(self) -> str:
        return f'"{self.value}"'

    def __eq__(a, b):
        return a.value == b.value

    def __hash__(self):
        return hash(self.value)

def Terminals(source: Iterable[str], weights: Option[list[float]] = Option.none()) -> Choice:
    # if weights is None: weights = [1] * len(list(source))
    return Choice([Terminal(x) for x in source])

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

    def length(self) -> int | Range[int]:
        # ?
        return self.rule.length() * self.n

    def expected_length(self) -> float:
        if isinstance(self.n, int):
            return self.rule.expected_length() * self.n / 2 # ??
        return self.rule.expected_length() * self.n.midpoint()

    def match(self, x: str) -> bool:
        # TODO: unfuck
        # ?
        # if not self.n > 0 and x != '': return False
        # should the check be inverted (string-based)?
        # TODO: BoundedRange type
        if (self.n < 1 if isinstance(self.n, int) else self.n.b < 1):
            return x == ''
            # return self.rule.match(x)
        if x == '': return (self.n == 0 if isinstance(self.n, int) else 0 in self.n)
        if (match := self.rule.partial_match(x)):
            # print(f'Matched "{x}" under {self} at {match}')
            return any(Repeat(self.rule, self.n - 1).match(x[i:]) for i in match)
        # print(f'Rejected "{x}" under {self}')
        return False

    def partial_match(self, x: str) -> set[int]:
        # raise NotImplementedError
        if (self.n < 1 if isinstance(self.n, int) else self.n.b < 1):
            # return set([0]) if x == '' else set()
            return set([0])
        if (matches := self.rule.partial_match(x)):
            status = (self.n == 1 if isinstance(self.n, int) else self.n.a == 1)
            return set.union(*[set(j + i for j in Repeat(self.rule, self.n - 1).partial_match(x[i:])) for i in matches] + ([matches] if status else []))
        return set()

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

class Empty(Rule):
    def __init__(self) -> None:
        super().__init__()

    def match(self, x: str) -> bool:
        return x == ''

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

    def length(self) -> int | Range[int]:
        return sum((Range.from_scalar(l) if isinstance(l := x.length(), int) else l)
                   for x in self.rules)

    def expected_length(self) -> float:
        if len(self.rules) == 0: return 0
        return Mean([unravel(x).expected_length() for x in self.rules])

    def match(self, x: str) -> bool:
        # if len(self.rules) == 0: return False
        return bool((m := self.partial_match(x)) and any(i >= len(x) for i in m))

    def partial_match(self, x: str) -> set[int]:
        if len(self.rules) == 0:
            # return set([0]) if x == '' else set() # ?
            return set([0])
        if (matches := self.rules[0].partial_match(x)):
            # print(f'Matched "{x}" under {self} at {matches}')
            # TODO: add offset to indices (?)
            if len(self.rules) == 1: return matches
            # ?
            return set.union(*[set(j + i for j in self[1:].partial_match(x[i:])) for i in matches])
        # print(f'Rejected "{x}" under {self}')
        return set()

    def __getitem__(self, i) -> Sequence:
        return Sequence(self.rules[i])

    def __repr__(self) -> str:
        return ' '.join(map(repr, self.rules))

class Grammar:
    def __init__(self, start):
        self.start = start

class Function:
    def __init__(self, f):
        self.f = f
    
    def __truediv__(a, b):
        return lambda *args, **kwargs: a(*args) / b(*args)

    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)

# class Production

def compose(f, g):
    return lambda *a, **kw: f(g(*a, **kw))
Sum = Function(sum)
Length = Function(compose(len, list))
Mean = Sum / Length

# test = Terminal('t') * 5
test2 = Choice([Terminal(x) for x in string.ascii_lowercase]) * 10
test4 = Sequence([Terminals('ab'), Terminals('cd')])

vowels = Terminals('aeiou') + Terminals(['oo', 'ee'], weights=Option.some([0.0] * 2))
consonants = Terminals(string.ascii_lowercase) - (vowels + Terminals('qy'))\
    + Terminals(['ph', 'sh', 'ch', 'ly', 'ze', 'ne'])
start_consonants = Terminals(['fl', 'tw', 'bl', 'pl', 'tr', 'gr', 'wh', 'qu'])
end_consonants = Terminals(['ng', 'ck', 'nt', 'lt'])
syllable = Sequence([Optional(consonants + start_consonants), vowels,
                     Optional(consonants + end_consonants)])
test = syllable * Range(1, 10)
# - 'oong'

# print(test.sample())

# test = Optional(consonants)
# print(len(list(test.iter())))
# n = list(test.iter()).index(max(test.iter(), key=len))
# TODO: interpolation of stochastic grammars
# TODO: show derivation used to generate a particular string

# n = 140000
n = 0
for x in itertools.islice(test.iter(), n, n + 200):
    print(x)
for i in range(20):
    print(test.sample())

print(OrderedSet('abc') | OrderedSet('cde'))
print(OrderedSet('abc') - OrderedSet('cde'))

# print(test)
print(test.length())
print(test.expected_length())

test3 = Terminals('ab') * 10
print(test3.expected_length())

# recursive = Terminals('ab') | (Terminal('c') & Repeat((lambda: recursive), 2))
recursive = (Terminal('a') & (lambda: recursive) & Terminals('a'))\
    | (Terminal('b') & (lambda: recursive) & Terminals('b'))\
    | ''
print(recursive.sample())
# print(recursive.expected_length())
# for x in itertools.islice(recursive.iter(), 10):
    # print(x)

# print(test.match('a'))
# print(test.match('apple'))
# print(Terminal('a').match('a'))

def test_match(rule, s):
    print(f'{rule} / {s} / {rule.match(s)} / {rule.partial_match(s)}')

test_match(Terminal('a'), 'a')
test_match(test, 'a')
test_match(test, 'apple')
test_match((Terminal('a') * 5), 'aaaaa')
test_match((Terminal('a') * 5), 'aaaa')
test_match((Terminal('a') * 5), 'aaaaaa')
test_match((Terminal('a') * Range(3, 10)), 'aaaaaa')
test_match((Terminal('a') * Range(3, 10)), 'aa')
test_match(Terminals('xyz'), 'a')
test_match(Terminals('xyz'), 'y')
test_match(Terminals('ab') & Terminals('cd'), 'ad')
test_match(Terminals('ab') & Terminals('cd'), 'be')

test_match(vowels, 'a')
test_match(syllable, 'a')
test_match(Sequence([Optional(vowels), vowels]), 'a')
test_match(Optional(vowels), 'a')
