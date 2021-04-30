from tkinter import *
import random
import numpy as np
import time
import matplotlib.pyplot as plt

class Automata:
    """A generic cellular automaton world"""

    def __init__(self, size=None):
        if size is None:
            size = [64, 64]
        self.size = np.array(size)
        self.cell_width = 10
        self.world = np.random.randint(0, 2, self.size)
        # self.world = np.zeros(self.size)
        self.zoom = 1
        self.birth = [3]
        self.live = [2, 3]
        self.population = []

    def evolve(self):
        temp = np.pad(self.world.copy(), 1, constant_values=0)
        for ix, iy in np.ndindex(self.world.shape):
            # :/
            current = self.world[ix, iy]
            neighbors = np.sum(temp[ix:ix+3, iy:iy+3]) - temp[ix+1, iy+1]
            # print(temp[ix-1:ix+2, iy-1:iy+2])
            # print(temp[ix:ix+3, iy:iy+3])
            # print(ix-1, ix, ix+1, iy-1, iy, iy+1)
            # print(neighbors)
            if neighbors in self.birth:
                self.world[ix, iy] = 1
            # elif?
            if neighbors not in self.live:
                self.world[ix, iy] = 0
        self.population.append(self.world.sum())
        # print(temp.shape)


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
    def step(self, i=0, n=20, render=True):
        if i < n:
            self.content.evolve()
            # self.canvas.create_rectangle(20, 20, 50, 50, fill='red')
            world = self.content.world
            self.canvas.delete('all')
            # print(np.where(world == 1))
            width = self.content.cell_width
            for ix, iy in zip(*np.where(world == 1)):
                x, y = ix * width, iy * width
                self.canvas.create_rectangle(x, y, x+width, y+width, fill='red')
            self.canvas.after(1, lambda: self.step(i=i+1, n=n, render=render))
        else:
            self.end_time = time.time()
            elapsed = round(self.end_time-self.start_time, 1)
            print('Simulated {} frames in {} seconds'.format(n, elapsed))
    def simulate(self, frames=10):
        self.start_time = time.time()
        self.step(n=frames, render=render)

main_scene = Scene()
main_scene.simulate(frames=500, render=False)
main_scene.root.mainloop()

plt.plot(main_scene.content.population)
plt.show()

# TODO: cube visualization, pattern search
