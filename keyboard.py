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
    if positioning == 'random':
        pos = np.random.randint([0, 0], np.array(layout.shape), (pointers, 2))
    cost = 0
    for c in text[1:]:
        new = pos.copy()
        key = np.array(np.where(layout == c)).reshape((2,))
        if positioning == 'random':
            index = np.random.randint(0, pointers)
        new[index] = key
        cost += np.sum(np.linalg.norm(pos - new, axis=0))
        stretch_cost = np.linalg.norm(new[...,None] - new.T[None,...])
        cost += stretch_cost * stretch_penalty
        pos = new
    return cost
