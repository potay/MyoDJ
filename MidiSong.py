"""
MidiSong Class
---------------

Limitations
    - Only accepts midi files with one track.

- Markov Matrix is a dictionary with each key and value pair representing the
  current state and dictionary representing all the adjacent states mapped to
  corresponding number of occurences
- A Pattern is a list of events, each events represented by their class.
"""

import midi, pprint, random

class MidiState(list):
    def __init__(self, noteList = []):
        for note in noteList:
            self.isValidNote(note)
        self.state = dict(noteList)


    def isValidNote(self, note):
        if type(note) != tuple or len(note) != 2:
            raise Exception("Note is invalid.")
        for attr in note:
            if type(attr) != int:
                raise Exception("Note has invalid attributes.")
        if note[1] <= 0:
            raise Exception("Note is an empty note.")
        return True


    def set(self, notes):
        if notes == list:
            for note in notes:
                if self.isValidNote(note):
                    pitch = note[0]
                    velocity = note[1]
                    self.state[pitch] = velocity
        else:
            if self.isValidNote(notes):
                pitch = notes[0]
                velocity = notes[1]
                self.state[pitch] = velocity

    def unset(self, pitch):
        if pitch in self.state:
            del self.state[pitch]


    def __eq__(self, other):
        if len(self.state) != len(other.state):
            return False

        for note in self.state:
            if note not in other.state:
                return False
            if self.state[note] != other.state[note]:
                return False

        return True


    def __ne__(self, other):
        return not self == other


    def __str__(self):
        return str(self.state)


    def __repr__(self):
        return repr(self.state)


    def __hash__(self):
        return hash(tuple(self.state.items()))


    def getDiff(self, other):
        if not isinstance(other, MidiState):
            raise Exception("Other state is not a valid state.")

        missingNotes = []
        pitches = sorted(self.state.keys())
        otherPitches = sorted(other.state.keys())
        for pitch in list(set(otherPitches) - set(pitches)):
            missingNotes.append((pitch, other.state[pitch]))
        extraPitches = list(set(pitches) - set(otherPitches))

        return missingNotes, extraPitches



class MidiSong(object):

    # Default class settings
    maxTrackCount = 1
    factorEvents = [midi.NoteOnEvent, midi.NoteOffEvent]
    maxOrder = 200


    @staticmethod
    def gcd(a, b):
        while (b > 0):
            (a,b) = (b,a%b)
        return a


    def __init__(self, inputMidiPath = None, tracks = []):
        self.midiPattern = None
        self.trackCount = None
        self.tracks = tracks
        self.inputMidiPath = inputMidiPath
        if self.tracks != [] and self.inputMidiPath != None:
            raise Exception("Cannot initialize with both sample midi and \
tracks.")
        if self.inputMidiPath != None:
            self.initInputMidi()
            self.initMarkovMatrices()
        elif self.tracks != []:
            self.initMidiPattern()


    def isValidTracks(self):
        if len(self.tracks) < 1:
            raise Exception("Tracks is not valid.")

        for index in xrange(len(self.tracks)):
            self.isValidTrack(index)


    def isValidTrack(self, trackIndex):
        if trackIndex < 0 or trackIndex >= len(self.tracks):
            raise Exception("Track does not exist.")
        return True


    def isValidTrackState(self, trackIndex, state):
        self.isValidTrack(trackIndex)
        track = self.tracks[trackIndex]
        return state in track['matrix']


    def isValidTrackStateHistory(self, trackIndex, stateHistory):
        self.isValidTrack(trackIndex)
        track = self.tracks[trackIndex]
        for i in xrange(len(stateHistory)-1):
            if (stateHistory[i] not in track['matrix'] or
                stateHistory[i+1] not in track['matrix'][stateHistory[i]]):
                return False
        return True


    def initInputMidi(self, inputMidiPath = None):
        if inputMidiPath != None:
            self.inputMidiPath = inputMidiPath

        try:
            self.midiPattern = midi.read_midifile(self.inputMidiPath)
        except:
            raise Exception("Unable to read sample midi file.")

        # Ensure that input midi has only one track
        self.trackCount = len(self.midiPattern)
        if self.trackCount > MidiSong.maxTrackCount:
            raise Exception("Sample midi file has too many tracks. Max number \
of tracks: %d" % MidiSong.maxTrackCount)

        # Detect state width
        for track in self.midiPattern:
            # Filter out unwanted events
            track = filter(lambda x: type(x) in MidiSong.factorEvents, track)
            trackStateWidth = 0
            for event in track:
                trackStateWidth = self.gcd(event.tick, trackStateWidth)

            # Create dictionary representing current state
            stateList = []
            state = MidiState()
            stateCounter = 0
            tickCounter = 0
            for event in track:
                tickCounter += event.tick

                # Take snapshot of state if moving to next state
                if tickCounter > stateCounter*trackStateWidth:
                    while tickCounter > stateCounter*trackStateWidth:
                        stateList.append(state)
                        stateCounter += 1
                    state = MidiState()

                # Update state
                pitch, velocity = event.data
                if velocity == 0:
                    state.unset(pitch)
                else:
                    state.set(tuple(event.data))

            stateList.append(state)
            stateCounter += 1

            trackDict = self.createTrackDict(trackStateWidth,
                                             stateCounter,
                                             stateList)
            self.tracks.append(trackDict)


    def createTrackDict(self, width, length, states, matrix=None):
        return {'width':width,
                'length':length,
                'states':states,
                'matrix':matrix}


    def initMarkovMatrices(self):
        for track in self.tracks:
            track['matrix'] = {}
            for order in xrange(1, MidiSong.maxOrder):
                track['matrix'][order] = self.getMarkovMatrix(track['states'],
                                                              order)


    def getMarkovMatrix(self, states, order):
        matrix = {}
        for i in xrange(len(states)-order):
            statesHistory = []
            for j in xrange(order):
                statesHistory.append(states[i+j])
            statesHistory = tuple(statesHistory)
            if statesHistory in matrix:
                if states[i+order] in matrix[statesHistory]:
                    matrix[statesHistory][states[i+order]] += 1
                else:
                    matrix[statesHistory][states[i+order]] = 1
            else:
                matrix[statesHistory] = {states[i+order]: 1}

        return matrix


    def getRandomState(self, trackIndex):
        if self.isValidTrack(trackIndex):
            track = self.tracks[trackIndex]
            return random.choice(track['matrix'][1].keys())[0]


    def getRandomNextState(self, trackIndex, stateHistory):
        order = len(stateHistory)
        if len(stateHistory) > MidiSong.maxOrder:
            stateHistory = stateHistory[-MidiSong.maxOrder:]
            order = MidiSong.maxOrder

        if self.isValidTrackStateHistory(trackIndex, stateHistory):
            track = self.tracks[trackIndex]
            stateHistory = tuple(stateHistory)
            while stateHistory not in track['matrix'][order]:
                stateHistory = stateHistory[1:]
                order -= 1
                if order == 0:
                    return self.getRandomState(trackIndex)
            totalCount = sum(track['matrix'][order][stateHistory].values())
            selectedCount = random.randrange(1, totalCount + 1)
            currCount = 0
            for currState in track['matrix'][order][stateHistory]:
                currCount += track['matrix'][order][stateHistory][currState]
                if currCount >= selectedCount:
                    return currState
        else:
            return self.getRandomState(trackIndex)


    def generateTrackStates(self, trackIndex, length):
        currState = self.getRandomState(trackIndex)
        states = [currState]
        stateHistory = [currState]
        for i in xrange(1, length):
            currState = self.getRandomNextState(trackIndex,
                                                tuple(stateHistory))
            states.append(currState)
            stateHistory.append(currState)
            if len(stateHistory) > MidiSong.maxOrder:
                stateHistory = stateHistory[-MidiSong.maxOrder:]

        return states


    def generateTracks(self, length):
        tracks = []
        for index in xrange(len(self.tracks)):
            states = self.generateTrackStates(index, length)
            width = self.tracks[index]['width']
            matrix = self.getMarkovMatrix(states, MidiSong.maxOrder)
            tracks.append(self.createTrackDict(width, length, states, matrix))
        return tracks


    def generateSong(self, length):
        tracks = self.generateTracks(length)
        return MidiSong(None, tracks)


    def getMidiTrackFromStates(self, states, width, channel):
        track = midi.Track()
        currState = MidiState()
        for state in states:
            tick = width
            if state != currState:
                missingNotes, extraPitches = currState.getDiff(state)
                for note in missingNotes:
                    event = midi.NoteOnEvent(tick=tick,
                                             channel=channel,
                                             data=list(note))
                    track.append(event)
                    tick = 0
                for pitch in extraPitches:
                    event = midi.NoteOnEvent(tick=tick,
                                             channel=channel,
                                             data=(pitch, 0))
                    track.append(event)
                    tick = 0
                currState = state
        track.append(midi.EndOfTrackEvent(tick=1))
        return track


    def initMidiPattern(self):
        self.isValidTracks()
        self.trackCount = len(self.tracks)

        pattern = midi.Pattern()
        for i in xrange(len(self.tracks)):
            track = self.getMidiTrackFromStates(self.tracks[i]['states'],
                                                self.tracks[i]['width'],
                                                i)
            pattern.append(track)

        self.midiPattern = pattern


    def isValidMidiPattern(self):
        if (self.midiPattern == None or
           not isinstance(self.midiPattern, midi.Pattern)):
            raise Exception("Midi pattern has not been initialized or is \
invalid.")
        return True


    def exportToFile(self, path):
        self.isValidMidiPattern()
        try:
            midi.write_midifile(path, self.midiPattern)
            return True
        except:
            return False



# Testing
#Song = MidiSong('sample_midi/DukeSingleLonger.mid')
#NewSong = Song.generateSong(289*10)
#NewSong.exportToFile('generated_midi/Testing.mid')
