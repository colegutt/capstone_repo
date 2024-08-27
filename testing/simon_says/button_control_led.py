# LED: GPIO 17
# BUTTON: GPIO 18

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

led_pin = 17
button_pin = 18

GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        button_state = GPIO.input(button_pin)

        if button_state == GPIO.LOW:
            GPIO.output(led_pin, GPIO.HIGH)
        else:
            GPIO.output(led_pin, GPIO.LOW)

        sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()


