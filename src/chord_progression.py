import random
from music21 import key, note, chord, stream, meter, dynamics

class ChordGraph:
    chordDict: dict = {
        'I':    [[1, 3, 5], ['iim', 'iiim', 'IV', 'V', 'vim']],
        'iim':  [[2, 4, 6], ['I', 'iiim', 'V']],
        'iiim': [[3, 5, 7], ['I', 'IV', 'vim']],
        'IV':   [[4, 6, 8], ['I', 'iim', 'V']],
        'V':    [[5, 7, 9], ['I', 'iiim', 'vim']],
        'vim':  [[6, 1, 3], ['iim', 'IV']]
    }

    chordRythms = [[2, 2, 2, 2], [4, 4, 4, 4]]

    def __init__(self, ks: key.KeySignature, ts: meter.TimeSignature) -> None:
        self.ks = ks
        self.k = self.ks.asKey()
        self.ts = ts
            
    def getNextChord(self, chordName: str) -> str:
        return random.choice(self.chordDict[chordName][1])

    def generateFourChordProgression(self) -> list[str]:
        initialChord = random.choice(['I', 'iim', 'iiim', 'IV', 'V', 'vim'])
        currentChord = initialChord
        progression: list[str] = [initialChord]
        while(len(progression) < 4):
            currentChord = self.getNextChord(currentChord)
            progression.append(currentChord)
        return progression

    def generateChord(self, chordName: str, quarterLength: int) -> chord.Chord:
        notesInChord = []
        rootNote = True
        for p in self.k.pitchesFromScaleDegrees(self.chordDict[chordName][0]):
            n = note.Note(p)
            n.octave = 3 if rootNote else 4
            rootNote = False
            notesInChord.append(n)
        c = chord.Chord(notesInChord, quarterLength=quarterLength)
        c.insertLyric(chordName)
        return c

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
