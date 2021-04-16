import random
import time

from pitch import *
from note import *

class Melody:
    def __init__(self, seq=[], key=None):
        self.sequence = seq
        self.key = key

    def randomize(self, length, note_length=(1/32,1/2), quantize='log2'):
        for n in range(length):
            rand_length = random.uniform(*note_length)
            if type(quantize) is str:
                if quantize == 'log2':
                    possible_lengths = [1/(2**r) for r in range(0, 5)]
            else:
                # Quantize to nearest linear increment
                # quantize = 4 -> [0.25, 0.5, 0.75, 1.0]
                possible_lengths = [r/quantize for r in range(1, quantize)]
            rand_length = min(possible_lengths, key=lambda x: abs(rand_length - x))
            print(rand_length)

            # next_note = Note(random.choice(naturals))
            next_note = Note(Pitch(random.randint(30, 40), ptype='natural'), length=rand_length, key=self.key)
            self.sequence.append(next_note)
        return self

    def play(self, player, tempo=60, clip=True):
        for part in self.sequence:
            part.play(player)
            if type(part) is Note:
                time.sleep(part.seconds(tempo))
                if clip:
                    part.stop()

    def step(self, change):
        for part in self.sequence:
            part.step(change)
        return self

    shift = step
