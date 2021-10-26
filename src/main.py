import random
from music21 import key, meter, stream
import compose, chordmap, melody

def main():
    keySignature = key.KeySignature(random.randint(-6, 6))
    timeSignature = meter.TimeSignature('4/4')
    
    chordMap = chordmap.ChordMap(keySignature, timeSignature)
    progression = chordMap.generateRepeatableProgression()
    progression += progression
    progression += progression
    chords = chordMap.generateChords(progression)
    numMeasures = len(chords.getElementsByClass(stream.Measure))

    compose.Measure.ks = keySignature
    composition = compose.Composition(numMeasures, keySignature, timeSignature)

    mg = melody.MelodyGraph(numMeasures, keySignature, timeSignature)
    
    s = stream.Score()
    s.keySignature = keySignature
    s.timeSignature = timeSignature


    # s.append(composition.compose())
    s.append(mg.walkTest())
    s.append(chords)
    s.write('midi', '../composition.midi')
    s.show()
    


if __name__ == '__main__':
    main()
