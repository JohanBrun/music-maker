from music21 import note, duration, key, meter, stream
import noise_util


class Measure:
    notes: list[note.Note]
    durations: list[duration.Duration]

    def __init__(self) -> None:
        noise_util.gen_normal()


class Movement:
    chordProgression: list[int]
    measures: list[Measure]

    def __init__(self, numMeasures) -> None:
        for i in range(numMeasures):
            newMeasure = Measure()
            self.measures.append(newMeasure)


class Composition:
    k: key.Key = key.Key('C')
    ts: meter.TimeSignature = meter.TimeSignature('4/4')
    tempo: int = 120
    numMeasures: int = 15
    movements: list[Movement]

    def __init__(self) -> None:
        firstMovement = Movement()
        secondMovement = Movement()
        self.movements = [firstMovement, secondMovement, firstMovement]

    def compose(self) -> None:
        s = stream.Stream()
        for movement in self.movements:
            s.append(movement)
        s.show()
