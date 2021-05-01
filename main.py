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
        elif type(size) is int:
            size = [size] * 2
        self.size = np.array(size)
        self.cell_width = 5
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

        self.kernel = np.ones([self.neighborhood*2+1]*2)
        # np.put(self.conv, self.neighborhood**2//2, 0)
        np.put(self.kernel, self.kernel.size//2, 0)
        # print(self.conv)

    def evolve(self, n=1, use_convolutions=True):
        # for i in range(n)
        if use_convolutions:
            self.temp = self.world.copy()
            n = signal.convolve2d(self.temp, self.kernel, boundary='wrap')
            n = n[1:-1, 1:-1]
            # print(n.shape)
            # print(np.isin(np.array([2, 3, 5]), self.live))
            birth_cond = np.logical_and(self.temp == 0, np.isin(n, self.birth))
            survival_cond = np.logical_and(self.temp == 1, np.isin(n, self.live))
            indices = np.where(np.logical_or(survival_cond, birth_cond), 1, 0)
            # self.world = np.where(indices == 1)
            # self.world = indices
            self.world = indices.copy()
            self.age += indices
            self.age *= indices
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

        return self.world
        # print(temp.shape)

class Aggregator:
    def __init__(self, hyperparameters=None, metrics=None, selection='random', randomizer=random.uniform, trials=20):
        self.simulations = []
        if hyperparameters is None:
            hyperparameters = {
                'size': 32
            }
        if metrics is None:
            metrics = ['population', 'age_history']

        self.hyperparameters = hyperparameters
        self.hp = self.hyperparameters
        self.metrics = metrics
        self.results = []
        self.trials = trials

    def run(self, trials=None):
        if trials is None:
            trials = self.trials
        print('Running {} trials'.format(trials))

        for t in range(trials):
            trial = Automata()
            for g in range(100):
                trial.evolve(use_convolutions=True)
            self.results.append([getattr(trial, m)[-1] for m in self.metrics])

    def display(self):
        print(list(zip(*self.results)))
        plt.scatter(*zip(*self.results))
        plt.show()

class CGOL(Automata):
    """Convenience class that produces a cellular automata based on Conway's Game of Life"""

    def __init__(self, **kwargs):
        super(CGOL, self).__init__(**kwargs)


class Scene:
    def __init__(self, content=None):
        self.root = Tk()
        # root.title()
        # root.resizable(False, False)
        if content is None:
            content = Automata()
        self.content = content
        self.dimensions = self.content.size * self.content.cell_width
        w, h = self.dimensions
        self.canvas = Canvas(self.root, width = w, height = h)
        self.canvas.pack()
        self.m = []
        self.paused = False
        self.pen_size = 1
        # self.canvas.mainloop()

    # self.canvas.bind("<B1-Motion>", click_callback)
    def click_callback(self, event):
        # print(event.x, event.y)
        print(event)
        coords = event.x, event.y
        coords = np.array(coords)
        cw = self.content.cell_width
        coords = np.round(coords / cw).astype(int)
        print(coords)
        x, y = tuple(coords)
        p = self.pen_size
        x_, y_ = x+p, y+p
        self.content.world[x:x_, y:y_] = 1
        self.content.temp[x:x_, y:y_] = 1
        x, y = coords * cw
        print(x, y)
        self.m.append(event)
        # self.canvas.create_rectangle(x, y, x+cw, y+cw, fill='green')
        # self.root.update_idletasks()
        # self.canvas.update_idletasks()
        # self.canvas.draw_idle()

    def right_click(self, event):
        coords = event.x, event.y
        coords = np.array(coords)
        cw = self.content.cell_width
        coords = np.round(coords / cw).astype(int)
        self.content.world[tuple(coords)] = 0
        self.content.temp[tuple(coords)] = 0

    def toggle_pause(self, event):
        if self.paused:
            self.paused = False
        else:
            self.paused = True

    def key_press(self, event):
        char = event.char
        # print(char)
        if char == '-' and self.pen_size > 1:
            self.pen_size -= 1
        elif char == '=' and self.pen_size < 100:
            self.pen_size += 1
        print('Changed pen size to {}'.format(self.pen_size))
        # self.canvas.update_idletasks()

    def step(self, i=0, n=20, render=True, cell_colors='age'):
        color_source = getattr(self.content, cell_colors)
        if i < n:
            # new_frame = self.content.evolve()
            if not self.paused:
                self.content.evolve()
            # print(new_frame.mean())
            # self.canvas.create_rectangle(20, 20, 50, 50, fill='red')
            world = self.content.world
            new_frame = world
            self.canvas.delete('all')
            # print(len(self.m))
            # print(np.where(world == 1))
            width = self.content.cell_width
            for ix, iy in zip(*np.where(new_frame)):
                x, y = ix * width, iy * width
                intensity = color_source[ix, iy] / color_source.max()
                c = Color(hue=intensity, saturation=1, luminance=0.5)
                hex = c.hex
                self.canvas.create_rectangle(x, y, x+width, y+width, fill=hex)
            self.canvas.after(1, lambda: self.step(i=i+1, n=n, render=render))
            self.canvas.bind("<B1-Motion>", self.click_callback)
            self.canvas.bind("<B3-Motion>", self.right_click)
            self.canvas.bind("<Double-Button-1>", self.toggle_pause)
            self.root.bind("<Key>", self.key_press)
        else:
            self.end_time = time.time()
            elapsed = round(self.end_time-self.start_time, 1)
            print('Simulated {} frames in {} seconds ({} cells processed)'.format(n, elapsed, self.content.compute))
    def simulate(self, frames=10, render=True):
        self.start_time = time.time()
        self.step(n=frames, render=render)

live_rule = [random.randint(3, 10) for v in range(2)]
# automata = Automata(birth=[(2,4)], live=live_rule, neighborhood=(1,2))
automata = CGOL(size=128)
main_scene = Scene(content=automata)
main_scene.simulate(frames=500, render=False)
main_scene.root.mainloop()

# plt.plot(main_scene.content.population)
# plt.plot(main_scene.content.age_history)
# plt.show()

# TODO: cube visualization, pattern search
