import random
from numpy.random import default_rng
from music21 import key, note, chord, stream, meter

rng = default_rng()


class ChordMap:
    chordDict: dict = {
        'I': [[1, 3, 5], [2, 9, 11, 14, 'sus'], ['iim', 'iiim', 'IV', 'V', 'vim']],
        'iim': [[2, 4, 6], [10, 14], ['I', 'iiim', 'V']],
        'iiim': [[3, 5, 7], [10], ['I', 'IV', 'vim']],
        'IV': [[4, 6, 8], [9, 11, 'm', 8], ['I', 'iim', 'V']],
        'V': [[5, 7, 9], [11, 14, 17, 21, 'sus'], ['I', 'iiim', 'vim']],
        'vim': [[6, 1, 3], [10, 14], ['iim', 'IV']]
    }

    def __init__(self) -> None:
        self.ks = key.KeySignature(rng.integers(-6, 6))
        self.k = self.ks.asKey()
        self.ts = meter.TimeSignature('3/4')

    def addExtension(self, c: chord.Chord, extensions: list[str], p=0.3):
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

    def generateProgression(self):
        s = stream.Stream()
        s.keySignature = self.ks
        s.timeSignature = self.ts
        currentChord = 'I'
        chordNum = 0
        while(chordNum < 20 or currentChord != 'I'):
            newChord = self.generateChord(currentChord)
            s.append(newChord)
            chordNum += 1
            currentChord = self.getNextChord(currentChord)
            
        s.append(self.generateChord(currentChord))
        s.show()
        s.write('midi', '../akkorder.midi')

class Chord:
    extensions: list[str] = ['2', '6', 'M7', 'M9']
    nextChords: list[str] = ['IV/I, V/I']

cm = ChordMap()
cm.generateProgression()