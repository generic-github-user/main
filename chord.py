import time

from note import *
from pitch import *

class Chord:
    def __init__(self, start, player=None, num=3, offset=2, key=None, length=1, interval=None, custom=None, variation=0.1, ptype='natural'):
        self.notes = []
        self.player = player
        self.key = key
        self.length = length
        self.variation = variation

        if type(start) is Note:
            start = start.pitch.nat
        elif type(start) is Pitch:
            start = start.nat
        elif type(start) is str:
            start = Note(start, ptype='natural')
            start = start.pitch.nat


        def cn(pitch):
            chord_note = Note(Pitch(pitch, ptype='natural'), key=self.key)
            self.notes.append(chord_note)
            # step?

        if custom:
            for b in custom:
                cn(start + b)
        elif interval:
            x, y, z = interval
            for c in range(x, y+1, z):
                cn(start + c)
        elif num:
            for n in range(num):
                cn(start + (offset * n))



    def play(self, player=None):
        if player:
            self.player = player
        for note in self.notes:
            note.play(player=self.player)
        # TODO:
        time.sleep(self.seconds(tempo=80))

        return self

    def seconds(self, tempo):
        v = self.variation
        return self.length * (60 / tempo) * (1+random.uniform(-v, v))

    def print_tree(self, l):
        pass
