import RPi.GPIO as GPIO
from time import sleep, time
import random
import threading
from general_functions import GeneralFunctions

# Game Parameters
GAME_RUN_TIME = 5
SPEED = 0.25

class FastTapGame:
    def __init__(self):
        self.pause_event = threading.Event()  # Event to handle pausing
        self.gen_funcs = GeneralFunctions()
        self.end_game = False
        self.time_remaining = GAME_RUN_TIME
        self.start_time = None
        self.pin_dict, self.buttons, self.leds = self.gen_funcs.init_gpio()
        self.gen_funcs.turn_off_all_leds()

    def run_game(self, update_score_callback, update_timer_callback, on_game_over_callback):
        score = 0
        self.start_time = time()
        while not self.end_game and self.time_remaining > 0:
            # Light up a random LED
            current_led = random.choice(self.leds)
            self.gen_funcs.light_up_led(current_led)
            user_input = False
            while not user_input:
                # Update time
                self.update_time()

                if self.time_remaining == 0 :
                    print('flashing led')
                    self.gen_funcs.game_over_flash()
                    break

                # Pause Condition
                if self.wait_to_resume(current_led) == 1:
                    GPIO.cleanup()
                    return

                if GPIO.input(self.pin_dict[current_led]) == GPIO.LOW:
                    user_input = True
                    self.gen_funcs.turn_off_all_leds()
                    score += 1  
                    update_score_callback(score)
                elif any(GPIO.input(self.pin_dict[led]) == GPIO.LOW for led in self.pin_dict if led != current_led):
                    user_input = True
                    self.gen_funcs.flash_all_leds() 

            # Update time
            self.update_time()
            update_timer_callback(self.time_remaining)

            # Pause for next LED to light up
            sleep(SPEED)

        on_game_over_callback()
        GPIO.cleanup()

    def update_time(self):
        elapsed_time = time() - self.start_time
        self.time_remaining = GAME_RUN_TIME - int(elapsed_time)
    
    def light_up_led_if_needed(self, current_led):
        if GPIO.input(current_led) == GPIO.LOW:
            self.gen_funcs.light_up_led(current_led)

    def wait_to_resume(self, current_led):
        while self.pause_event.is_set():
            self.gen_funcs.turn_off_all_leds()
            print('Game paused...')
            if self.end_game:
                print('GAME IS ENDING')
                return 1
            sleep(0.25)
        self.light_up_led_if_needed(current_led)
        return 0

    def stop(self):
        self.end_game = True
        self.pause_event.set()  # Ensure the game is stopped

    def pause(self):
        self.pause_event.set()  # Pause the game

    def resume(self):
        self.pause_event.clear()  # Resume the game

if __name__ == '__main__':
    fast_tap_game = FastTapGame()
    fast_tap_game.run_game(None, None, None)
