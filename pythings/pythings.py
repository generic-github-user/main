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
            hide_empty=True,
            generate_examples=True):
        if astype: return self.name

        output = None
        nl = '\n'
        match doc_format:
            case 'markdown':
                z = '#' * depth
                methods = f"""
                    {z}# Methods

                    {(nl*2).join(f'- {m.doc("markdown", depth=depth+1)}' for m in self.methods) or "This class has no methods."}
                """
                if hide_empty and not self.methods: methods = ''

                output = f"""
                    {z} class `{self.name}`

                    {self.info.strip()}

                    {z}# Fields

                    {nl.join(f'- {x.doc("markdown")}' for x in self.attrs)}

                    {methods}
                """
            case 'text':
                return str(self)

            case _:
                raise ValueError
        #print(output, textwrap.dedent(output))
        #return textwrap.dedent(output)
        return '\n'.join(map(str.lstrip, output.splitlines()))
