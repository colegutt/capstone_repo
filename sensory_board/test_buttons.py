# YELLOW LED:    GPIO 17
# YELLOW BUTTON: GPIO 18
# RED LED:       GPIO 27
# RED BUTTON:    GPIO 15
# GREEN LED:     GPIO 22
# GREEN BUTTON:  GPIO 14

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

balk_button = 26


GPIO.setup(balk_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        button_state = GPIO.input(balk_button)

        if button_state == GPIO.LOW:
            print('button pressed')
        else:
            print('NONE')

        sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()


