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


def predicate_factory(y):
    def np(self, other):
        return RefinementType(self, getattr(operator, y), other)
    return np

for op in ['eq', 'ne', 'gt', 'ge', 'lt', 'le']:
    setattr(Type, f'__{op}__', predicate_factory(op))
    #setattr(Type, f'__{op}__', staticmethod(predicate_factory(op)))


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

# A generic metaclass
class Class:
    def __init__(self, *attrs, **kwargs):
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

        class Z:
            def __init__(inner, *args, **kwargs):
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
        return f'[class] {self.name} {nl}{textwrap.indent(nl.join(map(str, self.attrs)), " "*4)}'

    def doc(self,
            doc_format,
            depth=3,
            python_types=True,
            generate_examples=True):
        output = None
        nl = '\n'
        match doc_format:
            case 'markdown':
                z = '#' * depth
                output = f"""
                    {z} class `{self.name}`

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
    ('weight?', (Float | Int) > 0)
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
    print(File.doc('markdown'))
    print(File.doc('text'))

demo()
