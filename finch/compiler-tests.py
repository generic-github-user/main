import unittest
# from cinch import parse, Token, Int, Float
from ftoken import Token
from node import Int, Float
from parse import parse


# Based on example(s) from https://docs.python.org/3/library/unittest.html
class TestParser(unittest.TestCase):
    def test_int_literal(self):
        self.assertEqual(parse("42"), Int([Token("42")]))

    def test_float_literal(self):
        self.assertEqual(parse("4.2"), Float([Token("4.2")]))

    def test_string_literal(self):
        self.assertEqual(parse('"forty-two"'), Float([Token('"forty-two"')]))


if __name__ == "__main__":
    unittest.main()
