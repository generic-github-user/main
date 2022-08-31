import random
import time
import copy

from pitch import *
from note import *
from chord import *

class Melody:
    """Container for a sequence of notes or chords"""
    def __init__(self, seq=None, key=None, tempo=100, velocity=100, player=None):
        """Create a new melody"""

        if seq is None:
            self.sequence = []
        else:
            self.sequence = seq
        self.key = key
        assert self.key is not None

        self.level = None
        self.tempo: int = tempo
        """The tempo to play this melody at (in beats per minute)"""
        self.velocity: int = velocity
        """The velocity of each note; will be overridden by velocities set at lower levels (nested melodies)"""
        self.player = player

    def randomize(self, length, note_length=(1/32,1), quantize='log2', chord=True, dist='exp', tempo=(50, 150, 'uniform'), velocity=(90, 127, 'uniform')):
        """Generate a random melody"""

        quantize = 4
        self.tempo = random.randint(*tempo[:2])
        self.velocity = random.randint(*velocity[:2])

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
        """Play this melody and all sub-melodies"""

        # if tempo is None:
        tempo = self.tempo
        if player:
            self.player = player

        for part in self.sequence:
            part.play(player)
            if type(part) is Note or type(part) is Chord:
                time.sleep(part.seconds(self.tempo))
                if clip:
                    part.stop()
        time.sleep(0.0)

    def step(self, change):
        """Shift all notes, chords, and sub-melodies by the specified amount"""

        for part in self.sequence:
            part.step(change)
        return self

    shift = step

    def clone(self):
        """Make a deep copy of this melody and nested notes/melodies"""

        return copy.deepcopy(self)

    def add(self, x):
        self.sequence.append(x)

    def print_tree(self, l=0):
        """Recursively print information about each nested part in the sequence"""

        print(('\t'*l)+str(l))
        for t in self.sequence:
            t.print_tree(l=l+1)

    def reverse(self, recursive=True):
        """Invert the melody"""

        self.sequence.reverse()
        if recursive:
            for t in self.sequence:
                if type(t) in [Melody]:
                    t.reverse(recursive=True)

        return self

    def clear(self):
        self.sequence = []
        return self

    def time(self, tempo=None):
        """Get length of melody in seconds"""

        if hasattr(self, 'tempo'):
            tempo = self.tempo

        self.duration = 0
        for t in self.sequence:
            self.duration += t.time(tempo=self.tempo)
        return self.duration

    def merge(self, other):
        self.tempo = mean(self.tempo, other.tempo)
        self.velocity = mean(self.velocity, other.velocity)
        return self

    # TODO: allow combination of more than 2 at a time
    def interlay(self, other, average=True, steps=(1, 1)):
        if average:
            self.merge(other)

        for i in range(0, len(other.sequence), steps[0]):
            self.sequence.insert(i, other.sequence[i])
        return self
