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
