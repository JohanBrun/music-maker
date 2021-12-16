import random
from music21 import key, meter, stream, note
import util
from melody import MelodyGraph
from chord_progression import ChordGraph
def main():
    # Initializing key parameters
    seed  = 12345
    random.seed(seed)
    keySignature = key.KeySignature(random.randint(-5, 5))
    timeSignature = meter.TimeSignature('4/4')
    numMeasures = 12
    interpolationRate = 4
    
    # Generating chords
    random.seed(seed)
    cg = ChordGraph(keySignature, timeSignature)
    progression = cg.generateFourChordProgression()
    generatedChords = cg.generateChords(progression, numMeasures)

    # Generating melody
    mg = MelodyGraph(keySignature, timeSignature)
    random.seed(seed)
    midiValues, durationValues = mg.generateMidiValuesFromMarkovModel(numMeasures)
    random.seed(seed)
    markovMidiValues, _ = mg.generateMidiValuesFromMarkovModel(numMeasures, True)
    random.seed(seed)
    uniformMidiValues = mg.generateMidiValuesFromUniform(numMeasures, interpolationRate)
    random.seed(seed)
    normalMidiValues = mg.generateMidiValuesFromNormal(numMeasures, interpolationRate)

    random.seed(seed)
    interpolateFromUniform, durationValuesUniform = mg.interpolateMelody(uniformMidiValues)
    random.seed(seed)
    interpolateFromNormal, durationValuesNormal = mg.interpolateMelody(normalMidiValues)
    random.seed(seed)
    interpolateFromMarkov, durationValuesMarkov = mg.interpolateMelody(markovMidiValues)


    generatedMelody = mg.generateNotesFromMidi(midiValues, durationValues, numMeasures)
    interpolatedUniformMelody = mg.generateNotesFromMidi(interpolateFromUniform, durationValuesUniform, numMeasures)
    interpolatedNormalMelody = mg.generateNotesFromMidi(interpolateFromNormal, durationValuesNormal, numMeasures)
    interpolatedMarkovMelody = mg.generateNotesFromMidi(interpolateFromMarkov, durationValuesMarkov, numMeasures)

    # Putting together parts and storing generated midi file
    s = stream.Score([generatedMelody, generatedChords])
    s1 = stream.Score([interpolatedUniformMelody, generatedChords])
    s2 = stream.Score([interpolatedNormalMelody, generatedChords])
    s3 = stream.Score([interpolatedMarkovMelody, generatedChords])
    s.write('midi', '../composition.mid')
    s.show()
    s1.show()
    s2.show()
    s3.show()


if __name__ == '__main__':
    main()
