import string
import itertools
from .grammars import (PEG, Symbol, Symbols, Terminals, Repeat, Range,
                       Sequence, Choice, Optional, space)

Python = PEG(Symbol('start'), dict(
    digit = Terminals(string.digits),

    int = Repeat(Symbol('digit'), Range(1, 5)),
    bool = Terminals(['True', 'False']),
    group = Repeat(Sequence([Symbol('expr'), ',']), Range(1, 2)).join(space),
    tuple = Sequence(['(', Symbol('group'), ')']),
    list = Sequence(['[', Symbol('group'), ']']),
    str = Sequence(['"', (Terminals(string.printable) - Terminals(r'"\n')) * Range(1, 10), '"']),

    slice = Optional(Symbol('expr')) & ':' & Optional(Symbol('expr'))\
        & Optional(Sequence([':', Symbol('expr')])),
    index = Symbol('expr') & '[' & Symbol('slice') & ']',

    name = (Terminals(string.ascii_lowercase) * Range(1, 8))\
        | (Symbol('name') * 2).join('_'),
    typed_name = Sequence([Symbol('name'), ':', Symbol('expr')]).join(space),
    ref = Symbol('name'),

    call = Sequence([Symbol('expr'), '(', Symbol('expr'), ')']),
    # TODO: this causes infinite recursion unless a terminal is used as the
    # first option in the `Choice`
    expr = Choice(Symbols('int name call op tuple list bool str'.split())),
    operator = (Terminals('+-*/%|&^') & Optional('='))\
             | Terminals(['**', '//', '==', '<', '>', '<=', '>=']),
    op = Sequence(Symbols('expr operator expr'.split())).join(space),
    assignment = Sequence([Choice([Symbol('name'), Symbol('typed_name')]),
                           '=', Symbol('expr')]).join(space),

    arg_list = Repeat(Sequence([Symbol('name'), ',']),
                                 Range(1, 3)).join(space),
    signature = Sequence(['(', Symbol('arg_list'),
                          Optional(Sequence(['*', Symbol('name')])), ')']),
    fn = Sequence(['def', Symbol('name'), Symbol('signature')]).join(space),

    while_ = Sequence(['while', Symbol('expr'), ':']).join(space),
    for_ = Sequence(['for', Symbol('name'), 'in', Symbol('expr'), ':']).join(space),
    statement = (Choice(Symbols('assignment expr while_ for_ fn'.split())) | 'pass') & '\n',
    # statement = TR('x'),
    block = Repeat(Symbol('statement'), Range(1, 10)),
    # start = Repeat(Symbol('statement'), Range(1, 10))
    start = Symbol('expr')
))

for x in itertools.islice(Python.iter(), 50): print(x)
