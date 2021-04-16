import playsound
from pydub import AudioSegment
import random

import pygame as pg
import time
import pygame.midi

from itertools import chain

from noteinfo import *
from pitch import *
from note import *
from melody import *
from composition import *

audio_path = './Middle_C.mp3'
# playsound.playsound(audio_path)

pg.mixer.init()
pg.init()

# notes = ['c', 'd', 'a']
# sounds = []
# for i in range(2):
#     note = random.choice(notes)
#     note_path = './piano-{}_{}_major.wav'.format(note, note.upper())
    # playsound.playsound(note_path, False)

#     sounds.append(pg.mixer.Sound(note_path))
#
# pg.mixer.set_num_channels(20)


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




mainkey = 'B_,E_'
comp = Composition(key=mainkey, instrument=0)
# comp.scale('B_.2', 8, velocity=126, note_length=0.2, use_chord=True, chord_size=3)

mainkey = mainkey.split(',')
m = Melody(key=mainkey).randomize(length=5)
comp.repeat_melody(melody=m, n=4, offset=1)

# comp.play_melody(m)

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
