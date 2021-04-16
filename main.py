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


pg.midi.init()
player = pg.midi.Output(0)

notes = 'C,C^/D_,D,D^/E_,E,F,F^/G_,G,G^/A_,A,A^/B_,B'
notes = [n.split('/') for n in notes.split(',')]
print(notes)

def midi_note(note_name, octave=None):
    nn = note_name.split('.')
    if len(nn) > 1:
        octave = int(nn[1])
    nn = nn[0]
    for i, note in enumerate(notes):
        if nn in note:
            return ((octave + 2) * len(notes)) + i
    return -1

print(midi_note('D',8))

def scale(start, steps, use_chord=False, chord_size=3):
    player.set_instrument(0)

    if type(start) is str:
        start = midi_note(start)

    # for i in [range(0, steps) + range(steps, 0)]:
    # print(list(chain(range(0, steps), range(steps, 0, -1))))
    for i in list(chain(range(0, steps), range(steps, 0, -1))):
        if use_chord:
            chord(start+i, num=chord_size)
        else:
            player.note_on(start+i, 127)
        time.sleep(0.20)


# scale(60, 20)

def chord(start, num=3):
    if type(start) is str:
        start = midi_note(start)
    for n in range(num):
        player.note_on(start+(2*n), 127)

# chord('C.3', 3)
scale('C.3', 8, use_chord=True, chord_size=3)

time.sleep(10)

del player
pg.midi.quit()


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
