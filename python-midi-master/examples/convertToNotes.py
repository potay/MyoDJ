import midi, pprint

def getNoteLetter(note):
   if note % 12 == 9:
      note = "A"
   elif note % 12 == 10:
      note = "A#"
   elif note % 12 == 11:
      note = "B"
   elif note % 12 == 0:
      note = "C"
   elif note % 12 == 1:
      note = "C#"
   elif note % 12 == 2:
      note = "D"
   elif note % 12 == 3:
      note = "D#"
   elif note % 12 == 4:
      note = "E"
   elif note % 12 == 5:
      note = "F"
   elif note % 12 == 6:
      note = "F#"
   elif note % 12 == 7:
      note = "G"
   elif note % 12 == 8:
      note = "G#"
   return note

def make2dList(rows, cols, content):
     a=[]
     for row in xrange(rows): a += [[content]*cols]
     return a

def getNoteCounts(l):
   numOfNotes = 12
   numOfChannels = 
   notesDict = {"A": 9, "A#": 10, "B": 11, "C": 0, "C#": 1, "D": 2, "D#": 3, 
                "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8}
   noteCounts = make2dList(12, 12, 0)
   for i in xrange(len(l)-1):
      curNote = notesDict[l[i][0]]
      nextNote = notesDict[l[i+1][0]]
      noteCounts[curNote][nextNote] += 1
   return noteCounts

def getNoteProbabilities(l):
   noteCounts = getNoteCounts(l)
   for row in xrange(len(noteCounts)):
      sumOfRow = sum(noteCounts[row])
      if sumOfRow == 0: sumOfRow = 1
      for col in xrange(len(noteCounts[row])):
         noteCounts[row][col] = round(noteCounts[row][col]/float(sumOfRow), 4)
   return noteCounts

def createNotes(filename):
   pattern = midi.read_midifile(filename)
   print pattern
   notesAndTicks = []
   for i in xrange(1, len(pattern)):
      for j in xrange(len(pattern[i])):
         if type(pattern[i][j]) == midi.events.NoteOnEvent:
            channel = pattern[i][j].channel
            pitch = pattern[i][j].data[0]
            note = getNoteLetter(pitch)
            tick = pattern[i][j].tick
            notesAndTicks.append((note, tick, channel))
   noteProbabilities = getNoteProbabilities(notesAndTicks)
   # pprint.pprint(noteProbabilities)

createNotes("duke.mid")
