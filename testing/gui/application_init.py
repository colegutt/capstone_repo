from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from main_menu import MainMenu
from rot_main_menu import RotMainMenu
from settings_screen import SettingsScreen
from single_player_screen import SPScreen
from pregame_screens import MemoryPregameScreen # Add more classes here

class ApplicationInit(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('GUI Test')
        self.setStyleSheet("background-color: black;")

        self.stacked_widget = QStackedWidget()
        # Index   Screen
        #   0     Main Menu
        #   1     Single Player Screen
        #   2     Settings Screen
        #   3     Memory Pregame Screen 
        self.stacked_widget.addWidget(RotMainMenu(self.stacked_widget))
        self.stacked_widget.addWidget(SPScreen(self.stacked_widget))
        self.stacked_widget.addWidget(SettingsScreen(self.stacked_widget))
        self.stacked_widget.addWidget(MemoryPregameScreen(self.stacked_widget))
        # self.stacked_widget.addWidget(MP_Screen(self.stacked_widget))

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        self.showFullScreen()