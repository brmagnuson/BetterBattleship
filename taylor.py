import pysynth
import play_wav
import os

def singIt(song):
    pysynth.make_wav(song, fn = 'test.wav')
    play_wav.Sound().playFile('test.wav')

def makeRecord(song, name):
    pysynth.make_wav(song, fn = name + '.wav')

def sayIt(phrase, voice=''):
    if voice != '':
        voice = '-v "%s"' % (voice)
    os.system('say %s "%s"' % (voice, phrase))
    # play_wav.Sound().playFile('test.wav')


#
# # Miss
# missSong = [('c', 16), ('g3', 16)]
# singIt(missSong)
# makeRecord(missSong, 'miss')
#
# # Sunk ship
# sunkSong = [('g', 4), ('e', 4), ('b3', 2)]
# singIt(sunkSong)
# makeRecord(sunkSong, 'sunk')
#
# # Hit
# hitSong = [('a3', 8), ('a3', 8), ('c', 4)]
# singIt(hitSong)
# makeRecord(hitSong, 'hit')
#
# # Victory
# triple = [('g', 32), ('e', 32), ('c', 32)]
# finish = [('c5', 1)]
# victorySong = (triple * 3) + finish
# victorySong = victorySong * 2
# singIt(victorySong)
# makeRecord(victorySong, 'victory')
#
# # Loss
# lossSong = [('c5', 16), ('b', 16), ('a', 16), ('g', 16), ('f', 16), ('e', 16), ('d', 16), ('c', 8)]
# singIt(lossSong)
# makeRecord(lossSong, 'loss')
