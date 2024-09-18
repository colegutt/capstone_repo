# Button Test

# make sure library is installed (outside this file)
# sudo apt-get update
# sudo apt-get install python3-rpi.gpio

import RPi.GPIO as GPIO
import time

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)

# Defines the GPIO pins for each button (need to add gpio numbers on campus)
RED_BUTTON = 25
ORA_BUTTON = 24
YEL_BUTTON = 23
GRE_BUTTON = 4
BLU_BUTTON = 27
PUR_BUTTON = 22

# Set up the buttons as inputs with pull-up resistors
GPIO.setup(RED_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ORA_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(YEL_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(GRE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BLU_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PUR_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    print("Waiting for button press...")
    while True:
        # Check each button
        if GPIO.input(RED_BUTTON) == GPIO.LOW:
            print("Red button pressed!")
        
        if GPIO.input(ORA_BUTTON) == GPIO.LOW:
            print("Orange button pressed!")
        
        if GPIO.input(YEL_BUTTON) == GPIO.LOW:
            print("Yellow button pressed!")
        
        if GPIO.input(GRE_BUTTON) == GPIO.LOW:
            print("Green button pressed!")
        
        if GPIO.input(BLU_BUTTON) == GPIO.LOW:
            print("Blue button pressed!")
        
        if GPIO.input(PUR_BUTTON) == GPIO.LOW:
            print("Purple button pressed!")
        
        time.sleep(0.25)  # Small delay to avoid CPU overload
    
except KeyboardInterrupt:
    print("Program stopped by User.")
finally:
    GPIO.cleanup()  # Clean up GPIO on exit
