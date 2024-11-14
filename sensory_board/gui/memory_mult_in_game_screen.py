from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from game_logic.memory_game import MemoryGame
from general_functions import GeneralFunctions

# Thread that runs the game simultaneously
class GameThread(QThread):
    # Signals that allow screen parameters to change in real time
    score_updated = pyqtSignal(int)
    game_over = pyqtSignal(int)
    player_changed = pyqtSignal(int, bool)

    def __init__(self, stacked_widget, app_init, player_count, game_mode):
        super().__init__()
        self.memory_game = MemoryGame(stacked_widget, app_init, True, player_count, game_mode)
        
    # Function that runs when the thread starts
    def run(self):

        # Update score on screen when signaled
        def update_score(num_round):
            self.score_updated.emit(num_round)
        
        # Update player number when signaled
        def update_player(player_num, eliminated=False):
            self.player_changed.emit(player_num, eliminated)
        
        # Show game over layout when signaled
        def on_game_over(player_num=None):
            self.game_over.emit(player_num)

        # Run Memory 2P Game
        self.memory_game.run_game(update_score, on_game_over, update_player)
    
    # Stops the Memory 2P Game
    def stop(self):
        if self.memory_game:
            self.memory_game.stop()

class MemoryMultInGameScreen(QWidget):
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
        self.title = self.gen_funcs.set_title('Memory Multiplayer')
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
    
    # Start Memory 2P game
    def start_game(self):
        if self.game_thread is None or not self.game_thread.isRunning():
            self.game_thread = GameThread(self.stacked_widget, self.app_init, self.app_init.memory_mult_pregame_screen.get_player_count(), self.app_init.memory_mult_pregame_screen.get_game_mode())
            self.game_thread.score_updated.connect(self.update_score_from_game)
            self.game_thread.player_changed.connect(self.update_player_label)
            self.game_thread.game_over.connect(self.end_game)
            self.game_thread.start()
        self.game_over_label.setVisible(False)
        self.turn_label.setVisible(True)
    
    # Save Memory 2P high score if needed
    def save_high_score(self):
        if self.app_init.memory_mult_hs < self.score:
            self.app_init.memory_mult_hs = self.score
            self.app_init.mp_screen.update_displayed_values()
            self.app_init.save_memory_mult_high_score()

    # Update score in screen
    def update_score_from_game(self, num_round):
        self.score = num_round
        self.score_label.setText(f'Score: {self.score}')

    # Update "Player #'s Turn" label
    def update_player_label(self, player_num, eliminated=False):
        if player_num == 1:
            if eliminated:
                self.turn_label.setText("Player 1 Eliminated!")
            else:
                self.turn_label.setText("Player 1's Turn")
            self.turn_label.setStyleSheet("color: blue; font-size: 50px; font-weight: bold;")
        elif player_num == 2:
            if eliminated:
                self.turn_label.setText("Player 2 Eliminated!")
            else:
                self.turn_label.setText("Player 2's Turn")
            self.turn_label.setStyleSheet("color: red; font-size: 50px; font-weight: bold;")
        elif player_num == 3:
            if eliminated:
                self.turn_label.setText("Player 3 Eliminated!")
            else:
                self.turn_label.setText("Player 3's Turn")
            self.turn_label.setStyleSheet("color: teal; font-size: 50px; font-weight: bold;")
        elif player_num == 4:
            if eliminated:
                self.turn_label.setText("Player 4 Eliminated!")
            else:
                self.turn_label.setText("Player 4's Turn")
            self.turn_label.setStyleSheet("color: orange; font-size: 50px; font-weight: bold;")
        elif player_num == 5:
            if eliminated:
                self.turn_label.setText("Player 5 Eliminated!")
            else:
                self.turn_label.setText("Player 5's Turn")
            self.turn_label.setStyleSheet("color: green; font-size: 50px; font-weight: bold;")
        elif player_num == 6:
            if eliminated:
                self.turn_label.setText("Player 6 Eliminated!")
            else:
                self.turn_label.setText("Player 6's Turn")
            self.turn_label.setStyleSheet("color: cyan; font-size: 50px; font-weight: bold;")
        elif player_num == 7:
            if eliminated:
                self.turn_label.setText("Player 7 Eliminated!")
            else:
                self.turn_label.setText("Player 7's Turn")
            self.turn_label.setStyleSheet("color: pink; font-size: 50px; font-weight: bold;")
        elif player_num == 8:
            if eliminated:
                self.turn_label.setText("Player 8 Eliminated!")
            else:
                self.turn_label.setText("Player 8's Turn")
            self.turn_label.setStyleSheet("color: #E6E6FA; font-size: 50px; font-weight: bold;")
    
    # Pause game and go to pause screen
    def pause_game(self):
        if self.game_thread and self.game_thread.isRunning():
            self.game_thread.memory_game.pause()
        self.stacked_widget.setCurrentIndex(14)

    # Resume game if needed
    def resume_game(self):
        if self.game_thread:
            self.game_thread.memory_game.resume()
        else:
            self.start_game()

    # End game by ending thread and hiding/showing needed labels and buttons
    def end_game(self, winning_player=None):
        if self.game_thread and self.game_thread.isRunning():
            self.game_thread.memory_game.stop()
            self.game_thread.quit()
            self.game_thread.wait()
        self.show_game_over(winning_player)
        self.gen_funcs.hide_or_show_end_game_buttons(self.game_over_label, self.play_again_button, self.go_back_button, True)
        self.turn_label.setVisible(False)
    
    def show_game_over(self, winning_player):
        if winning_player == 1:
            self.game_over_label.setText('PLAYER 1 WINS! GAME OVER!')
            self.game_over_label.setStyleSheet("color: blue; font-size: 40px; font-weight: bold;")
        elif winning_player == 2:
            self.game_over_label.setText('PLAYER 2 WINS! GAME OVER!')
            self.game_over_label.setStyleSheet("color: red; font-size: 40px; font-weight: bold;")
        elif winning_player == 3:
            self.game_over_label.setText('PLAYER 3 WINS! GAME OVER!')
            self.game_over_label.setStyleSheet("color: teal; font-size: 40px; font-weight: bold;")
        elif winning_player == 4:
            self.game_over_label.setText('PLAYER 4 WINS! GAME OVER!')
            self.game_over_label.setStyleSheet("color: orange; font-size: 40px; font-weight: bold;")
        elif winning_player == 5:
            self.game_over_label.setText('PLAYER 5 WINS! GAME OVER!')
            self.game_over_label.setStyleSheet("color: green; font-size: 40px; font-weight: bold;")
        elif winning_player == 6:
            self.game_over_label.setText('PLAYER 6 WINS! GAME OVER!')
            self.game_over_label.setStyleSheet("color: cyan; font-size: 40px; font-weight: bold;")
        elif winning_player == 7:
            self.game_over_label.setText('PLAYER 7 WINS! GAME OVER!')
            self.game_over_label.setStyleSheet("color: pink; font-size: 40px; font-weight: bold;")
        elif winning_player == 8:
            self.game_over_label.setText('PLAYER 8 WINS! GAME OVER!')
            self.game_over_label.setStyleSheet("color: #E6E6FA; font-size: 40px; font-weight: bold;")
    
    # Reset game if needed
    def reset_game(self):
        self.end_game()
        self.save_high_score()
        self.score = 0
        self.score_label.setText(f'Score: {self.score}')
        self.update_player_label(1)
        self.gen_funcs.hide_or_show_end_game_buttons(self.game_over_label, self.play_again_button, self.go_back_button, False)
