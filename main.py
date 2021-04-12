import numpy as np
import matplotlib.pyplot as plt

canvas = np.zeros([300, 600])
plt.imshow(canvas)
plt.show()
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
