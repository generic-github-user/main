import numpy as np
import deepcopy

class RowGame:
    def __init__(self, m=3, k=3, n=3, r=1):
        self.m = m
        self.k = k
        self.n = n
        self.r = r
        self.board = np.zeros([m, k])

    def clone(self):
        return deepcopy.copy(self)
