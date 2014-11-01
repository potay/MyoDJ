import midi, pprint, random

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
    noteCounts = {}
    for i in xrange(len(l)-1):
        curNote = l[i][0]
        nextNote = l[i+1][0]
        if curNote in noteCounts:
            if nextNote in noteCounts[curNote]:
                noteCounts[curNote][nextNote] += 1
            else:
                noteCounts[curNote][nextNote] = 1
        else:
            noteCounts[curNote] = {}
            noteCounts[curNote][nextNote] = 1
    return noteCounts

def getNoteProbabilities(l):
    noteCounts = getNoteCounts(l)
    """
    for row in xrange(len(noteCounts)):
        sumOfRow = sum(noteCounts[row])
        if sumOfRow == 0: sumOfRow = 1
        for col in xrange(len(noteCounts[row])):
            noteCounts[row][col] = round(noteCounts[row][col]/float(sumOfRow), 4)
    """
    return noteCounts

def createTransMatrix(filename):
    pattern = midi.read_midifile(filename)
    #print pattern
    notesAndTicks = {}
    for i in xrange(1, len(pattern)):
        for j in xrange(len(pattern[i])):
            if type(pattern[i][j]) == midi.events.NoteOnEvent:
                channel = pattern[i][j].channel
                pitch = pattern[i][j].data[0]
                note = pitch
                tick = pattern[i][j].tick
                if channel in notesAndTicks:
                    notesAndTicks[channel].append((note, tick))
                else:
                    notesAndTicks[channel] = [(note, tick)]
    pprint.pprint(notesAndTicks)
    noteProbabilities = {}
    for track in notesAndTicks:
        noteProbabilities[track] = getNoteProbabilities(notesAndTicks[track])
    return noteProbabilities

def createPattern(matrixDict):
    length = 200
    patternDict = {}
    for track in matrixDict:
        matrix = matrixDict[track]
        startingNote = random.choice(matrix.keys())
        pattern = []

        for i in xrange(length):
            counted_sum = 0
            count_sum = sum(matrix[startingNote].values())
            selected_count = random.randrange(1, count_sum + 1)
            for key in matrix[startingNote]:
                counted_sum += matrix[startingNote][key]
                if(counted_sum >= selected_count):
                    startingNote = key
                    pattern.append((key, 100))
                    break
        patternDict[track] = pattern
    return patternDict

def createMidiTrackNotes(patternDict):
    pattern = midi.Pattern()
    for trackKey in patternDict:
        track = midi.Track()
        pattern.append(track)

        notesList = []
        for i in xrange(len(patternDict[trackKey])):
            note = patternDict[trackKey][i][0]
            tick = patternDict[trackKey][i][1]
            notesList.append((note, tick))

        for note, tick in notesList:
            track.append(midi.NoteOnEvent(tick=0, data=[note, 100]))
            track.append(midi.NoteOffEvent(tick=tick, data=[note, 0]))

        track.append(midi.EndOfTrackEvent(tick=1))

        pprint.pprint(track)
    midi.write_midifile("generated.mid", pattern)

matrixDict = createTransMatrix("duke.mid")
#pprint.pprint(matrixDict)
patternDict = createPattern(matrixDict)
#pprint.pprint(patternDict)
createMidiTrackNotes(patternDict)

