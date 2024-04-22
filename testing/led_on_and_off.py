# Connect LED and resistor to GPIO 17 (BCM)
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

led_pin = 17

GPIO.setup(led_pin, GPIO.OUT)


GPIO.output(led_pin, GPIO.HIGH)
print("LED ON")
sleep(1)

GPIO.output(led_pin, GPIO.LOW)
print("LED OFF")
sleep(1)

GPIO.cleanup()
