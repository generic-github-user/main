__all__ = ['Geometry', 'Point', 'Line', 'Polygon', 'RegularPolygon', 'r', 'Circle', 'Manifold', 'Event', 'Foldable',
           'F']

import matplotlib.pyplot as plt
import svgwrite

import sympy
from sympy import Point2D, Point3D, Segment, Polygon, N, Rational, pi
from sympy.abc import x, y, z, t

import math
import numpy as np
import random


import time
from IPython.display import display, SVG


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


class Point:
    pos: np.ndarray
    precision: int

    def __init__(self, pos: list, p: int = 8):
        """
        Create a new Point instance

        Params:
            pos: The new point's position in the coordinate system
            p: The level of precision to store the point's position with
        """
        self.pos = np.array(pos, dtype=float)
        self.precision = p
        self.update()

    def update(self):
        varnames = 'xyzw'
        for i, axis in enumerate(self.pos):
            setattr(self, varnames[i], self.pos[i])
        return self

    def move(self, delta: list):
        """
        Translate the point

        Params:
            delta: A list of offsets to move the point along each axis in space by
        """
        self.pos += np.array(delta)
        self.update()
        return self

    def rotate(self, a: list, theta: int, rad: float = None):
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

        # Move the point so its coordinate is relative to the origin
        self.move(-a.pos)

        # Apply the rotation matrix
        self.pos = np.dot(self.pos, rotation_matrix)

        # Move point back
        self.move(a.pos)

        # Round to specified precision
        self.pos = self.pos.round(self.precision)

        self.update()
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


# 1D geometry convenience subclass
class Line:
    def __init__(self, a, b):
        """Create a new line

        Params:
            a: The start point of the line
            b: The end point of the line
        """
        self.a = a
        self.b = b

    def move(self, delta):
        """Translate the line

        Params:
            delta: The amount (in each direction/axis) to move the line by
        """
        for p in [self.a, self.b]:
            p.move(delta)
        return self

    def rotate(self, *args, **kwargs):
        for p in [self.a, self.b]:
            p.rotate(*args, **kwargs)
        return self

    def divide(self, n: int = 1) -> list['Line']:
        """Split the line into several smaller line segments

        Params:
            n: The number of sections to divide the line into
        """
#         return [Line(Point(np.average([self.a, self.b], weights=[]))) for i in range(n)]
        sections = []
        for i in range(n):
            a_ = np.average([self.a(), self.b()], weights=[i, n-i], axis=0)
            b_ = np.average([self.a(), self.b()], weights=[i+1, n-i-1], axis=0)
            s = Line(
                Point(b_),
                Point(a_),
            )
            sections.append(s)
        return sections[::-1]

    def intersects(self, B):
        if all([P >= max(B.a.x, B.b.x) for P in [self.a.x, self.b.x]]) or all([P <= min(B.a.x, B.b.x) for P in [self.a.x, self.b.x]]):
            return False
        elif all([P >= max(B.a.y, B.b.y) for P in [self.a.y, self.b.y]]) or all([P <= min(B.a.y, B.b.y) for P in [self.a.y, self.b.y]]):
            return False
        else:
            solution = self.solve(B)
            if solution:
    #             Check that solution is within bounds of both line segments
    #             (only need to check one axis)
                if (self.a.x <= solution.x <= self.b.x) or (self.a.x >= solution.x >= self.b.x):
                    if (B.a.x <= solution.x <= B.b.x) or (B.a.x >= solution.x >= B.b.x):
                        return True
    #             else:
    #                 print('Not in bounds')
            else:
                return False

    def intersection(self, L2):
        if self.intersects(L2):
            return self.solve(L2)

    def midpoint(self):
        return (self.a + self.b) / 2

    def slope(self):
        return (self.a.y - self.b.y) / (self.a.x - self.b.x)

    def yintercept(self):
        return self.a - Point((self.a.x, self.a.x*self.slope()))

    def coefficients(self):
#         - ?
        return [-self.slope(), 1, self.yintercept().y]

    def solve(self, L2):
        try:
            A, B = self.coefficients(), L2.coefficients()
            solution = np.linalg.solve(np.array([A[:2], B[:2]]), np.array([A[-1], B[-1]]))
            return Point(solution)
        except:
            return False

    def __str__(self):
        return 'Line\n\t' + '\n\t'.join(str(v) for v in [self.a, self.b])

    def __repr__(self):
        return str(self)


# 2D geometry convenience subclass
class Shape(Geometry):
    def __init__(self):
        super().__init__(dimensions=2)


# 3D geometry convenience subclass
class Solid(Geometry):
    def __init__(self):
        super().__init__(dimensions=3)


# 4D geometry convenience subclass
class Hypersolid(Geometry):
    def __init__(self):
        super().__init__(dimensions=4)


# should this subclass Geometry instead?
class Polygon(Shape):
    """General polygon class that extends the Shape class"""
    def __init__(self):
        """Create a new polygon"""
        super().__init__()
        self.sides: [line] = []
        self.vertices = self.v = []

    def regular(self, sides, radius):
        """Define polygon's geometry as a regular polygon; one with equal sides
        and angles"""
        for s in range(sides):
            self.sides.append(Line())

    def rotate(self, *args, **kwargs):
        for p in self.v:
            p.rotate(*args, **kwargs)
        return self

    def __str__(self):
        return 'Polygon\n\t' + '\n\t'.join(str(v) for v in self.v)

    def __repr__(self):
        return str(self)


class RegularPolygon(Polygon):
    def __init__(self, r=1, n=4, c=None, manifold=2, axis=0):
        super().__init__()
        start = [0] * manifold
        start[axis] = r
        self.v.append(Point(start))
        if not c:
            c = Point([0] * manifold)
        self.center = c
        for i in range(n-1):
            self.v.append(Point(self.v[-1].pos).rotate(c, 360 / n, axis=axis))


class Circle(Shape):
    """A geometric 2D circle with a certain radius; subclass of Shape"""
    def __init__(self, radius):
        super().__init__()
        self.radius: Scalar = radius


class Manifold:
    def __init__(self, dimensions=2):
        assert dimensions >= 1
        self.dimensions = dimensions
