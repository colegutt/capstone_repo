# YELLOW LED:    GPIO 17
# YELLOW BUTTON: GPIO 18
# RED LED:       GPIO 27
# RED BUTTON:    GPIO 15
# GREEN LED:     GPIO 22
# GREEN BUTTON:  GPIO 14

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

yellow_led = 17
red_led = 27
green_led = 22
yellow_button = 18
red_button = 15
green_button = 14

pin_dict = {
    yellow_led: yellow_button,
    red_led: red_button,
    green_led: green_button
}

GPIO.setup(yellow_led, GPIO.OUT)
GPIO.setup(red_led, GPIO.OUT)
GPIO.setup(green_led, GPIO.OUT)
GPIO.setup(yellow_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(red_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(green_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        y_button_state = GPIO.input(yellow_button)
        r_button_state = GPIO.input(red_button)
        g_button_state = GPIO.input(green_button)

        if y_button_state == GPIO.LOW:
            GPIO.output(yellow_led, GPIO.HIGH)
        else:
            GPIO.output(yellow_led, GPIO.LOW)

        if r_button_state == GPIO.LOW:
            GPIO.output(red_led, GPIO.HIGH)
        else:
            GPIO.output(red_led, GPIO.LOW)

        if g_button_state == GPIO.LOW:
            GPIO.output(green_led, GPIO.HIGH)
        else:
            GPIO.output(green_led, GPIO.LOW)

        sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()


