import string
import operator
from datetime import datetime
import textwrap
from box import Box

class Type:
    def __init__(self, name=None, **kwargs):
        if name is not None:
            self.name = name

    def __str__(self):
        if hasattr(self, 'name'): return self.name
        else: return type(self).__name__

    __repr__ = __str__

    def __or__(self, b):
        return UnionType(self, b)

class UnionType(Type):
    def __init__(self, *members):
        self.members = members

    def validate(self, x):
        return any(m.validate(x) for m in self.members)

# TODO: is another class necessary?
class RefinementType(Type):
    def __init__(self, this, p, other):
        super().__init__()
        self.this, self.p, self.other = this, p, other

    def validate(self, x):
        return all(
            (self.this.evaluate(x) if isinstance(self.this, OperationType)
                else self.this.validate(x)),
            self.p(x, other)
        )

class OperationType(Type):
    def __init__(self, a, b, op):
        super().__init__()
        self.a, self.b, self.op = a, b, op

    #def validate(self, x):
        #return all(
            #self.a.validate(x),

    def evaluate(self, x):
        return self.op(x, self.b)
