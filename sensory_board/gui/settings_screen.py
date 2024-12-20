from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
from general_functions import GeneralFunctions

class SettingsScreen(QWidget):
    def __init__(self, stacked_widget, app_init, previous_index):
        # Intializations
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_init = app_init
        self.gen_funcs = GeneralFunctions(app_init=self.app_init, stacked_widget=self.stacked_widget)
        self.button_dict, self.led_shapes = self.gen_funcs.init_leds_and_buttons()
        self.previous_index = previous_index
        self.create_screen()
        self.update_displayed_values() 
        self.gen_funcs.change_speaker_volume(self.app_init.sound_level)

    # Create screen
    def create_screen(self):
        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout()
        layout.addWidget(self.set_title())
        layout.addLayout(self.create_sound_control_layout())
        layout.addSpacing(20)
        layout.addLayout(self.create_brightness_control_layout())
        layout.addSpacing(20)
        layout.addLayout(self.create_narration_control_layout())
        layout.addStretch()
        layout.addLayout(self.gen_funcs.create_back_layout(self.previous_index))

        self.setLayout(layout)

    # Returns title label for screen
    def set_title(self):
        title = QLabel('Settings', self)
        title.setStyleSheet("color: white; font-size: 48px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        return title

    # Returns the sound control layout. Label, %, +/- buttons
    def create_sound_control_layout(self):
        sound_label = QLabel('Sound', self)
        sound_label.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        sound_label.setAlignment(Qt.AlignCenter)

        self.sound_percentage = QLabel(f'{self.app_init.get_sound_level()}%', self)
        self.sound_percentage.setStyleSheet("color: white; font-size: 30px; font-weight: bold;")
        self.sound_percentage.setAlignment(Qt.AlignCenter)

        minus_button = QPushButton('-', self)
        minus_button.setStyleSheet(self.button_style())
        minus_button.clicked.connect(self.decrease_sound_level)
        
        plus_button = QPushButton('+', self)
        plus_button.setStyleSheet(self.button_style())
        plus_button.clicked.connect(self.increase_sound_level)

        button_and_percent_layout = QHBoxLayout()
        button_and_percent_layout.addWidget(minus_button)
        button_and_percent_layout.addWidget(self.sound_percentage)
        button_and_percent_layout.addWidget(plus_button)

        sound_control_layout = QVBoxLayout()
        sound_control_layout.addWidget(sound_label)
        sound_control_layout.addLayout(button_and_percent_layout)

        return sound_control_layout

    # Returns the brightness control layout. Label, %, +/- buttons
    def create_brightness_control_layout(self):
        brightness_label = QLabel('Brightness', self)
        brightness_label.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        brightness_label.setAlignment(Qt.AlignCenter)

        self.brightness_percentage = QLabel(f'{self.app_init.get_brightness_level()}%', self)
        self.brightness_percentage.setStyleSheet("color: white; font-size: 30px; font-weight: bold;")
        self.brightness_percentage.setAlignment(Qt.AlignCenter)

        minus_button = QPushButton('-', self)
        minus_button.setStyleSheet(self.button_style())
        minus_button.clicked.connect(self.decrease_brightness_level)
        
        plus_button = QPushButton('+', self)
        plus_button.setStyleSheet(self.button_style())
        plus_button.clicked.connect(self.increase_brightness_level)

        button_and_percent_layout = QHBoxLayout()
        button_and_percent_layout.addWidget(minus_button)
        button_and_percent_layout.addWidget(self.brightness_percentage)
        button_and_percent_layout.addWidget(plus_button)

        brightness_control_layout = QVBoxLayout()
        brightness_control_layout.addWidget(brightness_label)
        brightness_control_layout.addLayout(button_and_percent_layout)

        return brightness_control_layout

    # General function for the +/- and narration buttons since they have similar appearances
    def button_style(self):
        return """
            background-color: gray; 
            color: white; 
            border-radius: 25px; 
            font-size: 24px; 
            font-weight: bold;
            width: 50px; 
            height: 70px; 
            padding: 0;
            text-align: center;
            line-height: 60px;
        """

    # Returns the narration control layout. Label and on/off buttons
    def create_narration_control_layout(self):
        narration_label = QLabel('Narration', self)
        narration_label.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        narration_label.setAlignment(Qt.AlignCenter)

        self.off_button = QPushButton('Off', self)
        self.on_button = QPushButton('On', self)
        self.narration_button_logic()

        self.off_button.clicked.connect(self.toggle_narration_off)
        self.on_button.clicked.connect(self.toggle_narration_on)

        narration_control_layout = QVBoxLayout()
        narration_control_layout.addWidget(narration_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.off_button)
        button_layout.addWidget(self.on_button)
        narration_control_layout.addLayout(button_layout)

        return narration_control_layout

    # Function that handles the selected button in narration turning green
    def narration_button_logic(self):
        self.off_button.setStyleSheet(f"{self.button_style()} background-color: {'green' if not self.app_init.get_narration_bool() else 'gray'};")
        self.on_button.setStyleSheet(f"{self.button_style()} background-color: {'green' if self.app_init.get_narration_bool() else 'gray'};")

    # Function that makes narration_on False and changes corresponding button color
    def toggle_narration_off(self):
        self.app_init.narration_on = False
        self.narration_button_logic()

    # Function that makes narration_on True and changes corresponding button color
    def toggle_narration_on(self):
        self.app_init.narration_on = True
        self.narration_button_logic()

    # Function that handles increasing the sound level and updating it in real-time
    def increase_sound_level(self):
        if self.app_init.sound_level < 100:
            self.app_init.sound_level += 10
            self.sound_percentage.setText(f'{self.app_init.get_sound_level()}%')
            self.gen_funcs.change_speaker_volume(self.app_init.sound_level)

    # Function that handles decreasing the sound level and updating it in real-time
    def decrease_sound_level(self):
        if self.app_init.sound_level > 0:
            self.app_init.sound_level -= 10
            self.sound_percentage.setText(f'{self.app_init.get_sound_level()}%')
            self.gen_funcs.change_speaker_volume(self.app_init.sound_level)

    # Function that handles increasing the brightness level and updating it in real-time
    def increase_brightness_level(self):
        if self.app_init.brightness_level < 100:
            self.app_init.brightness_level += 10
            self.brightness_percentage.setText(f'{self.app_init.get_brightness_level()}%')
            self.gen_funcs.light_up_settings_leds()

    # Function that handles decreasing the brightness level and updating it in real-time
    def decrease_brightness_level(self):
        if self.app_init.brightness_level > 0:
            self.app_init.brightness_level -= 10
            self.brightness_percentage.setText(f'{self.app_init.get_brightness_level()}%')
            self.gen_funcs.light_up_settings_leds()
    
    # Update displayed settings values for sound, brightness, and narration
    def update_displayed_values(self):
        self.sound_percentage.setText(f'{self.app_init.sound_level}%')
        self.brightness_percentage.setText(f'{self.app_init.brightness_level}%')
        self.narration_button_logic()