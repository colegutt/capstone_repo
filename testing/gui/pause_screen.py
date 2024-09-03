from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
from general_functions import GeneralFunctions

class PauseScreen(QWidget):
    def __init__(self, stacked_widget, game_index=1):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.game_index = game_index
        self.gen_funcs = GeneralFunctions(self.stacked_widget)

        self.create_screen()

    def create_screen(self):
        self.setStyleSheet("background-color: black;")

        # Create title
        title = QLabel('Pause', self)
        title.setStyleSheet("color: white; font-size: 48px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        # Create buttons
        settings_button = self.create_button("Settings", 3)
        new_game_button = self.create_button("Select a New Game", self.game_index)
        main_menu_button = self.create_button("Back to Main Menu", 0)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(settings_button)
        layout.addWidget(new_game_button)
        layout.addWidget(main_menu_button)
        layout.addStretch()

        # Add back button at the bottom right
        back_button_layout = self.gen_funcs.create_back_layout(6)
        layout.addLayout(back_button_layout)

        self.setLayout(layout)

    def create_button(self, text, index):
        button = QPushButton(text, self)
        button.setStyleSheet("""
            background-color: gray; 
            color: white; 
            font-size: 24px; 
            font-weight: bold;
            height: 50px;
        """)
        button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(index))
        return button

if __name__ == '__main__':
    app = QApplication([])
    stacked_widget = None  # Replace with actual QStackedWidget instance
    pause_screen = PauseScreen(stacked_widget)
    pause_screen.show()
    sys.exit(app.exec_())
