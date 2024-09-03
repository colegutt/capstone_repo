import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

class MemoryInGameScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.score = 0
        self.create_screen()
        self.start_score_timer()
    
    def create_screen(self):
        # Make background black
        self.setStyleSheet("background-color: black;")

        # Set title, score label, and pause button
        self.set_layout(
            self.set_title(),
            self.create_score_label(),
            self.create_pause_button()
        )

    def set_title(self):
        # Title name
        title = QLabel('Memory', self)

        # Title characteristics
        title.setStyleSheet("color: white; font-size: 48px; font-weight: bold;")

        # Title alignment
        title.setAlignment(Qt.AlignCenter)

        return title

    def create_score_label(self):
        # Score label
        self.score_label = QLabel(f'Score: {self.score}', self)

        # Score characteristics
        self.score_label.setStyleSheet("color: white; font-size: 32px; font-weight: bold;")

        # Score alignment
        self.score_label.setAlignment(Qt.AlignCenter)

        return self.score_label

    def create_pause_button(self):
        # Pause button
        pause_button = QPushButton('Pause', self)
        pause_button.setStyleSheet("""
            background-color: orange; 
            color: white; 
            border-radius: 120px; 
            font-size: 26px; 
            font-weight: bold;
            width: 240px;
            height: 240px;
            padding: 0;
            text-align: center;
            line-height: 240px;
        """)
        pause_button.clicked.connect(self.show_pause_screen)
        return pause_button

    def set_layout(self, title, score_label, pause_button):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(title)  # Add title at the top
        main_layout.addStretch()  # Add space between title and score
        main_layout.addWidget(score_label)  # Add score label
        main_layout.addStretch()  # Add space between score and pause button
        main_layout.addWidget(pause_button, alignment=Qt.AlignCenter)  # Add pause button
        main_layout.addStretch()  # Add space below pause button
        self.setLayout(main_layout)  # Set the final layout for the in-game screen
    
    def start_score_timer(self):
        # Timer to update score every 5 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_score)
        self.timer.start(5000)  # 5000 milliseconds = 5 seconds
    
    def update_score(self):
        # Increment score by 1
        self.score += 1
        self.score_label.setText(f'Score: {self.score}')

    def show_pause_screen(self):
        self.stacked_widget.setCurrentIndex(7)

    def showEvent(self, event):
        # Reset the score when the screen is shown
        self.score = 0
        self.score_label.setText(f'Score: {self.score}')
        super().showEvent(event)
