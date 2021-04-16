from noteinfo import *

class Pitch:
    def __init__(self, pitch, ptype='midi'):
        if type(pitch) is str:
            print(True)
            p = pitch.split('.')
            if len(p) > 1:
                self.octave = int(p[1])
            self.note_name = p[0]
            self.natural = self.note_name[0]
            self.nat = ((self.octave + 2) * num_naturals) + naturals.index(self.natural)

            for i, note in enumerate(note_list):
                if p in note:
                    self.midi = ((self.octave + 2) * len(note_list)) + i
                    break

        elif type(pitch) is int:
            if ptype == 'midi':
                self.midi = pitch
            elif ptype == 'natural':
                self.nat = pitch
                offset = self.nat % num_naturals
                self.natural = naturals[offset]
                self.octave = self.nat // num_naturals
                self.note_name = self.natural
                # self.midi = ((self.octave + 0) * len(note_list)) + (self.nat % num_naturals + 2)
                self.midi = ((self.octave) * num_notes) + note_list.index([self.note_name])
        self.ptype = ptype
    def step(self, change):
        self.midi += int(change * 2)
        self.note_name = self.name()
        # self.natural = self.note_name[0]
        self.natural = naturals[self.nat % num_naturals]
    def name(self):
        k = 12
        # print(self.notes[(midi % k)])
        midi = self.midi
        print(midi)
        # return '/'.join(note_list[(midi % k)]) + '.' + str(midi // k)
        return '/'.join(note_list[(midi % k) + 0])
    def info(self):
        print()
        for w in ['natural', 'octave', 'midi', 'nat', 'note_name']:
            value = getattr(self, w)
            print(w + ': ' + str(value))
