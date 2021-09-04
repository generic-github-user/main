import time
import random
import string
from fuzzywuzzy import fuzz, process

from test import Test
# @test
class Alternation(Test):
    def __init__(self, length=None, substring_length=2, ignore_trailing=True):
        if length is None:
            length = random.randint(10, 40)
        super().__init__()
        target = ''.join(random.choices(string.ascii_lowercase, k=substring_length))
        self.length = length
        self.target = (target*(self.length//substring_length+1))[:self.length]
        self.ignore_trailing = ignore_trailing

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
        return self
