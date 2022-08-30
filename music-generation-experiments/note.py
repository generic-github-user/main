import random

from pitch import *

class Note:
    def __init__(self, pitch, player=None, velocity=120, length=1/8, key=None, ptype='midi', variation=0.1):
        if type(pitch) is Pitch:
            self.pitch = pitch
        elif type(pitch) in [str, int]:
            self.pitch = Pitch(pitch, ptype)

        self.velocity = velocity
        self.length = length
        self.player = player
        self.variation = variation

        # if key:
        #     self.update_key(key)

        self.update_key(key)
        assert self.key is not None

    def seconds(self, tempo):
        # beats * (beats / minute) = beats * beats / 60 seconds
        # return self.length * (tempo / 60)
        v = self.variation
        return self.length * (60 / tempo) * (1+random.uniform(-v, v))

    time = seconds

    def play(self, player=None):
        if player:
            self.player = player
        # Turn on note using midi pitch and velocity
        self.player.note_on(self.pitch.midi, self.velocity)
    def stop(self, player=None):
        if player:
            self.player = player
        self.player.note_off(self.pitch.midi, self.velocity)
    def update_key(self, key):
        self.key = key
        # Extract naturals from key
        self.key_notes = [n[0] for n in self.key]

        natural = self.pitch.natural
        # print(natural)

        # Natural is listed in key signature
        if natural in self.key_notes:
            # Get corresponding accidental
            acc = self.key[self.key_notes.index(natural)][1]
            # Shift pitch accordingly
            if acc == '_':
                self.pitch.step(-0.5)
            elif acc == '^' or acc == '#':
                self.pitch.step(+0.5)
    def step(self, change):
        self.pitch.step(change)
        # ?
        self.update_key(self.key)
    def info(self):
        self.pitch.info()
        print()
        for w in ['key', 'velocity', 'length']:
            value = getattr(self, w)
            print(w + ': ' + str(value))

    def print_tree(self, l):
        print(('\t'*l)+self.pitch.note_name)

class Rest:
    pass
