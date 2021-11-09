from music21 import pitch, stream, note, instrument, duration, midi, tempo

class ClaveGenerator:
    def generate23Clave(self):
        s = stream.Stream()
        s.insert(instrument.Woodblock())
        mm = tempo.MetronomeMark(number=240)
        # s.append(mm)


        quarterClave1 = note.Note(77, quarterLength=1)
        quarterClave2 = note.Note(77, quarterLength=1)
        quarterClave3 = note.Note(77, quarterLength=1)
        quarterClave4 = note.Note(77, quarterLength=1)
        eighthClave = note.Note(77, quarterLength=0.5)

        quarterRest1 = note.Rest(quarterLength=1)
        quarterRest2 = note.Rest(quarterLength=1)
        quarterRest3 = note.Rest(quarterLength=1)
        eighthRest = note.Rest(quarterLength=0.5)

        m = stream.Measure()
        m.append(mm)

        m.append(quarterClave1)
        m.append(eighthRest)
        m.append(eighthClave)
        m.append(quarterRest1)
        m.append(quarterClave2)
        m.append(quarterRest2)
        m.append(quarterClave3)
        m.append(quarterClave4)
        m.append(quarterRest3)

        s.append(m)

        s.show()

cg = ClaveGenerator()
cg.generate23Clave()
