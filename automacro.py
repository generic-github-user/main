#!/usr/bin/env python
# coding: utf-8

# In[57]:


import itertools

examples = [
#     ['United States', 'US'],
#     ['Continuous Integration', 'CI'],
#     ['artificial intelligence', 'AI'],
#     ['Machine  learning', 'ML']
    ['First Last', 'Last, First'],
#     ['First Middle Last', 'Last, First Middle'],
]
manipulations = [
    [lambda x: x[0], 'First char'],
    [lambda x: x[::-1], 'Reverse', True],
    [str.lower, 'Lowercase'],
    [str.upper, 'Capitalize'],
    [str.split, 'Split'],
    [lambda x: ', '.join(x), '', True]
]
M = [m[0] for m in manipulations]
options = []
max_ops = 3
print(f'Testing {max_ops**len(manipulations)} operations across {len(examples)} examples')
checked = 0
for n in range(max_ops):
    print((n+1)**len(manipulations))
    for i in itertools.product(manipulations, repeat=n+1):
    #     sequence = []
        for ex in examples:
    #         print('Testing sample {} -> {}'.format(*ex))
            S = ex[0]
            for j in i:
#                 print(S, len(j))
                f = j[0]
                if type(S) is str:
                    S = f(S)
                elif type(S) in [list, tuple]:
                    if len(j) < 3:
                        S = list(map(f, S))
                    elif j[-1] == True:
                        S = f(S)
                        
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
        checked += 1
    
print(f'Checked {checked} combinations and found {len(options)} matches')
print(options)
# TODO: add heuristics (e.g., scoring intermediate results based on desirable properties of the generated string)


# In[111]:


manipulations[8][0](list('test'))


# In[ ]:




