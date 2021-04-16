import random
import time

from pitch import *
from note import *

class Melody:
    def __init__(self):
        self.notes = []

    def randomize(self, length, note_length=(1/16,1/4)):
        for n in range(length):
            # next_note = Note(random.choice(naturals))
            next_note = Note(Pitch(random.randint(40, 60), ptype='natural'), length=random.uniform(*note_length))
            self.notes.append(next_note)
        return self

    def play(self, player, tempo=120):
        for note in self.notes:
            note.play(player)
            time.sleep(note.seconds(tempo))
