#!/usr/bin/env python
# coding: utf-8


# In[2]:


import numpy as np
import matplotlib.pyplot as plt
import numba as nb
import itertools
import random


# In[3]:


dimensions = 2
D = dimensions
z = 10

start = [0, 0]
choices = []

for n in range(dimensions):
    for y in [-1, 1]:
        delta = np.zeros(dimensions).astype(np.int)
        delta[n] = y
        choices.append(delta)
choices = np.stack(choices)

print(choices)


# In[188]:


steps = []
@nb.njit
def valid_moves(g, m, q, o, n):
#     filtered = list(filter(lambda c: (0<=pos+c).all() and (pos+c<z).all() and grid[tuple(pos+c)] == 0, m))
    filtered = []
    for i in m:
#         print(pos, m)
        p = q+i
#         if (0<=p).all() and (p<z).all() and g[p[0], p[1]] == 0:
        if o:
            p %= n
        if (0<=p).all():
            if (p<n).all():
                if g[p[0], p[1]] == 0:
#                     print(p, g[p[0], p[1]], (p<z).all(), z)
                    filtered.append(i)
    return filtered


# In[189]:


@nb.jit(nopython=True)
def bound(x, a, b):
    if x >= b:
        x = b-1
    elif x < a:
        x = a
    return x

@nb.njit
def clip(x, a, b):
    for i in range(x.shape[0]):
        x[i] = bound(x[i], a, b)
    return x


# In[199]:


@nb.njit#(parallel=True)
def simulate(z, m=1, backtrack=True, randomize=True, open_edges=False):
    for x in range(1):
        pos = np.array([0, 0])
#         grid = np.zeros([z] * D)
        grid = np.zeros((z, z), dtype=np.int64)
#         walks = []
#         steps = []
#         steps.append(pos)

#         steps = np.zeros((z**2, 2))
#         steps[0] = pos
        level = 0 # ?
#         TODO: randomize initial branches

        if randomize:
#             np.random.shuffle(choices)
            branches = np.random.randint(0, 3, (z**2,))
        else:
            branches = np.zeros((z**2,), dtype=np.int64)
        
#         Loop through (n^2)*m steps, where n is the width of the grid and m is a coefficient
        for t in range(z**2*m):
    #         print(0<pos+delta[0]<z)
    #         print(grid[tuple(pos+delta[0])])
            possible = valid_moves(grid, choices, pos, open_edges, z)
#             print(possible)
            

#             if branches[level] > len(possible):
#                 branches[level] = len(possible) - 1
    
#             B = branches[level] < len(possible)
#             B = branches[level] < len(choices)
            B = True
#             print(possible)
            
            grid[pos[0], pos[1]] = level+1#+(z**2//4)
            if len(possible) > 0 and B:
#                 delta = random.choice(possible)
#                 delta = np.random.choice(possible)
#                 np.random.shuffle(possible)
#                 index = np.random.randint(0, len(possible))
#                 branches[level] = index
#                 delta = possible[index]

#                 if randomize:
#                     random.shuffle(possible)

                index = branches[level]
                if index >= len(possible):
                    index %= len(possible)
#                 print(index)
                delta = possible[index]
                
#                 grid[tuple(pos)] = 1
#                 print(pos[0])

                
#                 steps.append(delta)
                pos += delta
#                 steps.append(delta)
#                 steps[l] = delta

#                 pos = np.clip(pos, 0, z-1)

                if open_edges:
                    pos %= z
                else:
                    pos = clip(pos, 0, z)

#                 Move to the next "level" below the current one
#                 Only increase the step count if there are still spaces to move to
                if np.count_nonzero(grid) <= z**2-1 and level < z**2-1:
                    level += 1
#                     if randomize:
#                         branches[level] = np.random.randint(0, 4)
#                     else:
                    if not randomize:
                        branches[level] = 0
            

            elif np.count_nonzero(grid) < z**2:
#                 lengths.append(t)
#                 walks.append(grid)
                if backtrack:
                    # TODO: prevent reselection of "stuck" path
            
#                     Reset value of current position and checked sub-branch
                    grid[pos[0], pos[1]] = 0
#                     if not randomize:
                    branches[level] = 0
                    
                    pos -= delta
                    pos = clip(pos, 0, z)

#                     steps.pop()
                    level -= 1
                    if level < 0:
                        level = 0
#                     print(f'Backtracking to level {level} (position: {pos})')
#                     print(level)
                    branches[level] += 1
                else:
                    break
                
        #                 End simulation early if a "perfect" path which covers the entire grid is found
            if np.count_nonzero(grid) >= z**2:
                break
#         else:
#         walks.append(grid)
    return grid


# In[217]:


# Store the best discovered path (i.e., the one that covers the most cells in the grid)
best = None
# Track walks/paths and their lengths
lengths = []
walks = []
# Run multiple simulations
for i in range(8000):
    G = simulate(8, 2, True, True, False)
#     if best:
#         print(best.max())
#     lengths.append(G.max())
    L = np.count_nonzero(G)
    lengths.append(L)
    walks.append(G)
    
#     If current path is longer than the best one found, store it instead
#     if best is None or G.max() > best.max():
    if best is None or np.count_nonzero(G) >= np.count_nonzero(best):
        best = G

# Display a visualization of the generated path
plt.figure(figsize=(10, 10))
plt.imshow(best, cmap='inferno')
plt.axis('off')

# decision trees? + parity
# random walks that close to a polygon
# (self-avoiding) random walks around obstructions
# add heuristics
# avoid and/or break at 
# add backtracking
# add step labels
# implement backbite algorithm for Hamiltonian path generation
# progressive upscaling+mutation?
# tracing/wrapping paths
# estimate needed compute
# allow crossing grid boundaries (i.e., a torus manifold)


# In[120]:


# Plot a histogram of the path lengths
plt.figure(figsize=(10, 5))
x = plt.hist(lengths, bins=25)


# In[256]:


# Display the "average path", the mean of all those simulated
plt.imshow(np.average(np.stack(walks), axis=0))


# In[ ]:




