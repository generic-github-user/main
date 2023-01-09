from __future__ import annotations
# __all__ = ['Geometry', 'Point', 'Line', 'Polygon', 'RegularPolygon', 'r',
# 'Circle', 'Manifold', 'Event', 'Foldable', 'F']

import numpy as np
import random
import math
import time
import curses

from lib.pylist import List

# TODO: global geometry sessions? (moved from fold.py)
# TODO: numerical precision setting
# TODO: separate simulation and rendering loops?


class Geometry:
    """Generalized multidimensional shape class"""
    def __init__(self, parts: List[Geometry], dimensions: int):
        """Create a new geometry object"""

        self.parts: List[Geometry] = parts
        self.dimensions: int = dimensions


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

    def __add__(self, B: Point) -> Point:
        return Point(self.pos + B.pos)

    def __sub__(self, B: Point) -> Point:
        return Point(self.pos - B.pos)

    def __mul__(self, B: Point) -> Point:
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
    def __init__(self: Polygon):
        """Create a new polygon"""
        super().__init__()
        self.sides: List[Line] = List()
        self.vertices = List()

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
    def __init__(self, radius: float):
        super().__init__()
        self.radius: float = radius


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
        for i, axis in enumerate(self.pos):
            setattr(self, varnames[i], self.pos[i])
        return self

    def info(self):
        """Get a string representing the object's properties (mostly for
        debugging)"""
        return '\n'.join(str(n) for n in [self.x, self.y, self.vel])


class Camera:
    def __init__(self: Camera, pos: Point, zoom=1):
        self.zoom: float = zoom
        self.pos: Point = pos


class Renderer:
    """Class for renderer to convert object data into a final image"""
    def __init__(self: Renderer, rtype: str, shape: Vector, camera: Camera,
                 objects: List[Object]) -> None:
        """Create a new renderer"""

        self.rtype: str = rtype
        """Renderer type; either `line`, `opengl`, or `canvas`"""

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

    def dot(self, m):
        if m > 0:
            return self.default_char
        else:
            return self.empty

    def at(self, x, y):
        # return list(filter(lambda o: round(o.x) == x and round(o.y) == y, self.objects))
        return list(filter(lambda o: np.array_equal(np.round_(o.pos()), np.array([x, y])), self.objects))

    def combine_output(self, g):
        return '\n'.join([''.join(h) for h in g])

    def form_output(self, angles):
        char_array = []
        dims = self.dims()
        for x in range(dims[0]):
            row = []
            for y in range(dims[1]):
                if angles[x, y] == 0:
                    row.append(' ')
                else:
                    row.append(self.fetch_line_glyph(angles[x, y], 0.5))
            char_array.append(row)
        return char_array

    def render_frame(self, callback, steps=300, current=0, show=True, delay=0):
        self.console.clear()

        if self.rtype == 'point':
            output_text = '\n'.join([''.join([self.dot(len(self.at(x, y))) for
                                              x in range(0, self.dims.x)]) for
                                     y in range(0, self.dims.y)])

        self.console.addstr(output_text)
        self.console.refresh()

        callback()
        if current < steps:
            self.root.after(33, lambda: self.render_frame(callback=callback, current=current+1, steps=300))


class Scene:
    """A class that brings together a world and a renderer, and provides
    high-level functions to facilitate their interaction"""
    def __init__(self: Scene, shape: Vector, edge_mode: str = 'wrap'):
        """Create a new scene"""

        self.objects: List[Object] = List()
        """A list of objects to initialize the scene with"""
        self.units = {
            'dist': 'm',
            'time': 's'
        }
        self.shape: Vector = shape
        """The width/height of the scene"""

        self.edge_mode: str = edge_mode
        """
        Defines the behavior for objects that go over the edges of the scene:
            - `wrap`: Wrap around so that an object passing through the bottom
              edge will come back down from the top edge, right will go to
              left, and so on
            - `bounce`: Bounce the object against the side of the scene as if
              it were a wall
            - `extend`: Let the object continue moving out of the frame
        """

        self.gravity_constant: float = 0.5
        self.drag: float = 1
        self.eta: float = 0.00000000001

        self.renderer = Renderer(rtype='canvas', shape=self.shape,
                                 camera=Camera(Point([2, 2])),
                                 objects=self.objects)

    def add(self, obj):
        self.objects.append(obj)
        return obj

    def edge_collision(self, obj):
        if self.edge_mode == 'wrap':
            obj.pos.n = obj.pos() % self.dims()
        elif self.edge_mode == 'bounce':
            raise NotImplementedError
        elif self.edge_mode == 'extend':
            raise NotImplementedError

    def gravity(self, obj):
        for o in self.objects:
            if obj is not o:
                dist = obj.pos.distance(o.pos)
                if dist == 0:
                    dist = self.eta

                obj.vel.n += (self.gravity_constant() * obj.mass() * o.mass() /
                              (dist ** 2)) / obj.mass() * (o.pos() - obj.pos())

    def clear(self):
        self.objects = List()

    def step(self, steps=1, step_length=1):
        for o in self.objects:
            # TODO: cache position, velocity, etc. before applying physics
            # step
            # TODO: collect list of forces acting on object
            delta = o.vel() * step_length
            o.pos.n += delta
            o.delta.n = delta
            self.edge_collision(o)
            self.gravity(o)

    def render(self, *args, **kwargs):
        self.renderer.render_frame(*args, **kwargs)

    def simulate(self, frames=300, steps=1, delay=None, fps=30):
        self.renderer.canvas.pack()

        if delay:
            pause = delay
        elif fps:
            pause = 1 / fps

        # phys_step = lambda: self.step(steps=steps, step_length=pause/steps)
        # root.after(round(pause * 1000), self.complete_step)
        self.complete_step(callback=self.step)

        # for frame in range(300):
            # self.render(pause)
            # for step in range(steps):

            # root.after(round(pause * 1000), self.rrender)
            # root.update_idletasks()
            # root.update()
            # myCanvas.update()
            # m+=1
            # or update canvas?
            # time.sleep(pause)

        self.renderer.root.mainloop()
