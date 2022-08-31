import numpy as np

t = tuple

class Object:
    def __init__(self, form, drawer, position=None, d=None, args=None, drawfunc=None, fill='black', stroke_fill='black', sides=3, rotation=0, text='text', scale=1, outline_color='black', outline_width=1):
        self.form = form
        self.drawer = drawer
        self.args = args
        self.drawfunc = drawfunc
        self.d = d
        if position is None:
            position = [100, 100]
        # TODO: make sure aliases don't interfere with updating/retrieving values
        self.position = self.p = np.array(position)
        self.r = 10
        self.size = self.r
        self.bounds = None
        self.circle = [*self.p[:2], self.r]
        self.sides = sides
        self.rotation = rotation
        self.text = text
        self.stroke_fill = stroke_fill

        self.children = []

        self.update()

        self.outline_color = outline_color
        self.outline_width = outline_width
        # self.fill = (200) * 3
        self.fill = fill

        self.scale = scale

    def draw(self, vflip=None):
        coords = self.bounds
        if vflip:
            # coords = [tuple(vflip - f for f in c) for c in coords]
            # coords = [(c[0], vflip - c[1]) for c in coords]
            pos_ = [b for b in self.p]
            pos_[1] = vflip - pos_[1]
            coords = self.bound(pos_)
            self.circle = [self.p[0], (vflip-self.p[1]), self.r]

        # self.drawer[drawfunc](args)
        if self.form == 'circle':
            # self.update()

            # self.drawer.arc(self.bounds, 0, 360, fill=0)
            self.drawer.ellipse(coords, fill=self.fill, outline=self.outline_color, width=self.outline_width)
        elif self.form == 'polygon':
            self.drawer.regular_polygon(t(self.circle), self.sides, fill=self.fill, rotation=self.rotation, outline=self.outline_color)
        elif self.form == 'text':
            font = ImageFont.truetype('arial.ttf', self.size*2)
            self.drawer.text(tuple(self.position), self.text, stroke_width=0, stroke_fill=self.stroke_fill, fill=self.fill, font=font)

        for c in self.children:
            c.draw(vflip)

        return self

    def move(self, w, d=False):
        self.position += w
        # self.bounds = [t(self.p-self.r), t(self.p+self.r)]
        self.update()
        if d:
            self.draw()

    def bound(self, pos):
        pos = np.array(pos)
        return [t(pos-self.r), t(pos+self.r)]

    def update(self):
        self.bounds = self.bound(self.p)
        self.circle = [*self.p[:2], self.r]

    def clone(self, clone_children=True):
        # return copy.deepcopy(self)
        obj_copy = Object(self.form, self.drawer, position=self.position)
        shallow = ['form', 'r', 'fill', 'drawer', 'sides']
        deep = ['bounds', 'position']
        for s in shallow:
            setattr(obj_copy, s, getattr(self, s))
        for d in deep:
            setattr(obj_copy, d, copy.deepcopy(getattr(self, d)))

        if self.children and clone_children:
            for c in self.children:
                obj_copy.children.append(c.clone(clone_children=clone_children))

        obj_copy.update()
        return obj_copy

    def add_child(self, c):
        self.children.append(c)



class Arrow(Object):
    """Arrow"""

    def __init__(self, start, end, length=None, direction=None):
        super(Arrow, self).__init__()
        self.start = start
        self.end = end
