import RPi.GPIO as GPIO
from time import sleep, time
import random
import threading
from general_functions import GeneralFunctions

class FastTapGame:
    def __init__(self):
        self.pause_event = threading.Event()  # Event to handle pausing
        self.gen_funcs = GeneralFunctions()
        self.end_game = False
        self.time_remaining = 5  # 30 seconds for the game duration
        self.start_time = None

    def stop(self):
        self.end_game = True
        self.pause_event.set()  # Ensure the game is stopped

    def light_up_led(self, pin):
        GPIO.output(pin, GPIO.HIGH)

    def turn_off_leds(self, leds):
        for led in leds:
            GPIO.output(led, GPIO.LOW)

    def run_game(self, update_score_callback, update_timer_callback, on_game_over_callback):
        pin_dict, buttons, leds = self.gen_funcs.set_up_gpio_and_get_pin_dict()

        self.turn_off_leds(leds)

        score = 0
        self.start_time = time()

        while not self.end_game and self.time_remaining > 0:
            # Light up a random LED
            current_led = random.choice(leds)
            self.light_up_led(current_led)
            user_input = False
            while not user_input:
                # Wait for user to press the corresponding button
                if self.wait_to_resume() == 1:  # If the resume condition is met, exit
                    GPIO.cleanup()
                    return
                if GPIO.input(pin_dict[current_led]) == GPIO.LOW:
                    user_input = True
                    self.turn_off_leds(leds)
                    sleep(0.2)
                    score += 1  
                    update_score_callback(score)
                elif any(GPIO.input(pin_dict[led]) == GPIO.LOW for led in pin_dict if led != current_led):
                    user_input = True
                    self.incorrect_button_delay(leds) 

            # Update the timer
            elapsed_time = time() - self.start_time
            self.time_remaining = 5 - int(elapsed_time)
            if update_timer_callback:
                update_timer_callback(self.time_remaining)

            # Brief pause before lighting up the next random LED
            sleep(0.5)

        # Game over actions
        print("GAME OVER!")
        for _ in range(5):
            self.light_up_led(leds[1])
            sleep(0.05)
            self.turn_off_leds(leds)
            sleep(0.05)


        if on_game_over_callback:
            on_game_over_callback()

        GPIO.cleanup()

    def incorrect_button_delay(self, leds):
        for _ in range(3):
            GPIO.output(leds[0], GPIO.HIGH)
            GPIO.output(leds[1], GPIO.HIGH)
            GPIO.output(leds[2], GPIO.HIGH)
            sleep(0.1)
            GPIO.output(leds[0], GPIO.LOW)
            GPIO.output(leds[1], GPIO.LOW)
            GPIO.output(leds[2], GPIO.LOW)
            sleep(0.1)

    def wait_to_resume(self):
        while self.pause_event.is_set():
            print('Game paused...')
            if self.end_game:
                print('GAME IS ENDING')
                return 1
            sleep(0.25)
        return 0

    def pause(self):
        self.pause_event.set()  # Pause the game

    def resume(self):
        self.pause_event.clear()  # Resume the game

if __name__ == '__main__':
    fast_tap_game = FastTapGame()
    fast_tap_game.run_game(None, None, None)
