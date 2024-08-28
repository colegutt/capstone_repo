from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout

class SettingsScreen(QWidget):
    def __init__(self, stacked_widget):
        # Initialize QWidget class
        super().__init__()

        # For screen navigation
        self.stacked_widget = stacked_widget

        # Initialize state
        self.sound_level = 50
        self.brightness_level = 50
        self.narration_on = False

        # Create screen
        self.create_screen()
        
    def create_screen(self):
        # Make background black
        self.setStyleSheet("background-color: black;")

        # Set screen layout
        self.set_layout(
            self.set_title(),
            self.create_sound_control(),
            self.create_brightness_control(),
            self.create_narration_control(),
            self.create_back_button()
        )
    
    def set_title(self):
        # Title name
        title = QLabel('Settings', self)
        title.setStyleSheet("color: white; font-size: 48px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        return title

    def create_sound_control(self):
        # Sound label
        sound_label = QLabel('Sound', self)
        sound_label.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        sound_label.setAlignment(Qt.AlignCenter)

        # Sound percentage display
        self.sound_percentage = QLabel(f'{self.sound_level}%', self)
        self.sound_percentage.setStyleSheet("color: white; font-size: 30px; font-weight: bold;")
        self.sound_percentage.setAlignment(Qt.AlignCenter)

        # "-" button
        minus_button = QPushButton('-', self)
        minus_button.setStyleSheet(self.button_style())
        minus_button.clicked.connect(self.decrease_sound_level)
        
        # "+" button
        plus_button = QPushButton('+', self)
        plus_button.setStyleSheet(self.button_style())
        plus_button.clicked.connect(self.increase_sound_level)

        # Layout of sound control
        button_and_percent_layout = QHBoxLayout()
        button_and_percent_layout.addWidget(minus_button)
        button_and_percent_layout.addWidget(self.sound_percentage)
        button_and_percent_layout.addWidget(plus_button)

        sound_control_layout = QVBoxLayout()
        sound_control_layout.addWidget(sound_label)
        sound_control_layout.addLayout(button_and_percent_layout)

        return sound_control_layout
    
    def create_brightness_control(self):
        # Brightness label
        brightness_label = QLabel('Brightness', self)
        brightness_label.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        brightness_label.setAlignment(Qt.AlignCenter)

        # Brightness percentage display
        self.brightness_percentage = QLabel(f'{self.brightness_level}%', self)
        self.brightness_percentage.setStyleSheet("color: white; font-size: 30px; font-weight: bold;")
        self.brightness_percentage.setAlignment(Qt.AlignCenter)

        # "+" and "-" buttons
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

    def create_narration_control(self):
        # Narration label
        narration_label = QLabel('Narration', self)
        narration_label.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        narration_label.setAlignment(Qt.AlignCenter)

        # "Off" and "On" buttons
        self.off_button = QPushButton('Off', self)
        self.on_button = QPushButton('On', self)

        self.narration_button_logic()

        self.off_button.clicked.connect(self.toggle_narration_off)
        self.on_button.clicked.connect(self.toggle_narration_on)

        # Layout for narration control
        narration_control_layout = QVBoxLayout()
        narration_control_layout.addWidget(narration_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.off_button)
        button_layout.addWidget(self.on_button)
        narration_control_layout.addLayout(button_layout)

        return narration_control_layout

    def narration_button_logic(self):
        # Set style for Off and On buttons
        self.off_button.setStyleSheet(f"{self.button_style()} background-color: {'green' if not self.narration_on else 'gray'};")
        self.on_button.setStyleSheet(f"{self.button_style()} background-color: {'green' if self.narration_on else 'gray'};")
    
    def toggle_narration_off(self):
        self.narration_on = False
        self.narration_button_logic()

    def toggle_narration_on(self):
        self.narration_on = True
        self.narration_button_logic()

    def increase_sound_level(self):
        if self.sound_level < 100:
            self.sound_level += 10
            self.sound_percentage.setText(f'{self.sound_level}%')

    def decrease_sound_level(self):
        if self.sound_level > 0:
            self.sound_level -= 10
            self.sound_percentage.setText(f'{self.sound_level}%')
            
    def increase_brightness_level(self):
        if self.brightness_level < 100:
            self.brightness_level += 10
            self.brightness_percentage.setText(f'{self.brightness_level}%')

    def decrease_brightness_level(self):
        if self.brightness_level > 0:
            self.brightness_level -= 10
            self.brightness_percentage.setText(f'{self.brightness_level}%')

    def create_back_button(self):
        # Back button
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
        back_button.clicked.connect(self.go_back)
        return back_button

    def set_layout(self, title, sound_control, brightness_control, narration_control, back_button):
        # Layout for sound, brightness, and narration controls
        control_layout = QVBoxLayout()
        control_layout.addLayout(sound_control)
        control_layout.addSpacing(20)
        control_layout.addLayout(brightness_control)
        control_layout.addSpacing(20)
        control_layout.addLayout(narration_control)
        control_layout.addStretch()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addStretch()
        main_layout.addLayout(control_layout)

        # Layout for the back button
        back_layout = QHBoxLayout()
        back_layout.addWidget(back_button)
        back_layout.addStretch()
        back_layout.setContentsMargins(20, 20, 20, 20)  # Margin around the back button

        # Combine main layout and back button layout
        final_layout = QVBoxLayout()
        final_layout.addLayout(main_layout)
        final_layout.addLayout(back_layout)
        self.setLayout(final_layout)

    def go_back(self):
        self.stacked_widget.setCurrentIndex(0)