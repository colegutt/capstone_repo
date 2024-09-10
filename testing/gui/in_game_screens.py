from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from memory_game import MemoryGame

class GameThread(QThread):
    score_updated = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.memory_game = MemoryGame()

    def run(self):
        def update_score(num_round):
            self.score_updated.emit(num_round)
        
        # Ensure the game is properly running
        self.memory_game.run_game(update_score)
    
    def stop(self):
        if self.memory_game:
            self.memory_game.stop()  # Stop the game if running


class MemoryInGameScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.score = 0
        self.create_screen()
        self.game_thread = None  # Initialize as None
    
    def create_screen(self):
        self.setStyleSheet("background-color: black;")
        self.set_layout(
            self.set_title(),
            self.create_score_label(),
            self.create_pause_button()
        )

    def set_title(self):
        title = QLabel('Memory', self)
        title.setStyleSheet("color: white; font-size: 72px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        return title

    def create_score_label(self):
        self.score_label = QLabel(f'Score: {self.score}', self)
        self.score_label.setStyleSheet("color: white; font-size: 68px; font-weight: bold;")
        self.score_label.setAlignment(Qt.AlignCenter)
        return self.score_label

    def create_pause_button(self):
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
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        top_layout.addWidget(pause_button, alignment=Qt.AlignLeft)
        top_layout.addStretch()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(title)
        main_layout.addStretch()
        main_layout.addWidget(score_label, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        self.setLayout(main_layout)
    
    def start_game(self):
        print('start game called')
        if self.game_thread is None or not self.game_thread.isRunning():
            self.game_thread = GameThread()
            self.game_thread.score_updated.connect(self.update_score_from_game)
            self.game_thread.start()

    def update_score_from_game(self, num_round):
        self.score = num_round
        self.score_label.setText(f'Score: {self.score}')

    def pause_game(self):
        if self.game_thread and self.game_thread.isRunning():
            self.game_thread.memory_game.pause()  # Pause the game
        self.stacked_widget.setCurrentIndex(7)  # Navigate to the pause screen

    def resume_game(self):
        if self.game_thread:
            print('thread exists!')
            self.game_thread.memory_game.resume()  # Resume the game
        else:
            print('thread does not exist!')
            self.start_game()  # Start the game if it's not running

    def reset_game(self):
        self.score = 0
        self.game_thread.stop()
        self.score_label.setText(f'Score: {self.score}')

