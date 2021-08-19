import numpy as np
import matplotlib.pyplot as plt
import string
import random


layout = """
~!@#$%^&*()_+
`1234567890-=
QWERTYUIOP{}|
qwertyuiop[]\\
ASDFGHJKL:"
asdfghjkl;'
ZXCVBNM<>?
zxcvbnm,./
???? ?
"""
layout = list(filter(None, layout.splitlines()))
max_len = len(max(layout, key=len))
layout = [l+('?'*(max_len-len(l))) for l in layout]
layout = list(map(list, layout))
layout = np.array(layout, dtype=str).reshape([9, max_len])
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
    'iuhfunwofinwguibogybnaon',
    'effervescent',
    'antidisestablishmentarianism',
    'was',
    '1010101010101010',
    'alkaline',
    'polonium',
    'polonius',
    'articulation',
    'ancillary',
    'auxiliary',
    'billions',
    'quintillions',
    'minimum',
    'infinite'
]

def transition_cost(pos1, pos2, index, stretch_mode, stretch_penalty, stretch_order, groups):
    new = pos1.copy()
    step_cost = 0
    new[index] = pos2
    # Get distance between old position and new position
    step_cost += np.sum(np.linalg.norm(pos1 - new, axis=0))
    # Calculate the cost associated with the distance between pointers (i.e., the distance fingers would need to stretch to reach certain keys)
    # TODO: add other stretch modes, limits
    if stretch_mode == 'mean':
        if groups:
            # TODO: move this outside of loop
            assert isinstance(groups, int)
            chunks = np.split(new, groups, axis=0)

            stretch_cost = 0
            for c in chunks:
                midpoint = np.mean(c, axis=0)
                stretch_cost += np.sum(np.linalg.norm(new - midpoint, ord=2))
        else:
            stretch_cost = np.sum(np.linalg.norm(new - np.mean(new, axis=0), ord=2))
    elif stretch_mode == 'all':
        stretch_cost = np.linalg.norm(new[..., None] - new.T[None, ...])
        # stretch_cost = np.linalg.norm(new[...,None] - new.T[None,...], axis=(0, 1), ord=2)
        # stretch_cost = np.sum(stretch_cost)
    step_cost += ((stretch_cost ** stretch_order) * stretch_penalty)
    return step_cost, new
    if log:
        print(text)
    if seed is not None:
        assert isinstance(seed, int)
        random.seed(seed)
        np.random.seed(seed)

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

def random_string(l=10):
    return ''.join(random.choices(string.ascii_lowercase+string.digits, k=l))

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
            s = random_string(l=l)
            strings.append(s)
        else:
            s = strings[i]
        values.append(score(s, **kwargs))
    return strings, values


defaults = dict(seed=42)
plt.style.use('seaborn')
# plt.hist(scores.values(), bins=20)
s, v = sample_random(500, l=10)
bins = np.linspace(0, 200, 100)
for method in ['random', 'nearest']:
    s2, v2 = sample_random(500, string_list=s, positioning=method, stretch_penalty=0.2, **defaults)
    plt.hist(v2, bins=bins, alpha=0.5, label=method)
plt.legend()
plt.show()

s, v = sample_random(string_list=test_strings, l=10, **defaults)
s2, v2 = sample_random(string_list=s, positioning='nearest', **defaults)
s, v, v2 = zip(*sorted(zip(s, v, v2), key=lambda x: x[1]))

# plt.bar(s, list(zip(v, v2)))

# Base code for grouped bar chart from https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html
x = np.arange(len(s))
width = 0.35

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, v, width, label='Random')
rects2 = ax.bar(x + width/2, v2, width, label='Nearest')

ax.set_ylabel('Scores')
ax.set_title('Typing Cost Values by Method')
ax.set_xticks(x)
ax.set_xticklabels(s)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.xticks(rotation='vertical')
plt.show()

points = []
methods = ['random', 'nearest']
for i in range(500):
    A = np.random.randint(5, 100)
    B = random.choice(methods)
    s = random_string(l=A)
    score_value = score(s, positioning=B)
    P = [A, score_value, methods.index(B)]
    points.append(P)
points = np.array(points)
args = points.T[:2]
kwargs = dict(c=points.T[2], cmap='rainbow', s=5)
plt.scatter(*args, **kwargs)
plt.show()
