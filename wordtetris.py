# import keyboard
import curses
import os
import numpy as np
import string
import random
import time

import nltk
from nltk import FreqDist
from nltk.corpus import brown
nltk.download('brown')

word_limit = 20000
word_frequencies = FreqDist(i.lower() for i in brown.words()).most_common()
# print(word_frequencies.most_common()[:10])
symbol_frequencies = {}
# words = word_frequencies.keys()[:10000]
words = [a for a, b in word_frequencies[:word_limit]]
words = [word.translate(str.maketrans('', '', string.punctuation)) for word in words]
for word, freq in word_frequencies[:word_limit]:
    for char in word.lower():
        if char in string.ascii_letters:
            if char in symbol_frequencies:
                symbol_frequencies[char] += freq
            else:
                symbol_frequencies[char] = freq
print(symbol_frequencies)
# breakpoint()

class Block:
    def __init__(self, letter, position, game) -> None:
        self.letter = letter
        self.position = np.array(position)
        self.game = game
        self.fixed = False

    def can_fall(self):
        if self.position[1] < self.game.height-1:
            below = self.game.board[tuple(self.position+np.array([0,1]))]
            if not isinstance(below, Block):
                return True
        self.fixed = True
        return False

    def fall(self):
        if self.can_fall():
            self.position[1] += 1
        return self

    def step(self):
        if self.game.timestep % self.game.speed == 0:
            self.fall()
        return self

    def drop(self):
        for i in range(self.game.height):
            self.fall()
        self.game.countdown = 0
        return self

    def __str__(self) -> str:
        return str(self.letter)
