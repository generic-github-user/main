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

class Composition:
    def __init__(self, key='B_,E_'):
        pg.midi.init()
        self.player = pg.midi.Output(0)

        self.notes = 'C,C^/D_,D,D^/E_,E,F,F^/G_,G,G^/A_,A,A^/B_,B'
        self.notes = [n.split('/') for n in self.notes.split(',')]
        print(self.notes)

        self.player.set_instrument(0)
        self.key = key.split(',')
        self.key_notes = [n[0] for n in self.key]

        self.accidentals = {
            '^': 1,
            '_': -1
        }

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

    def play_note(self, pitch, velocity=127):
        if type(pitch) is int:
            # base = self.get_base(pitch)
            base = round(pitch * (2/3))
            base = self.get_base(base)
            # print(base)
            if base in self.key_notes:
                pitch += self.accidentals[self.key[self.key_notes.index(base)][1]]
            print((self.note_name(pitch), pitch))
            self.player.note_on(pitch, velocity)

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

    def scale(self, start, steps, velocity=127, note_length=0.20, use_chord=False, chord_size=3):
        if type(start) is str:
            start = self.midi_note(start)

        # for i in [range(0, steps) + range(steps, 0)]:
        # print(list(chain(range(0, steps), range(steps, 0, -1))))
        for i in list(chain(range(0, steps), range(steps, 0, -1))):
            if use_chord:
                self.chord(start+i, num=chord_size)
            else:
                self.player.note_on(self.adjust_pitch(start+i), velocity)
            time.sleep(note_length)


    # scale(60, 20)


    # chord('C.3', 3)

    def end(self):
        del self.player
        pg.midi.quit()


comp = Composition()
comp.scale('C.3', 8, velocity=126, note_length=0.2, use_chord=False, chord_size=3)
time.sleep(10)
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
