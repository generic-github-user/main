import numpy as np
import matplotlib.pyplot as plt
import string
import random


layout = """
1234567890
qwertyuiop[]\\
asdfghjkl;'
zxcvbnm,./
???? ?
"""
layout = list(filter(None, layout.splitlines()))
max_len = len(max(layout, key=len))
layout = [l+('?'*(max_len-len(l))) for l in layout]
layout = list(map(list, layout))
layout = np.array(layout, dtype=str)
print(layout)

test_strings = [
    'thanatopsis',
    'alaska',
    'supercalifragilisticexpialidocious',
    'abacus',
    'philosophy of language',
    'aaaaaaaaaaaaa',
    '123456789',
    '7562855701275165783632875',
    'iuhfunwofinwguibogybnaon'
]

def score(text, pointers=5, groups=1, positioning='random', stretch_penalty=0.5, log=False):
    if log:
        print(text)

    if positioning == 'random':
        pos = np.random.randint([0, 0], np.array(layout.shape), (pointers, 2))
    elif positioning == 'nearest':
        pos = np.random.randint([0, 0], np.array(layout.shape), (pointers, 2))
        pos[0] = np.array(np.where(layout == text[0])).reshape((2,))
    elif positioning == 'heuristic':
        pos = None

    if log:
        print(text[0], pos)
    cost = 0
    for c in text[1:]:
        new = pos.copy()
        key = np.array(np.where(layout == c)).reshape((2,))
        if positioning == 'random':
            index = np.random.randint(0, pointers)
        elif positioning == 'nearest':
            index = np.argmin(np.linalg.norm(new - key, axis=0))

        new[index] = key
        cost += np.sum(np.linalg.norm(pos - new, axis=0))
        stretch_cost = np.linalg.norm(new[...,None] - new.T[None,...])
        cost += stretch_cost * stretch_penalty
        pos = new
        # print(c, pos)
    return cost

scores = {}
for s in test_strings:
    val = score(s, positioning='nearest')
    scores[s] = val
    print(val)

def sample_random(n=None, string_list=None, l=10, **kwargs):
    if string_list is None:
        strings = []
    else:
        strings = string_list
        if not n:
            n = len(strings)
    values = []
    for i in range(n):
        if string_list is None:
            s = ''.join(random.choices(string.ascii_lowercase+string.digits, k=l))
            strings.append(s)
        else:
            s = strings[i]
        values.append(score(s, **kwargs))
    return strings, values


plt.style.use('seaborn')
# plt.hist(scores.values(), bins=20)
s, v = sample_random(500, l=10)
bins = np.linspace(0, 200, 100)
for method in ['random', 'nearest']:
    s2, v2 = sample_random(500, string_list=s, positioning=method, stretch_penalty=0.2)
    plt.hist(v2, bins=bins, alpha=0.5, label=method)
plt.legend()
plt.show()
