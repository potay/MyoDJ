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