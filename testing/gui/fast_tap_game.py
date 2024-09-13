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
            if self.wait_to_resume() == 1:
                GPIO.cleanup()
                return
            
            # Light up a random LED
            current_led = random.choice(list(leds))
            self.light_up_led(current_led)

            # Wait for user to press the corresponding button
            user_input = False
            while not user_input:
                if self.wait_to_resume() == 1:
                    GPIO.cleanup()
                    return
                if GPIO.input(pin_dict[current_led]) == GPIO.LOW:
                    user_input = True
                    self.turn_off_leds(leds)  # Turn off all LEDs
                    sleep(0.2)  # Brief pause before lighting up the next LED
                    score += 1  # Increment the score
                    if update_score_callback:
                        update_score_callback(score)

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
            light_up_led(leds[1])
            sleep(0.05)
            turn_off_leds(leds)
            sleep(0.05)


        if on_game_over_callback:
            on_game_over_callback()

        GPIO.cleanup()

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
