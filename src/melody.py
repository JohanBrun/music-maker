from math import ceil
import random
import numpy as np
from music21 import key, meter, note, stream

class MelodyGraph:
    noteDict: dict = {
        1: [-7, -5, -3, -1, 0, 2, 4, 5, 7],
        2: [-7, -5, -3, -2, 0, 2, 3, 5, 7],
        3: [-7, -5, -4, -2, 0, 1, 3, 5, 7],
        4: [-6, -5, -3, -1, 0, 2, 4, 6, 7],
        5: [-7, -5, -3, -2, 0, 2, 4, 5, 7],
        6: [-7, -5, -4, -2, 0, 2, 3, 5, 7],
        7: [-7, -6, -4, -2, 0, 1, 3, 5, 6],
    }

    def __init__(self, numMeasures: int, ks: key.KeySignature, ts: meter.TimeSignature) -> None:
        self.numMeasures = numMeasures
        self.ks = ks
        self.ts = ts

    def walkTest(self):
        k = self.ks.asKey()
        s = stream.Part()
        s.keySignature = self.ks
        s.timeSignature = self.ts

        currentDegree = 1
        direction = 0
        ascendingWeights = [2, 3, 5, 10, 3, 10, 4, 1, 1]
        descendingWeights = [1, 1, 4, 10, 3, 10, 5, 3, 2]
        neutralWeights = [1, 1, 4, 10, 3, 10, 4, 1, 1]

        currentNote = note.Note(k.pitchFromDegree(currentDegree))
        
        for i in range(self.numMeasures):
            m = stream.Measure()
            for j in range(4):
                if (direction == -1):
                    inter, direction = self.getInterval(currentDegree, descendingWeights)
                elif (direction == 1):
                    inter, direction = self.getInterval(currentDegree, ascendingWeights)
                else:
                    inter, direction = self.getInterval(currentDegree, neutralWeights)

                currentNote = note.Note(currentNote.pitch.midi + inter)
                currentDegree = k.getScaleDegreeFromPitch(currentNote.pitch, comparisonAttribute='pitchClass')
                m.append(currentNote)
            s.append(m)
        
        return s
        
        

    def getInterval(self, currentDegree, weights):
        choices = []
        for interval, weight in zip(self.noteDict[currentDegree], weights):
            choices += [interval] * weight
        c = random.choice(choices)
        return c, np.sign(c)

