import pygame as pg
from itertools import chain
import copy
import random

from note import *
from pitch import *
from melody import *
from chord import *

class Composition:
    """A musical arrangement that brings together Melodies and properties such as a key signature, common tempo, etc."""
    def __init__(self, key='B_,E_', instrument=0):
        pg.midi.init()
        self.player = pg.midi.Output(0)
        self.p = self.player

        self.notes = 'C,C^/D_,D,D^/E_,E,F,F^/G_,G,G^/A_,A,A^/B_,B'
        self.notes = [n.split('/') for n in self.notes.split(',')]
        self.base_notes = list('CDEFGAB')
        print(self.notes)

        self.player.set_instrument(instrument)
        self.key = key.split(',')
        self.key_notes = [n[0] for n in self.key]

        self.accidentals = {
            '^': 1,
            '_': -1
        }

        self.tempo: int = 120
        """The tempo of the piece in beats per minute"""

        h = Note(Pitch((3*8)+5, ptype='natural'), self.player)
        h.update_key(self.key)
        # h.info()

        self.main_melody = Melody(key=self.key)
        print(self.main_melody.sequence)

    def gen(self, current=0, depth=2, pls=None):
        # print(current)
        new_section = Melody(key=self.key)
        pl = random.randint(*pls[current])
        if current < depth:
            for b in range(pl):
                new_section.add(self.gen(current=current+1, pls=pls))
        # Bottom level is reached
        elif current == depth:
            new_section = Melody(key=self.key).randomize(length=pl)

        return new_section

    def generate(self, part_lengths=[(3, 6), (4, 6), (2,3)]):
        """Generate a random piece of music based on a set of structural parameters"""

        # for g in range(6):
        self.main_melody.add(self.gen(pls=part_lengths))
            # rand_melody = Melody(key=self.key)
            # rand_melody.randomize(3)
            # self.main_melody.sequence.append(rand_melody.clone().randomize(3))
        print(self.main_melody.sequence[0].sequence[0].sequence[0].sequence)
        self.main_melody.print_tree()

    def play_(self):
        self.play_melody(self.main_melody)

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
        elif type(note) is Chord:
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

    def repeat_melody(self, melody, n, offset=0):
        """Repeat a melody x times"""
        # parent_melody = Melody([melody] * n)
        parent_melody = Melody([melody.clone().step(offset*j) for j in range(n)], key=self.key)
        self.play_melody(parent_melody)

    def scale(self, start, steps, velocity=127, note_length=0.20, use_chord=False, chord_size=3):
        """Generate a scale given a starting point, number of steps, and information about each note"""
        # if type(start) is str:
        #     start = self.midi_note(start)
        # start = 59
        # start = (8*5)
        start = Note(start)
        start = start.pitch.nat

        # for i in [range(0, steps) + range(steps, 0)]:
        # print(list(chain(range(0, steps), range(steps, 0, -1))))
        # s = steps + 1
        for i in list(chain(range(0, steps), range(steps, -1, -1))):
            if use_chord:
                # self.chord(start+i, num=chord_size)

                nnote = Chord(Pitch(start+i, ptype='natural'), player=self.p, key=self.key, length=note_length, num=chord_size)
                # self.play(nnote)
                nnote.play()
            else:
                # self.player.note_on(self.adjust_pitch(start+i), velocity)
                # print(start+i)
                # self.play_note(pitch=start+i)
                # self.play_note(note=Note(Pitch(start+i,type='natural')))

                # nnote.pitch.info()
                # nnote.play()

                nnote = Note(Pitch(start+i, ptype='natural'), self.player, key=self.key)
                self.play(nnote)
            # time.sleep(note_length)

    def play(self, content):
        if type(content) is Melody:
            self.play_melody(content)
        elif type(content) is Note:
            self.play_note(content)
        # self.play chord?

    def demo(self):
        Chord(Pitch(30, ptype='natural'), player=self.p, key=self.key, num=3).play()
        Chord(Pitch(30, ptype='natural'), player=self.p, key=self.key, num=5).play()
        Chord(Pitch(32, ptype='natural'), player=self.p, key=self.key, num=3).play()

        time.sleep(1)
        # self.scale('B_.2', 8, velocity=126, note_length=0.2, use_chord=False)
        for i in range(1, 5):
            print('Playing chord with {} simultaneous notes'.format(i))
            self.scale('B_.2', 8, velocity=126, note_length=0.2, use_chord=True, chord_size=i)
            time.sleep(1)

        time.sleep(5)

    # scale(60, 20)


    # chord('C.3', 3)

    def end(self):
        """Clean up pygame midi handlers"""
        del self.player
        pg.midi.quit()
