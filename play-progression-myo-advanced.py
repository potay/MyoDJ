#!/usr/bin/env python

import Myo
import MidiSong

class MingusListener(Myo.Listener):
    def __init__(self, poseMap, *args):
        self.poseMap = poseMap
        for i in xrange(len(args)):
            setattr(self, args[i][0], args[i][1])
        super(MingusListener, self).__init__()

    def on_pose(self, myo, timestamp, pose):
        if pose.name in self.poseMap:
                value = getattr(self, self.poseMap[pose.name][0][0]) + self.poseMap[pose.name][0][1]
                setattr(self, self.poseMap[pose.name][0][0], value)
                print self.poseMap[pose.name][0][0], value
        super(MingusListener, self).on_pose(myo, timestamp, pose)

    def on_orientation_data(self, myo, timestamp, orientation):
        pass
        # print "orientation"
        # super(MingusListener, self).on_orientation_data(myo, timestamp, orientation)
        # print "rolle", self.roll_w

from mingus.core import progressions, intervals
from mingus.core import chords as ch
from mingus.containers import NoteContainer, Note
from mingus.midi import fluidsynth
import time, sys
from random import random

class MingusHub(Myo.MyoHub):
    def init(self):
        self.SF2Index = 0
        self.SF2List = ["AJH_Piano.sf2", "soundfont.sf2", "Analog Age_set.sf2", "HeavyDTWaves.SF2", "jonnypad10.sf2", "space_wings.SF2"]

        # self.progression = ["I", "V"]
        # self.keyMap = {0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F',
        #                6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'}
        # self.prevKey = self.keyMap[listener.key % 12]
        # self.chords = progressions.to_chords(self.progression, self.prevKey)

        if not fluidsynth.init(self.SF2List[self.SF2Index%len(self.SF2List)]):
            print "Couldn't load soundfont", self.SF2List[self.SF2Index%len(self.SF2List)]
            sys.exit(1)

        self.Song = MidiSong.MidiSong('sample_midi/LetItGo.mid')
        self.tick = 0.002*listener.tickScale

    def run(self):
        self.init()
        self.hub.run(1000, self.listener)
        currState = self.Song.getRandomState(0)
        stateHistory = [currState]
        c = Note()
        previousSFIndex = self.SF2Index
        try:
            while self.hub.running:
                self.SF2Index = listener.SF2Index
                #print self.SF2Index, previousSFIndex
                if previousSFIndex != self.SF2Index:
                    if not fluidsynth.init(self.SF2List[self.SF2Index%len(self.SF2List)]):
                        print "Couldn't load soundfont", self.SF2List[self.SF2Index%len(self.SF2List)]
                        sys.exit(1)
                    previousSFIndex = self.SF2Index
                state = self.Song.getRandomNextState(0, tuple(stateHistory))
                
                if state != currState:
                    missingNotes, extraPitches = currState.getDiff(state)
                    for note in missingNotes:
                        fluidsynth.play_Note(c.from_int(note[0]+listener.noteOffset), 1, note[1]*listener.volumeScale)
                    for pitch in extraPitches:
                        fluidsynth.stop_Note(c.from_int(pitch+listener.noteOffset), 1)
                    currState = state

                stateHistory.append(currState)

                if len(stateHistory) > MidiSong.MidiSong.maxOrder:
                    stateHistory = stateHistory[-MidiSong.MidiSong.maxOrder:]

                # fluidsynth.modulation(1, listener.roll_w)

                time.sleep(self.tick*self.Song.tracks[0]['width'])

        except KeyboardInterrupt:
            print "Quitting ..."
            self.hub.stop(True)

poseMap = {'wave_in': [('volumeScale', -0.05)],
           'wave_out': [('volumeScale', +0.05)],
           'fist': [('noteOffset', -1),
                    ('SF2Index', -1),
                    ('tickScale', -1)],
           'fingers_spread': [('noteOffset', +1),
                              ('SF2Index', +1),
                              ('tickScale', +1)]}

listener = MingusListener(poseMap, ('volumeScale', 1),
                                   ('tickScale', 1),
                                   ('SF2Index', 0),
                                   ('noteOffset', 0))
hub = MingusHub(listener)

hub.run()