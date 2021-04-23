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
    def __init__(self, form, drawer, position=None, d=None, args=None, drawfunc=None, fill=None):
        self.form = form
        self.drawer = drawer
        self.args = args
        self.drawfunc = drawfunc
        self.d = d
        if position is None:
            position = [100, 100]
        self.position = self.p = np.array(position)
        self.r = 10
        self.bounds = None
        self.circle = [*self.p[:2], self.r]
        self.sides = sides

        self.update()

        # self.fill = (200) * 3
        self.fill = fill

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
            self.drawer.ellipse(coords, fill=self.fill)
        elif self.form == 'polygon':
            self.drawer.regular_polygon(t(self.circle), self.sides, fill=self.fill)

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

    def clone(self):
        # return copy.deepcopy(self)
        obj_copy = Object(self.form, self.drawer, position=self.position)
        shallow = ['form', 'r', 'fill', 'drawer', 'sides']
        deep = ['bounds', 'position']
        for s in shallow:
            setattr(obj_copy, s, getattr(self, s))
        for d in deep:
            setattr(obj_copy, d, copy.deepcopy(getattr(self, d)))
        obj_copy.update()
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
        self.fill = 'green'

        # self.renderer = plt.imshow(canvas)
        self.fig, self.ax = plt.subplots(1,1)
        # image = numpy.array([[1,1,1], [2,2,2], [3,3,3]])
        self.im = self.ax.imshow(self.canvas)
        self.fig.show()

        z = 30
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
        # Command is provided as string
        if type(c) is str:
            # Remove alternative separators
            c = c.replace('/', ' ')
            c = c.replace(',', ' ')
            # Split on space
            args = c.split(' ')
        # Command is provided as list of arguments
        elif type(c) is list:
            args = c

        x = args[0][0]

        q=40
        if x == 'a':
            if args[0][1] == 'c':
                # d = lambda: self.draw.arc([t(self.m-q), t(self.m+q)], 0, 360, fill=0, width=5)
                new_obj = Object('circle', self.draw, position=self.m, fill='green')
            elif args[0][1] == 'p':
                num = int(args[1])
                new_obj = Object('polygon', self.draw, position=self.m, sides=num, fill='green')

            self.add(new_obj)
            self.context = [new_obj]
        elif x == 'm':
            shift = self.directions[args[0][1]]
            shift = np.array(shift)
            for o in self.context:
                o.move(shift)
        # Change fill color
        elif x == 'f':
            for o in self.context:
                o.fill = args[1]
        elif x == 'd':
            # why only 6?
            print(self.objects)
            num = int(args[1])
            sel = self.context[0]
            con = [o for o in self.context]
            context_ = []
            for o in con:
                sel = o
                for n in range(num):
                    new = sel.clone()
                    self.context = [new]
                    self.command(args[2:])
                    self.add(new)
                    context_.append(new)
                    sel = new
            self.context = context_

        elif x == 'r':
            pass
        elif x == 'u':
            pass
        elif x == 'x':
            self.objects.remove(self.objects[-1])
        elif x == 'q':
            quit()

        self.clear()
        self.render()

    def render(self):
        for o in self.objects:
            o.draw(vflip=self.y)
        if self.grayscale:
            self.canvas.convert('L')

        # plt.imshow(np.asarray(self.canvas), cmap=self.cmap)
        # plt.show()

        # fig = plt.gcf()
        # fig.gca().add_artist(circle)
        # plt.draw()

        self.im.set_data(self.canvas)
        self.fig.canvas.draw_idle()

    def interact(self):
        for i in range(100):
            # Get input from user and pass string to command function
            c = input()
            self.command(c)



# plt.ion()
# img = np.ones((400, 400, 3))
# generate_panel(img)

s = Scene(dims=[400, 400])

s.command('ac')
# s.command('mr')
# scm = s.command
# scm('f red')
# scm('d 4 md')
# scm('r')

s.interact()
