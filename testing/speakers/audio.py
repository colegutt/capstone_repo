import RPi.GPIO as GPIO
import pygame
import time

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)

# Function to play the uploaded audio file
def play_audio(file_path):
    # Initialize pygame mixer for sound
    pygame.mixer.init()

    # Load the audio file
    pygame.mixer.music.load(file_path)

    # Start playing the audio file
    pygame.mixer.music.play()

    # Wait for the music to finish playing
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

# Main program
try:
    # Turn on the speaker (GPIO HIGH)
    GPIO.output(2, GPIO.HIGH)
    print("Speaker ON")

    # Play the uploaded audio file
    audio_file = "/mnt/data/zapsplat_animals_dinosaur_call_young_for_mother_forest_reverb_109819.mp3"
    play_audio(audio_file)

    # Turn off the speaker (GPIO LOW) after playing
    GPIO.output(2, GPIO.LOW)
    print("Speaker OFF")

finally:
    # Clean up GPIO settings
    GPIO.cleanup()