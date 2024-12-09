# YELLOW LED:    GPIO 
# YELLOW BUTTON: GPIO 18
# RED LED:       GPIO 
# RED BUTTON:    GPIO 15
# GREEN LED:     GPIO 
# GREEN BUTTON:  GPIO 14

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

test_button = 6

GPIO.setup(test_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        button_state = GPIO.input(test_button)

        if button_state == GPIO.LOW:
            print('button pressed')
        else:
            print('NONE')

        sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()


