import subprocess
import os
import sys

AUDIO_FILE = 'sample_sound.mp3'
VOLUME_PERCENTAGE = 10
USB_SPEAKER_SINK = 'alsa_output.usb-Solid_State_System_Co._Ltd._USB_PnP_Audio_Device_000000000000-00.analog-stereo'

def set_volume(volume_percentage, sink_name):
    try:
        subprocess.run(['pactl', 'set-sink-volume', sink_name, f'{volume_percentage}%'], check=True)
        print(f"Volume set to {volume_percentage}% for sink {sink_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error setting volume: {e}", file=sys.stderr)

def play_audio(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: File {file_path} does not exist.", file=sys.stderr)
        return
    try:
        # Play the audio file
        subprocess.run(['mpg123', file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error playing audio file: {e}", file=sys.stderr)

if __name__ == "__main__":
    # Check if the audio file exists
    if not os.path.exists(AUDIO_FILE):
        print(f"Error: {AUDIO_FILE} does not exist.", file=sys.stderr)
        sys.exit(1)

    try:
        # Prompt the user for a volume level
        set_volume(VOLUME_PERCENTAGE, USB_SPEAKER_SINK)

        # Play the audio file
        play_audio(AUDIO_FILE)

    except ValueError:
        print("Invalid input. Please enter a number between 0 and 153.", file=sys.stderr)
        sys.exit(1)
