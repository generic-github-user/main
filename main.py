import numpy as np
import matplotlib.pyplot as plt
import pprint
import random

npa = np.array

# TODO: simulate angle of writing implement

outlines = {
    # 'a': ['left', 'down']
    # 'a': 'ur,u,l,dl,d,r,ur,dr'
    'a': 'ur,l,dl,d,r,ur,u,d,d',
    'b': 'u,u,u,u,d,d,d,d,r,ru,ul',
    'c': 'ur,ur,l,dl,d,dr,r',
    'd': 'dl,d,r,u,u,u,u,d,d,d,d',
    'e': 'ur,ur,l,d,dr,r'
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
    def __init__(self, pos, vel, canvas, shaking=None):
        self.pos = pos
        self.vel = vel
        self.canvas = canvas
        self.penSize = 5
        self.friction = 0.04

        if not shaking:
            self.shaking = np.random.normal(0, 0.05, [2, 2])
        else:
            self.shaking = shaking
        # self.fineShaking = 
        print(self.shaking)
    def step(self, target):
        # self.vel += np.sqrt((target - self.pos))
        # self.vel = (target - self.pos) / 1000
        # delta =
        self.vel += (target - self.pos) / 80 - (self.vel * self.friction)
        # self.vel += (target - self.pos) / 800 * self.friction
        # self.vel += (target - self.pos) / 50 - (np.mean(self.vel) * self.friction)
        # print((target - self.pos))
        # print(np.sqrt((target - self.pos)))
        # self.vel += normalize(target - self.pos)
        if 1 > 0.5:
            s = self.shaking
            # subtract?
            self.pos += np.random.normal(-s[0], np.abs(s[1]), [2]) * self.vel
            # self.vel += np.random.normal(-s[0], np.abs(s[1]), [2]) * self.vel
        self.pos += self.vel * 0.1
        x, y = np.round(self.pos).astype('int')
        # print(x, y)
        v = int(self.penSize / 2)
        self.canvas[x-v: x+v, y-v: y+v].fill(1)

class Drawer:
    def __init__(self, text, dims=[900, 600], letterSize=20.):
        self.text = text
        self.canvas = np.zeros(dims)
        self.start = npa([200., 200.])
        self.letterSize = letterSize
        self.size2D = npa([1., -1.]) * letterSize
        self.letterSpacing = npa([4., 0.])
        self.points = []
        self.curveType = 'momentum'
        self.pen = Pen(pos=self.start, vel=npa([0., 0.]), canvas=self.canvas)

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
                # m *= npa([1, -1])
                letterShape.append(m)
            self.points.append(letterShape)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.points)

        offset = self.start
        size = self.size2D


        letterStart = self.points[0][0] * self.letterSize + offset - self.letterSize
        self.pen.pos = (self.points[0][0].astype('float') * self.letterSize) + letterStart

        targets = []
        for i, letter in enumerate(self.points):
            o = (self.letterSpacing * self.letterSize * float(i))
            # print(npa([0, 50]) * npa([50, 0]))
            letterStart = offset - self.letterSize + o - (letter[0] * self.letterSize)
            # letterStart = offset + o
            # print(letterStart)
            if False:
                for point in letter:
                    target = (point * self.letterSize) + letterStart
                    # print(target)
                    for i in range(200):
                        self.pen.step(target=target)
                    targets.append(target)
                    # print(self.pen.vel)

            target = npa([0., 0.])
            target += letterStart
            # target -= (letter[0] * self.letterSize)
            for point in letter:
                counter = 0
                target += (point * self.letterSize)
                targets.append(np.copy(target))
                print(target)
                while np.linalg.norm(target-self.pen.pos) > 2 and counter < 1000:
                    self.pen.step(target=target)
                    counter += 1
        # x, y = zip(*targets)
        # plt.scatter(x, y)
        # plt.show()

    def clear(self):
        self.canvas = np.zeros(dims)

    def show(self):
        plt.imshow(self.canvas.transpose())
        plt.show()

d = Drawer('abcde')
d.write()
d.show()
