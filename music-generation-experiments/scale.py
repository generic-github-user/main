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

        # TODO: allow start and stop arguments

        default_args = {
            'start': 40,
            'steps': 8,
            'velocity': 127,
            'chord_size': 3,
            'play_scale': False,
            'skip': 1,
            'use_chord': False,
            'note_length': 1/4,
            # 'direction': 'both',
            'dirs': ['up', 'down'],
            'custom': [(8,1), (0,-1)]
        }

        # Combine default arguments with provided arguments
        kwargs = default_args | kwargs
        # Loop through list of arguments
        for key, value in kwargs.items():
            # Tuple is provided; generate random value
            if type(value) is tuple:
                first = value[0]
                if type(first) is int:
                    param_value = random.randint(*value[:2])
                elif type(first) is float:
                    param_value = random.uniform(*value[:2])
            # Single numeric or boolean value is provided; use value as-is
            elif type(value) in [int, float, bool, list]:
                param_value = value
            elif type(value) is str:
                if value == 'rand':
                    if key == 'dirs':
                        param_value = random.choice([['up'], ['down'], ['up', 'down'], ['down', 'up']])
                    else:
                        param_value = random.choice([True, False])
                else:
                    raise ValueError('Invalid value; must be "rand"', key, value)
            # Incorrect type provided
            else:
                raise TypeError('Invalid type for argument ', key, value)

            setattr(self, key, param_value)

        start = self.start
        if type(start) is Pitch:
            start = Note(start, ptype='natural', key=self.key)
        elif type(start) is int:
            start = Note(Pitch(start, ptype='natural'), key=self.key)
        elif type(start) is str:
            start = Note(start, key=self.key)

        start = start.pitch.nat

        ranges = []
        for d in self.dirs:
            if d == 'up':
                # TODO: make relative
                ranges.append(range(0, self.steps, self.skip))
            elif d == 'down':
                ranges.append(range(self.steps, -1, -self.skip))

        # Combine ranges and loop through indices
        for i in list(chain(*ranges)):
            if self.use_chord:
                scale_note = Chord(Pitch(start+i, ptype='natural'), player=self.p, key=self.key, length=self.note_length, num=self.chord_size)
            else:
                scale_note = Note(Pitch(start+i, ptype='natural'), player=self.p, key=self.key, length=self.note_length)

            self.add(scale_note)

        if self.play_scale:
            self.play()

    def random_scale(self):
        pass
