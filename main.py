from PIL import Image, ImageDraw
import sys
import matplotlib.pyplot as plt
import numpy as np
import copy

# from IPython.display import clear_output


import matplotlib.image as mpimg



# with Image.open("hopper.jpg") as im:

canvas_size = np.array([100]*2)
n, m = canvas_size
im = Image.new('RGB', (n, m), (255, 255, 255))

draw = ImageDraw.Draw(im)
# draw.line((0, 0) + im.size, fill=128)
# draw.line((0, im.size[1], im.size[0], 0), fill=128)

# write to stdout
# im.save(sys.stdout, "PNG")
# im.show()
class Object:
    def __init__(self, form, drawer, position=None, d=None, args=None, drawfunc=None):
        self.form = form
        self.drawer = drawer
        self.args = args
        self.drawfunc = drawfunc
        self.d = d
        if position is None:
            position = [100, 100]
        self.position = self.p = position
        self.r = 50
        self.bounds = [t(self.p-self.r), t(self.p+self.r)]

        self.fill = (200) * 3

    def draw(self, vflip=None):
        # self.drawer[drawfunc](args)
        # self.d()
        if self.form == 'circle':
            print(self.p)
            coords = self.bounds
            if vflip:
                # coords = [tuple(vflip - f for f in c) for c in coords]
                # coords = [(c[0], vflip - c[1]) for c in coords]
                pos_ = [b for b in self.p]
                pos_[1] = vflip - pos_[1]
                coords = self.bound(pos_)
            # self.update()

            # self.drawer.arc(self.bounds, 0, 360, fill=0)
            self.drawer.ellipse(coords, fill=self.fill)
        return self

    def move(self, w, d=False):
        self.position += w
        self.bounds = [t(self.p-self.r), t(self.p+self.r)]
        if d:
            self.draw()

    def bound(self, pos):
        pos = np.array(pos)
        return [t(pos-self.r), t(pos+self.r)]

    def update(self):
        self.bounds = self.bound(self.p)

    def clone(self):
        # return copy.deepcopy(self)
        obj_copy = Object(self.form, self.drawer)
        shallow = ['form', 'r', 'fill', 'drawer']
        deep = ['bounds']
        for s in shallow:
            setattr(obj_copy, s, getattr(self, s))
        for d in deep:
            setattr(obj_copy, d, copy.deepcopy(getattr(self, d)))
        return obj_copy

class Scene:
    def __init__(self, dims=None, bg=255):
        self.bg = bg

        if dims is None:
            dims = [200, 200]
        self.dimensions = self.dims = np.array(dims)
        self.axes = list('xyzw')[:len(self.dims)]
        for i, a in enumerate(self.axes):
            setattr(self, a, self.dims[i])

        self.canvas = Image.new('RGB', t(self.dims), (self.bg,)*3)
        self.draw = ImageDraw.Draw(self.canvas)
        self.middle = self.m = self.dims / 2

        self.command_history = []
        self.objects = []
        self.selection = []
        self.context = []

        self.channels = 3
        self.cmap = None
        self.grayscale = False

        # self.renderer = plt.imshow(canvas)
        self.fig, self.ax = plt.subplots(1,1)
        # image = numpy.array([[1,1,1], [2,2,2], [3,3,3]])
        self.im = self.ax.imshow(self.canvas)
        self.fig.show()

        z = 50
        self.directions = {
            'r': [z, 0],
            'l': [-z, 0],
            'u': [0, z],
            'd': [0, -z]
        }

        self.cmds = {
            'c': lambda q: self.draw.arc([t(self.m-q), t(self.m+q)], 0, 360, fill=0, width=5)
            # 'c': lambda q: draw.line((0, im.size[1], im.size[0], 0), fill=128)
        }

    def clear(self):
        self.draw.rectangle((0, 0, *self.dims), fill=(self.bg,)*self.channels)

    def add(self, o):
        self.objects.append(o)
        return o

    def command(self, c):
        # self.cmds[c](20)
        c = c.replace('/', ' ')
        c = c.replace(',', ' ')
        args = c.split(' ')
        x = args[0][0]

        q=40
        if x == 'a':
            if args[0][1] == 'c':
                # d = lambda: self.draw.arc([t(self.m-q), t(self.m+q)], 0, 360, fill=0, width=5)
                self.add(Object('circle', self.draw, position=self.m))
