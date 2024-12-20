from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
from general_functions import GeneralFunctions

# Single player screen creation
class SPScreen(QWidget):
    def __init__(self, stacked_widget, app_init):
        super().__init__()
        self.app_init = app_init
        self.games_and_high_scores = {
            'Memory': self.app_init.memory_hs,
            'Fast Tap': self.app_init.fast_tap_hs,
        }
        self.hs_qlabels = {
            'Memory': None,
            'Fast Tap': None,
        }
        title = 'Single Player Games'
        colors = ['blue', 'green']
        self.gl_creator = GameListScreenCreator(
            stacked_widget, self.app_init, self.games_and_high_scores, title, False, self.hs_qlabels, colors
        )

        self.setLayout(self.gl_creator.create_screen())

    # Update high scores
    def update_displayed_values(self):
        self.hs_qlabels['Memory'].setText(f'{self.app_init.memory_hs}')
        self.hs_qlabels['Fast Tap'].setText(f'{self.app_init.fast_tap_hs}')
    
# Multiplayer screen creation
class MPScreen(QWidget):
    def __init__(self, stacked_widget, app_init):
        super().__init__()
        self.app_init = app_init
        games_and_high_scores = {
            'Tennis': self.app_init.tennis_hs,
            'Memory Multiplayer': self.app_init.memory_mult_hs
        }
        self.hs_qlabels = {
            'Tennis': None,
            'Memory Mutliplayer': None
        }
        title = 'Multiplayer Games'
        colors = ['orange', 'purple']
        self.gl_creator = GameListScreenCreator(
            stacked_widget, self.app_init, games_and_high_scores, title, True, self.hs_qlabels, colors
        )
        self.setLayout(self.gl_creator.create_screen())
    
    # Update high scores
    def update_displayed_values(self):
        self.hs_qlabels['Memory Multiplayer'].setText(f'{self.app_init.memory_mult_hs}')
        self.hs_qlabels['Tennis'].setText(f'{self.app_init.tennis_hs}')


# Common function for creating game list screens
class GameListScreenCreator(QWidget):
    def __init__(self, stacked_widget, app_init, games_and_high_scores, title, multiplayer, hs_qlabels, colors):
        # Initializations
        super().__init__()
        self.stacked_widget = stacked_widget
        self.gen_funcs = GeneralFunctions(self.stacked_widget)
        self.games_and_high_scores = games_and_high_scores
        self.hs_qlabels = hs_qlabels
        self.multiplayer = multiplayer
        self.app_init = app_init
        self.title = title
        self.colors = colors
    
    # Create screen
    def create_screen(self):
        self.setStyleSheet("background-color: black;")
        return self.set_layout(
            self.set_title(),
            self.create_games_layout(),
            self.gen_funcs.create_back_layout(0)
        )
    
    # Return title label
    def set_title(self):
        title = QLabel(self.title, self)
        title.setStyleSheet("color: white; font-size: 48px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        return title

    # Return layout of the "Game" and "High Score" headers
    def create_header_layout(self):
        game_header_title = QLabel('Game', self)
        game_header_title.setStyleSheet("color: white; font-size: 32px; font-weight: bold;")
        game_header_title.setAlignment(Qt.AlignCenter)

        high_score_header_title = QLabel('High Score', self)
        high_score_header_title.setStyleSheet("color: white; font-size: 32px; font-weight: bold;")
        high_score_header_title.setAlignment(Qt.AlignCenter)

        header_layout = QHBoxLayout()
        header_layout.addStretch()
        header_layout.addWidget(game_header_title)
        header_layout.addSpacing(150)
        header_layout.addWidget(high_score_header_title)
        header_layout.addStretch()

        return header_layout

    # Return the layout for the list of the game buttons and the high scores to the right of them
    def create_games_layout(self):
        header_layout = self.create_header_layout()

        game_layouts = []
        i = 0
        for game, hs in self.games_and_high_scores.items():
            temp_game_layout = QHBoxLayout()
            self.hs_qlabels[game] = QLabel(f'{hs}', self)
            self.hs_qlabels[game].setStyleSheet("color: white; font-size: 40px; font-weight: bold;")
            game_button = QPushButton(game, self)
            game_button.setStyleSheet(f'''
                background-color: {self.colors[i % len(self.colors)]}; 
                color: white; 
                border-radius: 10px; 
                width: 300px; 
                height: 100px; 
                font-size: 24px; 
                font-weight: bold;
                height: 100px;
            ''')
            game_button.clicked.connect(lambda checked, i=i: self.go_to_pregame_screen(i))
            temp_game_layout.addSpacing(165) 
            temp_game_layout.addWidget(game_button)
            temp_game_layout.addSpacing(125)
            temp_game_layout.addWidget(self.hs_qlabels[game])
            if game == 'Tennis':
                rally_label = QLabel('(Rally)', self)
                rally_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
                temp_game_layout.addSpacing(10)
                temp_game_layout.addWidget(rally_label)
                temp_game_layout.addSpacing(220) 
            else:
                temp_game_layout.addSpacing(300) 

            game_layouts.append(temp_game_layout)
            i += 1

        # Main games layout
        games_layout = QVBoxLayout()
        games_layout.addSpacing(50)
        games_layout.addLayout(header_layout)
        games_layout.addSpacing(25)
        for game_layout in game_layouts:
            games_layout.addLayout(game_layout)
            games_layout.addSpacing(50)
        games_layout.addStretch()

        return games_layout

    # Take created layouts and arrange them
    def set_layout(self, title, games_layout, back_layout):
        final_layout = QVBoxLayout()
        final_layout.addWidget(title)
        final_layout.addLayout(games_layout)
        final_layout.addLayout(back_layout)
        return final_layout
    
    # If button is clicked, go to the corresponding screen
    def go_to_pregame_screen(self, index):
        if self.multiplayer:
            if index == 0:
                self.stacked_widget.setCurrentIndex(16)
            elif index == 1:
                self.stacked_widget.setCurrentIndex(12)
        else:
            if index == 0:
                self.stacked_widget.setCurrentIndex(4)
            elif index == 1:
                self.stacked_widget.setCurrentIndex(8)
