import pygame
import time

# Initialize the mixer module
pygame.mixer.init()

# Load and play the MP3 file
pygame.mixer.music.load("sample_sound.mp3")
pygame.mixer.music.set_volume(1.0)  # Set the volume to maximum

# Play the sound
pygame.mixer.music.play()

# Keep the script running until the sound finishes playing
while pygame.mixer.music.get_busy():
    time.sleep(1)
import pygame
import time

# Initialize the mixer module
pygame.mixer.init()

# Load and play the MP3 file
pygame.mixer.music.load("sample_sound.mp3")
pygame.mixer.music.set_volume(1.0)  # Set the volume to maximum

# Play the sound
pygame.mixer.music.play()
print('playing sound')

# Keep the script running until the sound finishes playing
while pygame.mixer.music.get_busy():
    time.sleep(1)
