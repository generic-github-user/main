from tkinter import *
import random
import numpy as np

class Automata:
    """A generic cellular automaton world"""

    def __init__(self, size=None):
        if size is None:
            size = [64, 64]
        self.size = size
        self.cell_width = 10
        self.world = np.random.randint(0, 2, self.size)
        # self.world = np.zeros(self.size)
        self.zoom = 1
        self.birth = [3]
        self.live = [2, 3]

    def evolve(self):
        temp = np.pad(self.world.copy(), 1, constant_values=0)
        for ix, iy in np.ndindex(self.world.shape):
            # :/
            current = self.world[ix, iy]
            neighbors = np.sum(temp[ix:ix+3, iy:iy+3]) - temp[ix+1, iy+1]
            # print(temp[ix-1:ix+2, iy-1:iy+2])
            print(temp[ix:ix+3, iy:iy+3])
            # print(ix-1, ix, ix+1, iy-1, iy, iy+1)
            # print(neighbors)
            if neighbors in self.birth:
                self.world[ix, iy] = 1
            # elif?
            if neighbors not in self.live:
                self.world[ix, iy] = 0
        # print(temp.shape)


class Scene:
    def __init__(self):
        self.root = Tk()
        # root.title()
        # root.resizable(False, False)
        self.canvas = Canvas(self.root, width = 400, height = 400)
        self.canvas.pack()
    def step(self, i=0, n=10):
        self.canvas.create_rectangle(20, 20, 50, 50, fill='red')
        self.canvas.after(50, lambda: self.step(i=i+1))

main_scene = Scene()
main_scene.step()
main_scene.root.mainloop()
