from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
from general_functions import GeneralFunctions

class MemoryPregameScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.gen_funcs = GeneralFunctions(self.stacked_widget)
        # Create screen
        self.create_screen()
    
    def create_screen(self):
        self.setStyleSheet("background-color: black;")
        self.set_layout(
            self.set_title(),
            self.set_description(),
            self.create_start_button(),
            self.create_back_button()
        )
    
    def set_title(self):
        title = QLabel('Memory', self)
        title.setStyleSheet("color: white; font-size: 48px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        return title
    
    def set_description(self):
        description = QLabel('This is an example of a description text that describes the game. '
                             'It could talk about how to play, the rules, or what to expect in the game. '
                             'Make sure to pay attention to the instructions. '
                             'Good luck and have fun!', self)
        description.setStyleSheet("color: white; font-size: 18px;")
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)
        return description

    def create_start_button(self):
        start_button = QPushButton('Start', self)
        start_button.setStyleSheet("""
            background-color: blue; 
            color: white; 
            border-radius: 75px;  /* Circular button */
            font-size: 24px; 
            font-weight: bold;
            width: 150px; 
            height: 150px;
        """)
        start_button.clicked.connect(self.go_to_ingame_screen)

        start_layout = QHBoxLayout()
        start_layout.addWidget(start_button)
        start_layout.setAlignment(Qt.AlignCenter)
        start_layout.setContentsMargins(20, 20, 20, 20)

        return start_layout

    def create_back_button(self):
        return self.gen_funcs.create_back_layout(0)

    def set_layout(self, title, description, start_button, back_button):
        final_layout = QVBoxLayout()
        final_layout.addWidget(title)
        final_layout.addSpacing(20)  # Space between title and description
        final_layout.addWidget(description)
        final_layout.addSpacing(40)  # Space between description and start button
        final_layout.addLayout(start_button)
        final_layout.addStretch()  # Push back button to the bottom
        final_layout.addLayout(back_button)

        self.setLayout(final_layout)

    def go_back(self):
        self.stacked_widget.setCurrentIndex(1)
    
    def go_to_ingame_screen(self):
        self.stacked_widget.setCurrentIndex(0)  # Placeholder, adjust as needed