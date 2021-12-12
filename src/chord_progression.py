import random
from music21 import key, note, chord, stream, meter, dynamics

class ChordGraph:
    chordDict: dict = {
        'I': [[1, 3, 5], [9, 11, 14, 'sus'], ['iim', 'iiim', 'IV', 'V', 'vim']],
        'iim': [[2, 4, 6], [10, 14], ['I', 'iiim', 'V']],
        'iiim': [[3, 5, 7], [10], ['I', 'IV', 'vim']],
        'IV': [[4, 6, 8], [9, 11, 'm', 8], ['I', 'iim', 'V']],
        'V': [[5, 7, 9], [11, 14, 17, 21, 'sus'], ['I', 'iiim', 'vim']],
        'vim': [[6, 1, 3], [10, 14], ['iim', 'IV']]
    }

    chordRythms = [[2, 2, 2, 2], [4, 4, 4, 4]]
    # chordRythms = [[4, 4, 4, 4]]

    def __init__(self, ks: key.KeySignature, ts: meter.TimeSignature) -> None:
        self.ks = ks
        self.k = self.ks.asKey()
        self.ts = ts

    def addExtension(self, c: chord.Chord, extensions: list[str], p=0.0) -> chord.Chord:
        extension = random.choice(extensions)
        if (random.uniform(0, 1) < p):
            if (extension == 'sus'):
                c.remove(c.getChordStep(3))
                c.add(note.Note(c.getChordStep(1).midi + 5))
                return c
            elif (extension == 'm'):
                c.remove(c.getChordStep(3))
                c.add(note.Note(c.getChordStep(1).midi + 3))
                return c
            else:
                c.add(note.Note(c.getChordStep(1).midi + extension))
        return c
            
    def generateChord(self, chordName: str, quarterLength: int) -> chord.Chord:
        notesInChord = []
        bottomNote = True
        for p in self.k.pitchesFromScaleDegrees(self.chordDict[chordName][0]):
            n = note.Note(p)
            n.octave = 3 if bottomNote else 4
            bottomNote = False
            notesInChord.append(n)
        c = chord.Chord(notesInChord, quarterLength=quarterLength)
        # bassNote = note.Note(c.getChordStep(1).midi - 12)
        # c.add(bassNote)
        c.insertLyric(chordName)
        c = self.addExtension(c, self.chordDict[chordName][1])
        return c
    
    def getNextChord(self, chordName: str) -> str:
        return random.choice(self.chordDict[chordName][2])

    def generateRepeatableProgression(self) -> list[str]:
        initialChord = random.choice(['I', 'iim', 'iiim', 'IV', 'V', 'vim'])
        currentChord = initialChord
        progression: list[str] = [initialChord]
        # while(len(progression) < 4 or initialChord not in self.chordDict[currentChord][2]):
        while(len(progression) < 4):
            currentChord = self.getNextChord(currentChord)
            progression.append(currentChord)
        return progression

    def generateChords(self, progression: list[str], numMeasures: int) -> stream.Stream:
        s = stream.Stream()
        s.id = 'Chords'
        s.insert(0, dynamics.Dynamic(0.5))
        quarterLengths = random.choice(self.chordRythms)
        while s.duration.quarterLength < numMeasures * self.ts.numerator:
            for chordName, ql in zip(progression, quarterLengths):
                s.append(self.generateChord(chordName, ql))

        s.keySignature = self.ks
        s.timeSignature = self.ts
        return s
