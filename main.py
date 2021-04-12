import numpy as np
import matplotlib.pyplot as plt
import pprint

npa = np.array

# TODO: simulate angle of writing implement

outlines = {
    # 'a': ['left', 'down']
    'a': 'ur,u,l,dl,d,r,ur,dr'
}

coords = {
    'u': npa([0, -1]),
    'd': npa([0, 1]),
    'r': npa([1, 0]),
    'l': npa([-1, 0]),
    'm': npa([0, 0]),
}

def normalize(v):
    norm=np.linalg.norm(v, ord=1)
    if norm==0:
        norm=np.finfo(v.dtype).eps
    return v/norm

class Pen:
    def __init__(self, pos, vel, canvas):
        self.pos = pos
        self.vel = vel
        self.canvas = canvas
        self.penSize = 5
        self.friction = 0.04
    def step(self, target):
        # self.vel += np.sqrt((target - self.pos))
        # self.vel = (target - self.pos) / 1000
        self.vel += (target - self.pos) / 80 - (self.vel * self.friction)
        # self.vel += (target - self.pos) / 800 * self.friction
        # self.vel += (target - self.pos) / 50 - (np.mean(self.vel) * self.friction)
        # print((target - self.pos))
        # print(np.sqrt((target - self.pos)))
        # self.vel += normalize(target - self.pos)
        self.pos += self.vel * 0.1
        x, y = np.round(self.pos).astype('int')
        # print(x, y)
        v = int(self.penSize / 2)
        self.canvas[x-v: x+v, y-v: y+v].fill(1)

class Drawer:
    def __init__(self, text, dims=[300, 600], letterSize=30):
        self.text = text
        self.canvas = np.zeros(dims)
        self.start = [100, 100]
        self.letterSize = letterSize
        self.points = []
        self.curveType = 'momentum'
        self.pen = Pen(start, npa([0, 0]))

    def write(self):
        for letter in self.text:
            p = outlines[letter].split(',')
            letterShape = []
            for point in p:
                # m = npa([0, 0])
                if len(point) == 1:
                    m = coords[point]
                elif len(point) == 2:
                    m = coords[point[0]] + coords[point[1]]
                letterShape.append(m)
            self.points.append(letterShape)
        pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(self.points)

    def clear(self):
        self.canvas = np.zeros(dims)

    def show(self):
        plt.imshow(self.canvas)
        plt.show()

d = Drawer('aaa')
d.write()
