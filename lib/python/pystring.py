from __future__ import annotations
from lib.python.pylist import List


class String:
    def __init__(self, s=''):
        if isinstance(s, String):
            s = s.s
        self.s = s

    def split(self, x) -> List[String]:
        return List(self.s.split(x)).map(String)

    def lines(self) -> List[String]:
        return List(self.s.splitlines()).map(String)

    def chars(self) -> List[String]:
        return List(self.s)

    def to_string(self):
        return self

    def __iadd__(self, other):
        if isinstance(other, String):
            other = other.s
        return String(self.s + other)

    def __bool__(self):
        return bool(len(self.s))

    def __str__(self):
        return f'"{self.s}"'
