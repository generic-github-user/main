from itertools import chain

from melody import *

class Scale(Melody):
    def __init__(self, start, steps, velocity=127, note_length=1/4, use_chord=False, chord_size=3, play=False, skip=1, key=None, player=None):
        """Generate a scale given a starting point, number of steps, and information about each note"""
        assert key is not None
        assert player is not None
        self.key = key
        self.player = player
        self.p = self.player
        super().__init__(key=self.key, player=self.player)


        # if type(start) is str:
        #     start = self.midi_note(start)
        # start = 59
        # start = (8*5)
        if type(start) is Pitch:
            start = Note(start, ptype='natural', key=self.key)
        elif type(start) is int:
            start = Note(Pitch(start, ptype='natural'), key=self.key)
        elif type(start) is str:
            start = Note(start, key=self.key)

        start = start.pitch.nat

        if play:
            print(True)

        if play:
            # for i in [range(0, steps) + range(steps, 0)]:
            # print(list(chain(range(0, steps), range(steps, 0, -1))))
            # s = steps + 1
            for i in list(chain(range(0, steps, skip), range(steps, -1, -skip))):
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
        else:
            generated_scale = Melody(key=self.key)
            for i in list(chain(range(0, steps, skip), range(steps, -1, -skip))):
                if use_chord:
                    scale_note = Chord(Pitch(start+i,ptype='natural'), player=self.p, key=self.key, length=note_length, num=chord_size)
                else:
                    # scale_note = Note(Pitch(start+i, ptype='natural'), self.player, key=self.key, length=note_length)
                    scale_note = Note(Pitch(start+i, ptype='natural'), player=self.p, key=self.key, length=note_length)

                generated_scale.add(scale_note)
