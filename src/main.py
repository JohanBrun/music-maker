import random
from music21 import key, meter, stream
import compose, chordmap

def main():
    keySignature = key.KeySignature(random.randint(-6, 6))
    timeSignature = meter.TimeSignature('4/4')
    compose.Measure.ks = keySignature
    composition = compose.Composition()
    chordMap = chordmap.ChordMap(keySignature, timeSignature)
    
    s = stream.Score()
    s.keySignature = keySignature
    s.timeSignature = timeSignature
    s.append(composition.compose())
    s.append(chordMap.generateProgression())
    s.show()
    s.write('midi', '../composition.midi')
    


if __name__ == '__main__':
    main()
