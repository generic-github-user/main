#!/usr/bin/env python
# coding: utf-8

# # Fractals
# 
# Generation of Mandelbrots, Multibrots, and other fractals with Python

# In[101]:


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


# In[753]:


        

p = Point([0, 2])
t = Point([0, 1])
p.print()
t.print()
p.rotate(t, 90).pos


# In[3]:



l = Line(
    Point([0, 2]),
    Point([0, 1])
)
# l.rotate(t, 90).a.pos
print(l.divide(3)[2])


# In[4]:


            
r = RegularPolygon()
print(r)


# In[6]:


type(lambda x:x)


# In[1003]:


# In[1115]:



r = lambda x, f: f(x[-1], x[-2]) not in [2]
g = ChaosGame((3, 8)).generate(x=20000, y=(0.1, 0.9, 2), e=(-0.1, 0.1, 1), rule='random')
# g = ChaosGame(5).generate(x=10000, y=(0.1, 0.9, 2), e=(-0.1, 0.1, 1), rule=lambda x, f: x[-1] != x[-2])
print(g.compute)
plt.figure(figsize=(10, 10))
# plt.imshow(g.render(500, color=''), cmap='RdPu')
plt.imshow(g.canvas, cmap='RdPu')


# In[1044]:




# In[789]:


np.random.uniform()


# In[850]:


f.points[:100]


# In[427]:


# g = g.generate(100).render(300)
# plt.imshow(g, cmap='binary')


# In[295]:


# len(g.points)


# In[238]:


g.vertices[-10:]


# In[142]:


g.rule([0, 1, 3, 3, 4, 2], g.dist)
# inspect.getsource(g.rule)
# g.rule??
inspect.signature(g.rule)


# In[1126]:


class SierpinskiTriangle(ChaosGame):
    def __init__(self):
        super().__init__(3)
        
t = SierpinskiTriangle()
plt.imshow(t.generate(10000, direct=False).render(300))
t.compute


# In[856]:


# TODO: prior selected point weights


# In[207]:


abs(complex(-5, -10))


# In[344]:


def t():
    t.a = 5
t.a


# In[357]:


Fractal.norm.params


# In[379]:


test = list[int, Fractal]
(list, (int,))
test
# __annotations__
str(test)
vars(test)
typing.get_origin(test)
typing.get_args(test)


# In[466]:


f8 = Fractal()
f8.scale(-3, 0, 0.01)
np.interp(-0.5, [-1, 1], [0, 30])
np.interp([-2.9, 1.4], [-2, 2], [0, 50])


# In[480]:


(0, 0) in [int]


# In[640]:


# In[766]:


    
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


# In[765]:


np.var(np.random.uniform(0, 1, [5, 5, 3]))


# In[666]:


f.generate()

