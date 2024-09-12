import RPi.GPIO as GPIO
from time import sleep, time
import random
import threading

class FastTapGame:
    def __init__(self):
        self.pause_event = threading.Event()  # Event to handle pausing
        self.end_game = False
        self.time_remaining = 30  # 30 seconds for the game duration
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

        self.turn_off_leds(pin_dict.keys())

        score = 0
        self.start_time = time()

        while not self.end_game and self.time_remaining > 0:
            if self.wait_to_resume() == 1:
                return
            
            # Light up a random LED
            current_led = random.choice(list(pin_dict.keys()))
            self.light_up_led(current_led)

            # Wait for user to press the corresponding button
            user_input = False
            while not user_input:
                if self.wait_to_resume() == 1:
                    return
                if GPIO.input(pin_dict[current_led]) == GPIO.LOW:
                    user_input = True
                    self.turn_off_leds(pin_dict.keys())  # Turn off all LEDs
                    sleep(0.2)  # Brief pause before lighting up the next LED
                    score += 1  # Increment the score
                    if update_score_callback:
                        update_score_callback(score)

            # Update the timer
            elapsed_time = time() - self.start_time
            self.time_remaining = 30 - int(elapsed_time)
            if update_timer_callback:
                update_timer_callback(self.time_remaining)

            # Brief pause before lighting up the next random LED
            sleep(0.5)

        # Game over actions
        print("GAME OVER!")
        for _ in range(5):
            self.light_up_led(red_led)
            sleep(0.05)
            GPIO.output(red_led, GPIO.LOW)
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
