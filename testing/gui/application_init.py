from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from main_menu import MainMenu
from rot_main_menu import RotMainMenu
from settings_screen import SettingsScreen
from game_list_screens import SPScreen, MPScreen
from pregame_screens import MemoryPregameScreen, PingPongPregameScreen
from in_game_screens import MemoryInGameScreen
from pause_screen import PauseScreen
from PyQt5.QtCore import QSettings

class ApplicationInit(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('GUI Test')
        self.setStyleSheet("background-color: black;")

        self.stacked_widget = QStackedWidget()

        self.settings = QSettings("BEEPY", "BEEPY_GUI")

        self.brightness_level = self.settings.value("brightness", 50, int)
        self.sound_level = self.settings.value("sound", 50, int)
        self.narration_on = self.settings.value("narration", False, bool)
        
        self.main_menu = MainMenu(self.stacked_widget, self)
        self.sp_screen = SPScreen(self.stacked_widget, self)
        self.mp_screen = MPScreen(self.stacked_widget, self)
        self.settings_screen = SettingsScreen(self.stacked_widget, self, 0)
        self.memory_pregame_screen = MemoryPregameScreen(self.stacked_widget)
        self.ping_pong_pregame_screen = PingPongPregameScreen(self.stacked_widget)
        self.memory_ingame_screen = MemoryInGameScreen(self.stacked_widget)
        self.pause_screen = PauseScreen(self.stacked_widget, 7, self)
        self.pause_settings_screen = SettingsScreen(self.stacked_widget, self, 7)

        # Index   Screen
        #   0     Main Menu
        #   1     Single Player Screen
        #   2     Multiplayer Screen
        #   3     Settings Screen
        #   4     Memory Pregame Screen 
        #   5     Ping Pong Pregame Screen
        #   6     Memory In-Game Screen
        #   7     Pause Screen
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.sp_screen)
        self.stacked_widget.addWidget(self.mp_screen)
        self.stacked_widget.addWidget(self.settings_screen)
        self.stacked_widget.addWidget(self.memory_pregame_screen)
        self.stacked_widget.addWidget(self.ping_pong_pregame_screen)
        self.stacked_widget.addWidget(self.memory_ingame_screen)
        self.stacked_widget.addWidget(self.pause_screen)
        self.stacked_widget.addWidget(self.pause_settings_screen)

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
    
    def update_settings_screen(self):
        # This method is used to ensure the settings screen reflects the current values
        self.settings_screen.update_displayed_values()
    
    def update_pause_settings_screen(self):
        # This method is used to ensure the pause settings screen reflects the current values
        self.pause_settings_screen.update_displayed_values()
    
    def save_settings(self):
        # Save the current settings
        self.settings.setValue("brightness", self.brightness_level)
        self.settings.setValue("sound", self.sound_level)
        self.settings.setValue("narration", self.narration_on)
