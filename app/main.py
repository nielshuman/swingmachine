# SWING MACHINE
# Niels Huisman, 2024

import argparse
import librosa
import soundfile as sf
import sys, os
import pydub
from gooey import Gooey, GooeyParser
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from multiprocessing import Process

if len(sys.argv)>=2:
    if not '--ignore-gooey' in sys.argv:
        sys.argv.append('--ignore-gooey')

class Stagelog:
    def __init__(self, total_stages):
        self.total_stages = total_stages
        self.current_stage = 0
    def next(self, text=None):
        self.current_stage += 1
        print(f"[{self.current_stage}/{self.total_stages}]")
        if text:
            print(text)

@Gooey(
    program_name="SWING MACHINE",
    program_description="Niels Huisman, 2024", 
    image_dir="icons",
    default_size=(800, 700),
    progress_regex=r"^\[(?P<current>\d+)/(?P<total>\d+)\]$",
    progress_expr="current / total * 100",
    hide_progress_msg=True,
    show_failure_modal=False,
)
def main():
    save_wildcard = "MP3 files (*.mp3)|*.mp3|WAV files (*.wav)|*.wav|Audio files (*.wav;*.mp3)|*.wav;*.mp3"
    open_wildcard = "Audio files (*.wav;*.mp3)|*.wav;*.mp3"
    parser = GooeyParser(prog="swing", description="SWING MACHINE.\nNiels Huisman, 2024")
    parser.add_argument('-i', '--input-file', metavar="Input", help='Input audio file.\nEither an MP3 file or a WAV file.', widget='FileChooser', required=True, gooey_options={"wildcard": open_wildcard})
    parser.add_argument('-o', '--output-file', metavar="Output (optional)", help='Output audio file.\nDefaults to <inputfile>_swing.mp3', widget='FileSaver', gooey_options={"wildcard": save_wildcard, "default_file": "swing.mp3"})
    parser.add_argument('--halftime', metavar="Halftime", help='Use halftime swing.', action='store_true')
    parser.add_argument('--dubbletime', metavar="Dubbletime", help='Use dubbletime swing.', action='store_true')
    parser.add_argument('--remove-first-beat', metavar="Remove first beat", help='Remove the first beat. Useful when using halftime and first beat is off.', action='store_true')
    debug = parser.add_argument_group('Debug zooi')
    debug.add_argument('--produce-click-track', metavar="Produce clicktrack", action='store_true', help='Produce a click track as well. Useful for debugging or checking why the result is weird.')
    args = parser.parse_args()

    INFILE = args.input_file
    OUTFILE = args.output_file
    PRODUCE_CLICKTRACK = args.produce_click_track
    if not OUTFILE:
        OUTFILE = INFILE.replace(".wav", "_swing.wav").replace(".mp3", "_swing.mp3") 
    ENCODE_MP3 = OUTFILE.endswith(".mp3")
    WAV_OUTFILE = OUTFILE.replace(".mp3", ".wav")
    if not INFILE.endswith(".wav") and not INFILE.endswith(".mp3"):
        raise SystemExit("Only wav and mp3 files are supported as input")
    if not OUTFILE.endswith(".wav") and not OUTFILE.endswith(".mp3"):
        raise SystemExit("Output must end in either .wav or .mp3")
    if OUTFILE == INFILE:
        raise SystemExit("Input and output file can't be the same")
    stagelog = Stagelog(total_stages=(4 + PRODUCE_CLICKTRACK + ENCODE_MP3))
        
    
    print("Welcome to SWING MACHINE")
    print("Loading file...")
    y, sr = librosa.load(INFILE, sr=None)
    GRAPH_RESOLUTION_FACTOR = 200
    y_graph = y[::GRAPH_RESOLUTION_FACTOR]
    sr_graph = sr//GRAPH_RESOLUTION_FACTOR
    # show timestamps on x-axis for every 30 seconds
    xticks = range(0, len(y_graph), sr_graph*30)
    xticklabels = [f"{i//sr_graph//60}:{(i//sr_graph)%60:02}" for i in xticks]
    fig, ax = plt.subplots()
    def update(frame):
        ax.clear()
        ax.set_xlim(-10*sr_graph, len(y_graph)+10*sr_graph)
        ax.set_ylim(-1, 1)
        plt.xticks(xticks, xticklabels)
        ax.plot(y_graph[:frame])
    anim = FuncAnimation(fig, update, frames=range(0, len(y_graph), sr_graph*2), repeat=False, interval=0)
    p = Process(target=plt.show)
    p.start()
    stagelog.next("Detecting beats...")
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='samples')
    plt.close()
    p.terminate()
    # preprocessing
    if args.remove_first_beat:
        beats = beats[1:]
    if args.halftime:
        beats = beats[::2]
    if args.dubbletime:
        # insert a beat between every beat
        new_beats = []
        for i in range(len(beats)-1):
            new_beats.append(beats[i])
            new_beats.append(int((beats[i]+beats[i+1])/2))
        new_beats.append(beats[-1])
        beats = new_beats
    
    if PRODUCE_CLICKTRACK:
        stagelog.next("Producing click track (preprocessed)...")
        clicks = librosa.samples_to_time(beats, sr=sr)
        click = librosa.clicks(times=clicks, sr=sr, length=len(y))
        y_click = y + click
        filename = INFILE.replace(".wav", "_click.wav").replace(".mp3", "_click.wav")
        sf.write(filename, y_click, sr)

    stagelog.next("Swinging...")
    y_new = swing(y, sr, beats)
    
    
    stagelog.next("Saving file...")
    sf.write(WAV_OUTFILE, y_new, sr)

    if ENCODE_MP3:
        stagelog.next()
        pydub.AudioSegment.from_wav(WAV_OUTFILE).export(OUTFILE, format="mp3")
        os.remove(WAV_OUTFILE)

    print("[4/4]")
    print("Done! Saved to:", OUTFILE)
def swing(y, sr, beats):
    y_new = []
    for i in range(len(beats)-1):
        first_half = y[beats[i]:int((beats[i]+beats[i+1])/2)]
        second_half = y[int((beats[i]+beats[i+1])/2):beats[i+1]]

        first_half = librosa.effects.time_stretch(first_half, rate=(2/3))
        second_half = librosa.effects.time_stretch(second_half, rate=(4/3))

        y_new.extend(first_half)
        y_new.extend(second_half)
    return y_new

def deswing(y, sr, beats):
    y_new = []
    for i in range(len(beats)-1):
        first_two_thirds = y[beats[i]:int((beats[i]+beats[i+1])/2)]
        last_third = y[int((beats[i]+beats[i+1])/2):beats[i+1]]

        first_two_thirds = librosa.effects.time_stretch(first_two_thirds, rate=(3/2))
        last_third = librosa.effects.time_stretch(last_third, rate=(3/4))

        y_new.extend(first_two_thirds)
        y_new.extend(last_third)
    return y_new

if __name__ == "__main__":
    main()