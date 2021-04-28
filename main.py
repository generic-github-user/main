from tkinter import *
import random
import numpy as np

root = Tk()
# root.title()
# root.resizable(False, False)
canvas = Canvas(root, width = 400, height = 400)
canvas.pack()

def step(i=0, n=10):
    canvas.create_rectangle(20, 20, 50, 50, fill='red')
    canvas.after(50, lambda: step(i=i+1))

step()
root.mainloop()
