# Button Test

# make sure library is installed (outside this file)
# sudo apt-get update
# sudo apt-get install python3-rpi.gpio

import RPi.GPIO as GPIO
from time import sleep

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)

# Defines the GPIO pins for each button (need to add gpio numbers on campus)
red_button = 25
orange_button = 24
yellow_button = 23
green_button = 4
blue_button = 27
purple_button = 22

# Set up the buttons as inputs with pull-up resistors
GPIO.setup(red_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(orange_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(yellow_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(green_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(blue_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(purple_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def wait_for_button_release(button):
    while GPIO.input(button) == GPIO.LOW:
        sleep(0.1)
    return

try:
    print("Waiting for button press...")
    while True:
        if GPIO.input(red_button) == GPIO.LOW:
            print("Red")
            wait_for_button_release(red_button)
        elif GPIO.input(orange_button) == GPIO.LOW:
            print("orange")
            wait_for_button_release(orange_button)
        elif GPIO.input(yellow_button) == GPIO.LOW: 
            print("yellow")
            wait_for_button_release(yellow_button)
        elif GPIO.input(green_button) == GPIO.LOW: 
            print("green")
            wait_for_button_release(green_button)
        elif GPIO.input(blue_button) == GPIO.LOW:
            print("blue")
            wait_for_button_release(blue_button)
        elif GPIO.input(purple_button) == GPIO.LOW: 
            print("purple")
            wait_for_button_release(purple_button)
        
        sleep(0.15)
    
except KeyboardInterrupt:
    print("Program stopped by User.")
finally:
    GPIO.cleanup()  # Clean up GPIO on exit
