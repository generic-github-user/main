from note import *
from pitch import *

class Chord:
    def __init__(self, start, player=None, num=3, offset=2, key=None):
        self.notes = []
        self.player = player
        self.key = key

        if type(start) is Note:
            start = start.pitch.nat
        elif type(start) is Pitch:
            start = start.nat

        for n in range(num):
            pitch = start + (offset * n)
            chord_note = Note(Pitch(pitch, ptype='natural'), key=self.key)
            self.notes.append(chord_note)
            # step?

    def play(self, player=None):
        if player:
            self.player = player
        for note in self.notes:
            note.play(player=self.player)
