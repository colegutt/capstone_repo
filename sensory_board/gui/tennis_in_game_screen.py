from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from game_logic.tennis_game import TennisGame
from general_functions import GeneralFunctions

# Thread that runs the Tennis Game simultaneously
class GameThread(QThread):
    player1_score_updated = pyqtSignal(int)
    player2_score_updated = pyqtSignal(int)
    pause_button_updating = pyqtSignal(bool)
    rally_updated = pyqtSignal(int)
    game_over = pyqtSignal(int)

    def __init__(self, stacked_widget, app_init):
        super().__init__()
        self.tennis_game = TennisGame(stacked_widget, app_init)

    # Function that runs when the thread starts
    def run(self):
        # Update Player 2's score on screen when signaled
        def update_score(player, score):
            if player == 1:
                self.player1_score_updated.emit(score)
            elif player == 2:
                self.player2_score_updated.emit(score)
        
        def toggle_pause_button(activate):
            self.pause_button_updating.emit(activate)

        # Show game over layout when signaled
        def on_game_over(player):
            # self.tennis_game.disconnect_bluetooth()
            self.game_over.emit(player)  # Emit the winning player number
        
        def update_rally(rally):
            self.rally_updated.emit(rally)  # Emit rally count to the screen

        self.tennis_game.run_game(update_score, update_rally, toggle_pause_button, on_game_over)

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
            self.stacked_widget, self.player1_score, self.reset_game, self.start_game, self.pause_game, True
        )

        # Create labels and buttons that are used in set_layout
        self.title = self.gen_funcs.set_title('Tennis')
        self.game_over_label = self.gen_funcs.create_game_over_label()
        self.player1_score_label = self.gen_funcs.create_score_label(52)
        self.player2_score_label = self.gen_funcs.create_score_label(52)
        self.rally_label = QLabel('Rally: 0', self)  # New rally label
        self.rally_label.setStyleSheet("color: white; font-size: 32px; font-weight: bold;")
        self.rally_label.setAlignment(Qt.AlignCenter)
        self.rally_label.setVisible(True)
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

        score_layout = QHBoxLayout()

        # Player 1 Label
        self.player1_label = QLabel('Player 1', self)
        self.player1_label.setStyleSheet("color: purple; font-size: 56px; font-weight: bold;")
        self.player1_label.setAlignment(Qt.AlignCenter)

        # Player 2 Label
        self.player2_label = QLabel('Player 2', self)
        self.player2_label.setStyleSheet("color: green; font-size: 56px; font-weight: bold;")
        self.player2_label.setAlignment(Qt.AlignCenter)

        player1_layout = QVBoxLayout()
        player1_layout.addStretch()
        player1_layout.addWidget(self.player1_label)
        player1_layout.addSpacing(20)
        player1_layout.addWidget(self.player1_score_label, alignment=Qt.AlignCenter)

        player2_layout = QVBoxLayout()
        player2_layout.addStretch()
        player2_layout.addWidget(self.player2_label)
        player2_layout.addSpacing(20)
        player2_layout.addWidget(self.player2_score_label, alignment=Qt.AlignCenter)

        rally_layout = QVBoxLayout()
        rally_layout.addWidget(self.rally_label, alignment=Qt.AlignCenter)

        # Add player layouts to score layout
        score_layout.addStretch()
        score_layout.addLayout(player1_layout)
        score_layout.addStretch()
        score_layout.addLayout(player2_layout)
        score_layout.addStretch()

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.title)
        main_layout.addStretch()
        main_layout.addLayout(score_layout)
        main_layout.addStretch()
        main_layout.addLayout(rally_layout) 
        main_layout.addStretch()
        main_layout.addWidget(self.game_over_label, alignment=Qt.AlignCenter)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.play_again_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.go_back_button, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        self.setLayout(main_layout)

    # Start Tennis games
    def start_game(self):
        if self.game_thread is None or not self.game_thread.isRunning():
            self.game_thread = GameThread(self.stacked_widget, self.app_init)
            self.game_thread.player1_score_updated.connect(self.update_player1_score)
            self.game_thread.player2_score_updated.connect(self.update_player2_score)
            self.game_thread.pause_button_updating.connect(self.toggle_pause_button)
            self.game_thread.rally_updated.connect(self.update_rally)
            self.game_thread.game_over.connect(self.end_game)
            self.game_thread.start()
        self.rally_label.setVisible(True)
        self.game_over_label.setVisible(False)
    
    # def update_serving_label(self, player=None):
    #     self.player1_label.setText("Player 1")
    #     self.player2_label.setText("Player 2")

    #     if player == 1:
    #         self.player1_label.setText("SERVING: Player 1")
    #     elif player == 2:
    #         self.player2_label.setText("SERVING: Player 2")
    
    def toggle_pause_button(self, activate):
        if activate:
            self.pause_button.setStyleSheet("""
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
            self.pause_button.clicked.connect(self.pause_game)
        else:
            self.pause_button.setStyleSheet("""
                background-color: gray; 
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
            self.pause_button.clicked.disconnect()

    def update_player1_score(self, score):
        self.player1_score = score
        self.player1_score_label.setText(f'Score: {self.player1_score}')

    def update_player2_score(self, score):
        self.player2_score = score
        self.player2_score_label.setText(f'Score: {self.player2_score}')
    
    def update_rally(self, rally):
        self.rally_label.setText(f"Rally: {rally}")

    # Pause game and go to pause screen
    def pause_game(self):
        if self.game_thread and self.game_thread.isRunning():
            self.game_thread.tennis_game.pause()
        self.stacked_widget.setCurrentIndex(18)

    # Resume game if needed
    def resume_game(self):
        if self.game_thread:
            self.game_thread.tennis_game.resume()
        else:
            self.start_game()

    # End Tennis game and hide corresponding buttons/labels
    def end_game(self, winning_player=None):
        if self.game_thread and self.game_thread.isRunning():
            self.game_thread.tennis_game.stop()
            self.game_thread.quit()
            self.game_thread.wait()

        self.rally_label.setVisible(False)
        self.show_game_over(winning_player)
        self.gen_funcs.hide_or_show_end_game_buttons(self.game_over_label, self.play_again_button, self.go_back_button, True)


    def show_game_over(self, winning_player):
        if winning_player == 1:
            self.game_over_label.setText('PLAYER 1 WINS! GAME OVER!')
            self.game_over_label.setStyleSheet("color: purple; font-size: 40px; font-weight: bold;")
        elif winning_player == 2:
            self.game_over_label.setText('PLAYER 2 WINS! GAME OVER!')
            self.game_over_label.setStyleSheet("color: green; font-size: 40px; font-weight: bold;")

    # Reset game, save high score, and hide/show buttons/labels as needed
    def reset_game(self):
        self.end_game()
        self.player1_score = 0
        self.player2_score = 0
        self.player1_score_label.setText(f'Score: {self.player1_score}')
        self.player2_score_label.setText(f'Score: {self.player2_score}')
        self.rally_label.setText("Rally: 0")
        self.gen_funcs.hide_or_show_end_game_buttons(self.game_over_label, self.play_again_button, self.go_back_button, False)
