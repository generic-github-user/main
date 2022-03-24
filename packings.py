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
        self.offsets = offsets = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        self.pad()
        for i in range(size-1):
            self.grow()

    def erode(self, n=1):
        for x in range(n):
            i = np.random.randint(self.size)
            self.data[self.indices[i]] = 0
            self.size -= 1
            self.indices.pop(i)
        return self

    def adj(self, pos):
        return [tuple(np.array(pos) + o) for o in self.offsets]

    def grow(self):
        # indices = np.transpose(self.data.nonzero())
        edges = []
        for x in self.indices:
            for c in self.adj(x):
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


print(Polyomino().erode(5))
