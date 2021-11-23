from math import ceil
import random
import numpy as np
from music21 import duration, dynamics, key, meter, note, pitch, stream, tempo

class MelodyGraph:
    intervalDict: dict = {
        1: [-7, -5, -3, -1, 0, 2, 4, 5, 7],
        2: [-7, -5, -3, -2, 0, 2, 3, 5, 7],
        3: [-7, -5, -4, -2, 0, 1, 3, 5, 7],
        4: [-6, -5, -3, -1, 0, 2, 4, 6, 7],
        5: [-7, -5, -3, -2, 0, 2, 4, 5, 7],
        6: [-7, -5, -4, -2, 0, 2, 3, 5, 7],
        7: [-7, -6, -4, -2, 0, 1, 3, 5, 6],
    }

    degreeStateDict: dict = {
        1: np.array([1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1]),
        2: np.array([1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]),
        3: np.array([1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]),
        4: np.array([0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1]),
        5: np.array([1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1]),
        6: np.array([1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]),
        7: np.array([1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0])
    }

    markovNoteWeights = np.array([
        [0.1, 0.1, 0.1, 0.1, 0.2, 0.5, 0.5, 0.1, 0.85, 0.85, 0.34, 0.17, 0.17, 0.1, 0.1],
        [0.1, 0.1, 0.1, 0.1, 0.2, 0.5, 0.5, 0.1, 0.80, 0.80, 0.32, 0.16, 0.16, 0.1, 0.1],
        [0.1, 0.1, 0.1, 0.1, 0.2, 0.5, 0.5, 0.1, 0.75, 0.75, 0.30, 0.15, 0.15, 0.1, 0.1],
        [0.1, 0.1, 0.1, 0.1, 0.2, 0.5, 0.5, 0.1, 0.70, 0.70, 0.28, 0.14, 0.14, 0.1, 0.1],
        [0.1, 0.1, 0.1, 0.1, 0.2, 0.5, 0.5, 0.1, 0.65, 0.65, 0.26, 0.13, 0.13, 0.1, 0.1],
        [0.1, 0.1, 0.1, 0.1, 0.2, 0.5, 0.5, 0.1, 0.60, 0.60, 0.24, 0.12, 0.12, 0.1, 0.1],
        [0.1, 0.1, 0.1, 0.1, 0.2, 0.5, 0.5, 0.1, 0.55, 0.55, 0.22, 0.11, 0.11, 0.1, 0.1],
        [0.1, 0.1, 0.1, 0.1, 0.2, 0.5, 0.5, 0.1, 0.50, 0.50, 0.2, 0.1, 0.1, 0.1, 0.1],
        [0.1, 0.1, 0.11, 0.11, 0.22, 0.55, 0.55, 0.1, 0.5, 0.5, 0.2, 0.1, 0.1, 0.1, 0.1],
        [0.1, 0.1, 0.12, 0.12, 0.24, 0.60, 0.60, 0.1, 0.5, 0.5, 0.2, 0.1, 0.1, 0.1, 0.1],
        [0.1, 0.1, 0.13, 0.13, 0.26, 0.65, 0.65, 0.1, 0.5, 0.5, 0.2, 0.1, 0.1, 0.1, 0.1],
        [0.1, 0.1, 0.14, 0.14, 0.28, 0.70, 0.70, 0.1, 0.5, 0.5, 0.2, 0.1, 0.1, 0.1, 0.1],
        [0.1, 0.1, 0.15, 0.15, 0.30, 0.75, 0.75, 0.1, 0.5, 0.5, 0.2, 0.1, 0.1, 0.1, 0.1],
        [0.1, 0.1, 0.16, 0.16, 0.32, 0.80, 0.80, 0.1, 0.5, 0.5, 0.2, 0.1, 0.1, 0.1, 0.1],
        [0.1, 0.1, 0.17, 0.17, 0.34, 0.85, 0.85, 0.1, 0.5, 0.5, 0.2, 0.1, 0.1, 0.1, 0.1],
    ])

    durations = [1, 0.5, 2, 1.5, 0.75]
    durationsWeights = [8, 2, 2, 1, 1]

    def __init__(self, numMeasures: int, ks: key.KeySignature, ts: meter.TimeSignature) -> None:
        self.numMeasures = numMeasures
        self.ks = ks
        self.ts = ts

    def markovMelody(self):
        k = self.ks.asKey()
        p = stream.Part()
        p.keySignature = self.ks
        # p.timeSignature = self.ts
        p.id = 'melody'

        mm = tempo.MetronomeMark(120)
        
        currentDegree = 1
        currentInterval = 0
        currentNote = note.Note(k.pitchFromDegree(currentDegree))
        
        for i in range(self.numMeasures):
            m = stream.Measure()
            m.append(mm)
            rythmSum = 4
            while (rythmSum > 0):
                currentInterval = self.getIntervalFromWeightedGraph(currentDegree, currentInterval, currentNote)
                d, rythmSum = self.getDuration(rythmSum)
                currentNote = note.Note(currentNote.pitch.midi + currentInterval)
                currentNote.duration = duration.Duration(d)
                currentDegree = k.getScaleDegreeFromPitch(currentNote.pitch, comparisonAttribute='pitchClass')
                m.append(currentNote)
            p.append(m)
        return p

    def repeatableMarkovMelody(self) -> tuple[list[int], list[int]]:
        k = self.ks.asKey()
        midiValues: list[int] = []
        durationValues: list[int] = []

        currentDegree = 1
        currentInterval = 0
        currentNote = note.Note(k.pitchFromDegree(currentDegree))
        currentMidi = currentNote.pitch.midi
        
        rythmSum = self.ts.numerator * self.numMeasures
        while (rythmSum > 0):
            currentInterval = self.getIntervalFromWeightedGraph(currentDegree, currentInterval, currentMidi)
            d, rythmSum = self.getDuration(rythmSum)

            currentMidi = currentMidi + currentInterval
            currentDegree = k.getScaleDegreeFromPitch(pitch.Pitch(currentMidi), comparisonAttribute='pitchClass')

            midiValues.append(currentMidi)
            durationValues.append(d)
        return midiValues, durationValues

    def generateNotesFromMidi(self, midiValues: list[int], durationsValues: list[int], numMeasures: int) -> stream.Stream:
        assert len(midiValues) == len(durationsValues)
        s = stream.Stream()
        s.keySignature = self.ks
        s.timeSignature = self.ts
        s.insert(0, dynamics.Dynamic(0.75))
        while (s.duration.quarterLength < numMeasures * self.ts.numerator):
            for midi, d in zip(midiValues, durationsValues):
                n = note.Note(midi)
                n.duration = duration.Duration(d)
                s.append(n)
        return s

    def interpolateMelody(self, midiValues: list[int]):
        k = self.ks.asKey()
        interpolated = []
        currentInterval = 0
        for m in midiValues:
            interpolated.append(m)
            currentMidi = m
            for i in range(3):
                currentDegree = k.getScaleDegreeFromPitch(pitch.Pitch(currentMidi), comparisonAttribute='pitchClass')
                currentInterval = self.getIntervalFromWeightedGraph(currentDegree, currentInterval, currentMidi)
                currentMidi = currentMidi + currentInterval
                interpolated.append(currentMidi)
                
            


    def getIntervalFromWeightedGraph(self, currentDegree: int, currentInterval: int, currentMidi: int) -> int:
        intervalIndex = currentInterval + 7
        mask = self.degreeStateDict[currentDegree] > 0
        currentWeights = self.markovNoteWeights[intervalIndex][mask]
        lowerCutOff, upperCutOff = self.getCutOff(currentMidi)
        return random.choices(
            population=self.intervalDict[currentDegree][lowerCutOff:upperCutOff],
            weights=currentWeights[lowerCutOff:upperCutOff]
        )[0] # Choices returns a list even when it only chooses one element, therefore index 0 to extract from the list

    def getCutOff(self, currentMidi) -> tuple[int, int]:
        lower = 0
        upper = 9
        if (currentMidi < 57): lower = 4
        if (currentMidi > 87): upper = 5
        return lower, upper

    def getDuration(self, sum: int) -> tuple[float, float]:
        c = random.choices(population=self.durations, weights=self.durationsWeights)[0]
        sum -= c
        if sum < 0:
            c += sum
        return c, sum

