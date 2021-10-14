from music21 import note, duration, key, meter, stream, instrument
import util


class Measure:
    notesInMeasure: int = 4
    ks: key.KeySignature = key.KeySignature(0)

    def __init__(self) -> None:
        self.notes: note.Note = []
        self.durations: list[duration.Duration] = []
        midiValues = util.gen_normal(65, 2.25, self.notesInMeasure)
        durationValues = util.gen_normal(0, 1, self.notesInMeasure)
        for mv, dv in zip(midiValues, durationValues):
            self.notes.append(util.note_from_noise(mv, self.ks))
            self.durations.append(duration.Duration(2**dv))

    def getStream(self):
        s = stream.Measure()
        for n, d in zip(self.notes, self.durations):
            n.duration = d
            s.append(n)
        return s


class Movement:
    chordProgression: list[int]
    numMeasures: int = 5

    def __init__(self) -> None:
        self.measures: list[Measure] = []
        for i in range(self.numMeasures):
            newMeasure = Measure()
            self.measures.append(newMeasure)

    def getStream(self):
        s = []
        for measure in self.measures:
            s.append(measure.getStream())
        return s


class Composition:
    k: key.Key = key.Key('C')
    ts: meter.TimeSignature = meter.TimeSignature('4/4')
    tempo: int = 120

    def __init__(self) -> None:
        firstMovement = Movement()
        secondMovement = Movement()
        self.movements = [firstMovement, secondMovement]

    def compose(self) -> stream.Stream:
        part = []
        for movement in self.movements:
        #   s.append(movement.getStream())
            part += movement.getStream()
        s = stream.Part(part)
        return s


c = Composition()
s = c.compose()
s.show()
s.write('midi', '../melodi.midi')
