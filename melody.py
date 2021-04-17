import random
import time
import copy

from pitch import *
from note import *
from chord import *

class Melody:
    def __init__(self, seq=None, key=None, tempo=100, velocity=100):
        if seq is None:
            self.sequence = []
        else:
            self.sequence = seq
        self.key = key
        self.level = None
        self.tempo = tempo
        self.velocity = velocity

    def randomize(self, length, note_length=(1/32,1), quantize='log2', chord=True, dist='exp', temp=(50, 150, 'uniform'), vel=(90, 127, 'uniform')):
        quantize = 4
        self.tempo = random.randint(*temp[:2])
        self.velocity = random.randint(*vel[:2])

        for n in range(length):
            rand_length = random.uniform(*note_length)
            if type(quantize) is str:
                if quantize == 'log2':
                    possible_lengths = [1/(2**r) for r in range(0, 5)]
            elif type(quantize) is int:
                # Quantize to nearest linear increment
                # quantize = 4 -> [0.25, 0.5, 0.75, 1.0]
                possible_lengths = [r/quantize for r in range(1, quantize)]
            rand_length = min(possible_lengths, key=lambda x: abs(rand_length - x))
            # print(rand_length)

            # next_note = Note(random.choice(naturals))
            if chord:
                num = random.randint(1,5)
                offset = 2
                next_note = Chord(random.randint(25, 45), ptype='natural', length=rand_length, key=self.key, num=num, offset=offset, velocity=self.velocity)
            else:
                next_note = Note(Pitch(random.randint(30, 40), ptype='natural'), length=rand_length, key=self.key, velocity=self.velocity)

            self.sequence.append(next_note)
        return self

    def play(self, player, tempo=None, clip=True):
        # if tempo is None:
        tempo = self.tempo

        for part in self.sequence:
            part.play(player)
            if type(part) is Note or type(part) is Chord:
                time.sleep(part.seconds(self.tempo))
                if clip:
                    part.stop()
        time.sleep(0.0)

    def step(self, change):
        for part in self.sequence:
            part.step(change)
        return self

    shift = step

    def clone(self):
        return copy.deepcopy(self)

    def add(self, x):
        self.sequence.append(x)

    def print_tree(self, l=0):
        print(('\t'*l)+str(l))
        for t in self.sequence:
            t.print_tree(l=l+1)

    def reverse(self):
        self.sequence.reverse()
        return self
