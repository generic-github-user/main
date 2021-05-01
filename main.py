from tkinter import *
import random
import numpy as np
import time
import matplotlib.pyplot as plt
from colour import Color
from scipy import signal

class Automata:
    """A generic cellular automaton world"""

    def __init__(self, size=None, birth=[3], live=[2, 3], neighborhood=1):
        if size is None:
            size = [64, 64]
        self.size = np.array(size)
        self.cell_width = 10
        self.world = np.random.randint(0, 2, self.size)
        # self.world = np.zeros(self.size)
        # self.world[10:12,10:12]=1
        self.zoom = 1

        if type(birth[0]) in [tuple, list]:
            birth = [random.randint(*b) for b in birth]
        self.birth = birth
        self.live = live

        self.population = []
        self.generation = 0
        self.age = np.zeros(self.size)
        self.neighbors = np.zeros(self.size)
        self.age_history = []

        if type(neighborhood) in [tuple, list]:
            neighborhood = random.randint(*neighborhood)
        self.neighborhood = neighborhood

        self.conv = np.ones([self.neighborhood*2+1]*2)
        # np.put(self.conv, self.neighborhood**2//2, 0)
        np.put(self.conv, self.conv.size//2, 0)
        print(self.conv)

    def evolve(self, n=1, use_convolutions=True):
        # for i in range(n)
        if use_convolutions:
            self.temp = self.world.copy()
            n = signal.convolve2d(self.temp, self.conv, boundary='wrap')
            n = n[1:-1, 1:-1]
            # print(n.shape)
            # print(np.isin(np.array([2, 3, 5]), self.live))
            birth_cond = np.logical_and(self.temp == 0, np.isin(n, self.birth))
            survival_cond = np.logical_and(self.temp == 1, np.isin(n, self.live))
            indices = np.where(np.logical_or(survival_cond, birth_cond), 1, 0)
            # self.world = np.where(indices == 1)
            # self.world = indices
            self.world = indices.copy()
            # print(indices, n)
        else:
            self.temp = np.pad(self.world.copy(), self.neighborhood, constant_values=0)
            for ix, iy in np.ndindex(self.world.shape):
                # :/
                current = self.world[ix, iy]
                neighbors = np.sum(self.temp[ix:ix+2+self.neighborhood, iy:iy+2+self.neighborhood]) - self.temp[ix+self.neighborhood, iy+self.neighborhood]
                self.neighbors[ix, iy] = neighbors
                # print(temp[ix-1:ix+2, iy-1:iy+2])
                # print(temp[ix:ix+3, iy:iy+3])
                # print(ix-1, ix, ix+1, iy-1, iy, iy+1)
                # print(neighbors)
                if neighbors in self.birth:
                    self.world[ix, iy] = 1
                # elif?
                if neighbors not in self.live:
                    self.world[ix, iy] = 0
                    self.age[ix, iy] = 0
                else:
                    self.age[ix, iy] += 1

        self.population.append(self.world.sum())
        self.age_history.append(self.age.mean())
        self.generation += 1
        self.compute = self.generation * np.product(self.world.shape)
        # print(temp.shape)

class Aggregator:
    def __init__(self):
        self.simulations = []

class CGOL(Automata):
    """Convenience class that produces a cellular automata based on Conway's Game of Life"""

    def __init__(self):
        super(CGOL, self).__init__()


class Scene:
    def __init__(self, content=None):
        self.root = Tk()
        # root.title()
        # root.resizable(False, False)
        if content is None:
            content = Automata(size=[64, 64])
        self.content = content
        self.dimensions = self.content.size * self.content.cell_width
        w, h = self.dimensions
        self.canvas = Canvas(self.root, width = w, height = h)
        self.canvas.pack()

        def click_callback(event):
            # print(event.x, event.y)
            coords = event.x, event.y
            coords = np.array(coords)
            cw = self.content.cell_width
            coords = tuple(np.round(coords / cw).astype(int))
            print(coords)
            self.content.world[coords] = 1
            self.content.temp[coords] = 1

        self.canvas.bind("<B1-Motion>", click_callback)
    def step(self, i=0, n=20, render=True, cell_colors='age'):
        color_source = getattr(self.content, cell_colors)
        if i < n:
            self.content.evolve()
            # self.canvas.create_rectangle(20, 20, 50, 50, fill='red')
            world = self.content.world
            self.canvas.delete('all')
            # print(np.where(world == 1))
            width = self.content.cell_width
            for ix, iy in zip(*np.where(world == 1)):
                x, y = ix * width, iy * width
                intensity = color_source[ix, iy] / color_source.max()
                c = Color(hue=intensity, saturation=1, luminance=0.5)
                hex = c.hex
                self.canvas.create_rectangle(x, y, x+width, y+width, fill=hex)
            self.canvas.after(1, lambda: self.step(i=i+1, n=n, render=render))
        else:
            self.end_time = time.time()
            elapsed = round(self.end_time-self.start_time, 1)
            print('Simulated {} frames in {} seconds ({} cells processed)'.format(n, elapsed, self.content.compute))
    def simulate(self, frames=10, render=True):
        self.start_time = time.time()
        self.step(n=frames, render=render)

live_rule = [random.randint(3, 10) for v in range(2)]
# automata = Automata(birth=[(2,4)], live=live_rule, neighborhood=(1,2))
automata = CGOL()
main_scene = Scene(content=automata)
main_scene.simulate(frames=500, render=False)
main_scene.root.mainloop()

# plt.plot(main_scene.content.population)
# plt.plot(main_scene.content.age_history)
# plt.show()

# TODO: cube visualization, pattern search
