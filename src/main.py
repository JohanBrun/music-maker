from music21 import *
from music21.key import KeySignature
import numpy as np
from numpy.random import default_rng

rng = default_rng()

def gen_binomial(p: float):
    noise = rng.binomial(127, p, 100)
    return noise

def gen_normal(p: float):
    noise = rng.normal(1, p, 100)
    noise = noise * 60
    noise = np.rint(noise)
    return noise

def note_from_noise(p: int, ks: KeySignature):
    n = note.Note(pitch.Pitch(p))
    nStep = n.pitch.step
    rightAccidental = ks.accidentalByStep(nStep)
    n.pitch.accidental = rightAccidental
    return n

def main():
    noise1 = gen_normal(0.1)
    # noise1 = gen_binomial(0.5)
    noise2 = noise1 + 4
    noise3 = noise2 + 4
    durations = rng.binomial(4, 0.5, 100)
    durations = durations / 2
    stream1 = stream.Stream()
    ks = key.KeySignature(rng.integers(-6, 6))
    stream1.keySignature = ks
    print(ks)

    for p1, p2, p3, d in zip(noise1, noise2, noise3, durations):
        n1 = note_from_noise(p1, ks)
        n2 = note_from_noise(p2, ks)
        n3 = note_from_noise(p3, ks)
        c = chord.Chord([n1, n2, n3])
        # if (d == 0):
            # d = 1
        c.duration = duration.Duration(round(d, 1))
        stream1.append(c)

    stream1.show()

main()
