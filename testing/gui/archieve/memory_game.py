import RPi.GPIO as GPIO
from time import sleep
import random
import threading
from general_functions import GeneralFunctions

# Game Parameters
SPEED = 0.5

# This game is both Memory and Memory 2P
class MemoryGame:
    def __init__(self, multiplayer=False):
        # Intializations
        self.pause_event = threading.Event()
        self.gen_funcs = GeneralFunctions()
        self.end_game = False
        self.player = 1
        self.multiplayer = multiplayer
        self.pin_dict, self.buttons, self.leds = self.gen_funcs.init_gpio()
        self.gen_funcs.turn_off_all_leds()

    # Start memory game
    def run_game(self, update_score_callback, on_game_over_callback, update_player_callback=None):
        game_is_playing = True
        num_round = 0
        user_input = False
        led_sequence = []

        while game_is_playing:
            num_round += 1
            led_sequence.append(random.choice(self.leds))

            # Light up LED sequence
            for led in led_sequence:
                if self.wait_to_resume() == 1:
                    GPIO.cleanup()
                    return
                self.gen_funcs.light_up_led_w_sleep(led, SPEED)
                sleep(SPEED)
            
            # Get user input
            i = 0
            while True:
                user_input = False
                while not user_input:
                    if self.wait_to_resume() == 1:
                        GPIO.cleanup()
                        return
                    if GPIO.input(self.buttons[0]) == GPIO.LOW:
                        self.gen_funcs.light_up_led_as_long_as_pressed(self.leds[0], self.buttons[0])
                        user_input = True
                        pressed_button = self.buttons[0]
                    elif GPIO.input(self.buttons[1]) == GPIO.LOW:
                        self.gen_funcs.light_up_led_as_long_as_pressed(self.leds[1], self.buttons[1])
                        user_input = True
                        pressed_button = self.buttons[1]
                    elif GPIO.input(self.buttons[2]) == GPIO.LOW:
                        self.gen_funcs.light_up_led_as_long_as_pressed(self.leds[2], self.buttons[2])
                        user_input = True
                        pressed_button = self.buttons[2]
                
                if self.pin_dict[led_sequence[i]] != pressed_button:
                    game_is_playing = False
                    break

                i += 1
                if i == len(led_sequence):
                    break
            
            sleep(SPEED)
            if game_is_playing:
                self.gen_funcs.flash_all_leds()
                # Change player if playing the multiplayer version
                if self.multiplayer:
                    self.change_player()
                    update_player_callback(self.player)
                update_score_callback(num_round)
            else:
                self.gen_funcs.game_over_flash()
                on_game_over_callback()
        
        GPIO.cleanup()
    
    # Change player number
    def change_player(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1
    
    # Wait to resume if game is paused
    def wait_to_resume(self):
        while self.pause_event.is_set():
            self.gen_funcs.turn_off_all_leds()
            if self.end_game:
                return 1
            sleep(0.25)
        return 0
    
    # End game if needed
    def stop(self):
        self.end_game = True
        self.pause_event.set()

    # Pause game by setting pause_event
    def pause(self):
        self.pause_event.set()

    # Resume game by resuming pause_event
    def resume(self):
        self.pause_event.clear()

if __name__ == '__main__':
    memory_game = MemoryGame()
    memory_game.run_game(None)