from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from main_menu import MainMenu
from rot_main_menu import RotMainMenu
from settings_screen import SettingsScreen
from game_list_screens import SPScreen, MPScreen
from pregame_screens import MemoryPregameScreen, FastTapPregameScreen
from memory_in_game_screen import MemoryInGameScreen
from fast_tap_in_game_screen import FastTapInGameScreen
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

        # High scores for games
        self.memory_hs = self.settings.value("memory_hs", 0, int)

        
        self.main_menu = MainMenu(self.stacked_widget, self)
        self.sp_screen = SPScreen(self.stacked_widget, self)
        self.mp_screen = MPScreen(self.stacked_widget, self)
        self.settings_screen = SettingsScreen(self.stacked_widget, self, 0)
        self.memory_pregame_screen = MemoryPregameScreen(self.stacked_widget, self)
        self.fast_tap_pregame_screen = FastTapPregameScreen(self.stacked_widget, self)
        self.memory_ingame_screen = MemoryInGameScreen(self.stacked_widget, self)
        self.memory_pause_screen = PauseScreen(self.stacked_widget, 7, 5, self)
        self.memory_pause_settings_screen = SettingsScreen(self.stacked_widget, self, 6)
        self.fast_tap_ingame_screen = FastTapInGameScreen(self.stacked_widget, self)
        self.fast_tap_pause_screen = PauseScreen(self.stacked_widget, 11, 9, self)
        self.fast_tap_pause_settings_screen = SettingsScreen(self.stacked_widget, self, 10)

        # Index   Screen
        #   0     Main Menu
        #   1     Single Player Screen
        #   2     Multiplayer Screen
        #   3     Settings Screen
        #   4     Memory Pregame Screen 
        #   5     Memory In-Game Screen
        #   6     Memory Pause Screen
        #   7     Memory Pause Settings Screen
        #   8     Fast Tap Pregame Screen
        #   9     Fast Tap In-Game Screen
        #  10     Fast Tap Pause Screen
        #  11     Fast Tap Pause Settings Screen
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.sp_screen)
        self.stacked_widget.addWidget(self.mp_screen)
        self.stacked_widget.addWidget(self.settings_screen)
        self.stacked_widget.addWidget(self.memory_pregame_screen)
        self.stacked_widget.addWidget(self.memory_ingame_screen)
        self.stacked_widget.addWidget(self.memory_pause_screen)
        self.stacked_widget.addWidget(self.memory_pause_settings_screen)
        self.stacked_widget.addWidget(self.fast_tap_pregame_screen)
        self.stacked_widget.addWidget(self.fast_tap_ingame_screen)
        self.stacked_widget.addWidget(self.fast_tap_pause_screen)
        self.stacked_widget.addWidget(self.fast_tap_pause_settings_screen)

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
    
    def update_pause_settings_screen(self, index):
        # This method is used to ensure the pause settings screen reflects the current values
        if index == 5:
            self.memory_pause_settings_screen.update_displayed_values()
        elif index == 9:
            self.fast_tap_pause_settings_screen.update_displayed_values()
    
    def save_settings(self):
        # Save the current settings
        self.settings.setValue("brightness", self.brightness_level)
        self.settings.setValue("sound", self.sound_level)
        self.settings.setValue("narration", self.narration_on)
    
    def save_memory_high_score(self):
        # Save the current settings
        self.settings.setValue("memory_hs", self.memory_hs)
