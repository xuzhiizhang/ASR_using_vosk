#!/usr/bin/env python3
# This script uses Vosk-API for speech-to-text recognition and sounddevice to capture audio from a microphone.
# It records audio from the default or specified microphone device, processes it in real-time,
# and writes the recognized text to a file.

# Prerequisites:
# 1. 3.5 <= Python <=3.9: Install Python if it is not already installed.
# 2. sounddevice module: Install using `pip install sounddevice`.
#    This module is used to capture audio from a microphone.
# 3. vosk module: Install using `pip install vosk`.
#    This module is used for speech recognition.

# Usage:
# - To run the script, specify the language model using the -m flag. Example: `python script_name.py -m en-us`
# - To list available audio devices, use the -l or --list-devices flag.
# - To specify a particular audio device for recording, use the -d or --device flag with the device ID or name.
# - You can also specify the audio file to store recordings using the -f or --filename flag.
# - The script prints real-time partial recognition results to the console and writes full results to a specified file.

# Example command to run: `python script_name.py -m en-us`
# It's important to adjust the microphone settings and ensure your environment is quiet enough for accurate recognition.

import argparse
import queue
import sys
import sounddevice as sd
from vosk import Model, KaldiRecognizer

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="show list of audio devices and exit")
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    "-f", "--filename", type=str, metavar="FILENAME",
    help="audio file to store recording to", default='./recognized_text.txt')
parser.add_argument(
    "-d", "--device", type=int_or_str,
    help="input device (numeric ID or substring)")
parser.add_argument(
    "-r", "--samplerate", type=int, help="sampling rate")
parser.add_argument(
    "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
args = parser.parse_args(remaining)

results_list = []  # Initialize a list to store the recognition results

try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        args.samplerate = int(device_info["default_samplerate"])

    model = Model(lang=args.model if args.model else "en-us")

    with sd.RawInputStream(samplerate=args.samplerate, blocksize=8000, device=args.device,
                           dtype="int16", channels=1, callback=callback):
        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("#" * 80)

        rec = KaldiRecognizer(model, args.samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = rec.Result()  # Get the recognition result as a string
                results_list.append(result)  # Append the result to the list
            else:
                partial_result = rec.PartialResult()  # For real-time feedback
                print(partial_result)

except KeyboardInterrupt:
    print("\nDone")
    print("Writing results to file...")
    with open(args.filename, "w") as file:
        for result in results_list:
            file.write(result + '\n')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))
