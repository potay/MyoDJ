import midi

class MidiTune(object):
    @staticmethod
    def getNoteNum(note, octave):
        noteMap = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6,
                   'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
        middleOctaveOffset = 6
        if note not in noteMap:
            return None
        else:
            return (octave + middleOctaveOffset)*12 + noteMap(note)

    def __init__(self, *args):
        self.pattern = midi.Pattern()
        self.track = midi.Track()
        self.pattern.append(track)
        self.volume = 100


    notesList = []
    for i in xrange(0, len(args)):
        note = getNoteNumber(args[i][0])
        tick = args[i][1]
        notesList.append((note, tick))

    for note, tick in notesList:
        track.append(midi.NoteOnEvent(tick=0, channel=1, data=[note, 100]))
        track.append(midi.NoteOnEvent(tick=tick, channel=1, data=[note, 0]))

    track.append(midi.EndOfTrackEvent(tick=1))
