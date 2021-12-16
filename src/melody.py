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

    durationValues = [1, 0.5, 2, 1.5]
    durationValuesWeights = [8, 2, 2, 1]

    def __init__(self, ks: key.KeySignature, ts: meter.TimeSignature) -> None:
        self.ks = ks
        self.ts = ts

    def generateMidiValuesFromMarkovModel(self, numMeasures: int, interpolate: bool = False) -> tuple[list[int], list[int]]:
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
            durationValues.append(d)
        midiValues = midiValues[:numMeasures] if interpolate else midiValues
        return midiValues, durationValues

    def generateMidiValuesFromUniform(self, numMeasures: int, interpolationRate: int = 1) -> list[int]:
        midiValues = []
        for i in range(numMeasures):
            n = util.noteInKeyFromMidiValue(random.randint(67, 77), self.ks)
            midiValues.append(n.pitch.midi)
        return midiValues

    def generateMidiValuesFromNormal(self, numMeasures: int, interpolationRate: int = 1) -> list[int]:
        normalValues = util.gen_normal(72, 2, numMeasures)
        midiValues = []
        for mv in normalValues:
            n = util.noteInKeyFromMidiValue(mv, self.ks)
            midiValues.append(n.pitch.midi)
        return midiValues

    def generateNotesFromMidi(self, midiValues: list[int], durationValues: list[int], numMeasures: int) -> stream.Stream:
        assert len(midiValues) == len(durationValues)
        s = stream.Stream()
        s.keySignature = self.ks
        s.timeSignature = self.ts
        s.insert(0, dynamics.Dynamic(0.75))
        while (s.duration.quarterLength < numMeasures * self.ts.numerator):
            for midi, d in zip(midiValues, durationValues):
                n = util.noteInKeyFromMidiValue(midi, self.ks)
                n.duration = duration.Duration(d)
                s.append(n)
        return s

    def interpolateMelody(self, midiValues: list[int]):
        k = self.ks.asKey()
        interpolatedMidiValues = []
        durationValues = []
        currentInterval = 0
        for m in midiValues:
            rythmSum = self.ts.numerator
            d, rythmSum = self.getDuration(rythmSum)
            interpolatedMidiValues.append(m)
            durationValues.append(d)
            currentMidi = m
            while(rythmSum > 0):
                currentDegree = k.getScaleDegreeFromPitch(pitch.Pitch(currentMidi), comparisonAttribute='pitchClass')
                currentInterval = self.getIntervalFromWeightedGraph(currentDegree, currentInterval, currentMidi)
                currentMidi = currentMidi + currentInterval
                interpolatedMidiValues.append(currentMidi)

                d, rythmSum = self.getDuration(rythmSum)
                durationValues.append(d)

        return interpolatedMidiValues, durationValues
            
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
        c = random.choices(population=self.durationValues, weights=self.durationValuesWeights)[0]
        sum -= c
        if sum < 0:
            c += sum
        return c, sum

