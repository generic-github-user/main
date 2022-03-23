import numpy as np
import matplotlib.pyplot as plt
class Collection:
    def __init__(self, members=None):
        if members is None:
            members = []
        self.members = members

class Polyomino:
    def __init__(self, size=100):
        self.data = np.ones((1, 1))
        self.indices = [(0, 0)]
        self.neighbors = [0]
        self.size = 1

    def pad(self):
        # indices = np.transpose(self.data.nonzero())
        padding = np.stack([
            np.min(self.indices, axis=0)==0,
            np.max(self.indices, axis=0)==(np.array(self.data.shape)-1)
        ], axis=1).astype(int)
        lower = padding[:, 0]
        self.data = np.pad(
            self.data,
            padding
        )
        for i, ind in enumerate(self.indices):
            self.indices[i] = tuple(np.array(ind)+lower)
        return self
