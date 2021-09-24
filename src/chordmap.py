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

    def resolveExtension(self, extension: str, baseDegree):
        if (extension == 'sus'):
            return note.Note(self.k.pitchFromDegree(baseDegree + 3))
        # elif (extension in ['2', '6', ])
            

    def generateChord(self, chordName: str):
        c = chord.Chord([
            note.Note(p) for p in self.k.pitchesFromScaleDegrees(self.chordDict[chordName][0])
        ], quarterLength=2)
        c.insertLyric(chordName)
        return c
    
    def getNextChord(self, chordName: str):
        return random.choice(self.chordDict[chordName][2])

    def generateProgression(self):
        s = stream.Stream()
        s.keySignature = self.ks
        currentChord = 'I'
        chordNum = 0
        while(chordNum < 20 or currentChord != 'I'):
            s.append(self.generateChord(currentChord))
            chordNum += 1
            currentChord = self.getNextChord(currentChord)
            
        s.append(self.generateChord(currentChord))
        s.show()
        # s.write('midi', 'C:/Users/johabru/Music/newmidi.midi')

class Chord:
    extensions: list[str] = ['2', '6', 'M7', 'M9']
    nextChords: list[str] = ['IV/I, V/I']

cm = ChordMap()
cm.generateProgression()