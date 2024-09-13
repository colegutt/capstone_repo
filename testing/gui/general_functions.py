from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout 
import RPi.GPIO as GPIO
from time import sleep

class GeneralFunctions(QWidget):
    def __init__(self, stacked_widget=None):
        self.stacked_widget = stacked_widget
        self.pin_dict = None
        self.leds = None
        self.buttons = None
        super().__init__()
    
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
    
    def go_back(self, index):
        self.stacked_widget.setCurrentIndex(index)
    
    def set_up_gpio_and_get_pin_dict(self):
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

    def turn_off_all_leds(self):
        for led in self.leds:
            GPIO.output(led, GPIO.LOW)
    
    def light_up_all_leds(self):
        GPIO.output(self.leds[0], GPIO.HIGH)
        GPIO.output(self.leds[1], GPIO.HIGH)
        GPIO.output(self.leds[2], GPIO.HIGH)
    
    def flash_all_leds(self):
        for _ in range(3):
            self.light_up_all_leds()
            sleep(0.1)
            self.turn_off_all_leds()
            sleep(0.1)
    
    def light_up_led(self, led):
        GPIO.output(led, GPIO.HIGH)
    
    def turn_off_led(self, led):
        GPIO.output(led, GPIO.LOW)
    
    def game_over_flash(self):
        self.turn_off_all_leds()
        print('flashing led')
        for _ in range(5):
            self.light_up_led(self.leds[1])
            sleep(0.05)
            self.turn_off_led(self.leds[1])
            sleep(0.05)