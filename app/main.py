print("Welcome to SWING MACHINE")

import librosa
import soundfile as sf

print("Loading file...")
y, sr = librosa.load('/volume/samelove.wav', sr=None)
print("Detecting beats...")
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='samples')

y_new = []
for i in range(len(beats)-1):
    first_half = y[beats[i]:int((beats[i]+beats[i+1])/2)]
    second_half = y[int((beats[i]+beats[i+1])/2):beats[i+1]]
    first_half = librosa.effects.time_stretch(first_half, rate=(2/3))
    second_half = librosa.effects.time_stretch(second_half, rate=(4/3))


    y_new.extend(first_half)
    y_new.extend(second_half)

print("Saving file...")
# Save the new audio file
sf.write('/volume/sameswing.wav', y_new, sr)