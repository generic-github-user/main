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


class Point(Geometry):
    def __init__(self):
        # super(Geometry, self).__init__()
        super().__init__(dimensions=0)

# 1D geometry convenience subclass
class Line(Geometry):
    def __init__(self):
        super().__init__(dimensions=1)

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
    def regular(self, sides, radius):
        """Define polygon's geometry as a regular polygon; one with equal sides and angles"""
        for s in range(sides):
            self.sides.append(Line())

# TODO: numerical precision setting

class Ellipse(Shape):
    pass

