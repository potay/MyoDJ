#!/usr/bin/env python

import Myo
import foo

class MingusListener(Myo.Listener):
    def __init__(self, poseMap, *args):
        self.poseMap = poseMap
        self.isOn = False
        for i in xrange(len(args)):
            setattr(self, args[i][0], args[i][1])
        super(MingusListener, self).__init__()

    def on_pose(self, myo, timestamp, pose):
        if pose.name in self.poseMap:
            if pose.name == "fingers_spread" or pose.name == "fist":
                self.isOn = self.poseMap[pose.name][0][1]
            if self.isOn:
                for i in xrange(len(self.poseMap[pose.name])-2):
                    value = getattr(self, self.poseMap[pose.name][i][0]) + self.poseMap[pose.name][i][1]
                    setattr(self, self.poseMap[pose.name][i][0], value)
                    # print self.poseMap[pose.name][i][0], value
        super(MingusListener, self).on_pose(myo, timestamp, pose)

    def on_orientation_data(self, myo, timestamp, orientation):
        super(MingusListener, self).on_orientation_data(myo, timestamp, orientation)
        if self.isOn:
            setattr(self, "modulation", abs(self.pitch_w))

from mingus.core import progressions, intervals
from mingus.core import chords as ch
from mingus.containers import NoteContainer, Note
from mingus.midi import fluidsynth
import time, sys
from random import random

class MingusHub(Myo.MyoHub):
    def init(self):
        self.SF2 = "soundfont.sf2"
        self.progression = ["I", "V"]
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
        #####
        currentNotes = "SOMETHING"
        currNoteList = []
        try:
            # while self.hub.running:
                nextNotesDict = foo.MidiState()
                for key in nextNotesDict.state:
                    note = Note()
                    note.from_int(key)
                    note.velocity = nextNotesDict.state[key]
                    print note
                    if note in currNoteList:
                        currNoteList
                    else:
                        currNoteList.append(note)
                print currNoteList

                for note in currNoteList:
                    fluidsynth.play_Note(note, 1, note.velocity)

        except KeyboardInterrupt:
            print "Quitting ..."
            self.hub.stop(True)


poseMap = {'wave_in': [('baseRandom', -0.1), ('key', 1)],
           'wave_out': [('baseRandom', 0.1), ('key', -1)],
           'fist': [('isOn', False)],
           'fingers_spread': [('isOn', True)]}

listener = MingusListener(poseMap, ('baseRandom', 0.5),
                                   ('ninthRandom', 0.5),
                                   ('highRandom', 0.5),
                                   ('key', 1),
                                   ('modulation', 0))
hub = MingusHub(listener)

hub.run()
