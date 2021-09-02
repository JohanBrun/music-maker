from music21 import *

class Composition:
    k: key.Key = key.Key('C')
    ts: meter.TimeSignature = meter.TimeSignature('4/4')
    tempo: int = 120
    num_measures: int = 15

class Movement:
    chordProgression: list[int]

class Measure:
    notes: list[note.Note]
    durations: list[duration.Duration]