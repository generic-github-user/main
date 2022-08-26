import string
import operator
from datetime import datetime
import textwrap
from box import Box

import typing
import inspect

import os
from pathlib import Path

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
            (self.this.evaluate(x) if isinstance(self.this, OperationType)
                else self.this.validate(x)),
            self.p(x, other)
        )

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

class ArgumentError(ValueError):
    pass

""" An (abstract) class attribute, wrapping a name and a type (and possibly
documentation). This is essentially a data class with a couple methods for
generating documentation artifacts. """
class Attribute:
    def __init__(self, name, T, info=None, aliases=None):
        self.name = name
        self.T = T
        self.info = info
        self.aliases = aliases

    def __str__(self):
        return f'{self.name}: {self.T}'

    def doc(self, fmt):
        match fmt:
            case 'markdown':
                return f'**{self.name}**: *{self.T}* - {self.info or "attribute is not yet documented"}'

"""
An alternate class for `Attribute` meant to be used in decorator-style `Class`
initializations, where we specify attribute names and types Pythonically and
bind additional metadata by setting the value of a class attribute to an
instance of this class.
"""
class Attr(Attribute):
    def __init__(self, info):
        super().__init__(None, None, info)

class Function(Type):
    def __init__(self, name, input_types, output_type, info=None):
        super().__init__()
        self.input_types = input_types
        self.output_type = output_type
        self.name = name
        self.info = info

    def __str__(self): raise NotImplementedError

# A generic metaclass

"""
An enhanced Python class that stores complex type information about its
attributes and methods. Supports serialization, documentation generation,
logging, runtime type checking, and more. This class wraps a dynamically
generated internal class which is the one actually instantiated. In this sense
this is a "metaclass" that describes how to build a concrete class that can be
manipulated in the usual ways. This extra abstraction (e.g., instead of simply
using a subclass) might seem superfluous, but provides some nice benefits like
a more consistent mental model of typed objects, elimination of namespace
conflicts introduced by subclassing, etc.
"""
class Class:
    """
    Construct a metaclass from a high-level description. The variable-length
    `*attrs` is used to designate the class' attributes. If the first item is a
    string, it will be used as the class name; and if the second is also a
    string, it will be used as the description of the class that appears in
    generated documentation (both are optional), and subsequent items will be
    interpreted as attribute descriptors. Alternatively, you can use the `name`
    and `info` kwargs.
    """
    def __init__(self, *attrs, **kwargs):
        if len(attrs) == 1 and inspect.isclass(attrs[0]):
            src = attrs[0]
            #print(inspect.getsourcelines(src))

            src_attrs = filter(
                lambda x: not x[0].startswith('__'),
                inspect.getmembers(src, lambda a: not inspect.isroutine(a))
            )
            type_hints = typing.get_type_hints(src)
            self.attrs = []
            #print(list(src_attrs))
            for k, v in src_attrs:
                #if v: self.attrs.append(
                #T = getattr(type_hints, k, None)
                T = type_hints[k]
                if T is None:
                    print(type_hints)
                    raise TypeError
                self.attrs.append(Attribute(k, T, v.info))

            self.name = src.__name__
            self.info = src.__doc__ or f"No description of class `{self.name}` available yet; come back soon"
            # TODO: make this a dictionary
            self.methods = []

            src_methods = filter(lambda x: not x[0].startswith('__'),
                inspect.getmembers(src, lambda a: inspect.isroutine(a)))
            for mname, m in src_methods:
                T_in = []; T_out = None;
                for k, v in typing.get_type_hints(m).items():
                    T_out = v if k == 'return' else T_in.append(v)
                self.methods.append(Function(mname, T_in, T_out, m.__doc__))

            lines, start = inspect.getsourcelines(src)
            self.source = Box(file=inspect.getfile(src), lines=(start, start+len(lines)))
        else:
            attrs = list(attrs)
            for i in range(len(attrs)):
                match attrs[i]:
                    case [name, *alias], info, T: attrs[i] = Attribute(name, T, info, alias)
                    case name, T:
                        attrs[i] = Attribute(name, T)
                        print(f'Warning: Field "{attrs[i].name}" does not have an associated info parameter; it is recommended that all fields in a class include a short description of how they are used and/or created')
                    case name, info, T: attrs[i] = Attribute(name, T, info)

            if isinstance(attrs[0], str):
                self.name = attrs[0]
                self.info = textwrap.dedent(attrs[1])
                self.attrs = attrs[2:]
            else: self.attrs = attrs
            self.methods = []

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
    def derive(self, *args, **kwargs): return self
    def insert(self, *args, **kwargs): return self

    def new(self, *args, **kwargs):
        return self.cls(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        self.new(*args, **kwargs)

    def __str__(self):
        nl = '\n'
        return f'[class] {self.name} {nl}{textwrap.indent(nl.join(map(str, self.attrs)), " "*4)}'

    """
    Generate documentation for a constructed class (i.e., metaclass instance);
    currently only supports Markdown. By default, this method lists
    fields/attributes, methods, and examples of usage, which are each
    represented by another class with its own `doc` method.

    Some possibly useful information:

    - `depth` is the initial nesting level for Markdown-like languages, in which case it is used to create headers of the proper level
    - if `python_types` is `True`, the output will use basic Python types like `str` and `int` wherever possible, instead of the wrappers `String` and `Int`
    """
    def doc(self,
            doc_format,
            depth=3,
            python_types=True,
            generate_examples=True,
            link_src=None
        ):
        output = None
        nl = '\n'
        match doc_format:
            case 'markdown':
                z = '#' * depth
                #rpath = os.path.commonpath([self.source.file, Path().resolve()])
                output = f"""
                    {z} class `{self.name}`
                    {f"[`source`](./{Path(self.source.file).resolve().relative_to(Path('.').resolve())}#L{self.source.lines[0]}-L{self.source.lines[1]})" if link_src else ""}

                    {self.info}

                    {z}# Fields

                    {nl.join(f'- {x.doc("markdown")}' for x in self.attrs)}

                    {z}# Methods

                    {(nl*2).join(f'- {m.doc("markdown")}' for m in self.methods) or "This class has no methods."}
                """
            case 'text':
                return str(self)

            case _:
                raise ValueError
        #print(output, textwrap.dedent(output))
        #return textwrap.dedent(output)
        return '\n'.join(map(str.lstrip, output.splitlines()))
Animal = Class(
    "Animal", "A simple animal class.",
    #('name', String != '', (String[0] in string.ascii_uppercase).rec()),
    ('name', String != ''),
    ('species', String != ''),
    ('weight?', (Float | Int) > 0),
    suppress_warnings=True
)
x = Animal('Jerry', 'wolf', 50.0)



File = Class(
    "File", """\
        A class for representing an entry in a filesystem; includes some basic
        metadata.""",

    ('name', "The file's name, including its extension(s)", String != ''),
    ('base', "A file name, excluding any file extensions", String != ''),
    ('path', "A relative or absolute path to a file", String != ''),
    (('extension', 'ext'), "The file extension, not including the leading period", String),
    ('size', "The size of the file in bytes", Int >= 0),
    ('time', "Time metadata, normalized to a Python datetime object", Tuple(
            ('created', datetime),
            ('modified', datetime),
            ('accessed', datetime)
        )),

    #(File.name in File.path)
)
#f = File()

def demo():
    print(File.doc('markdown'))
    print(File.doc('text'))

#demo()


#class Point

Number = Int | Float
Point = Class('Point',
        'A simple point in two-dimensional Euclidean space; \
            can also be used to represent a vector.',

        x=Number,
        y=Number,

        _attrfmt="The point's {} coordinate",
        _fmt='({}, {})',
        _examples="""
            # initialize a new point (these are all equivalent)
            a = Point(3, 4)
            a = Point(x=3, y=4)
            a = Point([3, 4])
            a = Point({x: 3, y: 4})
            a = Point.set_x(3).set_y(4)


            #print(a.norm())
            a.norm()
            b = Point(2, 1)

            # use basic arithmetic operators on points
            a - b
            a + b

            # compare points
            a == b
            a != b

            (a + b).norm()
            a >= 4

            a.to(tuple)
            xa, ya = a
            a.x == a['x'] == a[0] == a.get('x')

            # scale points via broadcasting
            b * 3
            a / 2
            b ** 4
            a / 0
            a *= 2

            # the other operand is type-checked before the error gets to the
            # interpreter level so you can intercept it however you see fit
            a -= 'eclectic'
            a.z

            # find the distance between two points
            Point.dist(a, b)
            a.dist(b)
            # rshift is overloaded to compute distance
            a >> b

            c = Point(7, -4)
            Point.min([a, b, c])
            Point.max([a, b, c])
            Point.mean([a, b, c])

            # a binary mean operation is aliased as the midpoint method
            Point.midpoint(a, c)

            Point.min([a, b, c], key='norm')
            Point.max([a, b, c], key='norm')

            Point.reduce([a, b, c], Point.dist)
            Point.sum([a, b, c])

            a.x = 8
            a.y += 3
            a

            # convert Point instances to various formats
            b.to_dict()
            b.to_json()
            b.to_yaml()
            b.to_string()
            b.to_namedtuple()

            # create a new point by converting the datatype that Point wraps
            # (in this case, we start with `Number`s so existing `float`s
            # remain the same while `int`s are typecasted)
            a.cast(Float)
            Point.cast(a, Float)

            b2 = b.clone()
            b.y += 8
            print(b, b2)

            Point.doc('markdown')
            Point.doc('text')
            Point.doc('html')
        """,
        _tests="""
            Point(3, 4).norm() == 5
            Point(4, 5) + Point(6, 7) == Point(10, 12)
        """
    )\
    .derive('__add__', '__sub__', '__eq__', '__ne__', '__neg__', 'max', 'min')\
    .insert(
        norm=lambda x, y: math.sqrt(x**2 + y**2),
        dist=lambda a, b: (a - b).norm(),
        transpose=lambda x, y: Point(y, x)
    )

@Class
class Rect:
    """
    A simple rectangle class, implemented using the `Point` class.
    """

    pos: Point = Attr("""Location of the lower-left corner of the rectangle
                      (assume 2D Euclidean space)""")
    delta: Point = Attr("""Positive (Q1) point representing the difference
    between opposite corners of the rectangle (including `pos`)""")

    def area(self) -> Number:
        """Returns the rectangle's area"""
        return self.delta.x * self.delta.y

    def perimeter(self) -> Number:
        """Returns the perimeter ("edge length") of the rectangle"""
        return (2 * self.delta.x) + (2 * self.delta.y)

    def scale(self, x: Number >= 0):
        """Scales this rectangle by the given factor (`x`) and returns a new
        `Rect`"""
        return Rect(pos, delta * x)
    
#print(Rect.doc('markdown'))
#print(Rect.doc('text'))

@Class
class Contact:
    """
    A class representing a simple list of contact information for a person.
    """

    name: String != '' = Attr("The contact's name, most likely in [First] [Last] format")
    email: Option[String] = Attr("The contact's email address; may be `None`-like")
    phone: Option[String] = Attr("The contact's phone number; may be `None`-like")
    address: Option[String] = Attr("The contact's physical address; may be `None`-like")

dtest = Contact.doc('markdown', link_src=True)
print(dtest)
with open('contact.md', 'w+') as f: f.write(dtest)
#print(Contact.doc('text'))

