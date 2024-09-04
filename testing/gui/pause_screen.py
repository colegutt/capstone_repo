from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout

class PauseScreen(QWidget):
    def __init__(self, stacked_widget, previous_index, app_init):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.previous_index = previous_index
        self.app_init = app_init
        self.create_screen()

    def create_screen(self):
        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout()
        layout.addWidget(self.set_title())
        layout.addStretch()
        layout.addLayout(self.create_buttons_layout())

        self.setLayout(layout)

    def set_title(self):
        title = QLabel('Pause', self)
        title.setStyleSheet("color: white; font-size: 48px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        return title

    def create_buttons_layout(self):
        settings_button = QPushButton('Settings', self)
        settings_button.setStyleSheet("background-color: gray; color: white; font-size: 24px;")
        settings_button.clicked.connect(self.go_to_settings)

        new_game_button = QPushButton('Select a New Game', self)
        new_game_button.setStyleSheet("background-color: gray; color: white; font-size: 24px;")
        new_game_button.clicked.connect(self.select_new_game)

        back_button = QPushButton('Back to Main Menu', self)
        back_button.setStyleSheet("background-color: gray; color: white; font-size: 24px;")
        back_button.clicked.connect(self.go_to_main_menu)

        button_layout = QVBoxLayout()
        button_layout.addWidget(settings_button)
        button_layout.addWidget(new_game_button)
        button_layout.addWidget(back_button)

        return button_layout

    def go_to_settings(self):
        # Set settings_screen's previous_index to 7 (pause screen)
        self.app_init.update_pause_settings_screen() 
        self.stacked_widget.setCurrentIndex(8)

    def select_new_game(self):
        # Example: Navigate to a specific screen for a new game selection
        self.stacked_widget.setCurrentIndex(4)  # Example index for new game selection

    def go_to_main_menu(self):
        self.stacked_widget.setCurrentIndex(0)  # Go to main menu
