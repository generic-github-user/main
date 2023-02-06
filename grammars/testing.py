import string
import itertools
import operator

from lib.python.option import Option
from .grammars import (PEG, Symbol, Symbols, Terminal, Terminals, Repeat,
                       Range, Sequence, Choice, Optional, space, OrderedSet)

TR = Terminal

# name        = lambda: Terminals(string.ascii_lowercase)
# call        = lambda: expr() & '(' & expr() & ')'
# expr        = lambda: call() | op()
# op          = lambda: expr() & Terminals('+-*/') & expr
# assignment  = lambda: TR('x')
# statement   = lambda: assignment | expr()
# Python      = lambda: Star(statement).simplify()
# Python      = lambda: Repeat(statement, Range(1, 10)).simplify()
# print(Python().sample())

# test = Terminal('t') * 5
test2 = Choice([Terminal(x) for x in string.ascii_lowercase]) * 10
test4 = Sequence([Terminals('ab'), Terminals('cd')])

vowels = Terminals('aeiou') + Terminals(['oo', 'ee', 'oi', 'oa', 'ou', 'ia', 'ea', 'eau'], weights=Option.some([0.0] * 2))
consonants = Terminals(string.ascii_lowercase) - (vowels + Terminals('qy'))\
    + Terminals(['ph', 'sh', 'ch', 'ly', 'ze', 'ne', 'st', 'dy', 'ny', 'by',
                 'my', 'th', 'ty', 'oy', 'ay', 'ey'])
start_consonants = Terminals(['fl', 'tw', 'bl', 'pl', 'tr', 'gr', 'wh', 'qu', 'br',
                              'gh', 'gl', 'fr', 'dr', 'gl', 'sl'])
# end_consonants = Terminals(['ng', 'ck', 'nt', 'lt', 'ld', 'lz', 'nn', 'pp', 'nd'])
end_consonants = Terminals(['ng', 'ck', 'nt', 'nn', 'pp', 'ff', 'll', 'tt', 'nd',
                            'rd', 'sm', 'rp', 'ct', 'rc', 'mb', 'rt']) | (Terminal('l') & Terminals('tdzmpf')) # use "+"?
syllable = Sequence([Optional(consonants | start_consonants), vowels,
                     Optional(consonants | end_consonants)])\
    | Terminals(['dy'])
test = (syllable * Range(1, 10)) & Optional(Terminal('s')) & Optional(Terminal("'s"))
test_restricted = (syllable * Range(1, 10))
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
# print(test.length())
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
    print(f'{str(rule)[:100]} / {s} / {rule.match(s)} / {rule.partial_match(s)}')

test_match(Terminal('a'), 'a')
test_match(test, 'a')
test_match(test, 'apple')
test_match((Terminal('a') * 5), 'aaaaa')
test_match((Terminal('a') * 5), 'aaaa')
test_match((Terminal('a') * 5), 'aaaaaa')
test_match((Terminal('a') * Range(3, 10)), 'aaaaaa')
test_match((Terminal('a') * Range(3, 10)), 'aa')
test_match((Terminal('a') * Range(3, 5)), 'aaaaaaaaaaaa')
test_match(Terminals('xyz'), 'a')
test_match(Terminals('xyz'), 'y')
test_match(Terminals('ab') & Terminals('cd'), 'ad')
test_match(Terminals('ab') & Terminals('cd'), 'be')

test_match(vowels, 'a')
test_match(syllable, 'a')
test_match(Sequence([Optional(vowels), vowels]), 'a')
test_match(Optional(vowels), 'a')
test_match(test, 'zzzzz')
test_match(test, 'ba')

# simple ascii art generated using a visual attribute grammar
# test4 = 

with open('word_test.txt', 'w') as f:
    for x in itertools.islice(test_restricted.iter(), 40000): f.write(x + '\n')
with open('random_words.txt', 'w') as f:
    for x in range(1000): f.write(test_restricted.sample() + '\n')

with open('/usr/share/dict/words', 'r') as words:
    for w in itertools.islice(words, 200):
        w = w.strip().lower()
        if not test.match(w): print(w)

# for x in itertools.islice((Terminals('ab') * Range(1, 10)).iter(), 100):
for x in itertools.islice(Optional(Terminals('xy')).iter(), 100):
    print(x)

print(test.size())

# Python = Star(statement).simplify()
# Python = Repeat(statement, Range(1, 10)).simplify()

# print(Python.sample())
recursion_test = PEG(Symbol('start'), dict(
    start = Terminals('ab') | Symbol('expr') | Terminal('d'),
    expr = Sequence([Symbol('start') * 1, 'c'])))
recursion_test = PEG(Symbol('start'), dict(
    start = Sequence([Terminal('t'), Terminal('v') | Symbol('start')])))
for x in itertools.islice(recursion_test.iter(), 10): print(x)

# breakpoint()

# TODO: allow breadth-first iteration over implicit grammar trees?
# TODO: limit depth of generated trees for a specific rule/grammar (how?)

print(Repeat('gec', 4).join(' ').sample())

recursion_test_2 = PEG(Symbol('start'), dict(
    start = Terminals('ab') & Optional(Symbol('start'))
))
for x in itertools.islice(recursion_test_2.iter(), 10): print(x)

recursion_test_3 = PEG(Symbol('expr'), dict(
    digit = Terminals(string.digits),
    # expr = Symbol('digit') | Sequence([Symbol('expr'), '+', Symbol('expr')])
    expr = Symbol('digit') | Sequence([Symbol('expr'), '+', Symbol('expr')])
))
for x in itertools.islice(recursion_test_3.iter(), 50): print(x)

test_match(~ (Terminal('a') * 5), 'aaaaa')
test_match(~ (Terminal('a') * 5), 'aaaa')
test_match(~ (Terminal('a') * 5), 'aaaaaa')

ops = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,
    '%' : operator.mod,
    '^' : operator.xor,
}
math_expr = PEG(Symbol('expr'), dict(
   digit = Terminals(string.digits),
   nonzero = Terminals(string.digits) - Terminals('0'),
   int = Terminal('0') | Repeat(Symbol('nonzero'), Range(1, 2)),
   expr = Symbol('int') | Sequence(['(', Symbol('expr'), Terminals('+-*/%'),
      Symbol('expr'), ')']).join(space).attribute(value=lambda *c: ops[c[2]](c[1], c[3]))
))
print(math_expr.sample())
