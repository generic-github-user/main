import time
import random
import string
from fuzzywuzzy import fuzz, process

from test import Test

keyboard_layout = """
~!@#$%^&*()_+
`1234567890-=
QWERTYUIOP{}|
qwertyuiop[]\\
ASDFGHJKL:"
asdfghjkl;'
ZXCVBNM<>?
zxcvbnm,./
"""

# @test
class Alternation(Test):
    default_plot = ['length', 'elapsed', 'score']
    def __init__(self, length=None, substring_length=2, ignore_trailing=True, adjacent=False, **kwargs):
        if length is None:
            length = random.randint(10, 40)
        super().__init__()
        target = ''.join(random.choices(string.ascii_lowercase, k=substring_length))
        self.length = length
        self.target = (target*(self.length//substring_length+1))[:self.length]
        self.ignore_trailing = ignore_trailing

        defaults = []
        for k, v in kwargs.items():
            setattr(self, k, v)

    # def generate_statistics

    def calculate_score(self):
        return self.accuracy * (self.length / self.elapsed)

    def run(self):
        self.started = time.time()
        print(self.target)
        self.user_input = input()
        self.ended = time.time()
        self.elapsed = self.ended - self.started
        input_string = self.user_input
        if self.ignore_trailing:
            input_string = input_string[:self.length]
        self.accuracy = fuzz.WRatio(self.target, self.user_input)
        self.score = self.calculate_score()
        return self

    def upgrade(self, *args, **kwargs):
        super().upgrade(*args, **kwargs)
        if not hasattr(self, 'score'):
            self.score = self.calculate_score()
