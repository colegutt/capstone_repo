from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from game_logic.fast_tap_game import FastTapGame, GAME_RUN_TIME
from general_functions import GeneralFunctions

# Thread that runs the game simultaneously
class GameThread(QThread):
    # Signals that allow screen parameters to change in real time
    score_updated = pyqtSignal(int)
    time_updated = pyqtSignal(int)
    game_over = pyqtSignal()

    def __init__(self, app_init):
        super().__init__()
        self.fast_tap_game = FastTapGame(app_init)

    # Function that runs when the thread starts
    def run(self):

        # Update score on screen when signaled
        def update_score(num_round):
            self.score_updated.emit(num_round)
        
        # Update timer on screen when signaled
        def update_timer(time_remaining):
            self.time_updated.emit(time_remaining)
        
        # Show game over layout when signaled
        def on_game_over():
            self.fast_tap_game.disconnect_bluetooth()
            self.game_over.emit()
        
        # Run Fast Tap Game
        self.fast_tap_game.run_game(update_score, update_timer, on_game_over)

    # Stops the fast tap game
    def stop(self):
        if self.fast_tap_game:
            self.fast_tap_game.stop()

class FastTapInGameScreen(QWidget):
    def __init__(self, stacked_widget, app_init):
        # Intializations
        super().__init__()
        self.stacked_widget = stacked_widget
        self.score = 0
        self.time_remaining = GAME_RUN_TIME 
        self.app_init = app_init
        self.gen_funcs = GeneralFunctions(
            self.stacked_widget, self.score, self.reset_game, self.start_game, self.pause_game
        )
        # Create buttons and labels to put in layout later
        self.title = self.gen_funcs.set_title('Fast Tap')
        self.game_over_label = self.gen_funcs.create_game_over_label()
        self.timer_label = self.create_timer_label()
        self.score_label = self.gen_funcs.create_score_label()
        self.play_again_button = self.gen_funcs.create_play_again_button()
        self.go_back_button = self.gen_funcs.create_go_back_button()
        self.pause_button = self.gen_funcs.create_pause_button()

        self.create_screen()
        self.game_thread = None
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        # Timer updates every second (1000 ms)
        self.timer.setInterval(1000)

    # Creates the screen
    def create_screen(self):
        self.setStyleSheet("background-color: black;")
        self.set_layout()
        self.gen_funcs.hide_or_show_end_game_buttons(self.game_over_label, self.play_again_button, self.go_back_button, False)

    # Create timer label
    def create_timer_label(self):
        self.timer_label = QLabel(f'{self.time_remaining}', self)
        self.timer_label.setStyleSheet("color: white; font-size: 68px; font-weight: bold;")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setVisible(True)
        return self.timer_label

    # Uses labels and buttons created in init and arranges them on the screen
    def set_layout(self):
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.pause_button, alignment=Qt.AlignLeft)
        top_layout.addStretch()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.title)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.timer_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.score_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.game_over_label, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        main_layout.addWidget(self.play_again_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.go_back_button, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        self.setLayout(main_layout)

    # Start Fast Tap Game
    def start_game(self):        
        if self.game_thread is None or not self.game_thread.isRunning():
            self.game_thread = GameThread(self.app_init)
            self.game_thread.score_updated.connect(self.update_score)
            self.game_thread.game_over.connect(self.end_game)
            self.game_thread.start()
        self.game_over_label.setVisible(False)

        self.timer.start()

    # Update score on screen
    def update_score(self, score):
        self.score = score
        self.score_label.setText(f'Score: {self.score}')

    # Update timer on screen
    def update_timer(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.timer_label.setText(f'{self.time_remaining}')

    # Pause game by calling the pause function within the thread
    def pause_game(self):
        if self.game_thread and self.game_thread.fast_tap_game:
            self.game_thread.fast_tap_game.pause()
        self.timer.stop()
        self.stacked_widget.setCurrentIndex(10)

    # Resume game by calling the resume function within the thread
    def resume_game(self):
        if self.game_thread and self.game_thread.fast_tap_game:
            self.game_thread.fast_tap_game.resume()
        self.timer.start()

    # End game, save high score, reset parameters
    def reset_game(self):
        self.end_game()
        self.save_high_score()
        self.time_remaining = GAME_RUN_TIME
        self.score = 0
        self.timer_label.setText(f'{self.time_remaining}')
        self.score_label.setText(f'Score: {self.score}')
        self.gen_funcs.hide_or_show_end_game_buttons(self.game_over_label, self.play_again_button, self.go_back_button, False)
        self.show_or_hide_timer_label(True)
    
    # Save high score by calling app_init's function
    def save_high_score(self):
        if self.app_init.fast_tap_hs < self.score:
            self.app_init.fast_tap_hs = self.score
            self.app_init.sp_screen.update_displayed_values()
            self.app_init.save_fast_tap_high_score()

    # Stops the thread
    def end_game(self):
        if self.game_thread and self.game_thread.isRunning():
            self.game_thread.fast_tap_game.stop() 
            self.game_thread.quit()
            self.game_thread.wait()
        self.timer.stop()
        self.show_or_hide_timer_label(False)
        self.gen_funcs.hide_or_show_end_game_buttons(self.game_over_label, self.play_again_button, self.go_back_button, True)
    
    # Hide the timer label when the game ends
    def show_or_hide_timer_label(self, show):
        self.timer_label.setVisible(show)