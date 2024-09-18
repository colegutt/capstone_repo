#!/usr/bin/env python3

import subprocess
import sys
import os

VOLUME_PERCENTAGE = 100
HDMI_DEVICE = 'Built-in Audio Digital Stereo (HDMI)' 

def set_volume(volume_percentage, device):
    """
    Set the system volume using amixer.
    volume_percentage should be between 0 and 100.
    """
    if not (0 <= volume_percentage <= 100):
        raise ValueError("Volume percentage must be between 0 and 100.")
    
    try:
        # Set the volume for the specified audio device
        subprocess.run(['amixer', '-D', device, 'sset', 'Master', f'{volume_percentage}%'], check=True)
        print(f"System volume set to {volume_percentage}% for device {device}")
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

    set_volume(volume_percentage, HDMI_DEVICE)
    play_audio(audio_file)
