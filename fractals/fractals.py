#!/usr/bin/env python
# coding: utf-8

# Fractals
# Generation of Mandelbrots, Multibrots, and other fractals with Python

import matplotlib.pyplot as plt
import numpy as np
from itertools import product
import math
import random
import typing
import inspect

from fractal import Fractal
from fractalset import FractalSet
from utils import tile
from iterfunc import IteratedFunction
from geometry import Point, Line, Polygon, RegularPolygon
from attractor import Attractor, ChaosGame

r = lambda x, f: f(x[-1], x[-2]) not in [2]
g = ChaosGame((3, 8)).generate(x=20000, y=(0.1, 0.9, 2), e=(-0.1, 0.1, 1), rule='random')
# g = ChaosGame(5).generate(x=10000, y=(0.1, 0.9, 2), e=(-0.1, 0.1, 1), rule=lambda x, f: x[-1] != x[-2])
print(g.compute)
plt.figure(figsize=(10, 10))
# plt.imshow(g.render(500, color=''), cmap='RdPu')
plt.imshow(g.canvas, cmap='RdPu')

# g = g.generate(100).render(300)
# plt.imshow(g, cmap='binary')

class SierpinskiTriangle(ChaosGame):
    def __init__(self):
        super().__init__(3)
        
t = SierpinskiTriangle()
plt.imshow(t.generate(10000, direct=False).render(300))
t.compute

# TODO: prior selected point weights
# f = generate(r=(500, 1000), b=10, n=30, o=(-1, -0.5), m=2)
# f = Fractal(r=(50, 50), b=10, n=30, o=(-1, -0.5), m=2)
# f = FractalSet(z=[0, 1.5], d=[1, 5], r=[200]*2, q=10)(axes=[])
# print(f.find_regions())
# block = f.autozoom()
# f_ = f()
# ax.imshow(f, cmap='plasma')
# ax.imshow(block)
# plt.axis('off')
# list or dict for params?

f = Fractal(z=(-0.5, 0.5), d=(1.5, 3), b=10, n=30, r=(80, 80), o=(-0.1, 0.01), m=2, radius=2, point_spacing=0.01)
f()
f.generate()

