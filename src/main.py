import random
from music21 import key, meter, stream
import chordmap, melody

def main():
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
    mg = melody.MelodyGraph(numMeasures, keySignature, timeSignature)
    generatedMelody = mg.markovMelody()


    s = stream.Score([generatedMelody, generatedChords])
    s.write('midi', '../composition.midi')
    s.show()
    


if __name__ == '__main__':
    main()
