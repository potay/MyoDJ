import midi, pprint, random

# def getNoteAndTickAndVelocityCounts(l):
#     noteCounts = {}
#     tickCounts = {}
#     velocityCounts = {}
#     for i in xrange(len(l)-1):
#         currNote = l[i][0]
#         nextNote = l[i+1][0]
#         currTick = l[i][1]
#         nextTick = l[i+1][1]
#         currVelocity = l[i][2]
#         nextVelocity = l[i+1][2]
#         if currNote in noteCounts:
#             if nextNote in noteCounts[currNote]:
#                 noteCounts[currNote][nextNote] += 1
#             else:
#                 noteCounts[currNote][nextNote] = 1
#         else:
#             noteCounts[currNote] = {}
#             noteCounts[currNote][nextNote] = 1
#         if currTick in tickCounts:
#             if nextTick in tickCounts[currTick]:
#                 tickCounts[currTick][nextTick] += 1
#             else:
#                 tickCounts[currTick][nextTick] = 1
#         else:
#             tickCounts[currTick] = {}
#             tickCounts[currTick][nextTick] = 1
#         if currVelocity in velocityCounts:
#             if nextVelocity in velocityCounts[currVelocity]:
#                 velocityCounts[currVelocity][nextVelocity] += 1
#             else:
#                 velocityCounts[currVelocity][nextVelocity] = 1
#         else:
#             velocityCounts[currVelocity] = {}
#             velocityCounts[currVelocity][nextVelocity] = 1
#     return noteCounts, tickCounts, velocityCounts

def getNoteAndTickAndVelocityCounts(l):
    noteCounts = {}
    velocityCounts = {}
    for i in xrange(len(l)-1):
        currNote = l[i][0]
        nextNote = l[i+1][0]
        currTick = l[i][1]
        nextTick = l[i+1][1]
        currVelocity = l[i][2]
        nextVelocity = l[i+1][2]
        if (currNote, currTick) in noteCounts:
            if (nextNote, nextTick) in noteCounts[(currNote, currTick)]:
                noteCounts[(currNote, currTick)][(nextNote, nextTick)] += 1
            else:
                noteCounts[(currNote, currTick)][(nextNote, nextTick)] = 1
        else:
            noteCounts[(currNote, currTick)] = {}
            noteCounts[(currNote, currTick)][(nextNote, nextTick)] = 1
        
        if currVelocity in velocityCounts:
            if nextVelocity in velocityCounts[currVelocity]:
                velocityCounts[currVelocity][nextVelocity] += 1
            else:
                velocityCounts[currVelocity][nextVelocity] = 1
        else:
            velocityCounts[currVelocity] = {}
            velocityCounts[currVelocity][nextVelocity] = 1
    return noteCounts, velocityCounts

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
    # pprint.pprint(pattern)
    notesAndTicksAndVelocity = {}
    pitchAndTicks = {}
    pitchAndTickDiffs = {}
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
                pitch = pattern[i][j].data[0]
                notes.append(pitch)
                channel = pattern[i][j].channel
                tick = pattern[i][j].tick
                if type(pattern[i][j]) == midi.events.NoteOffEvent:
                    velocity = 0
                    tickDiff = abs(pitchAndTicks[pitch][2] - tick)
                    if pitch in pitchAndTickDiffs:
                        pitchAndTickDiffs[pitch].append(tickDiff)
                    else:
                        pitchAndTickDiffs[pitch] = [tickDiff]
                    pitchAndTicks[pitch] = (False, channel, tick)
                else:
                    velocity = pattern[i][j].data[1]
                    pitchAndTicks[pitch] = (True, channel, tick)
                prevVelocity = pattern[i][j].data[1]
                j += 1
                while ((type(pattern[i][j]) == midi.events.NoteOnEvent or
                        type(pattern[i][j]) == midi.events.NoteOffEvent) and
                       pattern[i][j].data[1] == prevVelocity):
                    if (type(pattern[i][j]) == midi.events.NoteOffEvent or 
                        velocity == 0):
                        tickDiff = abs(pitchAndTicks[pitch][2] - tick)
                        if pitch in pitchAndTickDiffs:
                            pitchAndTickDiffs[pitch].append(tickDiff) 
                        else:
                            pitchAndTickDiffs[pitch] = [tickDiff]
                        pitchAndTicks[pitch] = (False, channel, 0)
                    else:
                        pitchAndTicks[pitch] = (True, channel, tick)
                    notes.append(pitch)
                    prevVelocity = pattern[i][j].data[1]
                    j += 1
                if (channel, text, data) in notesAndTicksAndVelocity:
                    notesAndTicksAndVelocity[(channel, text, data)].append((tuple(notes), tick, velocity))
                else:
                    notesAndTicksAndVelocity[(channel, text, data)] = [(tuple(notes), tick, velocity)]
            else:
                j += 1
    
    matrix = {}
    for track in notesAndTicksAndVelocity:
        matrix[track] = getMatrix(notesAndTicksAndVelocity[track])
    return matrix, pitchAndTickDiffs

def createPattern(matrixDict, pitchAndTickDict):
    length = 200
    patternDict = {}
    for track in matrixDict:
        matrix = matrixDict[track]
        startingNoteAndTick = random.choice(matrix[0].keys())
        startingNote = startingNoteAndTick[0]
        startingTick = startingNoteAndTick[1]
        # if startingNote not in pitchAndTickDict:
        #     startingNote = (random.choice(pitchAndTickDict.keys()),)
        # startingTick = random.choice(pitchAndTickDict[startingNote[0]])
        startingVelocity = random.choice(matrix[1].keys())
        pattern = []
        for singleNote in startingNote:
            pattern.append((singleNote, startingTick, startingVelocity))

        for i in xrange(length):
            
            countedNoteAndTickSum = 0
            if startingNoteAndTick not in matrix[0]:
                startingNoteAndTick = random.choice(matrix[0].keys())
            # prevNote = startingNote[0]
            countNoteAndTickSum = sum(matrix[0][startingNoteAndTick].values())
            selectedNoteAndTickCount = random.randrange(1, countNoteAndTickSum + 1)
            for key in matrix[0][startingNoteAndTick]:
                print "key=", key
                print matrix[0][startingNoteAndTick]
                countedNoteAndTickSum += matrix[0][startingNoteAndTick][key]
                if(countedNoteAndTickSum >= selectedNoteAndTickCount):
                    startingNoteAndTick = key
                    startingNote = key[0]
                    startingTick = key[1]
                    break

            # while prevNote not in pitchAndTickDict.keys():
                # prevNote = random.choice(matrix[0].keys())[0]
            # startingTick = random.choice(pitchAndTickDict[prevNote])

            # countedTickSum = 0
            # if startingTick not in matrix[1]:
                # startingTick = random.choice(matrix[1].keys())
            # countTickSum = sum(matrix[1][startingTick].values())
            # selectedTickCount = random.randrange(1, countTickSum + 1)
            # for key in matrix[1][startingTick]:
                # countedTickSum += matrix[1][startingTick][key]
                # if(countedTickSum >= selectedTickCount):
                    # startingTick = key
                    # break

            countedVelocitySum = 0
            if startingVelocity not in matrix[1]:
                startingVelocity = random.choice(matrix[1].keys())
            countVelocitySum = sum(matrix[1][startingVelocity].values())
            selectedVelocityCount = random.randrange(1, countVelocitySum + 1)
            for key in matrix[1][startingVelocity]:
                countedVelocitySum += matrix[1][startingVelocity][key]
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
            track.append(midi.NoteOnEvent(tick=0, channel=trackKey[0], data=[note, velocity]))
            track.append(midi.NoteOnEvent(tick=tick, channel=trackKey[0], data=[note, velocity]))

        track.append(midi.EndOfTrackEvent(tick=1))
        #print trackKey, ":"
        #pprint.pprint(track)
        count += 1
    # print pattern
    midi.write_midifile("generated_4.mid", pattern)

matrixDict, pitchAndTickDict = createTransMatrix("duke.mid")
# pprint.pprint(matrixDict)
# pprint.pprint(pitchAndTickMatrix)
patternDict = createPattern(matrixDict, pitchAndTickDict)
#pprint.pprint(patternDict)
createMidiTrackNotes(patternDict)

