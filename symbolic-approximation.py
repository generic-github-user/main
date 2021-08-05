#!/usr/bin/env python
# coding: utf-8

# In[989]:


import numpy as np
import operator
import random
from IPython.display import Latex, Math
import IPython.display as display
import math
import matplotlib.pyplot as plt


# In[624]:


# Math()


# In[2]:


X = np.arange(10)
Y = np.random.randint(0, 20, 10)


# In[3935]:


# string rewriting?
expressions = [
    [['$'], ['F'], 1],
#     [['$'], ['E']],
#     [['F'], [[lambda: random.choice(functions[:3])[0], ['E', 'E']]]],
#     [['F'], [[lambda: random.choice(functions[3:])[0], ['E']]]],
    [['F'], [['O2', ['E', 'E']]], 3],
    [['F'], [['O1', ['E']]]],
    [['O2'], ['+']],
    [['O2'], ['-']],
    [['O2'], ['*']],
    [['O2'], ['/']],
    [['O2'], ['^'], 3],
    [['O2'], ['frac']],
    [['O1'], ['sqrt']],
    [['O1'], ['abs']],
    [['O1'], ['trig'], 1],
    [['O1'], ['fact']],
    [['E'], ['V']], #C
#     Grammar example; polynomial generation
#     [['V'], ['P']],
#     [['exp'], [['^', ['x', 'int']]]],
#     [['P'], [['+', ['term', 'term']]]],
#     [['term'], [['*', ['int', 'exp']]]],
    
#     [['E'], ['F']],
    [['V'], ['F'], 20],
    [['V'], ['x']],
    [['V'], ['y']],
    [['V'], ['int']],
#     [['O'], [lambda: random.choice(filter(lambda a: a[3]symbols['O']))[0]]],
#     [['V'], [lambda: random.choice(symbols['V'])()]],
    [['int'], [lambda: np.random.randint(-5, 5)], 2],
#     identity/input
#     [['$'], ['I']],
]
functions = [
    ['+', operator.add, '+', 2],
    ['-', operator.sub, '-', 2],
    ['*', operator.mul, '\cdot', 2],
    ['/', operator.truediv, '\div', 2],
    ['^', lambda a, b: (a ** b), '^', 2],
    ['frac', operator.truediv, r'\frac', 2],
    ['sqrt', lambda a: (a ** (1/2)), '\sqrt', 1],
    ['abs', abs, '|$|', 1],
    ['fact', math.factorial, '$!', 1],
#     ['sqrt', lambda a: math.factorial(a), '', 1]
]
trig_funcs = 'sin cos tan csc sec cot'.split()
for t in trig_funcs:
    functions.append([t, lambda a: math.sin(a), f'\\{t}'])
    expressions.append([['trig'], [t], 1])
values = [
    ['constant', [lambda: np.random.randint(-5, 5)]]
]
symbols = {
    'O': functions,
    'V': values
}

expressions = [(e+[1] if len(e)==2 else e) for e in expressions]
expressions = [[a[0], b, c] for a, b, c in expressions]


# In[ ]:


# for s in symbols
# hierarchical regular expressions?
def generate(exp=None, level=1, iterations=10, max_levels=10, limit_complexity=True):
    if exp is None:
        exp = ['$']
#     elif isinstance(exp, str):
#         exp = [exp]
#     if level == 1:
#     exp = [e if isinstance(e, list) else [e] for e in exp]
#     print(exp)
    matches = None
    if level > (0.75 * max_levels) and limit_complexity:
#         'E Q'.split()
        exp = ['V' if e in ['E'] else e for e in exp]
    for i in range(iterations):
        for e in expressions:
            e_ = e[0]
#             j, k = e
#             print(e_, exp)
            if e[0] in exp:
                ie = exp.index(e_)
#                 print(len(exp), ie)
                matches = list(filter(lambda a: a[0]==e[0], expressions))
#                 matches = list(filter(lambda a: (a[0] in exp or a[0][0] in exp), expressions))
                if level > (0.75 * max_levels) and limit_complexity:
                    matches = list(filter(lambda z: not z[1] in [['F']], matches))
#                 print(matches, e[0], exp)
                if matches:
#                     [print(m) for m in matches]
#                     print(exp)
                    
#                     sub = random.choice(matches)[1]
                    sub = random.choices(matches, weights=[v[2] for v in matches], k=1)[0][1]
                    sub = [s() if callable(s) else s for s in sub]
                    exp = exp[:ie] + sub + exp[ie+1:]
            #     refactor?
#     print(exp)
                if level <= max_levels and matches:
#                         exp = [eg for eg in generate(exp=e, level=level+1) for e in exp]
                        exp = [generate(exp=e, level=level+1) if isinstance(e, (list, tuple)) else e for e in exp]
#                     exp = [generate(exp=e, level=level+1) for e in exp]
    return exp
# for i in range(5):
#     print(generate())

def to_latex(exp):
#     type(exp)[0]
    if isinstance(exp, (list, tuple)):
#         print(exp)
#         ['sqrt', 'frac', 'sin', 'cos', 'tan']
        if (type(exp[0]) is str) and exp[0] in list('+-*/^')+['sqrt', 'frac', 'abs', 'fact']+trig_funcs:
            op, ins = exp
#             template
            op_tex = list(filter(lambda q: q[0]==op, functions))[0][2]
            if len(ins) == 2:
                if exp[0] in ['frac']:
                    result = fr'{op_tex}'+''.join(f'{{{to_latex(w)}}}' for w in ins)
                else:
                    result = fr'\left( {{{to_latex(ins[0])}}} {op_tex} {{{to_latex(ins[1])}}} \right)'
            elif len(ins) == 1:
                if '$' in op_tex:
                    result = op_tex.replace('$', '{}').format(to_latex(ins[0]))
                else:
                    result = fr'{op_tex}{{{to_latex(ins[0])}}}'
            else:
                print(ins)
        else:
            parts = [to_latex(e) if isinstance(e, (list, tuple)) else e for e in exp]
            result = ''.join(map(str, parts))
    elif isinstance(exp, (str, int)):
        result = exp
    else:
        print(exp)
    return result



for i in range(1):
    g = generate(
        iterations=5,
        max_levels=100,
        limit_complexity=True,
    )
#     print(g)
    L = to_latex(g)
    size = '\small'
    size = '\Large'
    print(L)
#     Math()
    S = fr'${size} f(x)={L}$'
    display.display_latex(S, raw=True)
# make graph (network)

try:
    plot_symbolic(
        g,
        B=1000,
#         use_complex=True,
        reducefunc=np.abs
    )
# np.angle
except Exception as E:
#     pass
    print(E)
# function interpolations
# simplification graph *
# add calculus functions
# self-referencing function?


# In[3846]:


# plt.get_current_fig_manager().set_size_inches((6, 6))
plt.gcf().set_size_inches((6, 6))
plot_symbolic(g, n=100, B=10, use_complex=True)
# plt.savefig('./angels.png', format='png')
# todo: add iterated functions
# parametrizer


# In[3215]:


expressions


# In[2911]:


def plot_symbolic(G, n=50, B=10, reducefunc=np.angle, plt_args={}, **kwargs):
    # xs, ys
    # grid = np.mgrid[-10:10,-10:10]
    grid = np.stack(np.meshgrid(*[np.linspace(-B, B, num=n)]*2))
    grid = grid.T
    # vals = np.vectorize(lambda f1, f2)
    roworder = 'A'
    vals = np.reshape(
        [reducefunc(evaluate(G, [x, y], **kwargs)) for x, y in grid.reshape((n**2, 2), order=roworder)],
        (n, n),
        order=roworder
    )
    plt_defaults = dict(cmap='rainbow')
    plt.imshow(vals.T, **(plt_defaults|plt_args))
    plt.grid(False)
    plt.axis('off')


# In[2900]:


evaluate(g, complex(5, 3))

# math.cos(5+3j)


# In[2906]:


# plt.imsave()


# In[2908]:


# plt.gcf()
plt.show()


# In[1185]:


# \csc{\left( {\sqrt{\left( {\left( {x} - {x} \right)} + {\sqrt{x}} \right)}} + {-3} \right)}
# \left( {\sec{\cos{\cot{y}}}} - {\tan{\sec{\left( {y} \cdot {x} \right)}}} \right)
# \left( {\left( {\sqrt{\left( {x} ^ {-4} \right)}} ^ {\sqrt{\sqrt{x}}} \right)} \div {\sqrt{\sqrt{\left( {x} \cdot {x} \right)}}} \right)
# \left( {\sqrt{\sqrt{\frac{x}{x}}}} \div {\sqrt{\sqrt{\left( {3} \div {3} \right)}}} \right)
# ?
# \sqrt{\left( {\left( {\sqrt{x}} - {\sqrt{3}} \right)} \div {\left( {\left( {-3} - {x} \right)} ^ {\frac{2}{x}} \right)} \right)}
# \left( {\sqrt{\left( {\sqrt{x}} \div {-2} \right)}} ^ {\left( {\left( {\left( {x} + {-4} \right)} + {\left( {x} \cdot {x} \right)} \right)} + {\left( {x} \cdot {\left( {x} + {x} \right)} \right)} \right)} \right)

# \left( {\left( {3} + {x} \right)} ^ {\left( {\left( {-2} ^ {\frac{-5}{x}} \right)} ^ {\left( {\left( {4} + {1} \right)} \cdot {\sqrt{-2}} \right)} \right)} \right)
# \left( {\left( {\frac{|x|}{|-5|}} - {\sqrt{|-2|}} \right)} ^ {x} \right)
# \left( {\left( {\left( {\left( {x} ^ {x} \right)} ^ {|4|} \right)} \cdot {4} \right)} ^ {\sqrt{\sqrt{\left( {x} ^ {-5} \right)}}} \right)
# \left( {\left( {\sqrt{\sqrt{y}}} \cdot {\left( {\frac{y}{x}} - {x!} \right)} \right)} ^ {\left( {|\left( {y} + {y} \right)|} - {\left( {\frac{x}{-4}} ^ {|x|} \right)} \right)} \right)
# \left( {\left( {\left( {\left( {y} \div {-5} \right)} ^ {x} \right)} ^ {\left( {\left( {x} \div {1} \right)} + {\left( {y} ^ {-1} \right)} \right)} \right)} ^ {\frac{\left( {y} ^ {\left( {4} + {y} \right)} \right)}{x}} \right)


# In[ ]:


def safe_op(k, l):
    try:
        val = k(*l)
        if val > 10e30:
            val = 10e3
        return val
    except:
        return 0


# In[3508]:


def evaluate(exp, x, use_complex=False):
    if isinstance(x, (int, float, complex)):
        x = [x]
    default = [1] * 2
    default[:len(x)] = x
    x = default
    for i, c in enumerate('xy'[:len(x)]):
        exp = [(x[i] if e==c else e) for e in exp]
    if use_complex:
        assert len(x) == 2
        x = complex(*x)
#     print(x)
    if isinstance(exp, (list, tuple)) and isinstance(exp[0], str):
        op = list(filter(lambda q: q[0]==exp[0], functions))[0][1]
        args = [evaluate(e, x) if isinstance(e, (list, tuple)) else e for e in exp[1]]
        for i, c in enumerate('xy'[:len(x)]):
            args = [(x[i] if e==c else e) for e in args]
#         print(args, exp)
#         print(op)
#         return op(*args)
        return safe_op(op, args)
    else:
        return evaluate(exp[0], x)
evaluate(g, [5, 7], use_complex=True)
