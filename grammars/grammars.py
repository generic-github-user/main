from __future__ import annotations

from lib.python.option import Option

import string
import random
import itertools
import math
import pathlib
import operator
import collections
from dataclasses import dataclass

import functools
from functools import reduce

import typing
from typing import TypeVar, Generic, Any, Iterable, Iterator, Callable
from typing_extensions import Protocol
T = TypeVar('T')
V = TypeVar('V')

def unravel(z):
    if callable(z): return z()
    return z

def string_terminal(f: Callable[[RuleLike], V]) -> Callable[[RuleLike | str], V]:
    def wrapped(x: RuleLike | str) -> V:
        return f(Terminal(x) if isinstance(x, str) else x)
    return wrapped

def string_terminal_method(f):
    def wrapped(self, x: RuleLike | str):
        return f(self, Terminal(x) if isinstance(x, str) else x)
    return wrapped


# from https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
class memoized(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   '''
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      if not isinstance(args, collections.abc.Hashable):
         # uncacheable. a list, for instance.
         # better to not cache than blow up.
         return self.func(*args)
      if args in self.cache:
         return self.cache[args]
      else:
         value = self.func(*args)
         self.cache[args] = value
         return value
   def __repr__(self):
      '''Return the function's docstring.'''
      return self.func.__doc__
   def __get__(self, obj, objtype):
      '''Support instance methods.'''
      return functools.partial(self.__call__, obj)

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

class RuleLike(Protocol):
    name: Option[str]

    def length(self) -> int | Range[int]:
        ...

    def expected_length(self) -> float:
        ...

    def match(self, x: str) -> bool:
        ...

    def partial_match(self, x: str) -> set[int]:
        ...

    def iter(self) -> Iterator[str]:
        ...

    def size(self) -> int:
        ...

    def bind(self, grammar: PEG) -> RuleLike:
        ...

    def sample(self) -> str:
        ...

    def to_productions(self) -> set[Production]:
        ...

    def __mul__(self, n: int | Range[int]) -> Repeat:
        ...

    def __or__(a: RuleLike, b: RuleLike | str) -> Choice:
        ...

    def __and__(a: RuleLike, b: RuleLike) -> Sequence:
        ...

class Rule:
    def __init__(self, name=Option.none()):
        self.name = name

    def __mul__(self, n: int | Range[int]) -> Repeat:
        return Repeat(self, n)

    def __or__(a: RuleLike, b: RuleLike | str) -> Choice:
        if isinstance(b, str): b = Terminal(b)
        return Choice([a, b])

    def __and__(a: RuleLike, b: RuleLike) -> Sequence:
        return Sequence([a, b])

    def bind(self, grammar: PEG) -> RuleLike:
        if hasattr(self, '_bound'): return self
        # very bad
        r = self
        if isinstance(r, Choice):
            r.options = [grammar.resolve(x.bind(grammar)) for x in r.options]
        if isinstance(r, Repeat):
            r.rule = grammar.resolve(r.rule.bind(grammar))
        if isinstance(r, Sequence):
            r.rules = [grammar.resolve(x.bind(grammar)) for x in r.rules]
        self._bound = True
        return self

class Namespace(Generic[T, V]):
    def __init__(self):
        self.names = BiDict[T, V]


class Choice(Rule):
    def __init__(self, options: list[RuleLike], name: str = Option.none()):
        super().__init__(name)
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

    @memoized
    def match(self, x: str) -> bool:
        return any(rule.match(x) for rule in self.options)

    @memoized
    def partial_match(self, x: str) -> set[int]:
        return set.union(*[rule.partial_match(x) for rule in self.options])

    def size(self) -> int:
        return sum(x.size() for x in self.options)

    # allow abstract rules on LHS (instead of simple strings)?
    # two dimensions of genericity: subrule type and subrule inner type/type parameter (?)
    # grid inheritance (RuleLike type -> Named[RuleLike type])
    def to_productions(self) -> set[Production]:
        # ns: Namespace[] = Namespace()
        return set(Production(Sequence([Symbol(self.name.unwrap()) if self.name.is_some else ns.symbol()]),
                              Sequence([Symbol(r.name.unwrap())])) for r in self.options)\
            | set.union(*[r.to_productions() for r in self.options])

    def __add__(self, b: Choice) -> Choice:
        return Choice(list(OrderedSet(self.options) | OrderedSet(b.options)))

    def __sub__(self, b: Choice) -> Choice:
        return Choice(list(OrderedSet(self.options) - OrderedSet(b.options)))

    def __repr__(self) -> str:
        return ' | '.join(map(repr, self.options))

    def __eq__(a, b) -> bool:
        return set(a.options) == set(b.options)

    def __hash__(self) -> int:
        return hash(tuple(self.options))

class Terminal(Rule):
    def __init__(self, value: str, name: str = Option.none()):
        super().__init__(name)
        self.value = value

    def sample(self) -> str:
        return self.value

    def iter(self) -> Iterator[str]:
        return [self.value]

    def length(self) -> int:
        return len(self.value)

    def expected_length(self) -> float:
        return len(self.value)

    @memoized
    def match(self, x: str) -> bool:
        return self.value == x

    @memoized
    def partial_match(self, x: str) -> set[int]:
        if x.startswith(self.value):
            # return set([len(x)])
            return set([len(self.value)])
        return set()

    def size(self) -> int:
        return 1

    def __repr__(self) -> str:
        return f'"{self.value}"'

    def __eq__(a, b):
        return a.value == b.value

    def __hash__(self):
        return hash(self.value)

def Terminals(source: Iterable[str], weights: Option[list[float]] = Option.none()) -> Choice:
    # if weights is None: weights = [1] * len(list(source))
    return Choice([Terminal(x) for x in source])

def Symbols(source: Iterable[str]) -> list[Symbol]:
    return [Symbol(x) for x in source]

# TODO: "static" repetition (select before repeating)?
# analogues?
class Repeat(Rule):
    def __init__(self, rule: RuleLike | str, n: int | Range[int],
                 name: str = Option.none()):
        super().__init__(name)
        if isinstance(rule, str): rule = Terminal(rule)
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

    @memoized
    def match(self, x: str) -> bool:
        return bool((m := self.partial_match(x)) and any(i >= len(x) for i in m))
        # TODO: BoundedRange type

    @memoized
    def partial_match(self, x: str) -> set[int]:
        # TODO work through low, mid, and high cases
        # how should the base case work on an empty string?
        result = set()
        if (matches := self.rule.partial_match(x)) and not self.n < 1: # ?
            result |= set.union(*[set(j + i for j in Repeat(self.rule, self.n - 1).partial_match(x[i:]))
                                  for i in matches])
        if (self.n < 1 if isinstance(self.n, int) else self.n.a < 1):
            result |= set([0])
        return result

    def size(self) -> int:
        if isinstance(self.n, int): return self.rule.size() ** self.n
        return sum(Repeat(self.rule, n).size() for n in self.n.iter())

    def __repr__(self) -> str:
        return f'{self.rule} {{ {self.n} }}'

    def __eq__(a, b) -> bool:
        return (a.rule == b.rule) and (a.n == b.n)

    def __hash__(self) -> int:
        return hash((self.rule, self.n))

    def simplify(self) -> Repeat:
        # TODO
        return self

    @string_terminal_method
    def join(self, x: RuleLike) -> RuleLike:
        return Repeat(self.rule & x, self.n - 1) & self.rule

# class Join

@string_terminal
def Optional(source: RuleLike) -> Repeat:
    return Repeat(source, Range(0, 1))

@string_terminal
def Star(source: RuleLike) -> Repeat:
    return Repeat(source, Range(0, math.inf))

class Empty(Rule):
    def __init__(self, name: str = Option.none()) -> None:
        super().__init__(name)

    def match(self, x: str) -> bool:
        return x == ''

class Sequence(Rule):
    def __init__(self, rules: list[RuleLike | str | Symbol],
                 name: str = Option.none()) -> None:
        super().__init__(name)
        self.rules: list[RuleLike | Symbol] = [(Terminal(r) if isinstance(r, str) else r)
                                      for r in rules]
        assert len(self.rules) < 1000

    def sample(self) -> str:
        return ''.join(unravel(x).sample() for x in self.rules)

    def iter(self) -> Iterable[str]:
        if len(self.rules) == 0:
            return [''] # should this be empty?
        if len(self.rules) == 1:
            return self.rules[0].iter()
        return (a + b for b in self[1:].iter() for a in self.rules[0].iter()) # ?

    def length(self) -> int | Range[int]:
        return sum((Range.from_scalar(l) if isinstance(l := x.length(), int) else l)
                   for x in self.rules)

    def expected_length(self) -> float:
        if len(self.rules) == 0: return 0
        return Mean([unravel(x).expected_length() for x in self.rules])

    @memoized
    def match(self, x: str) -> bool:
        return bool((m := self.partial_match(x)) and any(i >= len(x) for i in m))

    @memoized
    def partial_match(self, x: str) -> set[int]:
        if len(self.rules) == 0:
            return set([0])
        if (matches := self.rules[0].partial_match(x)):
            return set.union(*[set(j + i for j in self[1:].partial_match(x[i:]))
                               for i in matches])
        return set()

    def size(self) -> int:
        return reduce(operator.mul, [r.size() for r in self.rules], 1)

    def join(self, x: RuleLike) -> Sequence:
        return Sequence([y for r in self.rules for y in (r, x)][:-1])

    def __getitem__(self, i) -> Sequence:
        return Sequence(self.rules[i])

    def __repr__(self) -> str:
        return ' '.join(map(repr, self.rules))

@dataclass
class Symbol:
    name: str

    def bind(self, _):
        return self

    __mul__ = Rule.__mul__
    __and__ = Rule.__and__
    # __sub__ = Choice.__sub__
    __or__ = Rule.__or__

# TODO: reconcile this with other grammar representations
class PEG:
    def __init__(self, root: Symbol | RuleLike, rules: dict[str, RuleLike]) -> None:
        self.root = root
        self.rules = rules

        if isinstance(self.root, Symbol):
            self.root = self.rules[self.root.name]

        # make this less horrible later
        for name, rule in self.rules.items():
            rule.bind(self)
            rule.name = Option.some(name)
        self.root = self.resolve(self.root)

        self.sample = self.root.sample
        self.iter = self.root.iter

    def resolve(self, name: Symbol | RuleLike) -> RuleLike:
        if isinstance(name, Rule): return name
        assert isinstance(name, Symbol)
        return self.rules[name.name]

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

class Production:
    # TODO: support preserving data/attributes from left (input) rule
    def __init__(self, left: Rule, right: Rule):
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f'{self.left} -> {self.right}'

def compose(f, g):
    return lambda *a, **kw: f(g(*a, **kw))
Sum = Function(sum)
Length = Function(compose(len, list))
Mean = Sum / Length


# def infer(source: str) -> Rule:

# print(infer("A stochastic grammar (statistical grammar) is a grammar framework with a probabilistic notion of grammaticality."))


TR = Terminal
space = Terminal(' ')
