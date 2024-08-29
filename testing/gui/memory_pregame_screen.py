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
            self.set_description_layout(),
            self.create_start_button(),
            self.create_back_button()
        )
    
    def set_title(self):
        title = QLabel('Memory', self)
        title.setStyleSheet("color: white; font-size: 48px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        return title
    
    def set_description_layout(self):
        description_str = (
            "Match the sequence by pressing the buttons that light up. "
            "The sequence will get longer the better you do. How many "
            "can you get? Good luck!"
        )

        description = QLabel(description_str, self)
        description.setStyleSheet("color: white; font-size: 24px;")
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)
        description_layout = QVBoxLayout()
        description_layout.addStretch()
        description_layout.addWidget(description)
        description_layout.addStretch()
        return description_layout

    def create_start_button(self):
        start_button = QPushButton('Start', self)
        start_button.setStyleSheet("""
            background-color: blue; 
            color: white; 
            border-radius: 75px; 
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

    def set_layout(self, title, description_layout, start_button, back_button):
        final_layout = QVBoxLayout()
        final_layout.addWidget(title)
        final_layout.addSpacing(20)  # Space between title and description
        final_layout.addLayout(description_layout)
        final_layout.addSpacing(40)  # Space between description and start button
        final_layout.addLayout(start_button)
        final_layout.addStretch()  # Push back button to the bottom
        final_layout.addLayout(back_button)

        self.setLayout(final_layout)

    def go_back(self):
        self.stacked_widget.setCurrentIndex(1)
    
    def go_to_ingame_screen(self):
        self.stacked_widget.setCurrentIndex(0)  # Placeholder, adjust as needed