import RPi.GPIO as GPIO
from time import sleep
import random
import threading
from general_functions import GeneralFunctions

class MemoryGame:
    def __init__(self):
        self.pause_event = threading.Event()  # Event to handle pausing
        self.gen_funcs = GeneralFunctions()
        self.end_game = False

    def stop(self):
        self.end_game = True
        self.pause_event.set()  # Ensure the game is stopped

    def light_up_led(self, pin, sleep_time):
        GPIO.output(pin, GPIO.HIGH)
        sleep(sleep_time)
        GPIO.output(pin, GPIO.LOW)

    def run_game(self, update_score_callback, on_game_over_callback):
        pin_dict = self.gen_funcs.set_up_gpio_and_get_pin_dict()

        buttons = list(pin_dict.values())
        leds = list(pin_dict.keys())

        game_is_playing = True
        num_round = 0
        user_input = False
        led_sequence = []

        while game_is_playing:
            num_round += 1
            led_sequence.append(random.choice(list(pin_dict.keys())))

            # Light up LED sequence
            for led in led_sequence:
                if self.wait_to_resume() == 1:
                    return
                self.light_up_led(led, 0.5)
                sleep(0.5)
            
            # Get user input
            i = 0
            while True:
                if self.wait_to_resume() == 1:
                    return
                user_input = False
                while not user_input:
                    if self.wait_to_resume() == 1:
                        return
                    if GPIO.input(buttons[0]) == GPIO.LOW:
                        self.light_up_led(leds[0], 0.25)
                        user_input = True
                        pressed_button = buttons[0]
                    elif GPIO.input(buttons[1]) == GPIO.LOW:
                        self.light_up_led(leds[1], 0.25)
                        user_input = True
                        pressed_button = buttons[1]
                    elif GPIO.input(buttons[2]) == GPIO.LOW:
                        self.light_up_led(leds[2], 0.25)
                        user_input = True
                        pressed_button = buttons[2]
                
                if pin_dict[led_sequence[i]] != pressed_button:
                    game_is_playing = False
                    break

                i += 1
                if i == len(led_sequence):
                    break
                else:
                    sleep(0.5)
            
            sleep(0.5)
            if game_is_playing:
                for _ in range(3):
                    GPIO.output(leds[0], GPIO.HIGH)
                    GPIO.output(leds[1], GPIO.HIGH)
                    GPIO.output(leds[2], GPIO.HIGH)
                    sleep(0.1)
                    GPIO.output(leds[0], GPIO.LOW)
                    GPIO.output(leds[1], GPIO.LOW)
                    GPIO.output(leds[2], GPIO.LOW)
                    sleep(0.1)
                # Call the callback to update the score
                update_score_callback(num_round)
            else:
                print("INCORRECT SEQUENCE. GAME OVER!")
                for _ in range(5):
                    self.light_up_led(leds[1], 0.05)
                    sleep(0.05)
                on_game_over_callback() 
        
        GPIO.cleanup()
    
    def wait_to_resume(self):
        while self.pause_event.is_set():
            print('waiting...(2)')
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
    memory_game = MemoryGame()
    memory_game.run_game(None)