from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from game_logic.tennis_game import TennisGame
from general_functions import GeneralFunctions

# Thread that runs the Tennis Game simultaneously
class TennisGameThread(QThread):
    # Signals that allow screen parameters to change in real time
    player1_score_updated = pyqtSignal(int)
    player2_score_updated = pyqtSignal(int)
    game_over = pyqtSignal()

    def __init__(self, app_init):
        super().__init__()
        self.tennis_game = TennisGame(app_init)

    # Function that runs when the thread starts
    def run(self):
        # Update Player 1's score on screen when signaled
        def update_player1_score(score):
            self.player1_score_updated.emit(score)

        # Update Player 2's score on screen when signaled
        def update_player2_score(score):
            self.player2_score_updated.emit(score)

        # Show game over layout when signaled
        def on_game_over():
            self.tennis_game.disconnect_bluetooth()
            self.game_over.emit()

        # Run Tennis Game
        self.tennis_game.run_game()

    # Stops the Tennis Game
    def stop(self):
        if self.tennis_game:
            self.tennis_game.stop()


class TennisInGameScreen(QWidget):
    def __init__(self, stacked_widget, app_init):
        # Initializations
        super().__init__()
        self.stacked_widget = stacked_widget
        self.player1_score = 0
        self.player2_score = 0
        self.app_init = app_init
        self.gen_funcs = GeneralFunctions(
            self.stacked_widget, self.player1_score, self.reset_game, self.start_game, self.pause_game
        )

        # Create labels and buttons that are used in set_layout
        self.title = self.gen_funcs.set_title('Tennis')
        self.game_over_label = self.gen_funcs.create_game_over_label()
        self.player1_score_label = self.gen_funcs.create_score_label()
        self.player2_score_label = self.gen_funcs.create_score_label()
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

        score_layout = QHBoxLayout()

        # Left side: Player 1 score and label
        player1_layout = QVBoxLayout()
        player1_layout.addWidget(self.gen_funcs.create_score_label(), alignment=Qt.AlignCenter)
        player1_layout.addWidget(self.player1_score_label, alignment=Qt.AlignCenter)

        # Right side: Player 2 score and label
        player2_layout = QVBoxLayout()
        player2_layout.addWidget(self.gen_funcs.create_score_label(), alignment=Qt.AlignCenter)
        player2_layout.addWidget(self.player2_score_label, alignment=Qt.AlignCenter)

        # Add player layouts to score layout
        score_layout.addLayout(player1_layout)
        score_layout.addStretch()
        score_layout.addLayout(player2_layout)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.title)
        main_layout.addLayout(score_layout)
        main_layout.addStretch()
        main_layout.addWidget(self.game_over_label, alignment=Qt.AlignCenter)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.play_again_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.go_back_button, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        self.setLayout(main_layout)

    # Start Tennis game
    def start_game(self):
        if self.game_thread is None or not self.game_thread.isRunning():
            self.game_thread = TennisGameThread(self.app_init)
            self.game_thread.player1_score_updated.connect(self.update_player1_score)
            self.game_thread.player2_score_updated.connect(self.update_player2_score)
            self.game_thread.game_over.connect(self.end_game)
            self.game_thread.start()
        self.game_over_label.setVisible(False)

    # Update Player 1's score on screen
    def update_player1_score(self, score):
        self.player1_score = score
        self.player1_score_label.setText(f'Score: {self.player1_score}')

    # Update Player 2's score on screen
    def update_player2_score(self, score):
        self.player2_score = score
        self.player2_score_label.setText(f'Score: {self.player2_score}')

    # Pause game and go to pause screen
    def pause_game(self):
        if self.game_thread and self.game_thread.isRunning():
            self.game_thread.tennis_game.pause()
        self.stacked_widget.setCurrentIndex(6)

    # Resume game if needed
    def resume_game(self):
        if self.game_thread:
            self.game_thread.tennis_game.resume()
        else:
            self.start_game()

    # End Tennis game and hide corresponding buttons/labels
    def end_game(self):
        if self.game_thread and self.game_thread.isRunning():
            self.game_thread.tennis_game.stop()
            self.game_thread.quit()
            self.game_thread.wait()
        self.gen_funcs.hide_or_show_end_game_buttons(self.game_over_label, self.play_again_button, self.go_back_button, True)

    # Save high score if needed
    def save_high_score(self):
        if self.app_init.tennis_hs < max(self.player1_score, self.player2_score):
            self.app_init.tennis_hs = max(self.player1_score, self.player2_score)
            self.app_init.sp_screen.update_displayed_values()
            self.app_init.save_tennis_high_score()

    # Reset game, save high score, and hide/show buttons/labels as needed
    def reset_game(self):
        self.end_game()
        self.save_high_score()
        self.player1_score = 0
        self.player2_score = 0
        self.player1_score_label.setText(f'Score: {self.player1_score}')
        self.player2_score_label.setText(f'Score: {self.player2_score}')
        self.gen_funcs.hide_or_show_end_game_buttons(self.game_over_label, self.play_again_button, self.go_back_button, False)
