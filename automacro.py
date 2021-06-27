#!/usr/bin/env python
# coding: utf-8

# In[56]:


import itertools

examples = [
    ['United States', 'US'],
    ['Continuous Integration', 'CI'],
    ['artificial intelligence', 'AI'],
    ['Machine learning', 'ML']
]
manipulations = [
    [lambda x: x[0], 'First char'],
    [lambda x: x[::-1], 'Reverse'],
    [str.lower, 'Lowercase'],
    [str.upper, 'Capitalize'],
    [str.split, 'Split'],
    [lambda x: ''.join(x), 'Join'],
]
M = [m[0] for m in manipulations]
options = []
max_ops = 3
print(f'Testing {max_ops**len(manipulations)} operations across {len(examples)} examples')
for n in range(max_ops):
    for i in itertools.product(M, repeat=n+1):
    #     sequence = []
        for ex in examples:
    #         print('Testing sample {} -> {}'.format(*ex))
            S = ex[0]
            for j in i:
                if type(S) is str:
                    S = j(S)
                elif type(S) in [list, tuple]:
                    S = list(map(j, S))
                    if type(S[0]) is list:
                        S = list(itertools.chain(*S))
                else:
                    print(type(S))

            if type(S) is list:
                S = ''.join(S)
            if S != ex[1]:
    #             print(S)
                break
        else:
            print(S, True)
            options.append(i)
    
    
print(options)

