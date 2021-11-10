import random
from music21 import duration, key, note, chord, stream, meter

class ChordMap:
    chordDict: dict = {
        'I': [[1, 3, 5], [2, 9, 11, 14, 'sus'], ['iim', 'iiim', 'IV', 'V', 'vim']],
        'iim': [[2, 4, 6], [10, 14], ['I', 'iiim', 'V']],
        'iiim': [[3, 5, 7], [10], ['I', 'IV', 'vim']],
        'IV': [[4, 6, 8], [9, 11, 'm', 8], ['I', 'iim', 'V']],
        'V': [[5, 7, 9], [11, 14, 17, 21, 'sus'], ['I', 'iiim', 'vim']],
        'vim': [[6, 1, 3], [10, 14], ['iim', 'IV']]
    }

    def __init__(self, ks: key.KeySignature, ts: meter.TimeSignature) -> None:
        self.ks = ks
        self.k = self.ks.asKey()
        self.ts = ts

    def addExtension(self, c: chord.Chord, extensions: list[str], p=0.1):
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
            

    def generateChord(self, chordName: str):
        c = chord.Chord([
            note.Note(p) for p in self.k.pitchesFromScaleDegrees(self.chordDict[chordName][0])
        ], quarterLength=2)
        bassNote = note.Note(c.getChordStep(1).midi - 12)
        c.add(bassNote)
        c.insertLyric(chordName)
        c = self.addExtension(c, self.chordDict[chordName][1])
        return c
    
    def getNextChord(self, chordName: str):
        return random.choice(self.chordDict[chordName][2])

    def generateRepeatableProgression(self) -> list[str]:
        chordNum: int = 1
        currentChord: str = 'I'
        progression: list[str] = ['I']
        while(chordNum < 4 or 'I' not in self.chordDict[currentChord][2]):
            currentChord = self.getNextChord(currentChord)
            progression.append(currentChord)
            chordNum += 1
        return progression

    def generateChords(self, progression: list[str]) -> stream.Stream:
        s = stream.Stream()
        s.id = 'Chords'
        measures: list[stream.Measure] = []
        m = stream.Measure()
        for chordName in progression:
            if m.duration == duration.Duration(4):
                measures.append(m)
                m = stream.Measure()
            m.append(self.generateChord(chordName))

        measures.append(m)
        s.append(measures)
        s.keySignature = self.ks
        s.timeSignature = self.ts
        return s


 