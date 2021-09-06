import numpy as np
import time

from test import Test

class MinMax(Test):
    default_plot = ['length', 'elapsed', 'score']
    def __init__(self, minimum=0, maximum=100, number=5, goal='max'):
        self.minimum = minimum
        self.maximum = maximum
        self.number = number
        self.goal = goal
        self.values = np.random.randint(minimum, maximum, size=number)
        self.target = getattr(self.values, self.goal)()
