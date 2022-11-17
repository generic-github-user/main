class String:
    def __init__(self, s=''):
        if isinstance(s, String):
            s = s.s
        self.s = s

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
