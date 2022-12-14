__all__ = ['Attractor', 'IteratedFunctionSystem', 'rotation_matrix', 'rotate', 'simulate_accelerated', 'line',
           'RouletteCurve']

import IPython
# IPython.get_ipython().run_line_magic('matplotlib', 'widget')

import matplotlib
import matplotlib.pyplot as plt

import numpy as np
import numba as nb
import math
import random

import time
from scipy import signal, misc

from line import line
from rotate import rotate, rotation_matrix
from simulate import simulate_accelerated
from attractor import Attractor, IteratedFunctionSystem

# @nb.jit
class RouletteCurve(Attractor):
    def __init__(self, center=[0, 0], num_sections=4, lengths=None, speeds=None, random_distribution='uniform'):
        """
        Create a new `RouletteCurve` object. This subclasses `Attractor` and
        describes a process where one or more line segments, connected
        end-to-end, rotate continuously about their pivots/endpoints. The
        length of each line segment and the speed at which it rotates are
        adjustable parameters.

        -`center`: A `list`/`tuple`/`ndarray` of `float`s or `int`s; the pivot
        point/base of the first arm
        -`num_sections`: `int` >= 1; the number of arms/sections used to
        simulate the system. This will be used to randomly generate the lengths
        and speeds of each arm if those parameters are not provided
        -`lengths`: A `list`/`tuple`/`ndarray` of `float`s or `int`s > 0;
        length of each arm in n-dimensional Euclidian space
        -`speeds`: A `list`/`tuple`/`ndarray` of `float`s or `int`s; how
        quickly each arm rotates (note that negative values may be used for
        counterclockwise rotation, and 0 may be used for arms that do not
        rotate)
        -`random_distribution`: `'uniform'` or `'normal'`; what distribution to
        draw the lengths and speeds from if they are not provided

        Returns a `RouletteCurve` instance.
        """

        super().__init__()
        self.random_distribution = getattr(np.random, random_distribution)
        self.rd = self.random_distribution
        assert center
        self.center = np.array(center, dtype=float)
        self.rank = self.center.size
#         use rank?
        if lengths is None:
            assert num_sections
            lengths = np.random.uniform(-2, 2, num_sections)
        if speeds is None:
            assert num_sections
            speeds = np.random.normal(0, 2, num_sections)
        self.lengths = RouletteCurve.randomize_list(lengths).astype(float)
        self.speeds = RouletteCurve.randomize_list(speeds).astype(float)
#         self.angles = np.random.normal(0, 2*math.pi, num_sections).astype(float)
        self.angles = np.zeros(num_sections, dtype=float)
        self.angles_ = []
        self.start = center + np.array([[0, sum(self.lengths[:i])] for i in range(1, len(self.lengths)+1)])
        self.start = self.start.astype(float)
        self.pivots = self.start.copy()
        self.pivots_ = []
        self.points = np.zeros([1, 2])
        self.canvas = np.zeros([100, 100])
        self.position = 0

        self.zoom = 10
        self.offset = 0
        self.N = 0
        self.live_rendering = False

#         See colormaps by category at https://matplotlib.org/stable/tutorials/colors/colormaps.html; used here are the "sequential" cmaps and a few others
        self.cmaps = ['inferno', 'plasma', 'rainbow', 'hot', 'cool', 'autumn', 'winter', 'summer'] + [
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']

    def clear(self):
        """
        Remove all generated points from this `Attractor`

        Returns the class instance (a `RouletteCurve` object).
        """
        self.points = np.zeros([1, 2])
        return self

    def get_state(self):
        """
        Internal/helper function; gets current values of this instance's
        speeds, pivots, angles, etc. as a dictionary (mainly for use in typed
        functions like simulate_accelerated)

        Returns a `dict`
        """
        return dict(
            speeds=self.speeds,
            pivots=self.pivots,
            center=self.center,
            angles=self.angles,
            start=self.start,
            points=self.points
        )

    def simulate_accelerated(self, steps, duration=None):
        """
        A faster (but less dynamic) version of `simulate` based on Numba. The
        actual computation is offloaded to a simplified, strongly typed global
        function. This method is several times faster than `simulate`,
        especially for more complex `Attractor`s.

        Returns the class instance (a `RouletteCurve` object).
        """
        assert steps or duration
        start_time = time.time()
        sim_args = dict(
            **self.get_state(),
            steps=steps,
            clip=True
        )
        if duration:
            while (time.time() - start_time) < duration:
                self.start = self.pivots.copy()
                new_points = simulate_accelerated(**sim_args)
                self.points = np.append(self.points, new_points.copy(), axis=0)
#                 why does refreshing these change the pattern? (m=2)
                sim_args = dict(**self.get_state(), steps=steps, clip=True)
        else:
            self.points = simulate_accelerated(**sim_args)

        return self

#     @nb.jit#(forceobj=True)
    def simulate(self, steps=None, render_each=None, render_settings={}, clip=True, duration=None, timecheck_frequency=100, live_rendering=True):
        """
        Simulate the system by calculating the position of each point from data
        about the preceding points, and updating the internal state
        accordingly.

        - `steps`: (optional) integer >=1; the number of timesteps to simulate
        - `render_each`: (optional) integer >=1 representing how many steps to
          run before re-rendering the simulation result
        - `render_settings`: (optional) a `dictionary` that will be passed to
          `render` if using `render_each`
        - `clip`: `boolean`; whether to limit the maximum angle of each section
          (if `True`, the values will wrap around to 0; defaults to `True`)
        - `duration`: `float` or `int` >0; the maximum length of time, in
          seconds, to run the simulation for; if `steps` is not provided, the
          simulation will run until this amount of time has elapsed
        - `timecheck_frequency`: Not yet documented
        - `live_rendering`: Not yet documented

        Returns the class instance (a `RouletteCurve` object).
        """

        self.live_rendering = live_rendering
        start_time = time.time()
        rMatrices = []
        assert self.speeds
        for s in self.speeds:
#             theta = 1 * self.speeds[l]
            rMatrices.append(rotation_matrix(s))
        print(duration)
#         for s in range(steps):
        assert steps or duration, 'Either the number of steps to simulate or the length of time to run the simulation for must be provided.'
        if duration:
            assert duration > 0
            assert isinstance(duration, (int, float))
        s = 0
        while (s < steps if steps else True):
#             last = self.pivots.copy()
#             for l in list(range(len(self.pivots)))[::-1]:
            gamma = 0
            num_pivots = len(self.pivots)
            for l in list(range(num_pivots)):
#             theta = 1 * self.speeds
                rMatrix = rMatrices[l]
#                 rMatrix = np.array(rMatrix)#.swapaxes(0,2)
                offsets = self.center if l == 0 else self.pivots[l-1]#.copy() #?
#                 for f in list(range(l, num_pivots)):
    #                 print(s, rMatrix)
        #             print(self.pivots[:-1].shape)
    #                 offsets = np.concatenate([self.center[np.newaxis,...], self.pivots[:-1]], axis=0)
    #                 offsets=np.array(0)
    #                 len(self.pivots)-1
    #                 print(offsets)
        #             print(offsets.shape, rMatrix.shape, self.pivots.shape)
    #                 self.pivots[l] = (last[l] - offsets) @ rMatrix + offsets

    #                 func of t?
    #                 delta = (last[l] - offsets) @ rMatrix + offsets
#                     delta = (rMatrix @ (self.pivots[f] - offsets)) + offsets# + gamma
    #                 print(delta)
#                     gamma += delta
#                     self.pivots[f] = delta

                self.angles[l:] += self.speeds[l]
                if clip:
                    self.angles[l:] %= 2 * math.pi
#                 self.angles_.append(self.angles.copy())

    #             self.points.append(np.clip(self.pivots[-1], 0, np.array(self.canvas.shape)))
#     sequencemethod

            prev = rotate(self.start[0], self.center, self.angles[0])
            for p in range(1, num_pivots):
#                 print(p, prev)
                self.pivots[p] = rotate(self.start[p], self.center, self.angles[p]) + prev
                prev = self.pivots[p]

            if self.live_rendering:
                self.draw_point(self.pivots[-1].copy(), mode='pixel')
            else:
#                 self.pivots_.append(self.pivots.copy())
#                 self.points.append(self.pivots[-1].copy())
#                 self.points = np.concatenate([self.points, self.pivots[-1].copy()[np.newaxis, ...]], axis=0)
                self.points = np.append(self.points, self.pivots[-1].copy()[np.newaxis, ...], axis=0)

            if render_each is not None:
                assert isinstance(render_each, int)
                assert render_each >= 1
                if s % render_each == 0:
                    assert render_settings is none or isinstance(render_settings, dict)
                    self.render(**render_settings)

            if (duration is not None) and s % timecheck_frequency == 0:
                elapsed = time.time() - start_time
                if elapsed > duration:
#                     make a function for this?
                    comp = f'; {round(s / steps * 100, 3)}% complete)' if steps else ''
                    g = 'Terminating simulation early' if steps else 'Ending simulation'
                    print(f'{g} after {s+1} steps ({round(elapsed, 3)} seconds elapsed)' + comp)
                    break
            s += 1
        self.N = s
        print(f'Finished simulating {steps or s+1} steps in {round(elapsed, 3)} seconds')
        return self

    def transform_point(self, p):
        """
        Apply transformations to a point to prepare it for rendering.

        -p: The point to transform

        Returns the transformed point
        """

        p = p.astype(float)
        p *= self.zoom
#         if recenter:
        p += self.offset
        p = np.clip(p, 0, np.array(self.canvas.shape)-1)
        assert isinstance(p, np.ndarray)
        return p

    def draw_point(self, p, mode, blending='add', brush=None):
        """
        Draw a point on this `RouletteCurve`'s canvas.

        -p: The point to render
        -mode: See the `mode` parameter from `render`
        -blending: See the `blending` parameter from `render`
        -brush: An `ndarray`; the brush to apply at each point

        Returns `self` (the class instance; a `RouletteCurve` object).
        """

        if type(p) is int:
            prev = self.points[p-1]
            prev = self.transform_point(prev)
            p = self.points[p]
        else:
            assert isinstance(p, (np.ndarray, list, tuple))
        p = self.transform_point(p)
        w, h = self.canvas.shape
        x, y = p.astype(int)
        if mode == 'pixel':
            if blending == 'set':
                self.canvas[x, y] = 1
            elif blending == 'add':
                self.canvas[x, y] += 1
#                 TODO: add multiply mode
            else:
                raise ValueError
        elif mode in ['dist', 'brush']:
            assert isinstance(brush, np.ndarray)
            x, y = np.clip(x, 5, w-6), np.clip(y, 5, h-6)
            self.canvas[x-2:x+3, y-2:y+3] += brush
        elif mode in ['line']:
            assert prev is not None
            self.canvas = line(prev, p, self.canvas)
        else:
            raise ValueError
        return self

#     @nb.jit(forceobj=True)
    def render(self, discard=False, clip=False, axis=None, recenter=True, zoom=None, mode='line', blending='add', hist_args={}, cmap='random', point_value=1, falloff=3, **kwargs):
        """
        Render an image from the list of points stored in the class instance.

        - `discard`: `boolean`; if `True`, clear this `Attractor`'s points
          after rendering to free up memory
        - `axis`: A Matplotlib axis to render the finished image to (if one is
          not provided, it will be created)
        - `zoom`: A scaling factor by which to resize points relative to the
          `center` before rendering
        - `mode`: `str`, one of `pixel`, `dist`/`brush`, `line`, or `hist`
            -     `pixel`: Convert each point coordinate to the (integer)
                  coordinate of the nearest pixel
            -     `dist`: Generate a "brush" based on a distance function
                  relative to the point coordinates, then (for each point)
                  paint this over a region of the canvas centered on that point
            -     `line`: Draw a line from the last rendered point to the
                  current one (helpful for reducing the total number of points
                  that must be rendered)
            -     `hist`: Generate a 2D histogram using NumPy and display this
                  (similar to `pixel`)
        - `blending`: `str`, one of `set`, `add`, or `mul`; how the new pixel
          value (while rendering a point) should be combined with the current
          one
        - `cmap`: `random` or a Matplotlib colormap; the colormap to pass to
          `imshow` - if `random`, one will be selected from the sequential
          colormaps listed in `RouletteCurve().cmaps`
        - `point_value`
        - `**kwargs`
        """

        assert mode in ['hist', 'dist', 'brush', 'pixel', 'line']
        assert len(self.points) >= 1
        self.points = self.points[1:]
        cshape = np.array(self.canvas.shape)
        self.offset = cshape / 2
        if not self.live_rendering:# and (self.points):
            if zoom is None:
                zoom = np.min(cshape / np.max(np.abs(self.points), axis=0)) * 0.5
#             else:
            assert isinstance(zoom, (int, float))
            self.zoom = zoom
#         for p in self.points.copy():
        if mode == 'dist':
#             grid = np.stack(np.meshgrid([np.arange(5.)]*2))
            grid = np.mgrid[0:5, 0:5]
            assert isinstance(falloff, int) and falloff >= 1
            brush = 1 / np.linalg.norm(grid - 2.5, axis=0, ord=falloff)
            print(brush)

        if not self.live_rendering:
            if mode == 'hist':
                assert hist_args is None or isinstance(hist_args, dict)
                self.canvas = np.histogram2d(*np.array(self.points).T, **hist_args)[0]
                assert isinstance(point_value, (int, float))
#                 self.canvas *= point_value
                if blending == 'set':
    #                 self.canvas = np.power(self.canvas, 0)
                    self.canvas[self.canvas != 0] = point_value
                elif blending == 'mul':
                    self.canvas = point_value ** self.canvas
                else:
                    assert blending == 'add'
            else:
                if mode in ['line']:
                    for i in range(1, len(self.points)):
#                         self.canvas = line(self.points[i-1], self.points[i], self.canvas)
                        self.draw_point(i, mode=mode)
                else:
                    for i, p in enumerate(map(np.copy, self.points)):
            #             for j, p in enumerate(px):
                        if mode in ['dist', 'brush']:
                            self.draw_point(p, mode=mode, brush=brush)
                        else:
                            self.draw_point(p, mode=mode)
            #                 self.canvas[x, y] = j+1
            #         plt.style.use('fivethirtyeight')


#         pendulums
        if cmap == 'random':
            cmap = random.choice(self.cmaps)
        else:
            assert (isinstance(cmap, str) and cmap in self.cmaps) or (isinstance(plt.cm.colors.Colormap) or cmap in plt.colormaps())

        plot_args = dict(X=np.flip(self.canvas.T, axis=0), interpolation='none', cmap=cmap, **kwargs)
        if axis:
            P = axis.imshow(**plot_args)
        else:
            plt.style.use('classic')
            P = plt.imshow(**plot_args)
            plt.grid('off')

        if discard:
            self.clear()
        if clip:
            assert len(clip) == 2
            assert isinstance(clip, (np.ndarray, list, tuple))
            self.canvas = np.clip(self.canvas, *clip)

        return P
#         return self

    @staticmethod
    def randomize_list(L):
        assert isinstance(L, (np.ndarray, list, tuple))
        return np.array([self.rd(*x) if type(x) in [list, tuple] else x for x in L])
