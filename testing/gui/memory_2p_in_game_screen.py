from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from memory_game import MemoryGame
from general_functions import GeneralFunctions

# Thread that runs the game simultaneously
class GameThread(QThread):
    # Signals that allow screen parameters to change in real time
    score_updated = pyqtSignal(int)
    game_over = pyqtSignal()
    player_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.memory_game = MemoryGame(True)
    # Function that runs when the thread starts
    def run(self):

        # Update score on screen when signaled
        def update_score(num_round):
            self.score_updated.emit(num_round)
        
        # Update player number when signaled
        def update_player(player_num):
            self.player_changed.emit(player_num)
        
        # Show game over layout when signaled
        def on_game_over():
            self.game_over.emit()

        # Run Memory 2P Game
        self.memory_game.run_game(update_score, on_game_over, update_player)
    
    # Stops the Memory 2P Game
    def stop(self):
        if self.memory_game:
            self.memory_game.stop()

class Memory2PInGameScreen(QWidget):
    def __init__(self, stacked_widget, app_init):
        # Intializations
        super().__init__()
        self.stacked_widget = stacked_widget
        self.score = 0
        self.app_init = app_init
        self.gen_funcs = GeneralFunctions(
            self.stacked_widget, self.score, self.reset_game, self.start_game, self.pause_game, True
        )
        # Create labels and buttons that are used in set_layout
        self.title = self.gen_funcs.set_title('Memory 2 Player')
        self.turn_label = QLabel("Player 1's Turn", self)
        self.turn_label.setStyleSheet("color: blue; font-size: 50px; font-weight: bold;")
        self.score_label = self.gen_funcs.create_score_label()
        self.game_over_label = self.gen_funcs.create_game_over_label()
        self.pause_button = self.gen_funcs.create_pause_button()
        self.play_again_button = self.gen_funcs.create_play_again_button()
        self.go_back_button = self.gen_funcs.create_go_back_button()
        self.create_screen()
        self.game_thread = None

    # Create in-game screen
    def create_screen(self):
        self.setStyleSheet("background-color: black;")
        self.set_layout()
        self.gen_funcs.hide_or_show_end_game_buttons(self.game_over_label, self.play_again_button, self.go_back_button, False)

    # Use previously created buttons and labels and arrange them in the screen
    def set_layout(self):
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.pause_button, alignment=Qt.AlignLeft)
        top_layout.addStretch()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.title)
        main_layout.addStretch()
        main_layout.addWidget(self.score_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.turn_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.game_over_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.play_again_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.go_back_button, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        self.setLayout(main_layout)

    def start_game(self):
        if self.game_thread is None or not self.game_thread.isRunning():
            self.game_thread = GameThread()
            self.game_thread.score_updated.connect(self.update_score_from_game)
            self.game_thread.player_changed.connect(self.update_player_label)
            self.game_thread.game_over.connect(self.end_game)
            self.game_thread.start()
        self.game_over_label.setVisible(False)
        self.turn_label.setVisible(True)
    
    def save_high_score(self):
        if self.app_init.memory_2p_hs < self.score:
            self.app_init.memory_2p_hs = self.score
            self.app_init.mp_screen.update_displayed_values()
            self.app_init.save_memory_2p_high_score()

    def update_score_from_game(self, num_round):
        self.score = num_round
        self.score_label.setText(f'Score: {self.score}')

    def update_player_label(self, player_num):
        if player_num == 1:
            self.turn_label.setText("Player 1's Turn")
            self.turn_label.setStyleSheet("color: blue; font-size: 50px; font-weight: bold;")
        else:
            self.turn_label.setText("Player 2's Turn")
            self.turn_label.setStyleSheet("color: red; font-size: 50px; font-weight: bold;")

    def pause_game(self):
        if self.game_thread and self.game_thread.isRunning():
            self.game_thread.memory_game.pause()
        self.stacked_widget.setCurrentIndex(14)

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
        self.turn_label.setVisible(False)

    def reset_game(self):
        self.end_game()
        self.save_high_score()
        self.score = 0
        self.score_label.setText(f'Score: {self.score}')
        self.update_player_label(1)
        self.gen_funcs.hide_or_show_end_game_buttons(self.game_over_label, self.play_again_button, self.go_back_button, False)
