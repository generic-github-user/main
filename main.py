import playsound
from pydub import AudioSegment
import random

import pygame as pg
import time
import pygame.midi

audio_path = './Middle_C.mp3'
# playsound.playsound(audio_path)
notes = ['c', 'd', 'a']
sounds = []
for i in range(2):
    note = random.choice(notes)
    note_path = './piano-{}_{}_major.wav'.format(note, note.upper())
    # playsound.playsound(note_path, False)

    sounds.append(pg.mixer.Sound(note_path))
