import RPi.GPIO as GPIO
from time import sleep
import random
import threading

# # Define global flag for stopping the game
# PAUSE_GAME = False

class MemoryGame():
    def stop(self):
        # global PAUSE_GAME
        # PAUSE_GAME = True
        if self.game_thread and self.game_thread.is_alive():
            self.game_thread.join()

    def light_up_led(self, pin, sleep_time):
        GPIO.output(pin, GPIO.HIGH)
        sleep(sleep_time)
        GPIO.output(pin, GPIO.LOW)

    def run_game(self, update_score_callback):
        # global PAUSE_GAME
        # PAUSE_GAME = False

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
        
        GPIO.output(yellow_led, GPIO.LOW)
        GPIO.output(red_led, GPIO.LOW)
        GPIO.output(green_led, GPIO.LOW)

        game_is_playing = True
        num_round = 0
        user_input = False
        led_sequence = []

        print("BEGIN GAME")

        while game_is_playing:
            num_round += 1
            print("ROUND", num_round)
            led_sequence.append(random.choice(list(pin_dict.keys())))

            # Light up LED sequence
            print("Showing LED sequence")
            for led in led_sequence:
                # if PAUSE_GAME:
                #     GPIO.cleanup()
                #     return
                sleep(0.5)
                self.light_up_led(led, 0.5)
            
            # Get user input
            print("Repeat LED sequence")
            i = 0
            while True:
                user_input = False
                while not user_input:
                    # if PAUSE_GAME:
                    #     GPIO.cleanup()
                    #     return
                    if GPIO.input(yellow_button) == GPIO.LOW:
                        self.light_up_led(yellow_led, 0.25)
                        user_input = True
                        pressed_button = yellow_button
                    elif GPIO.input(green_button) == GPIO.LOW:
                        self.light_up_led(green_led, 0.25)
                        user_input = True
                        pressed_button = green_button
                    elif GPIO.input(red_button) == GPIO.LOW:
                        self.light_up_led(red_led, 0.25)
                        user_input = True
                        pressed_button = red_button
                
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
                print("CORRECT")
                for _ in range(3):
                    GPIO.output(yellow_led, GPIO.HIGH)
                    GPIO.output(red_led, GPIO.HIGH)
                    GPIO.output(green_led, GPIO.HIGH)
                    sleep(0.1)
                    GPIO.output(yellow_led, GPIO.LOW)
                    GPIO.output(red_led, GPIO.LOW)
                    GPIO.output(green_led, GPIO.LOW)
                    sleep(0.1)
                # Call the callback to update the score
                update_score_callback(num_round)
            else:
                print("INCORRECT SEQUENCE. GAME OVER!")
                for _ in range(5):
                    self.light_up_led(red_led, 0.05)
                    sleep(0.05)
        
        GPIO.cleanup()
