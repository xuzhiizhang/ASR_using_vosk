# Speech-to-Text Recognition with Vosk and Sounddevice

This script uses the Vosk-API for speech-to-text recognition and sounddevice to capture audio from a microphone. It records audio from the default or specified microphone device, processes it in real-time, and writes the recognized text to a file.

## Prerequisites
1. **Python (3.5 <= version <= 3.9):** Install Python if it is not already installed.
2. **sounddevice module:** Install using `pip install sounddevice`.
   - This module is used to capture audio from a microphone.
3. **vosk module:** Install using `pip install vosk`.
   - This module is used for speech recognition.

## Usage
- **Specifying the language model:** Use the `-m` flag to specify the language model. Example: `python test_microphone.py -m en-us`.
- **Listing audio devices:** Use the `-l` or `--list-devices` flag to list available audio devices.
- **Specifying an audio device:** Use the `-d` or `--device` flag with the device ID or name to choose a specific audio device for recording.
- **Specifying the output file:** Use the `-f` or `--filename` flag to specify the audio file where the recordings will be stored.
- **Output:** The script prints real-time partial recognition results to the console and writes full results to the specified file.

### Example Command
```bash
python test_microphone.py -m en-us
