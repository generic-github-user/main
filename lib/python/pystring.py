class String:
    def __init__(self, s=''):
        if isinstance(s, String):
            s = s.s
        self.s = s

    def to_string(self):
        return self

    def iter(self):
        from lib.pyiter import Iter

        class StringIter(Iter):
            def __init__(inner, string):
                # super().__init__(inner, None, StringIter.__next__)
                super().__init__(inner, None, inner.__next__)
                inner.i = 0
                inner.string = string

            def current(inner):
                return inner.string[inner.i]

            def __next__(inner):
                if inner.i < (inner.string.len() - 1):
                    inner.i += 1
                    return inner.current()
                return None

            def __str__(inner):
                return f'StringIter <i = {inner.i}>'

        return StringIter(self)

    def len(self):
        return len(self.s)

    def __getitem__(self, key):
        return self.s[key]

    def __iadd__(self, other):
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
