import midi

def getNoteNumber(note):
   if note == "A":
      note = 69
   elif note == "Asharp" or note == "A#" or note == "A sharp":
      note = 70
   elif note == "B":
      note = 71
   elif note == "C":
      note = 72
   elif note == "Csharp" or note == "C#" or note == "C sharp":
      note = 73
   elif note == "D":
      note = 74
   elif note == "Dsharp" or note == "D#" or note == "D sharp":
      note = 75
   elif note == "E":
      note = 76
   elif note == "F":
      note = 77
   elif note == "Fsharp" or note == "F#" or note == "F sharp":
      note = 78
   elif note == "G":
      note = 79
   elif note == "Gsharp" or note == "G#" or note == "G sharp":
      note = 80
   return note

def createMidiTrackNotes(*args):
   pattern = midi.Pattern()
   track = midi.Track()
   pattern.append(track)

   notesList = []
   for i in xrange(len(args)):
      note = getNoteNumber(args[i][0])
      tick = args[i][1]
      notesList.append((note, tick))

   for note, tick in notesList:
      track.append(midi.NoteOnEvent(tick=0, channel=1, data=[note, 100]))
      track.append(midi.NoteOnEvent(tick=tick, channel=1, data=[note, 0]))

   track.append(midi.EndOfTrackEvent(tick=1))
   print pattern
   midi.write_midifile("duke2.mid", pattern)

createMidiTrackNotes(('D#', 481), ('E', 0), ('B', 0), ('D#', 0), ('B', 0), ('G#', 0), ('B', 0), ('E', 0), ('G#', 0), ('G#', 2), ('D#', 0), ('D#', 0), ('B', 0), ('E', 0), ('B', 0), ('B', 0), ('G#', 0), ('E', 0), ('E', 0), ('G#', 0), ('B', 0), ('D#', 0), ('G#', 0), ('B', 0), ('D#', 0), ('B', 0), ('E', 0), ('E', 240), ('D#', 0), ('E', 0), ('G#', 0), ('G#', 0), ('B', 0), ('D#', 0), ('B', 0), ('B', 0), ('C#', 0), ('F#', 0), ('F#', 0), ('C#', 0), ('A#', 0), ('F#', 0), ('C#', 0), ('G#', 0), ('G#', 180), ('C#', 0), ('A#', 0), ('F#', 0), ('F#', 0), ('C#', 0), ('F#', 0), ('C#', 0), ('G#', 0), ('G#', 0), ('G#', 0), ('D#', 0), ('B', 0), ('D#', 0), ('B', 0), ('D#', 0), ('G#', 240), ('G#', 0), ('G#', 0), ('G#', 0), ('G#', 60), ('G#', 0), ('G#', 0), ('G#', 0), ('G#', 60), ('G#', 0), ('B', 0), ('B', 0), ('B', 0), ('B', 0), ('B', 60), ('B', 0), ('C#', 0), ('C#', 0), ('C#', 60), ('D#', 0), ('D#', 0), ('C#', 0), ('D#', 0), ('D#', 0), ('D#', 60))
