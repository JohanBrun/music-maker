import random
from numpy.random import default_rng
from music21 import key, note, chord, stream

rng = default_rng()


class ChordMap:
    chordDict: dict = {
        'I': [[1, 3, 5], ['2', '6', 'M7', 'M9', 'sus'], ['iim', 'iiim', 'IV', 'V', 'vim']],
        'iim': [[2, 4, 6], ['m7', 'm9'], ['I', 'iiim', 'V']],
        'iiim': [[3, 5, 7], ['m7'], ['I', 'IV', 'vim']],
        'IV': [[4, 6, 1], ['6', 'M7', 'm', 'm6'], ['I', 'iim', 'V']],
        'V': [[5, 7, 2], ['7', '9', '11', '13', 'sus'], ['I', 'iiim', 'vim']],
        'vim': [[6, 1, 3], ['m7', 'm9'], ['iim', 'IV']]
    }

    def __init__(self) -> None:
        self.ks = key.KeySignature(rng.integers(-6, 6))
        self.k = self.ks.asKey()

    def generateChord(self, chordName: str):
        return chord.Chord([
            note.Note(p) for p in self.k.pitchesFromScaleDegrees(self.chordDict[chordName][0])
        ], quarterLength=2)
    
    def getNextChord(self, chordName: str):
        return random.choice(self.chordDict[chordName][2])

    def generateProgression(self):
        s = stream.Stream()
        currentChord = 'I'
        chordNum = 0
        while(chordNum < 20 or currentChord != 'I'):
            s.append(self.generateChord(currentChord))
            chordNum += 1
            currentChord = self.getNextChord(currentChord)
            
        s.append(self.generateChord(currentChord))
        s.show()

class Chord:
    extensions: list[str] = ['2', '6', 'M7', 'M9']
    nextChords: list[str] = ['IV/I, V/I']

cm = ChordMap()
cm.generateProgression()