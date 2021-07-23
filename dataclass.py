#!/usr/bin/env python
# coding: utf-8

# # Punchcard

# ## Introduction

# This toolkit provides flexible and efficient data structures that abstract common manipulations, providing mappings, serialization, restructuring, convenience methods/wrappers, memoization, and more. Numerous convenience methods and data processing utilities are integrated into the class and universally accessible.
# 
# The core motivation is reducing the headaches often faced when iterating (and executing functions) over deeply nested and/or irregular data structures, which often results in boilerplate code and poorly standardized/optimized subroutines. The tools included in punchcard aim for brevity, intuitiveness, and developer productivity.
# 
# It is also designed to be highly computationally efficient, delegating operations to vectorized libraries like NumPy when doing so will provide a clear speedup. Some other optimizations planned or currently in progress include:
# 
#  - Automatic memoization/caching for every (or nearly every) function that is easy to work with out-of-the-box but can be fully tweaked and customized
#  - Just-in-time (JIT) compilation for repetitive operations on large data structures
#  - Meta-optimizers and meta-heuristics that select appropriate algorithms and third-party tools for a specific type of problem (e.g., search operations, data processing, dynamic programming)
#  - Storing generators in place of realized data/values when possible, and attempting to infer generators otherwise
#  - If possible, using online algorithms that only require a small subset of the entire dataset to be stored in memory at any given time during evaluation (e.g., $max(x_0 \dots x_n)$ only needs to store $x_i$ and the current largest value)
#  - Automatically restructuring internal representations of the data to facilitate more efficient computing of results
#  - Allowing fine-tuning of time-complexity and space-complexity tradeoff (as well as other similar high-level decisions), and handling the choice automatically when no particular direction is given
# In[641]:


import string
import operator
import uuid
import requests
import pprint
import math
import itertools
import functools
import numpy as np
from IPython import display
import copy
from bs4 import BeautifulSoup
import zlib
import sys
