import numpy as np
import matplotlib.pyplot as plt

def cartesian_product(*arrays):
    la = len(arrays)
    dtype = numpy.result_type(*arrays)
    arr = numpy.empty([len(a) for a in arrays] + [la], dtype=dtype)
    for i, a in enumerate(numpy.ix_(*arrays)):
        arr[...,i] = a
    return arr.reshape(-1, la)

class Collection:
    def __init__(self, members=None):
        if members is None:
            members = []
        self.members = members

class Polyomino:
    def __init__(self, size=100, delta=None, *args, **kwargs):
        self.data = np.ones((1, 1))
        self.indices = [(0, 0)]
        self.neighbors = [0]
        self.size = 1
        self.offsets = offsets = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        if delta is None:
            delta = np.zeros(2)
        self.delta = np.array(delta)

        self.pad()
        for i in range(size-1):
            self.grow(*args, **kwargs)

    def subset(self, *args, **kwargs):
        i = np.random.randint(self.size)
        root = self.indices[i]
        def growthConstraint(p, c):
            r = np.array(c) + p.delta
            # print(r)
            return np.all(r < np.array(self.data.shape)) and self.data[tuple(r)] == 1
        P = Polyomino(*args, delta=root, constraints=[growthConstraint], **kwargs)
        return P

    # def dissect

    def erode(self, n=1):
        for x in range(n):
            i = np.random.randint(self.size)
            self.data[self.indices[i]] = 0
            self.size -= 1
            self.indices.pop(i)
        return self

    def adj(self, pos):
        return [tuple(np.array(pos) + o) for o in self.offsets]

    def grow(self, constraints=None):
        # indices = np.transpose(self.data.nonzero())
        edges = []
        for x in self.indices:
            for c in self.adj(x):
                if self.data[c] != 1 and c not in edges and (constraints is None or all(g(self, c) for g in constraints)):
                    edges.append(c)
        if edges:
            z = edges[np.random.randint(len(edges))]
            self.data[z] = 1
            self.size += 1
            self.indices.append(z)
        # self.neighbors.append(np.sum(self.data[c] for c in self.adj(z)))
        # for c in self.adj(z):
            # self.neighbors[-1]


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
        # check this
        self.delta -= lower
        return self

    # def overlay(self, other, offset):

    # def join(self):

    def __str__(self):
        return '\n'.join(''.join('██' if cell else '  ' for cell in row) for row in self.data)


plt.style.use('seaborn')
x = Polyomino().erode(5)
print(x)
print(x.subset(size=50))

# TODO: generate polyominoes using grammars
# TODO: polyomino growth constraints
# overlay similarity
# fuzzy polyominoes
# try each possible overlaying?
# embeddings
