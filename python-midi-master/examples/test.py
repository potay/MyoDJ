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
   for i in xrange(0, len(args), 2):
      note = getNoteNumber(args[i])
      tick = args[i+1]
      notesList.append((note, tick))

   for note, tick in notesList:
      track.append(midi.NoteOnEvent(tick=0, channel=1, data=[note, 100]))
      track.append(midi.NoteOnEvent(tick=tick, channel=1, data=[note, 0]))

   track.append(midi.EndOfTrackEvent(tick=1))
   print pattern
   midi.write_midifile("test.mid", pattern)

# loop = [("G", 20)*10]
createMidiTrackNotes("A", 40, "F", 10, "Gsharp", 80)