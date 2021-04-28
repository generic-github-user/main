from tkinter import *
import random
import numpy as np

class Automata:
    """A generic cellular automaton world"""

    def __init__(self, size):
        if size is None:
            size = [64, 64]
        self.size = size


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
