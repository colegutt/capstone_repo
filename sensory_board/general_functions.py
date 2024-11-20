from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout 
import RPi.GPIO as GPIO
import time
from time import sleep
from bluetooth import *
import board
import neopixel

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

        self.pixels = None
        self.led_slices = None
        self.rgb_colors = None
        self.led_slice_array = None
        
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
        if self.led_slices != None:
            self.turn_off_all_leds()
        self.stacked_widget.setCurrentIndex(index)

    def init_leds_and_buttons(self):
        GPIO.setmode(GPIO.BCM)
        pixel_pin = board.D18
        num_leds = 40
        self.pixels = neopixel.NeoPixel(pixel_pin, num_leds)
        self.led_slice_array = list(range(num_leds + 1))

        self.led_slices = {
            'square': self.led_slice_array[slice(26,31)],
            'cloud': self.led_slice_array[slice(20, 26)],
            'triangle': self.led_slice_array[slice(17,20)],
            'heart': self.led_slice_array[slice(11, 17)],
            'circle': self.led_slice_array[slice(5,11)],
            'star': self.led_slice_array[slice(0, 5)]
        }

        self.rgb_colors = {
            'square': (0, 255, 0) ,
            'cloud': (0, 0, 255),
            'triangle': (128, 0, 128),
            'heart': (255, 0, 0),
            'circle': (255, 100, 0),
            'star': (255, 165, 0),
            'off': (0, 0, 0)
        }

        square_button = 19
        cloud_button = 6 
        triangle_button = 17
        heart_button = 25
        circle_button = 14
        star_button = 24

        button_dict = {
            'square': square_button,
            'cloud': cloud_button,
            'triangle': triangle_button,
            'heart': heart_button,
            'circle': circle_button,
            'star': star_button,
        }

        for button in button_dict.values():
            GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        return button_dict, list(self.led_slices.keys())

    # # Turn off all LEDs
    # def turn_off_all_leds(self):
    #     for led in self.leds:
    #         GPIO.output(led, GPIO.LOW)

    def turn_off_all_leds(self):
        for p in self.led_slices['star']:
            self.pixels[p] = (0, 0, 0) 
        for p in self.led_slices['triangle']:
            self.pixels[p] = (0, 0, 0)  
        for p in self.led_slices['circle']:
            self.pixels[p] = (0, 0, 0)  
        for p in self.led_slices['heart']:
            self.pixels[p] = (0, 0, 0) 
        for p in self.led_slices['cloud']:
            self.pixels[p] = (0, 0, 0)  
        for p in self.led_slices['square']:
            self.pixels[p] = (0, 0, 0)  

        self.pixels.show()
    
    def detect_button_press(self, button):
        if GPIO.input(button) == GPIO.LOW:
            sleep(0.01)
            if GPIO.input(button) == GPIO.LOW:
                return True
        return False

    def light_up_all_leds(self):
        for p in self.led_slices['star']:
            self.pixels[p] = self.dim_color(self.rgb_colors['star'], self.app_init.brightness_level / 100) 
        for p in self.led_slices['circle']:
            self.pixels[p] = self.dim_color(self.rgb_colors['circle'], self.app_init.brightness_level / 100) 
        for p in self.led_slices['heart']:
            self.pixels[p] = self.dim_color(self.rgb_colors['heart'], self.app_init.brightness_level / 100) 
        for p in self.led_slices['triangle']:
            self.pixels[p] = self.dim_color(self.rgb_colors['triangle'], self.app_init.brightness_level / 100) 
        for p in self.led_slices['cloud']:
            self.pixels[p] = self.dim_color(self.rgb_colors['cloud'], self.app_init.brightness_level / 100) 
        for p in self.led_slices['square']:
            self.pixels[p] = self.dim_color(self.rgb_colors['square'], self.app_init.brightness_level / 100) 

        self.pixels.show()
    
    def change_speaker_volume(self, sound_level):
        sound_level = sound_level / 100
        for sound in self.app_init.beep_sounds.values():
            sound.set_volume(sound_level)
        for sound in self.app_init.narration_sounds.values():
            sound.set_volume(sound_level)
        for sound in self.app_init.other_sounds.values():
            sound.set_volume(sound_level)
    
    def play_beep_sound(self, led_shape):
        if self.app_init.get_narration_bool():
            self.app_init.narration_sounds[led_shape].play()
        else:
            self.app_init.beep_sounds[led_shape].play()
    
    def dim_color(self, color, factor):
        return tuple(int(c*factor)for c in color)

    # Flash all LEDs 3 times
    def memory_correct_sequence_flash(self):
        self.flash_all_leds_helper('memory correct sequence', 0.5)
    
    def fast_tap_wrong_led(self):
        self.flash_all_leds_helper('fast tap wrong led', 0.5)
    
    def flash_all_leds_helper(self, sound, sleep_time):
        self.light_up_all_leds()
        self.app_init.other_sounds[sound].play()
        sleep(sleep_time)
        self.turn_off_all_leds()
        sleep(sleep_time)

    def light_up_led(self, led_shape, sound=True):
        for p in self.led_slices[led_shape]:
            self.pixels[p] = self.dim_color(self.rgb_colors[led_shape], self.app_init.brightness_level / 100) 
        if sound:
            self.play_beep_sound(led_shape)
        self.pixels.show()
    
    def light_up_settings_leds(self):
        for p in self.led_slices['heart']:
            self.pixels[p] = self.dim_color(self.rgb_colors['heart'], self.app_init.brightness_level / 100)
        for p in self.led_slices['circle']:
            self.pixels[p] = self.dim_color(self.rgb_colors['circle'], self.app_init.brightness_level / 100) 
        for p in self.led_slices['star']:
            self.pixels[p] = self.dim_color(self.rgb_colors['star'], self.app_init.brightness_level / 100) 

    def light_up_led_w_sleep(self, led_shape, sleep_time, sound=True):
        self.light_up_led(led_shape, sound)
        sleep(sleep_time)
        self.turn_off_led(led_shape)

    def light_up_led_as_long_as_pressed(self, led_shape, button):
        self.light_up_led(led_shape) 
        while GPIO.input(button) == GPIO.LOW:
            sleep(0.01)

        self.turn_off_led(led_shape)
        sleep(0.1)

    def turn_off_led(self, led_shape):
        for p in self.led_slices[led_shape]:
            self.pixels[p] = self.rgb_colors['off']
        self.pixels.show()

    def game_over_flash(self, sound=True):
        if sound:
            self.app_init.other_sounds['game over'].play()
        self.turn_off_all_leds()
        self.light_up_led_w_sleep('cloud', 0.2, False)
        self.light_up_led_w_sleep('triangle', 0.2, False)
        self.light_up_led_w_sleep('heart', 0.2, False)
        self.light_up_led_w_sleep('circle', 0.2, False)
        self.light_up_led_w_sleep('star', 0.2, False)
        self.light_up_led_w_sleep('square', 0.2, False)
    
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
    def create_score_label(self, font_size=68):
        self.score_label = QLabel(f'Score: {self.game_score}', self)
        self.score_label.setStyleSheet(f'color: white; font-size: {font_size}px; font-weight: bold;')
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