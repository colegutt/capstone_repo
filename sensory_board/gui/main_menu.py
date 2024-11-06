import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout

# Main menu screen creation
class MainMenu(QWidget):
    def __init__(self, stacked_widget, app_init):
        # Intializations
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_init = app_init

        # Create labels and buttons that are used in create_screen
        self.title = self.set_title()
        self.single_player_button = self.create_single_player_button()
        self.multiplayer_button = self.create_multiplayer_button()
        self.settings_button = self.create_settings_button()
        self.exit_button = self.create_exit_button()

        self.create_screen()
    
    # Create screen using previously created labels and buttons
    def create_screen(self):
        self.setStyleSheet("background-color: black;")
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.single_player_button)
        button_layout.addStretch()
        button_layout.addWidget(self.multiplayer_button)
        button_layout.addStretch()

        settings_layout = QVBoxLayout()
        settings_layout.addStretch()
        settings_layout.addWidget(self.settings_button, alignment=Qt.AlignCenter)
        settings_layout.addStretch()

        exit_layout = QHBoxLayout()
        exit_layout.addWidget(self.exit_button)
        exit_layout.addStretch()
        exit_layout.setContentsMargins(20, 20, 20, 20)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)  
        main_layout.addSpacing(20) 
        main_layout.addLayout(settings_layout) 
        main_layout.addStretch() 

        final_layout = QVBoxLayout()
        final_layout.addLayout(main_layout)
        final_layout.addLayout(exit_layout)
        final_layout.addStretch() 
        self.setLayout(final_layout) 
    
    # Return title label for main menu
    def set_title(self):
        title = QLabel('BEEPY', self)
        title.setStyleSheet("color: white; font-size: 48px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        return title

    # Returns single player button
    def create_single_player_button(self):
        single_player_button = QPushButton('Single Player', self)
        single_player_button.setStyleSheet("""
            background-color: green; 
            color: white; 
            border-radius: 105px; 
            font-size: 24px; 
            font-weight: bold;
            width: 210px;
            height: 210px;
            padding: 0;
            text-align: center;
            line-height: 200px;
        """)
        single_player_button.clicked.connect(self.show_SP_screen)
        return single_player_button

    # Returns multiplayer button
    def create_multiplayer_button(self):
        multiplayer_button = QPushButton('Multiplayer', self)
        multiplayer_button.setStyleSheet("""
            background-color: blue; 
            color: white; 
            border-radius: 105px; 
            font-size: 24px; 
            font-weight: bold;
            width: 210px; 
            height: 210px; 
            padding: 0;
            text-align: center;
            line-height: 200px;
        """)
        multiplayer_button.clicked.connect(self.show_MP_screen)
        return multiplayer_button
    
    # Returns settings button
    def create_settings_button(self):
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
    
    # Returns exit button
    def create_exit_button(self):
        exit_button = QPushButton()
        exit_button.setStyleSheet("""
            background-color: white; 
            color: white; 
            border-radius: 0px; 
            font-weight: bold;
            width: 20px; 
            height: 20px; 
            padding: 0;
            text-align: center;
            line-height: 20px;
        """)
        exit_button.clicked.connect(self.exit_app)
        return exit_button

    # Exit application if the exit button is clicked
    def exit_app(self):
        self.app_init.save_settings()
        sys.exit()
    
    # Navigate to single player screen (game_list_screens.py)
    def show_SP_screen(self):
        self.stacked_widget.setCurrentIndex(1)

    # Navigate to multiplayer screen (game_list_screens.py)
    def show_MP_screen(self):
        self.stacked_widget.setCurrentIndex(2)

    # Navigate to settings screen and update parameters
    def show_SETTINGS_screen(self):
        self.app_init.update_settings_screen() 
        self.stacked_widget.setCurrentIndex(3)