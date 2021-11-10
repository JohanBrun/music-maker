from copy import copy
import random, copy
from music21 import key, meter, stream
import chordmap, melody

def main():
    # Current metamodel info
    keySignature = key.KeySignature(random.randint(-6, 6))
    timeSignature = meter.TimeSignature('4/4')
    
    # Generating chords
    chordMap = chordmap.ChordMap(keySignature, timeSignature)
    progression = chordMap.generateRepeatableProgression()
    progression += progression
    progression += progression
    generatedChords = chordMap.generateChords(progression)
    numMeasures = len(generatedChords.getElementsByClass(stream.Measure))

    # generating melody
    mg = melody.MelodyGraph(numMeasures // 4, keySignature, timeSignature)
    # generatedMelody = mg.markovMelody()
    midiValues, durationValues = mg.repeatableMarkovMelody()
    midiValues += midiValues
    midiValues += midiValues
    durationValues += durationValues
    durationValues += durationValues
    generatedMelody = mg.generateNotes(midiValues, durationValues)
    #    generatedMelody.show()

    # Putting together parts and storing generated midi file
    s = stream.Score([generatedMelody, generatedChords])
    s.write('midi', '../composition.midi')
    s.show()
    


if __name__ == '__main__':
    main()
