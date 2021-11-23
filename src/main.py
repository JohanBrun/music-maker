from copy import copy
import random
from music21 import key, meter, stream
import chordmap, melody, clave

def main():
    # Current metamodel info
    keySignature = key.KeySignature(random.randint(-6, 6))
    timeSignature = meter.TimeSignature('4/4')
    numMeasures = 8
    
    # Generating chords
    chordMap = chordmap.ChordMap(keySignature, timeSignature)
    progression = chordMap.generateRepeatableProgression()
    generatedChords = chordMap.generateChords(progression, numMeasures)

    # Generating melody
    mg = melody.MelodyGraph(numMeasures // 4, keySignature, timeSignature)
    midiValues, durationValues = mg.repeatableMarkovMelody()
    generatedMelody = mg.generateNotesFromMidi(midiValues, durationValues, numMeasures)

    # Generating clave
    # cg = clave.ClaveGenerator()
    # generatedClave = cg.generate23Clave(numMeasures)

    # Putting together parts and storing generated midi file
    s = stream.Score([generatedMelody, generatedChords])
    s.write('midi', '../composition.mid')
    s.show()
    


if __name__ == '__main__':
    main()
