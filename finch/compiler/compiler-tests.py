import unittest
# from cinch import parse, Token, Int, Float
from ftoken import Token
from node import Int, Float
from chartype import CharType
from lex import lex
from parse import parse


# Based on example(s) from https://docs.python.org/3/library/unittest.html
class TestParser(unittest.TestCase):
    def test_int_literal(self):
        self.assertEqual(parse(lex("42")), Int([Token("42", CharType.Digit)]))

    def test_float_literal(self):
        self.assertEqual(parse(lex("4.2")), Float([Token("4.2")]))

    def test_string_literal(self):
        self.assertEqual(parse(lex('"forty-two"')), Float([Token('"forty-two"', CharType.String)]))


if __name__ == "__main__":
    unittest.main()
