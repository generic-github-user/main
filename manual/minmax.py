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

    def calculate_score(self):
        return self.accuracy

    def run(self):
        self.started = time.time()
        print(f'Find the {self.goal} of these values:')
        for value in self.values:
            print(f'[{value}]')
        self.user_input = input()
        self.ended = time.time()
        self.elapsed = self.ended - self.started
        self.accuracy = int(int(self.user_input) == self.target)
        self.score = self.calculate_score()
        return self

    def upgrade(self, *args, **kwargs):
        super().upgrade(*args, **kwargs)
        if not hasattr(self, 'score'):
            self.score = self.calculate_score()
