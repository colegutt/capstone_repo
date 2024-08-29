from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from main_menu import MainMenu
from settings_screen import SettingsScreen
from gpt_single_player_screen import SPScreen

class ApplicationInit(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('GUI Test')
        self.setStyleSheet("background-color: black;")

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(MainMenu(self.stacked_widget))
        self.stacked_widget.addWidget(SPScreen(self.stacked_widget))
        # self.stacked_widget.addWidget(MP_Screen(self.stacked_widget))
        self.stacked_widget.addWidget(SettingsScreen(self.stacked_widget))

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        self.showFullScreen()