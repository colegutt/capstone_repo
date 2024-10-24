from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from game_logic.tennis_game import TennisGame
from general_functions import GeneralFunctions

# Thread that runs the Tennis game simultaneously
class TennisGameThread(QThread):
    # Signals to update the player scores in real time
    player1_score_updated = pyqtSignal(int)
    player2_score_updated = pyqtSignal(int)
    game_over = pyqtSignal()

    def __init__(self, app_init):
        super().__init__()
        self.tennis_game = TennisGame(app_init)

    # Function that runs when the thread starts
    def run(self):
        # Update Player 1 score on screen
        def update_player1_score(score):
            self.player1_score_updated.emit(score)

        # Update Player 2 score on screen
        def update_player2_score(score):
            self.player2_score_updated.emit(score)

        # Signal when the game is over
        def on_game_over():
            self.tennis_game.disconnect()
            self.game_over.emit()

        # Run Tennis Game
        self.tennis_game.run_game(update_player1_score, update_player2_score, on_game_over)

    # Stops the tennis game
    def stop(self):
        if self.tennis_game:
            self.tennis_game.stop()


class TennisInGameScreen(QWidget):
    def __init__(self, stacked_widget, app_init):
        # Initializations
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_init = app_init
        self.gen_funcs = GeneralFunctions(self.stacked_widget, None, self.reset_game, self.start_game, self.pause_game)

        # Initial scores
        self.player1_score = 0
        self.player2_score = 0

        # Create title and labels for player scores
        self.title = self.gen_funcs.set_title('Tennis')
        self.player1_label = self.create_player_label('Player 1', self.player1_score)
        self.player2_label = self.create_player_label('Player 2', self.player2_score)

        # Create the pause button
        self.pause_button = self.gen_funcs.create_pause_button()

        self.create_screen()
        self.game_thread = None

    # Create labels for players
    def create_player_label(self, player_name, score):
        layout = QVBoxLayout()
        player_label = QLabel(player_name, self)
        player_label.setStyleSheet("color: white; font-size: 32px; font-weight: bold;")
        player_label.setAlignment(Qt.AlignCenter)

        score_label = QLabel(f'Score: {score}', self)
        score_label.setStyleSheet("color: white; font-size: 28px;")
        score_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(player_label)
        layout.addWidget(score_label)
        return layout

    # Create screen layout
    def create_screen(self):
        self.setStyleSheet("background-color: black;")
        self.set_layout()

    # Set up the main layout
    def set_layout(self):
        main_layout = QVBoxLayout()

        # Create a top layout for the pause button
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.pause_button, alignment=Qt.AlignLeft)  # Align the pause button to the left
        top_layout.addStretch()

        players_layout = QHBoxLayout()

        # Add Player 1 and Player 2 sides
        players_layout.addLayout(self.player1_label)
        players_layout.addStretch()
        players_layout.addLayout(self.player2_label)

        main_layout.addLayout(top_layout)  # Add the top layout with the pause button
        main_layout.addWidget(self.title, alignment=Qt.AlignCenter)
        main_layout.addLayout(players_layout)
        self.setLayout(main_layout)

    # Start Tennis Game
    def start_game(self):
        if self.game_thread is None or not self.game_thread.isRunning():
            self.game_thread = TennisGameThread(self.app_init)
            self.game_thread.player1_score_updated.connect(self.update_player1_score)
            self.game_thread.player2_score_updated.connect(self.update_player2_score)
            self.game_thread.game_over.connect(self.end_game)
            self.game_thread.start()

    # Update Player 1 score on screen
    def update_player1_score(self, score):
        self.player1_score = score
        self.player1_label.itemAt(1).widget().setText(f'Score: {self.player1_score}')

    # Update Player 2 score on screen
    def update_player2_score(self, score):
        self.player2_score = score
        self.player2_label.itemAt(1).widget().setText(f'Score: {self.player2_score}')

    # Reset game
    def reset_game(self):
        self.end_game()
        self.player1_score = 0
        self.player2_score = 0
        self.update_player1_score(self.player1_score)
        self.update_player2_score(self.player2_score)

    # End game
    def end_game(self):
        if self.game_thread and self.game_thread.isRunning():
            self.game_thread.tennis_game.stop()
            self.game_thread.quit()
            self.game_thread.wait()

    # Pause game
    def pause_game(self):
        if self.game_thread and self.game_thread.tennis_game:
            self.game_thread.tennis_game.pause()
        self.stacked_widget.setCurrentIndex(18)  # Navigate to index 18
