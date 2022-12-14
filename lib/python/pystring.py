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

    def to_str_guard(s):
        if isinstance(s, str):
            return s
        # return s.to_string()
        elif isinstance(s, String):
            return s.to_str()
        return str(s)

    def to_str(self):
        return self.s

    def to_string(self):
        return self

    def iter(self):
        from lib.pyiter import Iter

        class StringIter(Iter):
            def __init__(inner, string, i=-1):
                # super().__init__(inner, None, StringIter.__next__)
                super().__init__(inner, None, inner.__next__)
                inner.i = i
                inner.string = string
                inner.value = inner.string[inner.i]

            def current(inner):
                # return inner.string[inner.i]
                return inner.value

            def clone(inner):
                return StringIter(inner.string, inner.i)

            def windows(inner, *args, **kwargs):
                return super().windows(*args, **kwargs,
                                       size_hint=inner.string.len)
                                       # size_hint=String.len)

            def __next__(inner):
                if inner.i < (inner.string.len() - 1):
                    inner.i += 1
                    inner.value = inner.string[inner.i]
                    return inner.current()
                inner.value = None
                return None

            def __str__(inner):
                return f'StringIter <i = {inner.i}>'

        return StringIter(self)

    def len(self):
        return len(self.s)

    def __getitem__(self, key):
        # return String(self.s[key])
        return self.s[key]

    def __add__(self, other):
        if isinstance(other, String):
            other = other.s
        return String(self.s + other)

    def __bool__(self):
        return bool(len(self.s))

    def __str__(self):
        return f'"{self.s}"'

    def print(self):
        print(str(self))

    def println(self):
        print(str(self) + '\n')
