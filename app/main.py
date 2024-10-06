PRODUCE_CLICK_TRACK_AS_WELL = False
INFILE = 'volume/mardy.wav'
OUTFILE = 'volume/mardy_swang.wav'

print("Welcome to SWING MACHINE")

import librosa
import soundfile as sf

print("Loading file...")
y, sr = librosa.load(INFILE, sr=None)
print("Detecting beats...")
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='samples')

if PRODUCE_CLICK_TRACK_AS_WELL:
    print("Producing click track...")
    click = librosa.clicks(frames=beats, sr=sr, length=len(y))
    y_click = y + click
    sf.write(OUTFILE.replace(".wav", "_click.wav"), y_click, sr)


print("Swinging....")
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
sf.write(OUTFILE, y_new, sr)