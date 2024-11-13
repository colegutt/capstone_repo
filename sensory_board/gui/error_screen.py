from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout

class ErrorScreen(QWidget):
    def __init__(self, stacked_widget, app_init):
        # Initializations
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_init = app_init

        # Create labels and buttons used in the error screen
        self.title = self.set_title()
        self.error_message = self.set_error_message()
        self.return_button = self.create_return_button()

        self.create_screen()

    def create_screen(self):
        self.setStyleSheet("background-color: black;")
        
        # Layout for the screen
        title_layout = QVBoxLayout()
        title_layout.addWidget(self.title, alignment=Qt.AlignCenter)
        title_layout.addSpacing(20)
        title_layout.addWidget(self.error_message, alignment=Qt.AlignCenter)

        button_layout = QVBoxLayout()  # Changed to QVBoxLayout for vertical centering
        button_layout.addWidget(self.return_button, alignment=Qt.AlignCenter)  # Align the button to center

        main_layout = QVBoxLayout()
        main_layout.addLayout(title_layout)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def set_title(self):
        title = QLabel('Error', self)
        title.setStyleSheet("color: red; font-size: 48px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        return title

    def set_error_message(self):
        message = QLabel("Sorry, an error has occurred.", self)
        message.setStyleSheet("color: white; font-size: 24px;")
        message.setAlignment(Qt.AlignCenter)
        return message

    def create_return_button(self):
        return_button = QPushButton('Main Menu', self)
        return_button.setStyleSheet("""
            background-color: green; 
            color: white; 
            border-radius: 105px;  
            font-size: 24px; 
            font-weight: bold;
            width: 210px; 
            height: 210px;
            padding: 0;
            text-align: center;
            line-height: 210px;
        """)
        return_button.clicked.connect(self.return_to_main_menu)
        return return_button

    def return_to_main_menu(self):
        self.stacked_widget.setCurrentIndex(0)