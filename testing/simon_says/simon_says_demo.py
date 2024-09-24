# YELLOW LED:    GPIO 17
# YELLOW BUTTON: GPIO 18
# RED LED:       GPIO 27
# RED BUTTON:    GPIO 15
# GREEN LED:     GPIO 22
# GREEN BUTTON:  GPIO 14

import RPi.GPIO as GPIO
from time import sleep
import random

def light_up_led(pin, sleep_time):
   GPIO.output(pin, GPIO.HIGH) 
   sleep(sleep_time)
   GPIO.output(pin, GPIO.LOW)

def light_up_led_as_long_as_pressed(led, button):
        GPIO.output(led, GPIO.HIGH) 
        while GPIO.input(button) == GPIO.LOW:
            sleep(0.01)
        GPIO.output(led, GPIO.LOW) 

def main():
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
    # Initialize pins
    GPIO.setup(yellow_led, GPIO.OUT)
    GPIO.setup(red_led, GPIO.OUT)
    GPIO.setup(green_led, GPIO.OUT)
    GPIO.setup(yellow_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(red_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(green_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Make sure all LEDs are off
    GPIO.output(yellow_led, GPIO.LOW)
    GPIO.output(red_led, GPIO.LOW)
    GPIO.output(green_led, GPIO.LOW)

    # Initialize game parameters
    game_is_playing = True
    num_round = 0
    user_input = False
    led_sequence = []

    print("BEGIN GAME")

    while game_is_playing:
        num_round = num_round + 1
        print("ROUND ", num_round)
        random_led = random.choice(list(pin_dict.keys()))
        led_sequence.append(random_led)

        # Light up LED sequence
        print("Showing LED sequence")
        for led in led_sequence:
            sleep(0.5)
            light_up_led(led, 0.5)
        # Get user input
        print("Reapeat LED sequence")
        i = 0
        while True:
            user_input = False
            while not user_input:
                if GPIO.input(yellow_button) == GPIO.LOW:
                    light_up_led_as_long_as_pressed(yellow_button, yellow_button)
                    user_input = True
                    pressed_button = yellow_button
                elif GPIO.input(green_button) == GPIO.LOW:
                    light_up_led_as_long_as_pressed(green_led, green_button)
                    user_input = True
                    pressed_button = green_button
                elif GPIO.input(red_button) == GPIO.LOW:
                    light_up_led_as_long_as_pressed(red_led, red_button)
                    user_input = True
                    pressed_button = red_button
        
            if (pin_dict[led_sequence[i]] != pressed_button):
                game_is_playing = False

            i = i + 1
            if i == len(led_sequence):
                break
            else:
                sleep(0.5)
    
        sleep(0.5)
        if game_is_playing:
            print("CORRECT")
            for i in range(0,3):
                GPIO.output(yellow_led, GPIO.HIGH)
                GPIO.output(red_led, GPIO.HIGH)
                GPIO.output(green_led, GPIO.HIGH)
                sleep(0.1)     
                GPIO.output(yellow_led, GPIO.LOW)
                GPIO.output(red_led, GPIO.LOW)
                GPIO.output(green_led, GPIO.LOW)
                sleep(0.1)
        else:
            print("INCORRECT SEQUENCE. GAME OVER!")
            for i in range (0,5):
                light_up_led(red_led, 0.05)
                sleep(0.05)
    
    GPIO.cleanup()

if __name__ == "__main__":
   try:
       main()
   except KeyboardInterrupt:
       GPIO.cleanup()
