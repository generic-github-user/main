from __future__ import annotations
# __all__ = ['Geometry', 'Point', 'Line', 'Polygon', 'RegularPolygon', 'r',
# 'Circle', 'Manifold', 'Event', 'Foldable', 'F']

import numpy as np
import random
import math
import time
import curses

from lib.python.pylist import List

# TODO: global geometry sessions? (moved from fold.py)
# TODO: numerical precision setting
# TODO: separate simulation and rendering loops?


class Geometry:
    """Generalized multidimensional shape class"""
    def __init__(self, parts: List[Geometry], dimensions: int):
        """Create a new geometry object"""

        self.parts: List[Geometry] = parts
        self.dimensions: int = dimensions

    def __add__(self, B: Point) -> Geometry:
        return Geometry(self.parts.map(lambda x: x + B), self.dimensions)

    def __sub__(self, B: Point) -> Geometry:
        return Geometry(self.parts.map(lambda x: x - B), self.dimensions)

    def __mul__(self, B: Point) -> Geometry:
        return Geometry(self.parts.map(lambda x: x * B), self.dimensions)

    def __truediv__(self, B: Point) -> Geometry:
        return Geometry(self.parts.map(lambda x: x / B), self.dimensions)


class Point(Geometry):
    pos: np.ndarray

    def __init__(self, pos: list):
        """
        Create a new Point instance

        Params:
            pos: The new point's position in the coordinate system
        """

        super().__init__(List(), dimensions=0)
        self.pos = np.array(pos, dtype=float)
        self.update()

    def update(self):
        varnames = 'xyzw'
        for i, axis in enumerate(self.pos):
            setattr(self, varnames[i], self.pos[i])
        return self

    def move(self, delta: list) -> Point:
        """
        Translate the point

        Params:
            delta: A list of offsets to move the point along each axis in space
            by
        """
        return Point(self.pos + np.array(delta))

    def rotate(self, a: Point, theta: float) -> Point:
        """
        Rotate the point about another

        Params:
            a: The point to rotate about
            theta: The rotation to apply to the point, in radians
        """

        # Create a rotation matrix to apply a rotation to the point
        rotation_matrix = [
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ]

        return Point(np.dot((self - a).pos, rotation_matrix)) + a

    @staticmethod
    def distance(a: Point, b: Point) -> float:
        return float(np.linalg.norm(a.pos - b.pos))

    def __add__(self, B: Point) -> Point:
        return Point(self.pos + B.pos)

    def __sub__(self, B: Point) -> Point:
        return Point(self.pos - B.pos)

    def __mul__(self, B: Point) -> Point:
        if isinstance(B, Point):
            return Point(self.pos * B.pos)
        elif isinstance(B, (int, float)):
            return Point(self.pos * B)
        else:
            raise NotImplementedError

    def __truediv__(self, B):
        if isinstance(B, Point):
            return Point(self.pos / B.pos)
        elif isinstance(B, (int, float)):
            return Point(self.pos / B)
        else:
            raise NotImplementedError

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
class Line(Geometry):
    def __init__(self, a, b):
        """Create a new line

        Params:
            a: The start point of the line
            b: The end point of the line
        """
        super().__init__(dimensions=1)
        self.a = a
        self.b = b

    def move(self, delta: Point) -> Line:
        """Translate the line

        Params:
            delta: The amount (in each direction/axis) to move the line by
        """
        return Line(*List([self.a, self.b]).map(lambda p: p + delta))

    def rotate(self, *args, **kwargs) -> Line:
        return Line(*List([self.a, self.b]).map(
            lambda p: p.rotate(*args, **kwargs)))

    def divide(self, n: int = 1) -> list['Line']:
        """Split the line into several smaller line segments

        Params:
            n: The number of sections to divide the line into
        """
#         return [Line(Point(np.average([self.a, self.b], weights=[]))) for i
#         in range(n)]
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

    def intersects(self, B: Line) -> bool:
        if all([P >= max(B.a.x, B.b.x) for P in [self.a.x, self.b.x]]) or\
                all([P <= min(B.a.x, B.b.x) for P in [self.a.x, self.b.x]]):
            return False
        elif all([P >= max(B.a.y, B.b.y) for P in [self.a.y, self.b.y]]) or\
                all([P <= min(B.a.y, B.b.y) for P in [self.a.y, self.b.y]]):
            return False
        else:
            solution = self.solve(B)
            if solution:
                # Check that solution is within bounds of both line segments
                # (only need to check one axis)
                if (self.a.x <= solution.x <= self.b.x) or\
                        (self.a.x >= solution.x >= self.b.x):
                    if (B.a.x <= solution.x <= B.b.x) or\
                            (B.a.x >= solution.x >= B.b.x):
                        return True
    #             else:
    #                 print('Not in bounds')
            else:
                return False

    def intersection(self, L2: Line) -> Result[Point]:
        if self.intersects(L2):
            return self.solve(L2)

    def midpoint(self):
        return (self.a + self.b) / 2

    def slope(self):
        return (self.a.y - self.b.y) / (self.a.x - self.b.x)

    def yintercept(self):
        return self.a - Point((self.a.x, self.a.x*self.slope()))

    def coefficients(self):
        # - ?
        return [-self.slope(), 1, self.yintercept().y]

    def solve(self, L2):
        try:
            A, B = self.coefficients(), L2.coefficients()
            solution = np.linalg.solve(
                np.array([A[:2], B[:2]]),
                np.array([A[-1], B[-1]])
            )
            return Point(solution)
        except:
            return False

    def __str__(self):
        return 'Line\n\t' + '\n\t'.join(str(v) for v in [self.a, self.b])

    def __repr__(self):
        return str(self)


# 2D geometry convenience subclass
class Shape(Geometry):
    def __init__(self, parts):
        super().__init__(parts, 2)


# 3D geometry convenience subclass
class Solid(Geometry):
    def __init__(self, parts):
        super().__init__(parts, 3)


# 4D geometry convenience subclass
class Hypersolid(Geometry):
    def __init__(self, parts):
        super().__init__(parts, 4)


# should this subclass Geometry instead?
class Polygon(Shape):
    """General polygon class that extends the Shape class"""
    def __init__(self: Polygon):
        """Create a new polygon"""
        super().__init__(List())
        self.sides: List[Line] = List()
        self.vertices: List[Point] = List()

    @staticmethod
    def regular(self, sides: int, radius: float) -> Polygon:
        """Define polygon's geometry as a regular polygon; one with equal sides
        and angles"""
        class RegularPolygon(Polygon):
            def __init__(self, radius: float,
                         n: int,
                         center: Point = None,
                         manifold=2,
                         axis=0):
                super().__init__()
                start = [0] * manifold
                start[axis] = radius
                self.v.append(Point(start))
                if not center:
                    center = Point([0] * manifold)
                self.center = c
                for i in range(n-1):
                    self.v.append(Point(self.v[-1].pos).rotate(c, 360 / n, axis=axis))
        return RegularPolygon(radius, sides)

    def rotate(self, *args, **kwargs):
        for p in self.v:
            p.rotate(*args, **kwargs)
        return self

    def __str__(self):
        return 'Polygon\n\t' + '\n\t'.join(str(v) for v in self.v)

    def __repr__(self):
        return str(self)


class Circle(Shape):
    """A geometric 2D circle with a certain radius; subclass of Shape"""
    def __init__(self, center: Point, radius: float):
        super().__init__(List())
        self.center: Point = center
        self.radius: float = radius

    def contains(self, p: Point) -> bool:
        return Point.distance(self.center, p) <= self.radius

    def __add__(self, B: Point) -> Circle:
        return Circle(self.center + B, self.radius)


class Manifold:
    def __init__(self, dimensions=2):
        assert dimensions >= 1
        self.dimensions = dimensions


class Name:
    def __init__(self, name, abbr):
        self.name = name
        self.abbr = abbr


class Unit:
    def __init__(self, name, abbr, utype):
        self.name = name
        self.abbr = abbr
        self.utype = utype


class Angle:
    def __init__(self, angle: float):
        self.angle: float = angle % (math.pi * 2)

    def __add__(self, b: Angle):
        return Angle(self.angle + b.angle)

    def __mul__(self, w: float):
        return Angle(self.angle * w)


class Matter:
    def __init__(self, geometry, material):
        self.geometry = geometry
        self.material = material


Vector = Point


class Object:
    """A single physical object, like a box or a tree"""
    def __init__(self: Object, pos: Vector, vel: Vector, angle: Angle, angvel:
                 Angle, matter: List[Matter], mass: float):
        """Create a new object; creating it does not add it to any scene by
        default"""

        self.pos: Vector = pos
        """Initial xy location of the object (this will likely change when the
        simulation is run)"""

        self.vel: Vector = vel
        """Initial xy velocity of the object"""

        self.rotation: Angle = angle
        self.angvel: Angle = angvel

        self.matter = matter
        """Matter that the object is comprised of"""

        self.mass: float = mass
        """Mass of the object"""

        # not sure if keeping this
        self.canvas = None
        self.display = None
        self.delta = Point([0, 0])

        self.update()

    def update(self):
        varnames = 'xyzw'
        for i, axis in enumerate(self.pos.pos):
            setattr(self, varnames[i], self.pos.pos[i])
        return self

    def info(self):
        """Get a string representing the object's properties (mostly for
        debugging)"""
        return '\n'.join(str(n) for n in [self.x, self.y, self.vel])

    def contains(self, p: Point) -> bool:
        return self.matter.any(lambda x: (x.geometry + self.pos).contains(p))

    def step(self, step_length) -> Object:
        delta = self.vel * step_length
        self.pos += delta
        self.delta = delta

        theta = self.angvel * step_length
        self.rotation += theta

        return self


class Camera:
    def __init__(self: Camera, pos: Point, zoom=1):
        # ?
        self.scale: Vector = Vector([1, 1.6])
        self.zoom: float = zoom
        self.pos: Point = pos


class Renderer:
    """Class for renderer to convert object data into a final image"""
    def __init__(self: Renderer, shape: Vector, camera: Camera,
                 objects: List[Object]) -> None:
        """Create a new renderer"""

        self.shape: Vector = shape
        """The width and height of the scene"""

        self.camera: Camera = camera
        """A camera to store additional rendering properties"""

        self.default_char: str = 'o'
        """Character used for rendering points when line data is not
        available"""

        self.empty: str = ' '
        """Character used to fill areas where no objects are present"""

        self.objects = objects
        """List of objects for the renderer to display"""

        self.console = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.console.keypad(True)
        self.console.nodelay(True)

    def close(self):
        curses.nocbreak()
        self.console.keypad(False)
        curses.echo()
        curses.endwin()

    def dot(self, m):
        if m > 0:
            return self.default_char
        else:
            return self.empty

    def at(self, x, y):
        # ?
        return self.objects.filter(lambda o: o.contains((Point([x, y]) - (self.shape / 2) + self.camera.pos) *
                                                        self.camera.scale *
                                                        self.camera.zoom))

    def render_frame(self):
        self.console.clear()

        output_text = '\n'.join([''.join([self.dot(len(self.at(x, y))) for x in
                                          range(0, int(self.shape.x))]) for y
                                 in range(0, int(self.shape.y))])

        self.console.addstr(output_text)
        self.console.refresh()

        try:
            key = self.console.getkey() 
            if key == '=':
                self.camera.zoom *= 0.9
            if key == '-':
                self.camera.zoom *= 1.1

            w = 0.5
            if key == 'i':
                self.camera.pos += Point([0, -w])
            if key == 'k':
                self.camera.pos += Point([0, w])
            if key == 'j':
                self.camera.pos += Point([-w, 0])
            if key == 'l':
                self.camera.pos += Point([w, 0])
        except curses.error:
            pass


class Scene:
    """A class that brings together a world and a renderer, and provides
    high-level functions to facilitate their interaction"""
    def __init__(self: Scene, objects: List[Object], shape: Vector) -> None:
        """Create a new scene"""

        self.objects: List[Object] = objects
        """A list of objects to initialize the scene with"""
        self.units = {
            'dist': 'm',
            'time': 's'
        }

        self.gravity_constant: float = 0.5
        self.drag: float = 1
        self.eta: float = 0.00000000001

        self.renderer = Renderer(shape=shape, camera=Camera(Point([0, 0])),
                                 objects=self.objects)

    def add(self, obj):
        self.objects.append(obj)
        return obj

    def gravity(self, obj):
        for o in self.objects:
            if obj is not o:
                dist = obj.pos.distance(o.pos)
                if dist == 0:
                    dist = self.eta

                obj.vel.n += (self.gravity_constant() * obj.mass() * o.mass() /
                              (dist ** 2)) / obj.mass() * (o.pos() - obj.pos())

    def step(self, step_length=1):
        for o in self.objects:
            # TODO: cache position, velocity, etc. before applying physics
            # step
            # TODO: collect list of forces acting on object
            self.objects.for_each(lambda x: x.step(step_length))
            self.gravity(o)

    def simulate(self, frames: int, steps=1, delay=0.001):
        for frame in range(frames):
            # self.step(step_length=delay/steps)
            self.step(0.01)
            self.renderer.render_frame()
            # time.sleep(delay)
        self.renderer.close()


def main():
    print('starting...')
    Scene(List([Object(Point([0, 0]), Vector([5, 5]), Angle(0), Angle(0), List([Matter(Circle(Point([0, 0]), 10), None)]), 1)]),
          Vector([60, 30])).simulate(6000)


main()
