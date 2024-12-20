from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
from general_functions import GeneralFunctions

class PauseScreen(QWidget):
    def __init__(self, stacked_widget, pause_settings_screen_index, previous_index, app_init):
        # Intializations
        super().__init__()
        self.stacked_widget = stacked_widget
        self.previous_index = previous_index
        self.pause_settings_screen = pause_settings_screen_index
        self.gen_funcs = GeneralFunctions(self.stacked_widget)
        self.app_init = app_init
        self.create_screen()

    # Create pause screen
    def create_screen(self):
        self.setStyleSheet("background-color: black;")
        layout = QVBoxLayout()
        layout.addWidget(self.set_title())
        layout.addStretch()
        layout.addLayout(self.create_buttons_layout())
        layout.addStretch()
        layout.addLayout(self.create_resume_layout())
        self.setLayout(layout)

    # Return resume button layout
    def create_resume_layout(self):
        resume_button = QPushButton('Resume', self)
        resume_button.setStyleSheet("""
            background-color: green; 
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
        resume_button.clicked.connect(self.resume_game)
        resume_layout = QHBoxLayout()
        resume_layout.addWidget(resume_button)
        resume_layout.addStretch()
        resume_layout.setContentsMargins(20, 20, 20, 20)
        return resume_layout

    # Resume game depending on the previous index
    def resume_game(self):
        try:
            if self.previous_index == 5:
                self.app_init.memory_ingame_screen.resume_game()
            elif self.previous_index == 9:
                self.app_init.fast_tap_ingame_screen.resume_game()
            elif self.previous_index == 13:
                self.app_init.memory_mult_ingame_screen.resume_game()
            elif self.previous_index == 17:
                self.app_init.tennis_ingame_screen.resume_game()

            self.stacked_widget.setCurrentIndex(self.previous_index)
        except:
            self.stacked_widget.setCurrentIndex(20) 

    # Return pause screen title label
    def set_title(self):
        title = QLabel('Pause', self)
        title.setStyleSheet("color: white; font-size: 40px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        return title

    # Create button layout
    def create_buttons_layout(self):
        settings_button = self.create_button('Settings')
        settings_button.clicked.connect(self.go_to_settings)

        new_game_button = self.create_button('Select a New Game')
        new_game_button.clicked.connect(self.select_new_game)

        main_menu_button = self.create_button('Back to Main Menu')
        main_menu_button.clicked.connect(self.go_to_main_menu)

        button_layout = QVBoxLayout()
        button_layout.addWidget(settings_button)
        button_layout.addSpacing(20)
        button_layout.addWidget(new_game_button)
        button_layout.addSpacing(20)
        button_layout.addWidget(main_menu_button)
        return button_layout

    # General function for the buttons since they all have the same appearance
    def create_button(self, name):
        button = QPushButton(name, self)
        button.setStyleSheet(f'''
            background-color: gray;
            color: white; 
            border-radius: 10px; 
            width: 300px; 
            height: 300px; 
            font-size: 20px; 
            font-weight: bold;
            height: 75px;
        ''')
        return button

    # Navigate to pause settings screen
    def go_to_settings(self):
        try:
            self.app_init.update_pause_settings_screen(self.previous_index) 
            self.stacked_widget.setCurrentIndex(self.pause_settings_screen)
        except Exception as e:
            print(e)
            self.stacked_widget.setCurrentIndex(20) 

    # Navigate to corresponding game list screen and reset current game
    def select_new_game(self):
        try:
            index = self.reset_specific_game()
            self.stacked_widget.setCurrentIndex(index) 
        except Exception as e:
            print(e)
            self.stacked_widget.setCurrentIndex(20) 

    # Navigate to main menu and reset current game
    def go_to_main_menu(self):
        try:
            self.reset_specific_game()
            self.stacked_widget.setCurrentIndex(0)
        except Exception as e:
            print(e)
            self.stacked_widget.setCurrentIndex(20) 
    
    # Reset specific game
    def reset_specific_game(self):
        index = 1
        if self.previous_index == 5:
            self.app_init.memory_ingame_screen.reset_game() 
        elif self.previous_index == 9:
            self.app_init.fast_tap_ingame_screen.reset_game() 
        elif self.previous_index == 13:
            self.app_init.memory_mult_ingame_screen.reset_game() 
            index = 2
        elif self.previous_index == 17:
            self.app_init.tennis_ingame_screen.reset_game() 
            index = 2
            
        return index
