from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from memory_game import MemoryGame

class GameThread(QThread):
    score_updated = pyqtSignal(int)
    game_over = pyqtSignal()  # Add a signal for game over

    def __init__(self):
        super().__init__()
        self.memory_game = MemoryGame()

    def run(self):
        def update_score(num_round):
            self.score_updated.emit(num_round)
        
        def on_game_over():
            self.game_over.emit()  # Emit the game over signal
        
        self.memory_game.run_game(update_score, on_game_over)
    
    def stop(self):
        if self.memory_game:
            self.memory_game.stop()  # Stop the game if running


class MemoryInGameScreen(QWidget):
    def __init__(self, stacked_widget, app_init):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.score = 0
        self.app_init = app_init
        self.create_screen()
        self.game_thread = None  # Initialize as None
    
    def create_screen(self):
        self.setStyleSheet("background-color: black;")
        self.set_layout(
            self.set_title(),
            self.create_score_label(),
            self.create_pause_button(),
            self.create_game_over_label(),
            self.create_play_again_button(),
            self.create_go_back_button()
        )
        self.hide_end_game_buttons()  # Initially hide the end game buttons

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

    def create_game_over_label(self):
        self.game_over_label = QLabel(f'GAME OVER!', self)
        self.game_over_label.setStyleSheet("color: red; font-size: 40px; font-weight: bold;")
        self.game_over_label.setAlignment(Qt.AlignCenter)
        self.game_over_label.setVisible(False)  # Initially hidden
        return self.game_over_label

    def create_play_again_button(self):
        self.play_again_button = QPushButton('Play Again', self)
        self.play_again_button.setStyleSheet("""
            background-color: green; 
            color: white; 
            border-radius: 10px; 
            font-size: 24px; 
            font-weight: bold;
            width: 300px;
            height: 75px;
        """)
        self.play_again_button.clicked.connect(self.reset_game)
        self.play_again_button.setVisible(False)
        return self.play_again_button

    def create_go_back_button(self):
        self.go_back_button = QPushButton('Go Back', self)
        self.go_back_button.setStyleSheet("""
            background-color: red; 
            color: white; 
            border-radius: 10px; 
            font-size: 24px; 
            font-weight: bold;
            width: 300px;
            height: 75px;
        """)
        self.go_back_button.clicked.connect(self.select_new_game)
        self.go_back_button.setVisible(False)  # Initially hidden
        return self.go_back_button

    def set_layout(self, title, score_label, pause_button, game_over_label, play_again_button, go_back_button):
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        top_layout.addWidget(pause_button, alignment=Qt.AlignLeft)
        top_layout.addStretch()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(title)
        main_layout.addStretch()
        main_layout.addWidget(score_label, alignment=Qt.AlignCenter)
        main_layout.addSpacing(10)
        main_layout.addWidget(game_over_label, alignment=Qt.AlignCenter)
        main_layout.addSpacing(10)
        main_layout.addWidget(play_again_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(go_back_button, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        self.setLayout(main_layout)
    
    def start_game(self):
        if self.game_thread is None or not self.game_thread.isRunning():
            self.game_thread = GameThread()
            self.game_thread.score_updated.connect(self.update_score_from_game)
            self.game_thread.game_over.connect(self.show_end_game_buttons)  # Connect game over signal
            self.game_thread.start()
        self.game_over_label.setVisible(False)  # Hide the label when the game starts

    def show_end_game_buttons(self):
        self.game_over_label.setVisible(True) 
        self.play_again_button.setVisible(True) 
        self.go_back_button.setVisible(True)  
    
    def update_score_from_game(self, num_round):
        self.score = num_round
        self.score_label.setText(f'Score: {self.score}')
    
    def pause_game(self):
        if self.game_thread and self.game_thread.isRunning():
            self.game_thread.memory_game.pause()  # Pause the game
        self.stacked_widget.setCurrentIndex(7)  # Navigate to the pause screen

    def resume_game(self):
        if self.game_thread:
            self.game_thread.memory_game.resume()  # Resume the game
        else:
            self.start_game()  # Start the game if it's not running
    
    def end_game(self):
        if self.game_thread and self.game_thread.isRunning():
            self.game_thread.memory_game.stop() 
            self.game_thread.quit()
            self.game_thread.wait()
        self.show_end_game_buttons()  # Ensure end game buttons are shown
    
    def save_high_score(self):
        if self.app_init.memory_hs < self.score:
            self.app_init.memory_hs = self.score
            self.app_init.sp_screen.update_displayed_values()
            self.app_init.save_memory_high_score()

    def reset_game(self):
        self.end_game()
        self.save_high_score()
        self.score = 0
        self.score_label.setText(f'Score: {self.score}')
        self.hide_end_game_buttons()
        self.start_game()
    
    def select_new_game(self):
        self.stacked_widget.setCurrentIndex(1)

    def hide_end_game_buttons(self):
        self.game_over_label.setVisible(False)
        self.play_again_button.setVisible(False)
        self.go_back_button.setVisible(False)
