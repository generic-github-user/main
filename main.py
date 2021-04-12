import numpy as np
import matplotlib.pyplot as plt
import pprint

npa = np.array

outlines = {
    # 'a': ['left', 'down']
    'a': 'ur,u,l,dl,d,r,ur,dr'
}

coords = {
    'u': npa([0, 1]),
    'd': npa([0, -1]),
    'r': npa([1, 0]),
    'l': npa([-1, 0]),
    'm': npa([-1, 0]),
}

class Pen:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

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
