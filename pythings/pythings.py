import string
import operator
from datetime import datetime
import textwrap
from box import Box

import typing
import inspect

from ptypes import *

def predicate_factory(y):
    def np(self, other):
        return RefinementType(self, getattr(operator, y), other)
    return np

# bind predicate-generating operators (for refinement types); if n is an int, T
# > n is essentially shorthand for x: T, x > n
for op in ['eq', 'ne', 'gt', 'ge', 'lt', 'le']:
    setattr(Type, f'__{op}__', predicate_factory(op))
    #setattr(Type, f'__{op}__', staticmethod(predicate_factory(op)))



def expr_factory(y):
    def np(self, other):
        return OperationType(self, other, getattr(operator, y))
    return np

for op in ['getitem']:
    setattr(Type, f'__{op}__', expr_factory(op))
    #setattr(Type, f'__{op}__', staticmethod(expr_factory(op)))



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
        """
        Generates documentation for this attribute in the specified `fmt` (see
        `Class.doc` for more detailed information on this method). Note also
        that this is an internal method that will generally not need to be used
        outside of the module.
        """

        match fmt:
            case 'markdown':
                return f'**{self.name}**: *{self.T.doc("markdown", astype=True)}* - {self.info or "attribute is not yet documented"}'

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

    def doc(self, fmt, depth=0):
        """
        Generates documentation for this function in the specified `fmt` (see
        `Class.doc` for more detailed information on this method). Note also
        that this is an internal method that will generally not need to be used
        outside of the module.
        """

        match fmt:
            case 'markdown':
                lead = '#'*depth
                output = f"""
                    {lead} fn `{self.name}` ({', '.join(self.input_types)}) -> {self.output_type}

                    {self.info}

                    {lead}# Arguments
                """
            case _: raise ValueError

        return output

    def __str__(self): raise NotImplementedError

# A generic metaclass

"""
An enhanced Python class that stores complex type information about its
attributes and methods. Supports serialization, documentation generation,
logging, runtime type checking, and more. This class wraps a dynamically
generated internal class which is the one actually instantiated. In this sense
this is a "metaclass" that describes how to build a concrete class that can be
manipulated in the usual ways.

This extra abstraction (e.g., instead of simply using a subclass) might seem
superfluous, but provides some nice benefits like a more consistent mental
model of typed objects, elimination of namespace conflicts introduced by
subclassing, etc. There is a more detailed discussion of practical applications
of metaclasses
[here](https://stackoverflow.com/questions/392160/what-are-some-concrete-use-cases-for-metaclasses).
"""
class Class:
    tq = '"""'
    f"""
    Construct a metaclass from a high-level description. The variable-length
    `*attrs` is used to designate the class' attributes. If the first item is a
    string, it will be used as the class name; and if the second is also a
    string, it will be used as the description of the class that appears in
    generated documentation (both are optional), and subsequent items will be
    interpreted as attribute descriptors. Alternatively, you can use the `name`
    and `info` kwargs.

    `Class` can also be used as a
    [decorator](https://book.pythontips.com/en/latest/decorators.html), in
    which case the `inspect` and `typing` modules are used to extract
    information about the class' attributes and methods. This is a fairly
    natural way to declare a class while integrating `pythings`; as shown in
    the example below, the main difference is that attributes are declared with
    the `Attr` class since Python does not natively support attribute-level
    docstrings.

    ```py
    @Class
    class Point:
        {tq}A simple point in two-dimensional Euclidean space; can also be used to
        represent a vector.{tq}

        x: Number = Attr("x-coordinate of point")
        y: Number = Attr("y-coordinate of point")
    ```
    """
    def __init__(self, *attrs, **kwargs):
        # This branch is followed when `Class` is used as a decorator (via
        # "@Class...")
        if len(attrs) == 1 and inspect.isclass(attrs[0]):
            src = attrs[0]

            # Find class attributes and store information about them in the
            # metaclass
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
                # TODO: allow eliding type hints
                # TODO: permit type inference?
                if T is None:
                    print(type_hints)
                    raise TypeError
                self.attrs.append(Attribute(k, T, v.info))

            # Get class metadata from actual definition
            self.name = src.__name__
            self.info = src.__doc__ or f"No description of class `{self.name}` available yet; come back soon"

            # Extract methods from source class (`src`)
            # TODO: make this a dictionary
            self.methods = []

            # Get user-defined methods
            src_methods = filter(lambda x: not x[0].startswith('__'),
                inspect.getmembers(src, lambda a: inspect.isroutine(a)))
            for mname, m in src_methods:
                # Split type annotations into the return type and input types
                # (i.e., all others)
                T_in = []; T_out = None;
                for k, v in typing.get_type_hints(m).items():
                    T_out = v if k == 'return' else T_in.append(v)

                self.methods.append(Function(mname, T_in, T_out, m.__doc__))
        else:
            # needed because `attrs` is initially a tuple (immutable)
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
            # TODO: add conversion to/from list

            # naturally, this initializer is eventually called
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
        """
        Constructs a simple string representation of the class itself with
        attributes and methods each listed on one (indented) line. Potentially
        useful for debugging.
        """

        nl = '\n'
        return f'[class] {self.name} {nl}{textwrap.indent(nl.join(map(str, self.attrs)), " "*4)}'

    """
    Generate documentation for a constructed class (i.e., metaclass instance);
    currently only supports Markdown. By default, this method lists
    fields/attributes, methods, and examples of usage, which are each
    represented by another class with its own `doc` method.

    Some possibly useful information:

    - `depth` is the initial nesting level for Markdown-like languages, in
      which case it is used to create headers of the proper level
    - if `python_types` is `True`, the output will use basic Python types like
      `str` and `int` wherever possible, instead of the wrappers `String` and
      `Int`
    - if `astype` is `True`, a short representation (usually the class' name)
      will be returned instead of the class' full documentation; useful for
      type hinting
    """
    def doc(self,
            doc_format,
            depth=3,
            astype=False,
            python_types=True,
            generate_examples=True):
        if astype: return self.name

        output = None
        nl = '\n'
        match doc_format:
            case 'markdown':
                z = '#' * depth
                output = f"""
                    {z} class `{self.name}`

                    {self.info.strip()}

                    {z}# Fields

                    {nl.join(f'- {x.doc("markdown")}' for x in self.attrs)}

                    {z}# Methods

                    {(nl*2).join(f'{m.doc("markdown", depth=depth+1)}' for m in self.methods) or "This class has no methods."}
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

demo()


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

    pos: Point = Attr('Location of the lower-left corner of the rectangle (assume 2D Euclidean space)')
    delta: Point = Attr('Positive (Q1) point representing the difference between opposite corners of the rectangle (including `pos`)')

    def area(self) -> Number: return self.delta.x * self.delta.y
    area.__doc__ = """Returns the rectangle's area"""

    def perimeter(self) -> Number: return (2 * self.delta.x) + (2 * self.delta.y)
    def scale(self, x) -> Number: return Rect(pos, delta * x)
    
print(Rect.doc('markdown'))
print(Rect.doc('text'))

@Class
class Contact:
    """
    A class representing a simple list of contact information for a person.
    """

    name: String != '' = Attr("The contact's name, most likely in [First] [Last] format")
    email: Option[String] = Attr("The contact's email address; may be `None`-like")
    phone: Option[String] = Attr("The contact's phone number; may be `None`-like")
    address: Option[String] = Attr("The contact's physical address; may be `None`-like")

#print(Contact.doc('markdown'))
#print(Contact.doc('text'))
