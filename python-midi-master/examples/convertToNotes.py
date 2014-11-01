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

def getNoteAndTickAndVelocityCounts(l):
    noteCounts = {}
    tickCounts = {}
    velocityCounts = {}
    for i in xrange(len(l)-1):
        currNote = l[i][0]
        nextNote = l[i+1][0]
        currTick = l[i][1]
        nextTick = l[i+1][1]
        currVelocity = l[i][2]
        nextVelocity = l[i+1][2]
        if currNote in noteCounts:
            if nextNote in noteCounts[currNote]:
                noteCounts[currNote][nextNote] += 1
            else:
                noteCounts[currNote][nextNote] = 1
        else:
            noteCounts[currNote] = {}
            noteCounts[currNote][nextNote] = 1
        if currTick in tickCounts:
            if nextTick in tickCounts[currTick]:
                tickCounts[currTick][nextTick] += 1
            else:
                tickCounts[currTick][nextTick] = 1
        else:
            tickCounts[currTick] = {}
            tickCounts[currTick][nextTick] = 1
        if currVelocity in velocityCounts:
            if nextVelocity in velocityCounts[currVelocity]:
                velocityCounts[currVelocity][nextVelocity] += 1
            else:
                velocityCounts[currVelocity][nextVelocity] = 1
        else:
            velocityCounts[currVelocity] = {}
            velocityCounts[currVelocity][nextVelocity] = 1
    return noteCounts, tickCounts, velocityCounts

def getMatrix(l):
    counts = getNoteAndTickAndVelocityCounts(l)
    """
    for row in xrange(len(noteCounts)):
        sumOfRow = sum(noteCounts[row])
        if sumOfRow == 0: sumOfRow = 1
        for col in xrange(len(noteCounts[row])):
            noteCounts[row][col] = round(noteCounts[row][col]/float(sumOfRow), 4)
    """
    return counts

def createTransMatrix(filename):
    pattern = midi.read_midifile(filename)
    pprint.pprint(pattern)
    notesAndTicksAndVelocity = {}
    for i in xrange(0, len(pattern)):
        text = ''
        data = tuple([])
        j = 0
        prevVelocity = None
        while j < len(pattern[i]):
            if type(pattern[i][j]) == midi.events.TrackNameEvent:
                text = pattern[i][j].text
                data = tuple(pattern[i][j].data)
                j += 1
            elif (type(pattern[i][j]) == midi.events.NoteOnEvent or
                 type(pattern[i][j]) == midi.events.NoteOffEvent):
                notes = []
                notes.append(pattern[i][j].data[0])
                channel = pattern[i][j].channel
                if type(pattern[i][j]) == midi.events.NoteOffEvent:
                    velocity = 0
                else:
                    velocity = pattern[i][j].data[1]
                tick = pattern[i][j].tick
                prevVelocity = pattern[i][j].data[1]
                j += 1
                while ((type(pattern[i][j]) == midi.events.NoteOnEvent or
                        type(pattern[i][j]) == midi.events.NoteOffEvent) and
                       pattern[i][j].data[1] == prevVelocity):
                    notes.append(pattern[i][j].data[0])
                    prevVelocity = pattern[i][j].data[1]
                    j += 1
                if (channel, text, data) in notesAndTicksAndVelocity:
                    notesAndTicksAndVelocity[(channel, text, data)].append((tuple(notes), tick, velocity))
                else:
                    notesAndTicksAndVelocity[(channel, text, data)] = [(tuple(notes), tick, velocity)]
            else:
                j += 1
    #pprint.pprint(notesAndTicks)
    matrix = {}
    for track in notesAndTicksAndVelocity:
        matrix[track] = getMatrix(notesAndTicksAndVelocity[track])
    return matrix

def createPattern(matrixDict):
    length = 200
    patternDict = {}
    for track in matrixDict:
        matrix = matrixDict[track]
        startingNote = random.choice(matrix[0].keys())
        startingTick = random.choice(matrix[1].keys())
        startingVelocity = random.choice(matrix[2].keys())
        pattern = []
        for singleNote in startingNote:
            pattern.append((singleNote, startingTick, startingVelocity))

        for i in xrange(length):
            countedNoteSum = 0
            if startingNote not in matrix[0]:
                startingNote = random.choice(matrix[0].keys())
            countNoteSum = sum(matrix[0][startingNote].values())
            selectedNoteCount = random.randrange(1, countNoteSum + 1)
            for key in matrix[0][startingNote]:
                countedNoteSum += matrix[0][startingNote][key]
                if(countedNoteSum >= selectedNoteCount):
                    startingNote = key
                    break
            countedTickSum = 0
            if startingTick not in matrix[1]:
                startingTick = random.choice(matrix[1].keys())
            countTickSum = sum(matrix[1][startingTick].values())
            selectedTickCount = random.randrange(1, countTickSum + 1)
            for key in matrix[1][startingTick]:
                countedTickSum += matrix[1][startingTick][key]
                if(countedTickSum >= selectedTickCount):
                    startingTick = key
                    break
            countedVelocitySum = 0
            if startingVelocity not in matrix[2]:
                startingVelocity = random.choice(matrix[2].keys())
            countVelocitySum = sum(matrix[2][startingVelocity].values())
            selectedVelocityCount = random.randrange(1, countVelocitySum + 1)
            for key in matrix[2][startingVelocity]:
                countedVelocitySum += matrix[2][startingVelocity][key]
                if(countedVelocitySum >= selectedVelocityCount):
                    startingVelocity = key
                    break
            for singleNote in startingNote:
                pattern.append((singleNote, startingTick, startingVelocity))
        patternDict[track] = pattern
    return patternDict

def createMidiTrackNotes(patternDict):
    pattern = midi.Pattern()
    count = 0
    for trackKey in patternDict:
        track = midi.Track()
        track.append(midi.TrackNameEvent(tick=0, text=trackKey[1], data=trackKey[2]))
        pattern.append(track)

        notesList = []
        for i in xrange(len(patternDict[trackKey])):
            note = patternDict[trackKey][i][0]
            tick = patternDict[trackKey][i][1]
            velocity = patternDict[trackKey][i][2]
            notesList.append((note, tick, velocity))

        for note, tick, velocity in notesList:
            track.append(midi.NoteOnEvent(tick=tick, channel=trackKey[0], data=[note, velocity]))

        track.append(midi.EndOfTrackEvent(tick=1))
        #print trackKey, ":"
        #pprint.pprint(track)
        count += 1
    print pattern
    midi.write_midifile("generated.mid", pattern)

matrixDict = createTransMatrix("Bass_sample.mid")
pprint.pprint(matrixDict)
patternDict = createPattern(matrixDict)
#pprint.pprint(patternDict)
createMidiTrackNotes(patternDict)

