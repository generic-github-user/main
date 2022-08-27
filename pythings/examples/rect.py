@Class
class Rect:
    """
    A simple rectangle class, implemented using the `Point` class.
    """

    pos: Point = Attr('Location of the lower-left corner of the rectangle (assume 2D Euclidean space)')
    delta: Point = Attr('Positive (Q1) point representing the difference between opposite corners of the rectangle (including `pos`)')

    def area(self) -> Number: return self.delta.x * self.delta.y
    area.__doc__ = """Returns the rectangle's area"""

    def perimeter(self) -> Number: return (2 * self.delta.x) + (2 * self.delta.y)
    def scale(self, x) -> Number: return Rect(pos, delta * x)
    
print(Rect.doc('markdown'))
print(Rect.doc('text'))
