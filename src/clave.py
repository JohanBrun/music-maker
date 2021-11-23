from music21 import stream, note, instrument

class ClaveGenerator:
    def __init__(self) -> None:
        pass

    def generate23Clave(self, numMeasures: int):
        s = stream.Stream()
        s.insert(instrument.Woodblock())
        # mm = tempo.MetronomeMark(number=240)
        # s.append(mm)

        for i in range(numMeasures):
            quarterClave1 = note.Note(77, quarterLength=0.5)
            quarterClave2 = note.Note(77, quarterLength=0.5)
            quarterClave3 = note.Note(77, quarterLength=0.5)
            quarterClave4 = note.Note(77, quarterLength=0.5)
            eighthClave = note.Note(77, quarterLength=0.25)

            quarterRest1 = note.Rest(quarterLength=0.5)
            quarterRest2 = note.Rest(quarterLength=0.5)
            quarterRest3 = note.Rest(quarterLength=0.5)
            eighthRest = note.Rest(quarterLength=0.25)

            s.append(quarterClave1)
            s.append(eighthRest)
            s.append(eighthClave)
            s.append(quarterRest1)
            s.append(quarterClave2)
            s.append(quarterRest2)
            s.append(quarterClave3)
            s.append(quarterClave4)
            s.append(quarterRest3)

        return s
