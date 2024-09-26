from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
from general_functions import GeneralFunctions

# Create Memory Pregame Screen
class MemoryPregameScreen(QWidget):
    def __init__(self, stacked_widget, app_init):
        super().__init__()
        self.app_init = app_init
        self.ps_creator = PregameScreenCreator(stacked_widget, self.app_init)
        description_str = (
            "Match the sequence by pressing the buttons that light up. "
            "The sequence will get longer the better you do. "
            "How many can you get? Good luck!"
        )
        self.setLayout(self.ps_creator.create_pregame_screen('Memory', description_str, 'blue', 1, 5))

# Create Fast Tap Pregame Screen
class FastTapPregameScreen(QWidget):
    def __init__(self, stacked_widget, app_init):
        super().__init__()
        self.app_init = app_init
        self.ps_creator = PregameScreenCreator(stacked_widget, self.app_init)
        description_str = (
            "Press every button that lights up. Try"
            " to get as many as you can before the "
            "time runs out. Good luck!"
        )
        self.setLayout(self.ps_creator.create_pregame_screen('Fast Tap', description_str, 'green', 1, 9))

# Create Memory Multiplayer Pregame Screen
class MemoryMultPregameScreen(QWidget):
    def __init__(self, stacked_widget, app_init):
        super().__init__()
        self.app_init = app_init
        self.ps_creator = PregameScreenCreator(stacked_widget, self.app_init, True)
        description_str = (
            "Grab some friends and work together by matching the sequence by pressing the buttons that light up. "
            "The sequence will get longer the better your team does. "
            "How many can you get together? Good luck!"
        )
        self.setLayout(self.ps_creator.create_pregame_screen('Memory Multiplayer', description_str, 'purple', 2, 13))
    
    def get_player_count(self):
        return self.ps_creator.get_player_count()

# Create Tennis Pregame Screen
class TennisPregameScreen(QWidget):
    def __init__(self, stacked_widget, app_init):
        super().__init__()
        self.app_init = app_init
        self.ps_creator = PregameScreenCreator(stacked_widget, self.app_init)
        description_str = (
            "Grab an opponent and take turns hitting a ball back and forth. "
            "Player 1 uses the [green] button, and Player 2 uses the [yellow] button. "
            "First player to 5 points wins the game. Good luck!"
        )
        self.setLayout(self.ps_creator.create_pregame_screen('Tennis', description_str, 'orange', 2, 2))

# General class that create pregame screens given certain parameters
class PregameScreenCreator(QWidget):
    def __init__(self, stacked_widget, app_init, twoplayer_opt=False):
        # Intializations
        super().__init__()
        self.stacked_widget = stacked_widget

        # For Memory 2P
        self.player_count = 2
        self.twoplayer_opt = twoplayer_opt
        self.max_players = 8
        self.min_players = 2
        self.player_label = None

        self.gen_funcs = GeneralFunctions(self.stacked_widget)
        self.app_init = app_init

    # Create pregame screen    
    def create_pregame_screen(self, game_title, game_desc, button_color, game_index, in_game_screen_index):
        self.setStyleSheet("background-color: black;")
        return self.set_layout(
            self.set_title(game_title),
            self.set_description_layout(game_desc),
            self.create_start_button(button_color, in_game_screen_index),
            self.gen_funcs.create_back_layout(game_index)
        )
    
    # Return title label for the screen
    def set_title(self, game_title):
        title = QLabel(f'{game_title}', self)
        title.setStyleSheet("color: white; font-size: 48px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        return title
    
    # Return description label for the screen
    def set_description_layout(self, game_desc):
        description_str = game_desc

        description = QLabel(description_str, self)
        description.setStyleSheet("color: white; font-size: 26px;")
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)
        description_layout = QVBoxLayout()
        description_layout.addStretch()
        description_layout.addWidget(description)
        description_layout.addStretch()
        description_layout.setContentsMargins(100, 0, 100, 0)
        return description_layout

    # Create start button that starts the game when clicked
    def create_start_button(self, button_color, in_game_screen_index):
        start_button = QPushButton('Start', self)
        start_button.setStyleSheet(f"""
            background-color: {button_color}; 
            color: white; 
            border-radius: 75px; 
            font-size: 24px; 
            font-weight: bold;
            width: 150px; 
            height: 150px;
        """)
        start_button.clicked.connect(
            lambda checked, in_game_screen_index=in_game_screen_index: self.go_to_ingame_screen(in_game_screen_index)
        )

        start_layout = QHBoxLayout()
        start_layout.addWidget(start_button)
        start_layout.setAlignment(Qt.AlignCenter)
        start_layout.setContentsMargins(20, 20, 20, 20)

        return start_layout

    # Arrange created buttons and labels
    def set_layout(self, title, description_layout, start_button, back_button):
        final_layout = QVBoxLayout()
        final_layout.addWidget(title)
        final_layout.addSpacing(30)
        final_layout.addLayout(description_layout)
        final_layout.addSpacing(30) 
        # Add player count option if memory 2p
        if self.twoplayer_opt:
            final_layout.addLayout(self.create_player_count_layout())
            final_layout.addSpacing(10) 
        final_layout.addLayout(start_button)
        final_layout.addStretch()
        final_layout.addLayout(back_button)

        return final_layout

    def create_player_count_layout(self):
        self.player_label = QLabel(f"{self.player_count} players")
        self.player_label.setStyleSheet("color: white; font-size: 25px; font-weight: bold;")
        self.player_label.setAlignment(Qt.AlignCenter)  # Center the text

        minus_button = QPushButton('-', self)
        minus_button.setStyleSheet(self.button_style())
        minus_button.clicked.connect(self.decrease_player_count)

        plus_button = QPushButton('+', self)
        plus_button.setStyleSheet(self.button_style())
        plus_button.clicked.connect(self.increase_player_count)

        # Create a layout with spacers to center the label between the buttons
        player_and_count_layout = QHBoxLayout()
        
        # Adding stretch for spacing to center the label between buttons
        player_and_count_layout.addStretch(1)
        player_and_count_layout.addWidget(minus_button)
        player_and_count_layout.addSpacing(10)  # Small spacing between button and label
        player_and_count_layout.addWidget(self.player_label)
        player_and_count_layout.addSpacing(10)  # Small spacing between label and plus button
        player_and_count_layout.addWidget(plus_button)
        player_and_count_layout.addStretch(1)

        return player_and_count_layout

    def button_style(self):
        return """
            background-color: gray; 
            color: white; 
            border-radius: 10px;
            font-size: 24px; 
            font-weight: bold;
            width: 50px; 
            height: 50px;
            padding: 0;
            text-align: center;
        """

    # If start button is clicked, go to corresponding in-game screen
    def go_to_ingame_screen(self, in_game_screen_index):
        self.stacked_widget.setCurrentIndex(in_game_screen_index)
        if in_game_screen_index == 5:
            self.app_init.memory_ingame_screen.start_game()
        elif in_game_screen_index == 9:
            self.app_init.fast_tap_ingame_screen.start_game()
        elif in_game_screen_index == 13:
            self.app_init.memory_mult_ingame_screen.start_game()
    
    def decrease_player_count(self):
        if self.player_count > self.min_players:
            self.player_count -= 1
            self.player_label.setText(f"{self.player_count} players")
    
    def increase_player_count(self):
        if self.player_count < self.max_players:
            self.player_count += 1
            self.player_label.setText(f"{self.player_count} players")
    
    def get_player_count(self):
        return self.player_count
