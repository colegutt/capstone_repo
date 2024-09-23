#!/usr/bin/env python3

import subprocess
import sys
import os

# Ranges from 0 to 153
VOLUME_PERCENTAGE = 100

def set_volume(volume_percentage):
    if not (0 <= volume_percentage <= 153):
        raise ValueError("Volume percentage must be between 0 and 153.")

    try:
        # Set the volume for the default sink
        subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', f'{volume_percentage}%'], check=True)
        print(f"System volume set to {volume_percentage}%")
    except subprocess.CalledProcessError as e:
        print(f"Error setting system volume: {e}", file=sys.stderr)

def play_audio(file_path):
    """
    Play an audio file using mpg123.
    """
    if not os.path.isfile(file_path):
        print(f"Error: File {file_path} does not exist.", file=sys.stderr)
        return

    try:
        # Play the audio file
        subprocess.run(['mpg123', file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error playing audio file: {e}", file=sys.stderr)

if __name__ == "__main__":
    try:
        volume_percentage = VOLUME_PERCENTAGE
        audio_file = 'sample_sound.mp3'
    except ValueError:
        print("Volume percentage must be an integer.", file=sys.stderr)
        sys.exit(1)

    set_volume(volume_percentage)
    play_audio(audio_file)
