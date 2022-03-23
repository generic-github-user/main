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

        self.pad()
        for i in range(size-1):
            self.grow()

    def grow(self):
        # indices = np.transpose(self.data.nonzero())
        edges = []
        offsets = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        for x in self.indices:
            for o in np.array(offsets):
                c = tuple(np.array(x)+o)
                if self.data[c] != 1 and c not in edges:
                    edges.append(c)
        z = edges[np.random.randint(len(edges))]
        self.data[z] = 1
        self.size += 1
        self.indices.append(z)
        # self.neighbors.

        self.pad()
        return self


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

    def __str__(self):
        return '\n'.join(''.join('██' if cell else '  ' for cell in row) for row in self.data)
