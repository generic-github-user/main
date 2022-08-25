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


def predicate_factory(y):
    def np(self, other):
        return RefinementType(self, getattr(operator, y), other)
    return np

# bind predicate-generating operators (for refinement types); if n is an int, T
# > n is essentially shorthand for x: T, x > n
for op in ['eq', 'ne', 'gt', 'ge', 'lt', 'le']:
    setattr(Type, f'__{op}__', predicate_factory(op))
    #setattr(Type, f'__{op}__', staticmethod(predicate_factory(op)))


# an expression formed with a type and a value combined using an operator, e.g.
# when we access an object property or index (the exact semantics of this class
# might need some work)
class OperationType(Type):
    def __init__(self, a, b, op):
        super().__init__()
        self.a, self.b, self.op = a, b, op

    #def validate(self, x):
        #return all(
            #self.a.validate(x),

    def evaluate(self, x):
        return self.op(x, self.b)

def expr_factory(y):
    def np(self, other):
        return OperationType(self, other, getattr(operator, y))
    return np

for op in ['getitem']:
    setattr(Type, f'__{op}__', expr_factory(op))
    #setattr(Type, f'__{op}__', staticmethod(expr_factory(op)))


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

class ArgumentError(ValueError):
    pass

# A generic metaclass
class Class:
    def __init__(self, *attrs):
        attrs = list(attrs)
        for i in range(len(attrs)):
            match attrs[i]:
                case name, T:
                    attrs[i] = Box({'name': name, 'type': T})
                    print(f'Warning: Field "{attrs[i].name}" does not have an associated info parameter; it is recommended that all fields in a class include a short description of how they are used and/or created')
                case name, info, T: attrs[i] = Box({'name': name, 'info': info, 'type': T})

        if isinstance(attrs[0], str):
            self.name = attrs[0]
            self.info = textwrap.dedent(attrs[1])
            self.attrs = attrs[2:]
        else: self.attrs = attrs

        # this is the actual class that is instantiated when we want to
        # construct a member of this abstract (outer) class; it is not strictly
        # necessary to define an actual class but it makes it more clear what
        # is going on
        class Z:
            def __init__(inner, *args, **kwargs):
                # if we wanted, we could perform these checks in the outer
                # class' __call__/new method; as far as I can tell, there's no
                # significant functional difference
                if len(args) != len(self.attrs):
                    raise ArgumentError(textwrap.dedent(f"""
                            Incorrect number of arguments;
                            expected ({", ".join(map(str, (a.type for a in self.attrs)))})
                            but received ({", ".join(map(str, args))})
                        """).replace('\n', ' '))
        self.cls = Z

    def validate(self, x): pass

    def new(self, *args, **kwargs):
        return self.cls(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        self.new(*args, **kwargs)

    def __str__(self):
        nl = '\n'
        return f'[class] {self.name} ({nl.join(map(str, self.attrs))})'

Animal = Class(
    "Animal", "A simple animal class.",
    #('name', String != '', (String[0] in string.ascii_uppercase).rec()),
    ('name', String != ''),
    ('species', String != ''),
    ('weight?', (Float | Int) > 0)
)
x = Animal('Jerry', 'wolf', 50.0)



File = Class(
    "File", "A class for representing an entry in a filesystem; includes some basic\
    metadata.",

    ('name', "The file's name, including its extension(s)", String != ''),
    ('base', "A file name, excluding any file extensions", String != ''),
    ('path', "A relative or absolute path to a file", String != ''),
    (('extension', 'ext'), "The file extension, not including the leading period", String),
    ('size', 'The size of the file in bytes', Int >= 0),
    ('time', Tuple(
            ('created', datetime),
            ('modified', datetime),
            ('accessed', datetime)
        )),

    #(File.name in File.path)
)
#f = File()

def demo():
    #print(File.doc('markdown'))
    print(File.doc('text'))

demo()
