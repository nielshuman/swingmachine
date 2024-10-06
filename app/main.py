# PRODUCE_CLICK_TRACK_AS_WELL = False
# INFILE = 'volume/mardy.wav'
# OUTFILE = 'volume/mardy_swang.wav'

import argparse
import librosa
import soundfile as sf
from gooey import Gooey, GooeyParser

@Gooey
def main():
    # parser = argparse.ArgumentParser(description="Swing Machine: Add swing to your audio files.")
    # parser.add_argument('--infile', type=str, required=True, help='Input audio file')
    # parser.add_argument('--outfile', type=str, required=True, help='Output audio file')
    # parser.add_argument('--produce-click-track', action='store_true', help='Produce a click track as well')
    # args = parser.parse_args()

    parser = GooeyParser(description="Swing Machine: Add swing to your audio files.")
    parser.add_argument('infile', help='Input audio file', widget='FileChooser')
    parser.add_argument('outfile', help='Output audio file', widget='FileSaver')
    parser.add_argument('--produce-click-track', action='store_true', help='Produce a click track as well')
    parser.add_argument('--click-track-file', help='Click track file')
    args = parser.parse_args()

    PRODUCE_CLICK_TRACK_AS_WELL = args.produce_click_track
    INFILE = args.infile
    OUTFILE = args.outfile
    
    print("Welcome to SWING MACHINE")

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

if __name__ == "__main__":
    main()