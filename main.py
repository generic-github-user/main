from PIL import Image, ImageDraw
import sys
import matplotlib.pyplot as plt
import numpy as np
import copy
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

    def draw(self):
        # self.drawer[drawfunc](args)
        # self.d()
        if self.form == 'circle':
            print(self.p)
            # self.drawer.arc(self.bounds, 0, 360, fill=0)
            self.drawer.ellipse(self.bounds, fill=self.fill)
        return self
