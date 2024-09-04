import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

class MemoryInGameScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.score = 0
        self.create_screen()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_score)
        self.resuming = False  # To track if the game is resuming
    
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
        title.setStyleSheet("color: white; font-size: 72px; font-weight: bold;")

        # Title alignment
        title.setAlignment(Qt.AlignCenter)

        return title

    def create_score_label(self):
        # Score label
        self.score_label = QLabel(f'Score: {self.score}', self)

        # Score characteristics
        self.score_label.setStyleSheet("color: white; font-size: 68px; font-weight: bold;")

        # Score alignment
        self.score_label.setAlignment(Qt.AlignCenter)

        return self.score_label

    def create_pause_button(self):
        # Pause button
        pause_button = QPushButton('Pause', self)
        pause_button.setStyleSheet("""
            background-color: orange; 
            color: white; 
            border-radius: 50px; 
            font-size: 26px; 
            font-weight: bold;
            width: 100px;
            height: 100px;
            padding: 0;
            text-align: center;
            line-height: 100px;
        """)
        pause_button.clicked.connect(self.pause_game)
        return pause_button

    def set_layout(self, title, score_label, pause_button):
        # Main layout
        main_layout = QVBoxLayout()
        
        # Top layout for the pause button
        top_layout = QHBoxLayout()
        top_layout.addWidget(pause_button, alignment=Qt.AlignLeft)
        top_layout.addStretch()  # Add stretch to push the pause button to the left

        main_layout.addLayout(top_layout)  # Add top layout to main layout
        main_layout.addWidget(title)  # Add title below the top layout
        main_layout.addStretch()  # Add space between title and score
        main_layout.addWidget(score_label, alignment=Qt.AlignCenter)  # Add centered score label
        main_layout.addStretch()  # Add space below score label

        self.setLayout(main_layout)  # Set the final layout for the in-game screen
    
    def start_score_timer(self):
        # Start the score timer to update score every 5 seconds
        self.timer.start(5000)  # 5000 milliseconds = 5 seconds
    
    def stop_score_timer(self):
        # Stop the score timer
        self.timer.stop()

    def update_score(self):
        # Increment score by 1
        self.score += 1
        self.score_label.setText(f'Score: {self.score}')

    def pause_game(self):
        self.stop_score_timer()
        self.stacked_widget.setCurrentIndex(7)
    
    def resume_game(self):
        self.start_score_timer()
        self.resuming = True

    def reset_game(self):
        self.score = 0
        self.score_label.setText(f'Score: {self.score}')
        self.resuming = False
        self.start_score_timer()  # Start the timer when the game starts
