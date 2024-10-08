from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from main_menu import MainMenu
from settings_screen import SettingsScreen
from game_list_screens import SPScreen, MPScreen
from pregame_screens import MemoryPregameScreen, FastTapPregameScreen, MemoryMultPregameScreen, TennisPregameScreen
from memory_in_game_screen import MemoryInGameScreen
from fast_tap_in_game_screen import FastTapInGameScreen
from memory_mult_in_game_screen import MemoryMultInGameScreen
from pause_screen import PauseScreen
from PyQt5.QtCore import QSettings

class ApplicationInit(QWidget):
    def __init__(self):
        # Initialize the application
        super().__init__()
        self.setWindowTitle('GUI Test')
        self.setStyleSheet("background-color: black;")
        self.stacked_widget = QStackedWidget()
        self.settings = QSettings("BEEPY", "BEEPY_GUI")

        # Set default settings if we cannot load the previous settings
        self.brightness_level = self.settings.value("brightness", 50, int)
        self.sound_level = self.settings.value("sound", 50, int)
        self.narration_on = self.settings.value("narration", False, bool)

        # High scores for games
        self.memory_hs = self.settings.value("memory_hs", 0, int)
        self.fast_tap_hs = self.settings.value("fast_tap_hs", 0, int)
        self.memory_mult_hs = self.settings.value("memory_mult_hs", 0, int)

        # Intialize the screens
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
        self.memory_mult_pregame_screen = MemoryMultPregameScreen(self.stacked_widget, self)
        self.memory_mult_ingame_screen = MemoryMultInGameScreen(self.stacked_widget, self)
        self.memory_mult_pause_screen = PauseScreen(self.stacked_widget, 15, 13, self)
        self.memory_mult_pause_settings_screen = SettingsScreen(self.stacked_widget, self, 14)
        self.tennis_pregame_screen = TennisPregameScreen(self.stacked_widget, self)

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
        #  12     Memory 2P Pregame Screen
        #  13     Memory 2P In-Game Screen
        #  14     Memory 2P Pause Screen
        #  15     Memory Pause Settings Screen
        #  16     Tennis Pregame Screen
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
        self.stacked_widget.addWidget(self.memory_mult_pregame_screen)
        self.stacked_widget.addWidget(self.memory_mult_ingame_screen)
        self.stacked_widget.addWidget(self.memory_mult_pause_screen)
        self.stacked_widget.addWidget(self.memory_mult_pause_settings_screen)
        self.stacked_widget.addWidget(self.tennis_pregame_screen)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        self.showFullScreen()
    
    # Returns the sound level in the settings
    def get_sound_level(self):
        return self.sound_level
    
    # Returns the brightness level in the settings
    def get_brightness_level(self):
        return self.brightness_level
    
    # Returns the bool if narration is on or off in the settings
    def get_narration_bool(self):
        return self.narration_on
    
    # Function to update the displayed settings when the screen is accessed
    def update_settings_screen(self):
        self.settings_screen.update_displayed_values()
    
    # Function to update the displayed settings when the respective pause settings screens are accessed
    def update_pause_settings_screen(self, index):
        if index == 5:
            self.memory_pause_settings_screen.update_displayed_values()
        elif index == 9:
            self.fast_tap_pause_settings_screen.update_displayed_values()
    
    # Save current settings
    def save_settings(self):
        self.settings.setValue("brightness", self.brightness_level)
        self.settings.setValue("sound", self.sound_level)
        self.settings.setValue("narration", self.narration_on)
    
    # Save high score for memory
    def save_memory_high_score(self):
        self.settings.setValue("memory_hs", self.memory_hs)
    
    # Save high score for fast tap
    def save_fast_tap_high_score(self):
        self.settings.setValue("fast_tap_hs", self.fast_tap_hs)
    
    # Save high score for memory 2p
    def save_memory_mult_high_score(self):
        self.settings.setValue("memory_mult_hs", self.memory_mult_hs)

