import operator

class Type:
    """
    A class representing an abstract type (rather than the typical sense in
    which classes correspond roughly to types); instances of this class are
    themselves types, though these semantics can be occasionally abused for
    convenience or out of necessity. This (and its subclasses) is (are)
    intended to be an alternative to those in Python's `typing` module that
    suit the needs of this project. Accordingly, they are suitable for type
    signatures, documentation, type checking, interactive debugging etc.
    """

    def __init__(self, name=None, **kwargs):
        """
        Initialize a new type with name given by `name`.
        """

        if name is not None:
            self.name = name

    def __str__(self):
        """
        Create a short string representing this type.
        """

        if hasattr(self, 'name'): return self.name
        else: return type(self).__name__

    __repr__ = __str__
    def doc(self, fmt, **kwargs):
        """
        Generates documentation for this type in the specified `fmt` (see
        `Class.doc` for more detailed information on this method). Note also
        that this is an internal method that will generally not need to be used
        outside of the module.
        """

        return str(self)

    def __or__(self, b):
        """
        Create a union type joining this type and type `b`. The new type
        references this object.
        """

        return UnionType(self, b)

class UnionType(Type):
    def __init__(self, *members):
        super().__init__()
        self.members = members

    def validate(self, x):
        return any(m.validate(x) for m in self.members)

class RangeType(Type):
    def __init__(self, a=None, b=None):
        super().__init__()
        self.a = a
        self.b = b

    def canonical(self):
        return

# TODO: is another class necessary?
class RefinementType(Type):
    def __init__(self, this, p, other):
        super().__init__()
        self.this, self.p, self.other = this, p, other

    def validate(self, x):
        return all(
            # check compliance with the inner type ...
            (self.this.evaluate(x) if isinstance(self.this, OperationType)
                else self.this.validate(x)),
            # ... and with the predicate
            self.p(x, other)
        )

    #def doc(self, fmt): return str(self)

    def __str__(self):
        sym = None
        match self.p:
            case operator.eq: sym = '=='
            case operator.ne: sym = '!='
            case operator.gt: sym = '>'
            case operator.ge: sym = '>='
            case operator.lt: sym = '<'
            case operator.le: sym = '<='

        other = self.other
        if isinstance(other, str): other = f'"{other}"'
        return f'{self.this} {sym} {other}'

    def eng(self): pass

# an expression formed with a type and a value combined using an operator, e.g.
# when we access an object property or index (the exact semantics of this class
# might need some work)
class OperationType(Type):
    def __init__(self, a, b, op):
        """
        Generates a new expression type by applying `op` to `a` (left) and `b`
        (right).
        """

        super().__init__()
        self.a, self.b, self.op = a, b, op

    #def validate(self, x):
        #return all(
            #self.a.validate(x),

    def evaluate(self, x):
        return self.op(x, self.b)

# simple types that correspond roughly to Python datatypes

class StringType(Type):
    def __init__(self):
        super().__init__()

    def validate(self, x): return isinstance(x, str)
String = StringType()

#setattr(String, f'__getitem__', staticmethod(expr_factory('getitem')))

class FloatType(Type):
    def __init__(self):
        super().__init__()

    def validate(self, x): return isinstance(x, float)
Float = FloatType()

class IntType(Type):
    def __init__(self):
        super().__init__()

    def validate(self, x): return isinstance(x, int)
Int = IntType()

#Tuple = Type('Tuple')
class Tuple(Type):
    def __init__(self, *args, **kwargs):
        super().__init__()

class OptionType(Type):
    def __init__(self, *args, T=None, **kwargs):
        super().__init__()
        self.T = T

    def __getitem__(self, i):
        if not isinstance(i, Type): raise TypeError
        return OptionType(T=i)

    def __str__(self):
        return f'Option<{self.T}>'
Option = OptionType()
