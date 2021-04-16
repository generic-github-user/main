import pygame as pg

from note import *
from pitch import *
from melody import *

class Composition:
    def __init__(self, key='B_,E_'):
        pg.midi.init()
        self.player = pg.midi.Output(0)

        self.notes = 'C,C^/D_,D,D^/E_,E,F,F^/G_,G,G^/A_,A,A^/B_,B'
        self.notes = [n.split('/') for n in self.notes.split(',')]
        self.base_notes = list('CDEFGAB')
        print(self.notes)

        self.player.set_instrument(0)
        self.key = key.split(',')
        self.key_notes = [n[0] for n in self.key]

        self.accidentals = {
            '^': 1,
            '_': -1
        }

        self.tempo = 160

        h = Note(Pitch((3*8)+5, ptype='natural'), self.player)
        h.update_key(self.key)
        # h.info()

    def midi_note(self, note_name, octave=None):
        nn = note_name.split('.')
        if len(nn) > 1:
            octave = int(nn[1])
        nn = nn[0]
        for i, note in enumerate(self.notes):
            if nn in note:
                base = ((octave + 2) * len(self.notes)) + i
                if nn in self.key_notes:
                    base += self.accidentals[self.key[self.key_notes.index(nn)]]
                print((nn, base))
                return base
        return -1

    def note_name(self, midi, simple=False):
        k = 12
        # print(self.notes[(midi % k)])
        return '/'.join(self.notes[(midi % k)]) + '.' + str(midi // k)

    # print(midi_note('D',8))

    def play_note(self, note, velocity=127):
        if type(note) is int:
            # base = self.get_base(pitch)
            base = round(note * (2/3))
            base = self.get_base(base)
            # print(base)
            if base in self.key_notes:
                note += self.accidentals[self.key[self.key_notes.index(base)][1]]
            print((self.note_name(note), note))
            self.player.note_on(note, velocity)
        elif type(note) is Note:
            # self.player.note_on(note.pitch.midi, note.velocity)
            note.update_key(self.key)
            note.info()
            note.play()

    def adjust_pitch(self, note):
        if any([((note - m) % 12 == 0) for m in (1, 3, 6, 8, 10)]):
            print(True)
            note -= 1
        return note

    def chord(self, start, num=3):
        if type(start) is str:
            start = self.midi_note(start)

        for n in range(num):
            # self.player.note_on(start+(2*n), 127)
            pitch = start + (2 * n)
            self.player.note_on(self.adjust_pitch(pitch), 127)

    def get_base(self, pitch):
        rel_index = (pitch + 0) % len(self.base_notes)
        base = self.base_notes[rel_index]
        print((base, pitch))
        return base

    def play_melody(self, melody):
        melody.play(self.player, tempo=self.tempo)

    def repeat_melody(self, melody, n):
        parent_melody = Melody([melody] * n)
        self.play_melody(parent_melody)

    def scale(self, start, steps, velocity=127, note_length=0.20, use_chord=False, chord_size=3):
        # if type(start) is str:
        #     start = self.midi_note(start)
        # start = 59
        # start = (8*5)

        start = Note(Pitch(start))
        start = start.pitch.nat

        # for i in [range(0, steps) + range(steps, 0)]:
        # print(list(chain(range(0, steps), range(steps, 0, -1))))
        # s = steps + 1
        for i in list(chain(range(0, steps), range(steps, -1, -1))):
            if use_chord:
                self.chord(start+i, num=chord_size)
            else:
                # self.player.note_on(self.adjust_pitch(start+i), velocity)
                # print(start+i)
                # self.play_note(pitch=start+i)
                # self.play_note(note=Note(Pitch(start+i,type='natural')))

                nnote = Note(Pitch(start+i, ptype='natural'), self.player)
                # nnote.pitch.info()
                # nnote.play()

                self.play_note(nnote)
            time.sleep(note_length)

    def play(self, content):
        if type(content) is Melody:
            self.play_melody(content)
        elif type(content) is Note:
            self.play_note(content)


    # scale(60, 20)


    # chord('C.3', 3)

    def end(self):
        del self.player
        pg.midi.quit()
