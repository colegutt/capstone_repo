from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from gui.main_menu import MainMenu
from gui.settings_screen import SettingsScreen
from gui.game_list_screens import SPScreen, MPScreen
from gui.pregame_screens import MemoryPregameScreen, FastTapPregameScreen, MemoryMultPregameScreen, TennisPregameScreen
from gui.memory_in_game_screen import MemoryInGameScreen
from gui.fast_tap_in_game_screen import FastTapInGameScreen
from gui.memory_mult_in_game_screen import MemoryMultInGameScreen
from gui.tennis_in_game_screen import TennisInGameScreen
from gui.pause_screen import PauseScreen
from PyQt5.QtCore import QSettings
import pygame

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

        # Sound initialization
        pygame.mixer.init()
        self.beep_sounds = {
            'star': pygame.mixer.Sound("sounds/beep_1.wav"),
            'square': pygame.mixer.Sound("sounds/beep_2.wav"),
            'circle': pygame.mixer.Sound("sounds/beep_3.wav"),
            'heart': pygame.mixer.Sound("sounds/beep_4.wav"),
            'triangle': pygame.mixer.Sound("sounds/beep_5.wav"),
            'cloud': pygame.mixer.Sound("sounds/beep_6.wav"),
        }
        self.narration_sounds = {
            'star': pygame.mixer.Sound("sounds/yellow_star.wav"),
            'square': pygame.mixer.Sound("sounds/green_square.wav"),
            'circle': pygame.mixer.Sound("sounds/orange_circle.wav"),
            'heart': pygame.mixer.Sound("sounds/red_heart.wav"),
            'triangle': pygame.mixer.Sound("sounds/purple_triangle.wav"),
            'cloud': pygame.mixer.Sound("sounds/blue_cloud.wav"),
        }
        self.other_sounds = {
            'memory correct sequence': pygame.mixer.Sound("sounds/memory_correct_sequence.wav"),
            'fast tap wrong led': pygame.mixer.Sound("sounds/fast_tap_wrong_led.wav"),
            'game over': pygame.mixer.Sound("sounds/game_over.wav"),
        }

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
        self.tennis_ingame_screen = TennisInGameScreen(self.stacked_widget, self)
        self.tennis_pause_screen = PauseScreen(self.stacked_widget, 19, 17, self)
        self.tennis_pause_settings_screen = SettingsScreen(self.stacked_widget, self, 18)

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
        #  12     Memory Multiplayer Pregame Screen
        #  13     Memory Multiplayer In-Game Screen
        #  14     Memory Multiplayer Pause Screen
        #  15     Memory Pause Settings Screen
        #  16     Tennis Pregame Screen
        #  17     Tennis In-Game Screen
        #  18     Tennis Pause Menu
        #  19     Tennis Pause Settings Screen
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
        self.stacked_widget.addWidget(self.tennis_ingame_screen)
        self.stacked_widget.addWidget(self.tennis_pause_screen)
        self.stacked_widget.addWidget(self.tennis_pause_settings_screen)

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

