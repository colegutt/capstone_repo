from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout

class MainMenu(QWidget):
    def __init__(self, stacked_widget):
        # Initialize QWidget class
        super().__init__()

        # For screen navigation
        self.stacked_widget = stacked_widget

        # Create screen
        self.create_screen()
        
    def create_screen(self):
        # Make background black
        self.setStyleSheet("background-color: black;")

        # Set title and buttons
        self.set_layout(
            self.set_title(),
            self.create_single_player_button(),
            self.create_multiplayer_button(),
            self.create_settings_button(),
            self.create_exit_button()
        )
    
    def set_title(self):
        # Title name
        title = QLabel('BEEPY', self)

        # Title characteristics
        title.setStyleSheet("color: white; font-size: 48px; font-weight: bold;")

        # Title alignment
        title.setAlignment(Qt.AlignCenter)

        return title

    def create_single_player_button(self):
        # Single Player button
        single_player_button = QPushButton('Single Player', self)
        single_player_button.setStyleSheet("""
            background-color: green; 
            color: white; 
            border-radius: 120px; 
            font-size: 26px; 
            font-weight: bold;
            width: 240px;
            height: 240px;
            padding: 0;
            text-align: center;
            line-height: 240px;
        """)
        single_player_button.clicked.connect(self.show_SP_screen)
        return single_player_button

    def create_multiplayer_button(self):
        # Multiplayer button
        multiplayer_button = QPushButton('Multiplayer', self)
        multiplayer_button.setStyleSheet("""
            background-color: blue; 
            color: white; 
            border-radius: 120px; 
            font-size: 26px; 
            font-weight: bold;
            width: 240px; 
            height: 240px; 
            padding: 0;
            text-align: center;
            line-height: 240px;
        """)
        multiplayer_button.clicked.connect(self.show_MP_screen)
        return multiplayer_button
    
    def create_settings_button(self):
        # Settings button
        settings_button = QPushButton('Settings', self)
        settings_button.setStyleSheet("""
            background-color: gray; 
            color: white; 
            border-radius: 80px; 
            font-size: 26px; 
            font-weight: bold;
            width: 160px; 
            height: 160px; 
            padding: 0;
            text-align: center;
            line-height: 160px;
        """)
        settings_button.clicked.connect(self.show_SETTINGS_screen)
        return settings_button
    
    def create_exit_button(self):
        # Exit button
        exit_button = QPushButton('Exit', self)
        exit_button.setStyleSheet("""
            background-color: red; 
            color: white; 
            border-radius: 25px; 
            font-size: 16px; 
            font-weight: bold;
            width: 50px; 
            height: 50px; 
            padding: 0;
            text-align: center;
            line-height: 50px;
        """)
        exit_button.clicked.connect(QApplication.instance().quit)
        return exit_button

    def set_layout(self, title, single_player_button, multiplayer_button, settings_button, exit_button):
        # Layout for single player and multiplayer buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(single_player_button)
        button_layout.addStretch()
        button_layout.addWidget(multiplayer_button)
        button_layout.addStretch()

        # Layout for settings button
        settings_layout = QVBoxLayout()
        settings_layout.addStretch()
        settings_layout.addWidget(settings_button, alignment=Qt.AlignCenter)
        settings_layout.addStretch()

        # # Layout for exit button
        exit_layout = QHBoxLayout()
        exit_layout.addWidget(exit_button)
        exit_layout.addStretch()  # Add space to push exit button to the bottom
        exit_layout.addWidget(exit_button)
        settings_layout.addStretch()
        exit_layout.setContentsMargins(20, 20, 20, 20)  # Margin around the lay

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(title)  # Add title at the top
        main_layout.addStretch()  # Add space between title and buttons
        main_layout.addLayout(button_layout)  # Add buttons layout
        main_layout.addSpacing(20)  # Space between button row and settings button
        main_layout.addLayout(settings_layout)  # Add settings button layout
        main_layout.addStretch()  # Add space below settings button

        # Combine main layout and exit button layout
        final_layout = QVBoxLayout()
        final_layout.addLayout(main_layout)  # Add main content
        final_layout.addLayout(exit_layout)  # Add exit button
        final_layout.addStretch()  # Add space below settings button
        self.setLayout(final_layout)  # Set the final layout for the main menu
    
    def show_SP_screen(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_MP_screen(self):
        self.stacked_widget.setCurrentIndex(2)

    def show_SETTINGS_screen(self):
        self.stacked_widget.setCurrentIndex(1)