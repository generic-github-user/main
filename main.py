import playsound
from pydub import AudioSegment
import random

import pygame as pg
import time
import pygame.midi

from itertools import chain

audio_path = './Middle_C.mp3'
# playsound.playsound(audio_path)

pg.mixer.init()
pg.init()

notes = ['c', 'd', 'a']
sounds = []
for i in range(2):
    note = random.choice(notes)
    note_path = './piano-{}_{}_major.wav'.format(note, note.upper())
    # playsound.playsound(note_path, False)

    sounds.append(pg.mixer.Sound(note_path))

pg.mixer.set_num_channels(20)


# for s in sounds:
#     s.play()

# input()


# pg.midi.init()
# player = pg.midi.Output(0)
# player.set_instrument(0)
#
# player.note_on(60, 127)
# player.note_on(64, 127)
# player.note_on(67, 127)
#
# time.sleep(10)
#
# player.note_off(64, 127)
#
# del player
# pg.midi.quit()

note_list = 'C,C^/D_,D,D^/E_,E,F,F^/G_,G,G^/A_,A,A^/B_,B'
note_list = [n.split('/') for n in note_list.split(',')]
num_notes = len(note_list)

naturals = list('CDEFGAB')
num_naturals = len(naturals)

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

class Note:
    def __init__(self, pitch, player=None, velocity=120, length=1/8):
        self.pitch = pitch
        self.velocity = velocity
        self.length = length
        self.player = player
    def seconds(self, tempo):
        # beats * (beats / minute) = beats * beats / 60 seconds
        return self.length * (tempo / 60)
    def play(self, player=None):
        if player:
            self.player = player
        # Turn on note using midi pitch and velocity
        self.player.note_on(self.pitch.midi, self.velocity)
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
    def info(self):
        self.pitch.info()
        print()
        for w in ['key', 'velocity', 'length']:
            value = getattr(self, w)
            print(w + ': ' + str(value))

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

        self.tempo = 100

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
        melody.play(self.player)

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




comp = Composition(key='B_,E_')
# comp.scale('B_.3', 16, velocity=126, note_length=0.1, use_chord=False, chord_size=3)

m = Melody().randomize(length=50)
comp.play_melody(m)

time.sleep(1)
comp.end()
# TODO: evolved music composition


# sound = AudioSegment.from_file(audio_path)
# octaves = 0.5
# new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
# chipmunk_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
# chipmunk_ready_to_export = chipmunk_sound.set_frame_rate(44100)

# import soundfile as sf
# import pyrubberband as pyrb
# y, sr = sf.read(audio_path)
# # Play back at double speed
# y_stretch = pyrb.time_stretch(y, sr, 2.0)
# # Play back two semi-tones higher
# y_shift = pyrb.pitch_shift(y, sr, 2)


# import numpy as np
# import sox
# # sample rate in Hz
# sample_rate = 44100
# # generate a 1-second sine tone at 440 Hz
# y = np.sin(2 * np.pi * 440.0 * np.arange(sample_rate * 1.0) / sample_rate)
# # create a transformer
# tfm = sox.Transformer()
# # shift the pitch up by 2 semitones
# tfm.pitch(2)
