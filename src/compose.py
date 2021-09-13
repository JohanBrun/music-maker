from music21 import note, duration, key, meter, stream
import util


class Measure:
    durations: list[duration.Duration] = []
    notesInMeasure: int = 4
    ks: key.KeySignature = key.KeySignature(0)

    def __init__(self) -> None:
        self.notes: note.Note = []
        midiValues = util.gen_normal(60, 1, self.notesInMeasure)
        for mv in midiValues:
            self.notes.append(util.note_from_noise(mv, self.ks))
            self.durations.append(duration.Duration(1))

    def getStream(self):
        s = stream.Stream()
        for n in self.notes:
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
            print(newMeasure.notes)

    def getStream(self):
        s = stream.Stream()
        for measure in self.measures:
            s.append(measure.getStream())
        s.show()
        return s


class Composition:
    k: key.Key = key.Key('C')
    ts: meter.TimeSignature = meter.TimeSignature('4/4')
    tempo: int = 120

    def __init__(self) -> None:
        firstMovement = Movement()
        secondMovement = Movement()
        self.movements = [firstMovement, secondMovement, firstMovement]

    def compose(self) -> stream.Stream:
        s = stream.Stream()
        for movement in self.movements:
            s.append(movement.getStream())
        return s


c = Composition()
s = c.compose()
s.show()
