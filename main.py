# from BeatNet.BeatNet import BeatNet
from echonest.remix import audio

audio_file = audio.LocalAudioFile("samelove.m4a")

beats = audio_file.analysis.beats
beats.reverse()

# And render the list as a new audio file!
audio.getpieces(audio_file, beats).encode("goofy.mp3")

print('hoi dockertje de pockertje!')