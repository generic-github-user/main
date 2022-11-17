from lib.pystring import String


class Number:
    def __init__(self, x):
        if isinstance(x, Number):
            x = x.x
        self.x = x

    # to_string = str
    def to_string(self):
        return String(str(self.x))

    def print(self):
        print(self.to_string() + '\n')

    def __str__(self):
        return str(self.x)

    __repr__ = __str__


def generate_method(inner, wrap=False):
    def method(self, *args, **kwargs):
        # args = map(Number.__init__, args)
        args = map(Number, [self]+list(args))
        result = inner(*(map(lambda N: N.x, args)),
                       **kwargs)
        # breakpoint()
        if wrap:
            # result = Number(wrap)
            result = Number(result)
        return result
    return method


for m in ['add', 'sub', 'mul', 'floordiv', 'pow']:
    method_name = f'__{m}__'
    setattr(Number, method_name,
            generate_method(getattr(int, method_name), wrap=True))
for m in ['lt', 'gt', 'le', 'ge']:
    method_name = f'__{m}__'
    setattr(Number, method_name,
            generate_method(getattr(int, method_name), wrap=False))
