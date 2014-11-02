#!/usr/bin/env python

import Myo

class MingusListener(Myo.Listener):
    def __init__(self, poseMap, *args):
        self.poseMap = poseMap
        for i in xrange(len(args)):
            setattr(self, args[i][0], args[i][1])
        super(MingusListener, self).__init__()

    def on_pose(self, myo, timestamp, pose):
        if pose.name in self.poseMap:
            for i in xrange(len(self.poseMap[pose.name])):
                value = getattr(self, self.poseMap[pose.name][i][0]) + self.poseMap[pose.name][i][1]
                setattr(self, self.poseMap[pose.name][i][0], value)
                print self.poseMap[pose.name][i][0], value
        super(MingusListener, self).on_pose(myo, timestamp, pose)

from mingus.core import progressions, intervals
from mingus.core import chords as ch
from mingus.containers import NoteContainer, Note
from mingus.midi import fluidsynth
import time, sys
from random import random

class MingusHub(Myo.MyoHub):
    def init(self):
        self.SF2 = "soundfont.sf2"
        self.progression = ["I", "v"]
        self.keyMap = {0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F',
                       6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'}
        self.prevKey = self.keyMap[listener.key % 12]
        self.chords = progressions.to_chords(self.progression, self.prevKey)

        if not fluidsynth.init(self.SF2):
            print "Couldn't load soundfont", self.SF2
            sys.exit(1)

    def run(self):
        self.init()
        self.hub.run(1000, self.listener)

        try:
            while self.hub.running:
                i = 0
                if self.prevKey != self.keyMap[listener.key % 12]:
                    self.prevKey = self.keyMap[listener.key % 12]
                    self.chords = progressions.to_chords(self.progression, self.prevKey)
                for chord in self.chords:
                    c = NoteContainer(self.chords[i])
                    l = Note(c[0].name)
                    p = c[1]
                    l.octave_down()
                    print ch.determine(self.chords[i])[0]

                    # Play chord and lowered first note
                    fluidsynth.play_NoteContainer(c)
                    fluidsynth.play_Note(l)
                    time.sleep(1.0)

                    # Play highest note in chord
                    fluidsynth.play_Note(c[-1])

                    # 50% chance on a bass note
                    if random() > listener.baseRandom:
                        p = Note(c[1].name)
                        p.octave_down()
                        fluidsynth.play_Note(p)
                    time.sleep(0.50)

                    # 50% chance on a ninth
                    if random() > listener.ninthRandom:
                        l = Note(intervals.second(c[0].name, self.prevKey))
                        l.octave_up()
                        fluidsynth.play_Note(l)
                    time.sleep(0.25)

                    # 50% chance on the second highest note
                    if random() > listener.highRandom:
                        fluidsynth.play_Note(c[-2])
                    time.sleep(0.25)

                    fluidsynth.stop_NoteContainer(c)
                    fluidsynth.stop_Note(l)
                    fluidsynth.stop_Note(p)
                    i += 1
                print "-" * 20
                #myo.time.sleep(0.2)
        except KeyboardInterrupt:
            print "Quitting ..."
            self.hub.stop(True)


poseMap = {'wave_in': [('baseRandom', -0.1), ('key', 1)],
           'wave_out': [('baseRandom', 0.1), ('key', -1)],
           'fist': [('ninthRandom', -0.1), ('highRandom', -0.1)],
           'fingers_spread': [('ninthRandom', 0.1), ('highRandom', 0.1)],}
listener = MingusListener(poseMap, ('baseRandom', 0.5),
                                   ('ninthRandom', 0.5),
                                   ('highRandom', 0.5),
                                   ('key', 1))
hub = MingusHub(listener)

hub.run()
