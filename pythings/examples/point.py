#class Point

Number = Int | Float
Point = Class('Point',
        'A simple point in two-dimensional Euclidean space; \
            can also be used to represent a vector.',

        x=Number,
        y=Number,

        _attrfmt="The point's {} coordinate",
        _fmt='({}, {})',
        _examples="""
            # initialize a new point (these are all equivalent)
            a = Point(3, 4)
            a = Point(x=3, y=4)
            a = Point([3, 4])
            a = Point({x: 3, y: 4})
            a = Point.set_x(3).set_y(4)


            #print(a.norm())
            a.norm()
            b = Point(2, 1)

            # use basic arithmetic operators on points
            a - b
            a + b

            # compare points
            a == b
            a != b

            (a + b).norm()
            a >= 4

            a.to(tuple)
            xa, ya = a
            a.x == a['x'] == a[0] == a.get('x')

            # scale points via broadcasting
            b * 3
            a / 2
            b ** 4
            a / 0
            a *= 2

            # the other operand is type-checked before the error gets to the
            # interpreter level so you can intercept it however you see fit
            a -= 'eclectic'
            a.z

            # find the distance between two points
            Point.dist(a, b)
            a.dist(b)
            # rshift is overloaded to compute distance
            a >> b

            c = Point(7, -4)
            Point.min([a, b, c])
            Point.max([a, b, c])
            Point.mean([a, b, c])

            # a binary mean operation is aliased as the midpoint method
            Point.midpoint(a, c)

            Point.min([a, b, c], key='norm')
            Point.max([a, b, c], key='norm')

            Point.reduce([a, b, c], Point.dist)
            Point.sum([a, b, c])

            a.x = 8
            a.y += 3
            a

            # convert Point instances to various formats
            b.to_dict()
            b.to_json()
            b.to_yaml()
            b.to_string()
            b.to_namedtuple()

            # create a new point by converting the datatype that Point wraps
            # (in this case, we start with `Number`s so existing `float`s
            # remain the same while `int`s are typecasted)
            a.cast(Float)
            Point.cast(a, Float)

            b2 = b.clone()
            b.y += 8
            print(b, b2)

            Point.doc('markdown')
            Point.doc('text')
            Point.doc('html')
        """,
        _tests="""
            Point(3, 4).norm() == 5
            Point(4, 5) + Point(6, 7) == Point(10, 12)
        """
    )\
    .derive('__add__', '__sub__', '__eq__', '__ne__', '__neg__', 'max', 'min')\
    .insert(
        norm=lambda x, y: math.sqrt(x**2 + y**2),
        dist=lambda a, b: (a - b).norm(),
        transpose=lambda x, y: Point(y, x)
    )
