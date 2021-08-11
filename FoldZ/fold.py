# AUTOGENERATED! DO NOT EDIT! File to edit: 00_fold.ipynb (unless otherwise specified).

__all__ = ['Geometry', 'Point', 'Line', 'Polygon', 'Circle', 'Manifold', 'Foldable', 'F']

# Cell
%matplotlib widget
import matplotlib.pyplot as plt
import numpy as np
import svgwrite
import random

import sympy
from sympy import Point2D, Point3D, Segment, Polygon, N, Rational, pi
from sympy.abc import x, y, z, t

import math

from IPython.display import display, SVG

# Cell
class Geometry:
    """Generalized multidimensional shape class"""
    def __init__(self, parts=None, dimensions=None):
        """Create a new geometry object"""

        if parts:
            self.parts = parts
        else:
            self.parts = []

        if dimensions is None:
            self.dimensions = self.parts[0].dimensions + 1
        else:
            self.dimensions = dimensions

# Cell

# class Point(Geometry):
#     def __init__(self):
#         # super(Geometry, self).__init__()
#         super().__init__(dimensions=0)

class Point:
    pos: np.ndarray
    precision: int

    def __init__(self, pos:list, p:int=8):
        """
        Create a new Point instance

        Params:
            pos: The new point's position in the coordinate system
            p: The level of precision to store the point's position with
        """
        self.pos = np.array(pos, dtype=float)
        varnames = 'xyzw'
        for i, axis in enumerate(self.pos):
            setattr(self, varnames[i], self.pos[i])
        self.precision = p

    def move(self, delta:list):
        """
        Translate the point

        Params:
            delta: A list of offsets to move the point along each axis in space by
        """
        self.pos += np.array(delta)
        return self

    def rotate(self, a:list, theta:int, rad:float=None):
        """
        Rotate the point about another

        Params:
            a: The point to rotate about
            theta: The rotation to apply to the point, in degrees
            rad: The rotation in radians (supersedes `theta`)
        """
        theta = float(theta)
        # Convert to radians
        if not rad:
            theta = theta * math.pi / 180
        # Create a rotation matrix to apply a rotation to the point
        rotation_matrix = [
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ]
#         print(rotation_matrix)
#         self.pos *= rotation_matrix

        # Move the point so its coordinate is relative to the origin
        self.move(-a.pos)
        # Apply the rotation matrix
        self.pos = np.dot(self.pos, rotation_matrix)
        # Move point back
        self.move(a.pos)
        # Round to specified precision
        self.pos = self.pos.round(self.precision)
        return self

    def __add__(self, B):
        return Point(self.pos + B.pos)

    def __sub__(self, B):
        return Point(self.pos - B.pos)

    def __mul__(self, B):
        return Point(self.pos * B.pos)

    def __truediv__(self, B):
        if isinstance(B, Point):
            return Point(self.pos / B.pos)
        elif isinstance(B, (int, float)):
            return Point(self.pos / B)

    def __call__(self):
        """
        Returns this point's position
        """
        return self.pos

    def print(self):
        print(self)
        return self

    def __str__(self):
        """
        Generate a string representation of this point
        """
        return 'Point ' + str(self.pos)

# Cell
class Manifold:
    def __init__(self, dimensions=2):
        assert dimensions >= 1
        self.dimensions = dimensions

# Cell
class Event:
    def __init__(self):
        self.time = time.time()

    def __str__(self):
        return str(self.time)

    def __repr__(self):
        return str(self)

# Cell
class Foldable:
    def __init__(self, shape, manifold, exact=True, backend='geo'):
        if not isinstance(shape, (list, tuple)):
            shape = [shape]
        self.shape = shape
        self.manifold = manifold
        self.exact = exact
        self.backend = backend

    def render(self, filename='./rendered.svg', size=(400, 400), center=True, color='white', color_mapping='hue', color_by='order', style={}):
        image = svgwrite.Drawing(filename=filename, size=size)
        if self.backend == 'sympy':
            offset = Point2D(size)/2-self.shape[0].midpoint
        elif self.backend in ['geo', 'geometry']:
            offset = Point(size)/2-self.shape[0].midpoint()
        for i, part in enumerate(self.shape):
            if isinstance(part, Segment):
                p1 = self.plain(part.p1+offset)
                p2 = self.plain(part.p2+offset)
            elif isinstance(part, Line):
                p1 = (part.a+offset).pos
                p2 = (part.b+offset).pos
            if color_by == 'order':
                style |= {'style': f'stroke:hsl({round(i/len(self.shape)*360)}, 100%, 50%)'}
            line = image.line(
                start=p1,
                end=p2,
                stroke=color,
                stroke_width=1,
                **style
            )
            image.add(line)
        image.save()
        return self
