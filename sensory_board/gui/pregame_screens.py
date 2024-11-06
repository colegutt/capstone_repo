from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
from general_functions import GeneralFunctions

# Create Memory Pregame Screen
class MemoryPregameScreen(QWidget):
    def __init__(self, stacked_widget, app_init):
        super().__init__()
        self.app_init = app_init
        self.ps_creator = PregameScreenCreator(stacked_widget, self.app_init)
        description_str = (
            "Press the buttons in the right order as they light up! The better you do, "
            "the longer the sequence gets. How many can you remember? Good luck!"
        )
        self.setLayout(self.ps_creator.create_pregame_screen('Memory', description_str, 'blue', 1, 5))

# Create Fast Tap Pregame Screen
class FastTapPregameScreen(QWidget):
    def __init__(self, stacked_widget, app_init):
        super().__init__()
        self.app_init = app_init
        self.ps_creator = PregameScreenCreator(stacked_widget, self.app_init)
        description_str = (
            "Press each button as it lights up and see how many you can get before time runs out. Good luck!"
        )
        self.setLayout(self.ps_creator.create_pregame_screen('Fast Tap', description_str, 'green', 1, 9))

# Create Memory Multiplayer Pregame Screen
class MemoryMultPregameScreen(QWidget):
    def __init__(self, stacked_widget, app_init):
        super().__init__()
        self.app_init = app_init
        self.ps_creator = PregameScreenCreator(stacked_widget, self.app_init, True)
        description_str = (
            "Team up to match the light-up sequence! With each round, the pattern grows as your " 
            "team gets better. How far can you go together? Good luck!"
        )
        self.setLayout(self.ps_creator.create_pregame_screen('Memory Multiplayer', description_str, 'purple', 2, 13))
    
    def get_player_count(self):
        return self.ps_creator.get_player_count()
    
    def get_game_mode(self):
        return self.ps_creator.get_game_mode()

# Create Tennis Pregame Screen
class TennisPregameScreen(QWidget):
    def __init__(self, stacked_widget, app_init):
        super().__init__()
        self.app_init = app_init
        self.ps_creator = PregameScreenCreator(stacked_widget, self.app_init)
        description_str = (
            "Take turns hitting the ball back and forth! Player 1, press the purple triangle; "
            "Player 2, press the green square. First to 3 points wins. Good luck!"
        )
        self.setLayout(self.ps_creator.create_pregame_screen('Tennis', description_str, 'orange', 2, 17, True))

# General class that create pregame screens given certain parameters
class PregameScreenCreator(QWidget):
    def __init__(self, stacked_widget, app_init, twoplayer_opt=False):
        # Initializations
        super().__init__()
        self.stacked_widget = stacked_widget

        # For Memory 2P
        self.player_count = 2
        self.twoplayer_opt = twoplayer_opt
        self.max_players = 8
        self.min_players = 2
        self.player_label = None
        self.description = None

        # Game mode options
        self.game_modes = ["Cooperative", "Elimination"]
        self.current_mode_index = 0
        self.game_mode_label = self.game_modes[0]

        self.gen_funcs = GeneralFunctions(self.stacked_widget)
        self.app_init = app_init

    # Create pregame screen    
    def create_pregame_screen(self, game_title, game_desc, button_color, game_index, in_game_screen_index, tennis=False):
        self.setStyleSheet("background-color: black;")
        return self.set_layout(
            self.set_title(game_title),
            self.set_description_layout(game_desc, tennis),
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
    def set_description_layout(self, game_desc, tennis=False):
        description_str = game_desc
        self.description = QLabel(description_str, self)
        self.description.setStyleSheet("color: white; font-size: 24px;")
        self.description.setAlignment(Qt.AlignCenter)
        self.description.setWordWrap(True)
        description_layout = QVBoxLayout()
        description_layout.addStretch()
        description_layout.addWidget(self.description)
        if tennis:
            description_layout.addSpacing(10)
            description_layout.addWidget(self.get_tennis_additional_description())
        description_layout.addStretch()
        description_layout.setContentsMargins(25, 0, 25, 0)
        return description_layout

    def get_tennis_additional_description(self):
        descr_2_str = 'NOTE: This game is not compatible with the controller'
        descr_2 = QLabel(descr_2_str, self)
        descr_2.setStyleSheet("color: red; font-size: 24px;")
        descr_2.setAlignment(Qt.AlignCenter)
        descr_2.setWordWrap(True)
        return descr_2

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

        # Add player count and game mode option in a single horizontal layout if memory 2p
        if self.twoplayer_opt:
            player_and_mode_layout = QHBoxLayout()
            player_and_mode_layout.addStretch()
            player_and_mode_layout.addLayout(self.create_player_count_layout())
            player_and_mode_layout.addSpacing(40)
            player_and_mode_layout.addLayout(self.create_game_mode_layout())
            player_and_mode_layout.addStretch()
            final_layout.addLayout(player_and_mode_layout)
            final_layout.addSpacing(10)

        final_layout.addLayout(start_button)
        final_layout.addStretch()
        final_layout.addLayout(back_button)

        return final_layout

    def create_player_count_layout(self):
        self.player_label = QLabel(f"{self.player_count} players")
        self.player_label.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        self.player_label.setAlignment(Qt.AlignCenter)

        minus_button = QPushButton('-', self)
        minus_button.setStyleSheet(self.button_style())
        minus_button.clicked.connect(self.decrease_player_count)

        plus_button = QPushButton('+', self)
        plus_button.setStyleSheet(self.button_style())
        plus_button.clicked.connect(self.increase_player_count)

        player_and_count_layout = QHBoxLayout()
        player_and_count_layout.addStretch(1)
        player_and_count_layout.addWidget(minus_button)
        player_and_count_layout.addSpacing(10)
        player_and_count_layout.addWidget(self.player_label)
        player_and_count_layout.addSpacing(10)
        player_and_count_layout.addWidget(plus_button)
        player_and_count_layout.addStretch(1)

        return player_and_count_layout

    def create_game_mode_layout(self):
        # Create label to display the current game mode
        self.game_mode_label = QLabel(self.game_modes[self.current_mode_index], self)
        self.game_mode_label.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        self.game_mode_label.setAlignment(Qt.AlignCenter)

        left_arrow = QPushButton('<', self)
        left_arrow.setStyleSheet(self.button_style())
        left_arrow.clicked.connect(self.previous_game_mode)

        right_arrow = QPushButton('>', self)
        right_arrow.setStyleSheet(self.button_style())
        right_arrow.clicked.connect(self.next_game_mode)

        game_mode_layout = QHBoxLayout()
        game_mode_layout.addStretch(1)
        game_mode_layout.addWidget(left_arrow)
        game_mode_layout.addSpacing(10)
        game_mode_layout.addWidget(self.game_mode_label)
        game_mode_layout.addSpacing(10)
        game_mode_layout.addWidget(right_arrow)
        game_mode_layout.addStretch(1)

        return game_mode_layout

    def button_style(self):
        return """
            background-color: gray; 
            color: white; 
            border-radius: 10px;
            font-size: 22px; 
            font-weight: bold;
            width: 40px; 
            height: 40px;
            padding: 0;
            text-align: center;
        """

    # Cycle through game modes
    def next_game_mode(self):
        self.current_mode_index = (self.current_mode_index + 1) % len(self.game_modes)
        self.update_game_mode_label()
        self.update_game_description()

    def previous_game_mode(self):
        self.current_mode_index = (self.current_mode_index - 1) % len(self.game_modes)
        self.update_game_mode_label()
        self.update_game_description()
    
    def update_game_description(self):
        cooperative_descr = (
            "Team up to match the light-up sequence! With each round, the pattern grows as your " 
            "team gets better. How far can you go together? Good luck!"
        )
        elimination_descr = (
            "Match the light-up sequence to stay in the game! Each round, the pattern gets tougher "
            "as your opponents succeed. Miss a step, and you're out - but the next player has to "
            "complete it to stay in the game!"
        )
        if self.current_mode_index == 0:
            self.description.setText(cooperative_descr)
        else:
            self.description.setText(elimination_descr)

    def update_game_mode_label(self):
        self.game_mode_label.setText(self.game_modes[self.current_mode_index])

    def go_to_ingame_screen(self, in_game_screen_index):
        self.stacked_widget.setCurrentIndex(in_game_screen_index)
        if in_game_screen_index == 5:
            self.app_init.memory_ingame_screen.start_game()
        elif in_game_screen_index == 9:
            self.app_init.fast_tap_ingame_screen.start_game()
        elif in_game_screen_index == 13:
            self.app_init.memory_mult_ingame_screen.start_game()
        elif in_game_screen_index == 17:
            self.app_init.tennis_ingame_screen.start_game()
            
    def increase_player_count(self):
        if self.player_count < self.max_players:
            self.player_count += 1
            self.player_label.setText(f"{self.player_count} players")

    def decrease_player_count(self):
        if self.player_count > self.min_players:
            self.player_count -= 1
            self.player_label.setText(f"{self.player_count} players")

    def get_player_count(self):
        return self.player_count

    def get_game_mode(self):
        return self.game_modes[self.current_mode_index]
