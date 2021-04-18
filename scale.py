from itertools import chain
import random

from melody import *

class Scale(Melody):
    def __init__(self, key=None, player=None, **kwargs):
        """Generate a scale given a starting point, number of steps, and information about each note"""

        assert key is not None
        assert player is not None
        self.key = key
        self.player = player
        self.p = self.player
        super().__init__(key=self.key, player=self.player)

        default_args = {
            'start': 40,
            'steps': 8,
            'velocity': 127,
            'chord_size': 3,
            'play_scale': False,
            'skip': 1,
            'use_chord': False,
            'note_length': 1/4
        }

        kwargs = default_args | kwargs
        for key, value in kwargs.items():
            if type(value) is tuple:
                first = value[0]
                if type(first) is int:
                    setattr(self, key, random.randint(*value[:2]))
                elif type(first) is float:
                    setattr(self, key, random.uniform(*value[:2]))
            elif type(value) is int or type(value) is float:
                setattr(self, key, value)
            elif type(value) is bool:
                setattr(self, key, value)
            elif type(value) is str and value == 'rand':
                setattr(self, key, random.choice([True, False]))
            else:
                print('Invalid type for argument '+key)

        start = self.start
        if type(start) is Pitch:
            start = Note(start, ptype='natural', key=self.key)
        elif type(start) is int:
            start = Note(Pitch(start, ptype='natural'), key=self.key)
        elif type(start) is str:
            start = Note(start, key=self.key)

        start = start.pitch.nat

        for i in list(chain(range(0, self.steps, self.skip), range(self.steps, -1, -self.skip))):
            if self.use_chord:
                scale_note = Chord(Pitch(start+i, ptype='natural'), player=self.p, key=self.key, length=self.note_length, num=self.chord_size)
            else:
                scale_note = Note(Pitch(start+i, ptype='natural'), player=self.p, key=self.key, length=self.note_length)

            self.add(scale_note)

        if self.play_scale:
            self.play()

    def random_scale(self):
        pass
