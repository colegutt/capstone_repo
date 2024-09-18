import pygame
import time

# Initialize pygame mixer
pygame.mixer.init()

# Load the audio file
pygame.mixer.music.load("sample_sound.mp3")

# Play the audio file
pygame.mixer.music.play()

# Keep the script running while the audio play
while pygame.mixer.music.get_busy():
    time.sleep(1)  # Wait for 1 second and check again