import random
from music21 import key, meter, stream
import chordmap, melody, util
def main():
    # Current metamodel info
    keySignature = key.KeySignature(random.randint(-6, 6))
    timeSignature = meter.TimeSignature('4/4')
    numMeasures = 12
    
    # Generating chords
    chordMap = chordmap.ChordMap(keySignature, timeSignature)
    progression = chordMap.generateRepeatableProgression()
    generatedChords = chordMap.generateChords(progression, numMeasures)

    # Generating melody
    mg = melody.MelodyGraph(numMeasures, keySignature, timeSignature)
    midiValues, durationValues = mg.generateMidiValuesFromMarkovModel()
    generatedMelody = mg.generateNotesFromMidi(midiValues, durationValues, numMeasures)

    # Alternative melody
    principalMidis = []
    interpolationRate = 4
    for i in range(numMeasures*timeSignature.numerator // interpolationRate):
        note = util.noteInKeyFromMidiValue(random.randint(67, 77), keySignature)
        principalMidis.append(note.pitch.midi)

    interpolatedMidis, durationValues = mg.interpolateMelody(principalMidis, interpolationRate)
    interpolatedMelody = mg.generateNotesFromMidi(interpolatedMidis, durationValues, numMeasures)


    # Putting together parts and storing generated midi file
    s = stream.Score([interpolatedMelody, generatedChords])
    # s = stream.Score([generatedMelody, generatedChords])
    s.write('midi', '../composition.mid')
    s.show()


if __name__ == '__main__':
    main()
