from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout 
import RPi.GPIO as GPIO
from time import sleep
from bluetooth import *
import subprocess
import os
import pygame

USB_SPEAKER_SINK = 'alsa_output.usb-Solid_State_System_Co._Ltd._USB_PnP_Audio_Device_000000000000-00.analog-stereo'

# These are general functions that are used in all scripts in this directory
# to reduce code space and simplify functions
class GeneralFunctions(QWidget):
    def __init__(self, stacked_widget=None, game_score=None, reset_game_func=None, start_game_func=None, pause_game_func=None, multiplayer=False, app_init=None):
        # Intializations
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_init = app_init
        self.game_score = game_score
        self.reset_game_func = reset_game_func
        self.start_game_func = start_game_func
        self.pause_game_func = pause_game_func
        self.multiplayer = multiplayer
        self.pin_dict = None
        self.leds = None
        self.buttons = None
        
    # Create common back button that is in bottom left of all screens
    def create_back_layout(self, index):
        back_button = QPushButton('Back', self)
        back_button.setStyleSheet("""
            background-color: red; 
            color: white; 
            border-radius: 0px; 
            font-size: 16px; 
            font-weight: bold;
            width: 150px; 
            height: 50px; 
            padding: 0;
            text-align: center;
            line-height: 50px;
        """)
        back_button.clicked.connect(lambda checked, index=index: self.go_back(index))
        back_layout = QHBoxLayout()
        back_layout.addWidget(back_button)
        back_layout.addStretch()
        back_layout.setContentsMargins(20, 20, 20, 20)
        return back_layout
    
    # Function that goes back to the previous screen when button is clicked
    def go_back(self, index):
        self.stacked_widget.setCurrentIndex(index)
    
    # Intialize GPIO pins:
    # Yellow LED    (GPIO 17)
    # Red LED       (GPIO 27)
    # Green LED     (GPIO 22)
    # Yellow Button (GPIO 18)
    # Red Button    (GPIO 15)
    # Green Button  (GPIO 14)
    def init_gpio(self):
        GPIO.setmode(GPIO.BCM)
        yellow_led = 17
        red_led = 27
        green_led = 22
        yellow_button = 18
        red_button = 15
        green_button = 14

        self.pin_dict = {
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

        self.buttons = list(self.pin_dict.values())
        self.leds = list(self.pin_dict.keys())

        return self.pin_dict, self.buttons, self.leds

    # Turn off all LEDs
    def turn_off_all_leds(self):
        for led in self.leds:
            GPIO.output(led, GPIO.LOW)
    
    # Light up all LEDs
    def light_up_all_leds(self):
        GPIO.output(self.leds[0], GPIO.HIGH)
        GPIO.output(self.leds[1], GPIO.HIGH)
        GPIO.output(self.leds[2], GPIO.HIGH)
    
    def change_speaker_volume(self, sound_level):
        sound_level = sound_level / 100
        for sound in self.app_init.sounds.values():
            sound.set_volume(sound_level)

    def play_beep_sound(self, led):
        self.app_init.sounds[led].play()

    # Flash all LEDs 3 times
    def flash_all_leds(self):
        for _ in range(3):
            self.light_up_all_leds()
            sleep(0.1)
            self.turn_off_all_leds()
            sleep(0.1)
    
    # Light up only one LED
    def light_up_led(self, led):
        GPIO.output(led, GPIO.HIGH)
        self.play_beep_sound(led)
    
    # Light up LED and turn off within a set time
    def light_up_led_w_sleep(self, led, sleep_time):
        self.light_up_led(led)
        sleep(sleep_time)
        self.turn_off_led(led)

    # Light up LED as long as a button is pressed
    def light_up_led_as_long_as_pressed(self, led, button):
        self.light_up_led(led) 
        while GPIO.input(button) == GPIO.LOW:
            sleep(0.01)

        self.turn_off_led(led)
        sleep(0.1)
    
    # Turn off a singular LED
    def turn_off_led(self, led):
        GPIO.output(led, GPIO.LOW)
    
    # Blink red LED 5 times rapidly, signaling game over
    def game_over_flash(self):
        self.turn_off_all_leds()
        for _ in range(5):
            self.light_up_led(self.leds[1])
            sleep(0.05)
            self.turn_off_led(self.leds[1])
            sleep(0.05)
    
    # Returns title label for screen
    def set_title(self, label):
        title = QLabel(label, self)
        title.setStyleSheet("color: white; font-size: 72px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        return title
    
    # Returns game over label for in-game screens
    def create_game_over_label(self):
        game_over_label = QLabel(f'GAME OVER!', self)
        game_over_label.setStyleSheet("color: red; font-size: 40px; font-weight: bold;")
        game_over_label.setAlignment(Qt.AlignCenter)
        game_over_label.setVisible(False)
        return game_over_label
    
    # Returns pause button for in-game screens
    def create_pause_button(self):
        pause_button = QPushButton('Pause', self)
        pause_button.setStyleSheet("""
            background-color: orange; 
            color: white; 
            border-radius: 50px; 
            font-size: 26px; 
            font-weight: bold;
            width: 100px;
            height: 100px;
            padding: 0;
            text-align: center;
            line-height: 100px;
        """)
        pause_button.clicked.connect(self.pause_game_func)
        return pause_button
    
    # Returns score label for in-game screens
    def create_score_label(self):
        self.score_label = QLabel(f'Score: {self.game_score}', self)
        self.score_label.setStyleSheet("color: white; font-size: 68px; font-weight: bold;")
        self.score_label.setAlignment(Qt.AlignCenter)
        return self.score_label

    # Returns play again button that is shown when a game ends
    def create_play_again_button(self):
        play_again_button = QPushButton('Play Again', self)
        play_again_button.setStyleSheet("""
            background-color: green; 
            color: white; 
            border-radius: 10px; 
            font-size: 24px; 
            font-weight: bold;
            width: 300px;
            height: 75px;
        """)
        play_again_button.clicked.connect(self.play_game_again)
        play_again_button.setVisible(False)
        return play_again_button
    
    # Returns go back button that is shown when a game ends
    def create_go_back_button(self):
        go_back_button = QPushButton('Go Back', self)
        go_back_button.setStyleSheet("""
            background-color: red; 
            color: white; 
            border-radius: 10px; 
            font-size: 24px; 
            font-weight: bold;
            width: 300px;
            height: 75px;
        """)
        go_back_button.clicked.connect(self.select_new_game)
        go_back_button.setVisible(False)
        return go_back_button
    
    # Function that hides or shows the game over, play again, and go back buttons
    def hide_or_show_end_game_buttons(self, game_over_label, play_again_button, go_back_button, show):
        game_over_label.setVisible(show)
        play_again_button.setVisible(show)
        go_back_button.setVisible(show)
    
    # General play again function
    def play_game_again(self):
        self.reset_game_func()
        self.start_game_func()
    
    # Select new game by resetting current game and going to the correct index screen
    def select_new_game(self):
        self.reset_game_func()
        if self.multiplayer:
            self.stacked_widget.setCurrentIndex(2)
        else:
            self.stacked_widget.setCurrentIndex(1)