import numpy as np
import matplotlib.pyplot as plt
import math

# Line generator credit:
# Marco Spinaci
# https://stackoverflow.com/a/47381058
# (CC BY-SA 3.0); https://creativecommons.org/licenses/by-sa/3.0/
def trapez(y,y0,w):
    return np.clip(np.minimum(y+1+w/2-y0, -y+1+w/2+y0),0,1)

def weighted_line(r0, c0, r1, c1, w, rmin=0, rmax=np.inf):
    # The algorithm below works fine if c1 >= c0 and c1-c0 >= abs(r1-r0).
    # If either of these cases are violated, do some switches.
    if abs(c1-c0) < abs(r1-r0):
        # Switch x and y, and switch again when returning.
        xx, yy, val = weighted_line(c0, r0, c1, r1, w, rmin=rmin, rmax=rmax)
        return (yy, xx, val)

    # At this point we know that the distance in columns (x) is greater
    # than that in rows (y). Possibly one more switch if c0 > c1.
    if c0 > c1:
        return weighted_line(r1, c1, r0, c0, w, rmin=rmin, rmax=rmax)

    # The following is now always < 1 in abs
    slope = (r1-r0) / (c1-c0)

    # Adjust weight by the slope
    w *= np.sqrt(1+np.abs(slope)) / 2

    # We write y as a function of x, because the slope is always <= 1
    # (in absolute value)
    x = np.arange(c0, c1+1, dtype=float)
    y = x * slope + (c1*r0-c0*r1) / (c1-c0)

    # Now instead of 2 values for y, we have 2*np.ceil(w/2).
    # All values are 1 except the upmost and bottommost.
    thickness = np.ceil(w/2)
    yy = (np.floor(y).reshape(-1,1) + np.arange(-thickness-1,thickness+2).reshape(1,-1))
    xx = np.repeat(x, yy.shape[1])
    vals = trapez(yy, y.reshape(-1,1), w).flatten()

    yy = yy.flatten()

    # Exclude useless parts and those outside of the interval
    # to avoid parts outside of the picture
    mask = np.logical_and.reduce((yy >= rmin, yy < rmax, vals > 0))

    return (yy[mask].astype(int), xx[mask].astype(int), vals[mask])

# Point rotation functions credit:
# Lyle Scott, III  // lyle@ls3.io
# https://gist.github.com/LyleScott/e36e08bfb23b1f87af68c9051f985302

def rotate_via_numpy(xy, radians):
    """Use numpy to build a rotation matrix and take the dot product."""
    x, y = xy
    c, s = np.cos(radians), np.sin(radians)
    j = np.matrix([[c, s], [-s, c]])
    m = np.dot(j, [x, y])

    return float(m.T[0]), float(m.T[1])


def rotate_origin_only(xy, radians):
    """Only rotate a point around the origin (0, 0)."""
    x, y = xy
    xx = x * math.cos(radians) + y * math.sin(radians)
    yy = -x * math.sin(radians) + y * math.cos(radians)

    return xx, yy


def rotate_around_point_lowperf(point, radians, origin=(0, 0)):
    """Rotate a point around a given point.

    I call this the "low performance" version since it's recalculating
    the same values more than once [cos(radians), sin(radians), x-ox, y-oy).
    It's more readable than the next function, though.
    """
    x, y = point
    ox, oy = origin

    qx = ox + math.cos(radians) * (x - ox) + math.sin(radians) * (y - oy)
    qy = oy + -math.sin(radians) * (x - ox) + math.cos(radians) * (y - oy)

    return qx, qy


def rotate_around_point_highperf(xy, radians, origin=(0, 0)):
    """Rotate a point around a given point.

    I call this the "high performance" version since we're caching some
    values that are needed >1 time. It's less readable than the previous
    function but it's faster.
    """
    x, y = xy
    offset_x, offset_y = origin
    adjusted_x = (x - offset_x)
    adjusted_y = (y - offset_y)
    cos_rad = math.cos(radians)
    sin_rad = math.sin(radians)
    qx = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
    qy = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y

    return qx, qy
rfast = rotate_around_point_highperf

class Spinner:
    def __init__(self, theta=0, speed=0.05, radius=30, linewidth=1, opacity=1):
        self.spinners = []
        self.speed = speed
        self.radius = self.r = radius
        self.theta = theta
        self.position = [0, self.r]
        self.x, self.y = self.position
        self.linewidth = self.lw = linewidth
        self.opacity = opacity
        self.render = True

    def step(self, w=1):
        self.theta += self.speed * w
        self.theta = self.theta % 2*math.pi
        self.position = [*rfast(self.position, self.theta)]
        # print(self.position)
        for s in self.spinners:
            s.step(w)

    def draw(self, c, method='add'):
        for s in self.spinners:
            # c +=
            c = s.draw(c, method=method)
            # s.draw(c)
        if self.render:
            offset = np.array(c.shape) / 2
            x_, y_ = (np.array(self.position, dtype='int') + offset).astype('int')
            lw = self.lw
            # print(self.position)
            # c[self.x: self.x+self.lw, self.y: self.y+self.lw] += self.opacity
            if method == 'add':
                c[x_:x_+lw, y_:y_+lw] += self.opacity
            elif method == 'set':
                c[x_:x_+lw, y_:y_+lw] = self.opacity
        return c

    def add(self, s):
        s.parent = self
        self.spinners.append(s)
        return self

class Roulette:
    def __init__(self, base=None, dims=None):
        if base is None:
            self.base = Spinner()
            self.base.add(Spinner(radius=10, speed=0.001))
        else:
            self.base = base

        if dims is None:
            dims = [100, 100]
        self.dimensions = self.dims = dims

        self.canvas = np.zeros(self.dims)

    def step(self, n=1, w=1, r=True, method='set'):
        for i in range(n):
            self.base.step(w)
            if r:
                self.render(method=method)

    def render(self, method='add'):
        if len(self.dims) == 2:
            # self.base.draw(c=self.canvas)
            self.canvas = self.base.draw(c=self.canvas, method=method)

        return self.canvas


r = Roulette(dims=[300]*2)
r.step(n=300, method='set')
im = r.render(method='set')
plt.imshow(im)
plt.show()
# input()
