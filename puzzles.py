#!/usr/bin/env python
# coding: utf-8

# # Programming Puzzles
# 
# This is a list of (hopefully interesting) programming puzzles I created (mainly for my own enrichment) with solutions and brief explanations. I didn't want to place any unnecessary restrictions on how the problems are to be approached, but there will be some occasional suggestions about possible variants you might want to try (e.g., finding an answer with a certain time/space complexity, using a certain data structure, etc). Pull requests with better or more interesting solutions, as well as new problems, are welcome.

# Find the smallest palindromic positive integer greater than 100,000 which contains, in its sequence of digits, the floor of its own square root.

# In[1]:


base = ''
for d in range(4):
    for i in range(10):
        s = str(i)
        num = s+base+s
        root = int(num) ** (1/2)
        if str(root) in str(num):
            print(num)
            break


# In[2]:


import math
def check(A, B=None):
    s = str(A)
    if B is None:
        num = s+s[::-1]
    else:
        num = s+str(B)+s[::-1]
#     print(num)
    root = math.floor(int(num) ** (1/2))
    if str(root) in num:
#         print(num)
        return num, root

for a in range(10000):
    r = check(a)
    if r:
#         break
        print(r)
    for b in range(10):
        t = check(a, b)
        if t:
            print(t)


# Write a function that takes as an input a (ASCII) string of an arbitrary length $l$ (at least one character) and compactly encodes it into a square binary matrix with $n$ rows and columns, where $1<=n<=l$. Write a second function that accepts a matrix generated by the first function and returns the original string.

# Let $a$ be the set of natural numbers (positive integers) in the range $[1, 1000]$; that is, $a=\{x \in N | 1 \le x \le 1000 \}$. Then, let $F$ be a function such that $F(g) = \{\left\|(h!)\right\| | h \in g \}$, where for an integer $j$ in the set $g$, $\|j\|$ denotes the number of digits in $h$ (length of its string form, ignoring leading zeros). $V$ is a function that iteratively applies $F$ to its initial inputs: $V(t, n)=F^n(t)$. Efficiently compute this process for each value through 42 iterations ($n=42$) and output the sum of these values; your answer will be:

# \begin{equation}
# \displaystyle
# \sum\limits_{b \in a} V(b, 42)
# \end{equation}

# If you attain sufficient efficiency on these terms (perhaps execution in under 30 seconds), attempt to further optimize your algorithm and scale the number of inputs by an order of magnitude or more.

# In[3]:


math.log10(567)


# In[8]:


import math
import numpy as np
import matplotlib.pyplot as plt


# In[91]:


previous = {}


# In[134]:
# Determine the number of possible ways a 2-dimensional chessboard (i.e., an 8 by 8 grid) could be covered in dominoes if a single domino covers two directly adjacent squares on the board, each domino must not overlap or share any squares with another, and the entire board would be covered. For a hint, take a look at this illuminating slideshow: https://www.math.cmu.edu/~bwsulliv/domino-tilings.pdf

# Challenge: assume the chessboard in the previous problem is projected onto the surface of a torus such that its edges "wrap" around to the other size. That is, a domino can cross between two opposite edges of the board.

# Generalize the chessboard-tiling algorithm to the case where the board size is $n \times m$ and $n\ge1, m\ge1$. Note that some combinations (most obviously, the 1 by 1 board) cannot be perfectly tiled using only 1 by 2 dominoes (as an additional challenge, you may find a heuristic for determining which board sizes are solvable).

# Further generalize the algorithm from the previous questions to 3 dimensions (with an 8x8x8 chessboard). The third dimension of the dominoes should be one unit wide (so they are 2x1x1).
