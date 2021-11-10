import random
from music21 import note, duration, key, meter, stream
import util


class Measure:
    ks: key.KeySignature = key.KeySignature(0)
    ts: meter.TimeSignature = meter.TimeSignature('4/4')
    beatsInMeasure = ts.numerator

    def __init__(self) -> None:
        self.notes: note.Note = []
        self.durations: list[duration.Duration] = []
        midiValues = util.gen_normal(65, 2.25, self.beatsInMeasure)
        durationValues = util.gen_normal(0, 1, self.beatsInMeasure)
        durationSum: float = 0.0

        for mv, dv in zip(midiValues, durationValues):
            self.notes.append(util.note_from_noise(mv, self.ks))
            self.durations.append(duration.Duration(2**dv))
            durationSum += 2**dv
            if (durationSum >= self.beatsInMeasure):
                break

    def getStream(self):
        s = stream.Measure()
        for n, d in zip(self.notes, self.durations):
            n.duration = d
            s.append(n)
        return s


class Movement():
    def __init__(self, numMeasures: int) -> None:
        self.numMeasures = numMeasures
        self.measures: list[Measure] = []
        for i in range(self.numMeasures):
            newMeasure = Measure()
            self.measures.append(newMeasure)

    def getStream(self):
        s = []
        for measure in self.measures:
            s.append(measure.getStream())
        return s


class Composition():
    ts: meter.TimeSignature = meter.TimeSignature('4/4')

    def __init__(self, numMeasures: int, ks: key.KeySignature, ts: meter.TimeSignature) -> None:
        self.numMeasures = numMeasures
        self.ks = ks
        self.ts = ts
        firstMovement = Movement(numMeasures // 2)
        secondMovement = Movement(numMeasures // 2)
        self.movements = [firstMovement, secondMovement]

    def compose(self) -> stream.Stream:
        part = []
        for movement in self.movements:
            part += movement.getStream()
        s = stream.Part(part)
        s.keySignature = self.ks
        s.timeSignature = self.ts
        return s

