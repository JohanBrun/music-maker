import numpy as np
from numpy.random import default_rng
from music21 import key, note, pitch

rng = default_rng()


def gen_normal(mu: float, sigma: float, length: int) -> np.array:
    '''
    mu:     defines the average value for the noise
    sigma:  defines variance in noise
    length: defines amount of descrete noise values should be generated
    '''
    inMidiRange = mu >= 0 and mu <= 127 and length > 0
    if (inMidiRange):
        noise = rng.normal(mu, sigma, length)
        noise = np.rint(noise)
        return noise
    else:
        print('Mu not in range!')
        return np.array([])


def noteInKeyFromMidiValue(midiValue: int, ks: key.KeySignature):
    n = note.Note(midiValue)
    nStep = n.pitch.step
    rightAccidental = ks.accidentalByStep(nStep)
    n.pitch.accidental = rightAccidental
    return n
