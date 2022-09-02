#
# simpleArith.py
#
# Example of defining an arithmetic expression parser using
# the infixNotation helper method in pyparsing.
#
# Copyright 2006, by Paul McGuire
#

# Adapted from https://github.com/pyparsing/pyparsing/blob/master/examples/simpleArith.py

import sys
from pyparsing import *

ppc = pyparsing_common

ParserElement.enablePackrat()
sys.setrecursionlimit(3000)

integer = ppc.integer
variable = Word(alphas, exact=1)
operand = integer | variable

expop = Literal("^")
signop = oneOf("+ -")
multop = oneOf("* /")
plusop = oneOf("+ -")
factop = Literal("!")

arith = infixNotation(
    operand,
    [
        ("!", 1, opAssoc.LEFT),
        ("^", 2, opAssoc.RIGHT),
        (signop, 1, opAssoc.RIGHT),
        (multop, 2, opAssoc.LEFT),
        (plusop, 2, opAssoc.LEFT),
    ],
)

test = [
    "9 + 2 + 3",
    "9 + 2 * 3",
    "(9 + 2) * 3",
    "(9 + -2) * 3",
    "(9 + -2) * 3^2^2",
    "(9! + -2) * 3^2^2",
    "M*X + B",
    "M*(X + B)",
    "1+2*-3^4*5+-+-6",
    "(a + b)",
    "((a + b))",
    "(((a + b)))",
    "((((a + b))))",
    "((((((((((((((a + b))))))))))))))",
]
# for t in test:
#     print(t)
#     print(arith.parseString(t))
#     print("")
