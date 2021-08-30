# import keyboard
import curses
import os
import numpy as np
import string
import random
import time
import itertools

import colorama
from colorama import Fore, Style

import nltk
from nltk import FreqDist
from nltk.corpus import brown
nltk.download('brown')

# while True:
#     if keyboard.is_pressed('q'):
#         print('q')

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

letters = string.ascii_lowercase
class Game:
    def __init__(self, dimensions=(11, 20), selection_method='symbol_frequency') -> None:
        self.dimensions = np.array(dimensions)
        self.width, self.height = self.dimensions
        self.bg = ' '
        self.board = np.full(tuple(dimensions), self.bg, dtype=object)
        self.timestep = 0
        self.blocks = []
        self.active_block = None
        self.speed = 5
        self.frequency = self.speed * self.height
        # self.countdown = self.frequency
        self.countdown = 0
        self.score = 0
        self.difficulty = 0.5
        self.min_length = 3
        self.orientations = ['horizontal', 'vertical']
        # self.directions = ['horizontal']
        self.selection_method = selection_method
        self.debug = False
        self.update()

    def update(self):
        self.board = np.full(tuple(self.dimensions), self.bg, dtype=object)
        for block in self.blocks:
            self.board[tuple(block.position)] = block
        self.slice_sources = dict(
            horizontal=self.board.T,
            vertical=self.board,
            diagonal=self.board,
        )
        return self

    def calculate_score(self, word):
        return round(10 * (len(word) ** 2))

    def step(self, delay=0.5):
        # if self.timestep % self.frequency == 0:
        if self.active_block and self.active_block.fixed:
            self.countdown = 0
        if self.countdown == 0:
            if self.selection_method == 'random':
                next_letter = random.choice(letters)
            elif self.selection_method == 'symbol_frequency':
                next_letter = random.choices(list(symbol_frequencies.keys()), weights=list(symbol_frequencies.values()), k=1)[0]
            new_block = Block(next_letter, (self.width // 2, 0), self)
            self.blocks.append(new_block)
            self.active_block = new_block
            self.countdown = self.frequency
        for block in self.blocks:
            block.step()
        self.slices = []
        for orient in self.orientations:
            if orient in self.slice_sources:
                self.slices.append(self.slice_sources[orient])

        # for y, row in enumerate(np.concatenate(self.slices, axis=0)):
        # combined = []
        # map(combined.extend, map(list, self.slices))
        combined = list(itertools.chain.from_iterable(self.slices))
        if self.debug:
            breakpoint()
        for y, row in enumerate(combined):
            row_str = ''.join(map(str, row))
            matches = list(filter(lambda x: x in row_str, words))
            if matches:
                # match
                longest = max(matches, key=len)
                if len(longest) >= self.min_length:
                    index = row_str.index(longest)
                    # for block in self.board[index:index+len(longest), y]:
                    for block in row[index:index+len(longest)]:
                        # print(block, True)
                        if block in self.blocks:
                            self.blocks.remove(block)
                    self.score += self.calculate_score(longest)

        self.update()
        self.timestep += 1
        self.countdown -= 1
        # time.sleep(delay)
        return self
