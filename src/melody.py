from math import ceil
import random
import util
from music21 import duration, dynamics, key, meter, note, pitch, stream, tempo

class MelodyGraph:
    degreeToIntervalsDict: dict = {
        1: [-7, -5, -3, -1, 0, 2, 4, 5, 7],
        2: [-7, -5, -3, -2, 0, 2, 3, 5, 7],
        3: [-7, -5, -4, -2, 0, 1, 3, 5, 7],
        4: [-6, -5, -3, -1, 0, 2, 4, 6, 7],
        5: [-7, -5, -3, -2, 0, 2, 4, 5, 7],
        6: [-7, -5, -4, -2, 0, 2, 3, 5, 7],
        7: [-7, -6, -4, -2, 0, 1, 3, 5, 6],
    }

    indexDict: dict = {
        -7: 0, -6: 1, -5: 1, -4: 2, -3: 2, -2: 3, -1: 3,
        0: 4, 1: 5, 2: 5, 3: 6, 4: 6, 5: 7, 6: 7, 7: 8
    }

    markovIntervalWeights = [
        [0.1, 0.10, 0.20, 0.50, 0.05, 0.85, 0.34, 0.10, 0.1],
        [0.1, 0.10, 0.20, 0.50, 0.05, 0.70, 0.28, 0.10, 0.1],
        [0.1, 0.10, 0.20, 0.50, 0.05, 0.60, 0.24, 0.10, 0.1],
        [0.1, 0.10, 0.50, 0.50, 0.05, 0.55, 0.22, 0.10, 0.1],
        [0.1, 0.10, 0.20, 0.50, 0.01, 0.50, 0.20, 0.10, 0.1],
        [0.1, 0.10, 0.22, 0.55, 0.05, 0.50, 0.20, 0.10, 0.1],
        [0.1, 0.10, 0.24, 0.60, 0.05, 0.50, 0.20, 0.10, 0.1],
        [0.1, 0.10, 0.28, 0.70, 0.05, 0.50, 0.20, 0.10, 0.1],
        [0.1, 0.10, 0.34, 0.85, 0.05, 0.50, 0.20, 0.10, 0.1],
    ]

    durationsValues = [1, 0.5, 2, 1.5]
    durationsValuesWeights = [8, 2, 2, 1]

    def __init__(self, ks: key.KeySignature, ts: meter.TimeSignature) -> None:
        self.ks = ks
        self.ts = ts

    def generateMidiValuesFromMarkovModel(self, numMeasures) -> tuple[list[int], list[int]]:
        k = self.ks.asKey()
        midiValues: list[int] = []
        durationValues: list[int] = []

        currentDegree = 1
        currentInterval = 0
        currentNote = note.Note(k.pitchFromDegree(currentDegree))
        currentMidi = currentNote.pitch.midi
        
        rythmSum = self.ts.numerator * numMeasures
        while (rythmSum > 0):
            currentInterval = self.getIntervalFromWeightedGraph(currentDegree, currentInterval, currentMidi)
            d, rythmSum = self.getDuration(rythmSum)

            currentMidi = currentMidi + currentInterval
            currentDegree = k.getScaleDegreeFromPitch(pitch.Pitch(currentMidi), comparisonAttribute='pitchClass')

            midiValues.append(currentMidi)
            durationValues.append(1)
        return midiValues, durationValues

    def generateNotesFromMidi(self, midiValues: list[int], durationsValuesValues: list[int], numMeasures: int) -> stream.Stream:
        assert len(midiValues) == len(durationsValuesValues)
        s = stream.Stream()
        s.keySignature = self.ks
        s.timeSignature = self.ts
        s.insert(0, dynamics.Dynamic(0.75))
        while (s.duration.quarterLength < numMeasures * self.ts.numerator):
            for midi, d in zip(midiValues, durationsValuesValues):
                n = util.noteInKeyFromMidiValue(midi, self.ks)
                n.duration = duration.Duration(d)
                s.append(n)
        return s

    def interpolateMelody(self, midiValues: list[int], interpolationRate: int):
        k = self.ks.asKey()
        interpolatedMidiValues = []
        durationsValues = []
        currentInterval = 0

        for m in midiValues:
            interpolatedMidiValues.append(m)
            durationsValues.append(1)
            currentMidi = m

            for i in range(interpolationRate-1):
                currentDegree = k.getScaleDegreeFromPitch(pitch.Pitch(currentMidi), comparisonAttribute='pitchClass')
                currentInterval = self.getIntervalFromWeightedGraph(currentDegree, currentInterval, currentMidi)
                currentMidi = currentMidi + currentInterval
                interpolatedMidiValues.append(currentMidi)
                durationsValues.append(1)
                
        return interpolatedMidiValues, durationsValues
            
    def getIntervalFromWeightedGraph(self, currentDegree: int, currentInterval: int, currentMidi: int) -> int:
        weightIndex = self.indexDict[currentInterval]
        currentWeights = self.markovIntervalWeights[weightIndex]
        lowerCutOff, upperCutOff = self.getCutOff(currentMidi)
        return random.choices(
            population=self.degreeToIntervalsDict[currentDegree][lowerCutOff:upperCutOff],
            weights=currentWeights[lowerCutOff:upperCutOff]
        )[0] # Choices always returns a list, therefore [0] is added to just get the result

    def getCutOff(self, currentMidi) -> tuple[int, int]:
        lower = 0
        upper = 9
        if (currentMidi < 57): lower = 4
        if (currentMidi > 87): upper = 5
        return lower, upper

    def getDuration(self, sum: int) -> tuple[float, float]:
        c = random.choices(population=self.durationsValues, weights=self.durationsValuesWeights)[0]
        sum -= c
        if sum < 0:
            c += sum
        return c, sum

