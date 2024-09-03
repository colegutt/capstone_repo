from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from main_menu import MainMenu
from rot_main_menu import RotMainMenu
from settings_screen import SettingsScreen
from game_list_screens import SPScreen, MPScreen
from pregame_screens import MemoryPregameScreen, PingPongPregameScreen # Add more classes here
from in_game_screens import MemoryInGameScreen
from pause_screen import PauseScreen

class ApplicationInit(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('GUI Test')
        self.setStyleSheet("background-color: black;")

        self.stacked_widget = QStackedWidget()
        
        self.sound_level = 50
        self.brightness_level = 50
        self.narration_on = False

        # Index   Screen
        #   0     Main Menu
        #   1     Single Player Screen
        #   2     Multiplayer Screen
        #   3     Settings Screen
        #   4     Memory Pregame Screen 
        #   5     Ping Pong Pregame Screen
        #   6     Memory In-Game Screen
        #   7     Pause Screen
        self.stacked_widget.addWidget(MainMenu(self.stacked_widget))
        self.stacked_widget.addWidget(SPScreen(self.stacked_widget))
        self.stacked_widget.addWidget(MPScreen(self.stacked_widget))
        self.stacked_widget.addWidget(SettingsScreen(self.stacked_widget, self))
        self.stacked_widget.addWidget(MemoryPregameScreen(self.stacked_widget))
        self.stacked_widget.addWidget(PingPongPregameScreen(self.stacked_widget))
        self.stacked_widget.addWidget(MemoryInGameScreen(self.stacked_widget))
        self.stacked_widget.addWidget(PauseScreen(self.stacked_widget))



        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        self.showFullScreen()
    
    def get_sound_level(self):
        return self.sound_level
    
    def get_brightness_level(self):
        return self.brightness_level
    
    def get_narration_bool(self):
        return self.narration_on