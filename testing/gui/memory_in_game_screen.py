from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from memory_game import MemoryGame
from general_functions import GeneralFunctions

class GameThread(QThread):
    score_updated = pyqtSignal(int)
    game_over = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.memory_game = MemoryGame()

    def run(self):
        def update_score(num_round):
            self.score_updated.emit(num_round)
        
        def on_game_over():
            self.game_over.emit()
        
        self.memory_game.run_game(update_score, on_game_over)
    
    def stop(self):
        if self.memory_game:
            self.memory_game.stop()


class MemoryInGameScreen(QWidget):
    def __init__(self, stacked_widget, app_init):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.score = 0
        self.app_init = app_init
        self.gen_funcs = GeneralFunctions(
            self.stacked_widget, self.score, self.reset_game, self.start_game, self.pause_game
        )
        self.title = self.gen_funcs.set_title('Memory')
        self.game_over_label = self.gen_funcs.create_game_over_label()
        self.score_label = self.gen_funcs.create_score_label()
        self.pause_button = self.gen_funcs.create_pause_button()
        self.play_again_button = self.gen_funcs.create_play_again_button()
        self.go_back_button = self.gen_funcs.create_go_back_button()
        self.create_screen()
        self.game_thread = None
    
    def create_screen(self):
        self.setStyleSheet("background-color: black;")
        self.set_layout()
        self.gen_funcs.hide_or_show_end_game_buttons(self.game_over_label, self.play_again_button, self.go_back_button, False)

    def set_layout(self):
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.pause_button, alignment=Qt.AlignLeft)
        top_layout.addStretch()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.title)
        main_layout.addStretch()
        main_layout.addWidget(self.score_label, alignment=Qt.AlignCenter)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.game_over_label, alignment=Qt.AlignCenter)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.play_again_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.go_back_button, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        self.setLayout(main_layout)
    
    def start_game(self):
        if self.game_thread is None or not self.game_thread.isRunning():
            self.game_thread = GameThread()
            self.game_thread.score_updated.connect(self.update_score_from_game)
            self.game_thread.game_over.connect(self.end_game) 
            self.game_thread.start()
        self.game_over_label.setVisible(False)
    
    def update_score_from_game(self, num_round):
        self.score = num_round
        self.score_label.setText(f'Score: {self.score}')
    
    def pause_game(self):
        if self.game_thread and self.game_thread.isRunning():
            self.game_thread.memory_game.pause()
        self.stacked_widget.setCurrentIndex(6)

    def resume_game(self):
        if self.game_thread:
            self.game_thread.memory_game.resume()
        else:
            self.start_game()
    
    def end_game(self):
        if self.game_thread and self.game_thread.isRunning():
            self.game_thread.memory_game.stop() 
            self.game_thread.quit()
            self.game_thread.wait()
        self.gen_funcs.hide_or_show_end_game_buttons(self.game_over_label, self.play_again_button, self.go_back_button, True)
    
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
        self.gen_funcs.hide_or_show_end_game_buttons(self.game_over_label, self.play_again_button, self.go_back_button, False)
