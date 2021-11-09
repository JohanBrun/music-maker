from util import gen_normal, note_from_noise
from music21 import stream, key, chord, note
from numpy.random import default_rng
rng = default_rng()


def gen_noises():
    noise1 = gen_normal(0.1)
    # noise1 = gen_binomial(0.5)
    noise2 = noise1 + 4
    noise3 = noise2 + 4
    durations = rng.binomial(4, 0.5, 100)
    durations = durations / 2
    return noise1, noise2, noise3, durations


def gen_chords():
    stream1 = stream.Stream()
    noise1, noise2, noise3, durations = gen_noises()
    ks = key.KeySignature(rng.integers(-6, 6))
    stream1.keySignature = ks
    K = ks.asKey()

    for p1, p2, p3, d in zip(noise1, noise2, noise3, durations):
        n1 = note_from_noise(p1, ks)
        n2 = note_from_noise(p2, ks)
        n3 = note_from_noise(p3, ks)
        c = chord.Chord([n1, n2, n3])
        # c.duration = duration.Duration(round(d, 1))
        stream1.append(c)
        if (n1.pitch.name == K.tonic.name and stream1.__len__() > 50):
            break

    return stream1


def get_triad(k: key.Key, degree: int) -> list[note.Note]:
    return [
        note.Note(k.pitchFromDegree(degree)),
        note.Note(k.pitchFromDegree(degree + 2)),
        note.Note(k.pitchFromDegree(degree + 4))
    ]


def harmonize(noise):
    ks = key.KeySignature(rng.integers(-6, 6))
    k = ks.asKey()
    stream1 = stream.Stream()
    stream1.keySignature = ks
    for i in range(3, len(noise), 4):
        firstTriad = get_triad(k, 1)
        secondTriad = get_triad(k, 5)
        thirdTriad = get_triad(k, 6)
        fourthTriad = get_triad(k, 4)
        firstTriad.append(note_from_noise(noise[i - 3], ks))
        secondTriad.append(note_from_noise(noise[i - 2], ks))
        thirdTriad.append(note_from_noise(noise[i - 1], ks))
        fourthTriad.append(note_from_noise(noise[i], ks))
        stream1.append(chord.Chord(firstTriad, quarterLength=2))
        stream1.append(chord.Chord(secondTriad, quarterLength=2))
        stream1.append(chord.Chord(thirdTriad, quarterLength=2))
        stream1.append(chord.Chord(fourthTriad, quarterLength=2))
    return stream1

def walkTest(self):
    k = self.ks.asKey()
    s = stream.Part()
    s.keySignature = self.ks
    s.timeSignature = self.ts

    currentDegree = 1
    direction = 0
    ascendingWeights = [2, 3, 5, 10, 3, 10, 4, 1, 1]
    descendingWeights = [1, 1, 4, 10, 3, 10, 5, 3, 2]
    neutralWeights = [1, 1, 4, 10, 3, 10, 4, 1, 1]

    currentNote = note.Note(k.pitchFromDegree(currentDegree))
    
    for i in range(self.numMeasures):
        m = stream.Measure()
        rythmSum = 4
        while (rythmSum > 0):
            if (direction == -1):
                currentInterval, direction = self.getInterval(currentDegree, descendingWeights)
            elif (direction == 1):
                currentInterval, direction = self.getInterval(currentDegree, ascendingWeights)
            else:
                currentInterval, direction = self.getInterval(currentDegree, neutralWeights)
            d, rythmSum = self.getDuration(rythmSum)
            currentNote = note.Note(currentNote.pitch.midi + currentInterval)
            currentNote.duration = duration.Duration(d)
            currentDegree = k.getScaleDegreeFromPitch(currentNote.pitch, comparisonAttribute='pitchClass')
            m.append(currentNote)

            self.getIntervalFromWeightedGraph(currentDegree, currentInterval)

        s.append(m)
    
    return s