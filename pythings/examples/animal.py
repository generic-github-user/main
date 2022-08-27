
Animal = Class(
    "Animal", "A simple animal class.",
    #('name', String != '', (String[0] in string.ascii_uppercase).rec()),
    ('name', String != ''),
    ('species', String != ''),
    ('weight?', (Float | Int) > 0),
    suppress_warnings=True
)
x = Animal('Jerry', 'wolf', 50.0)
