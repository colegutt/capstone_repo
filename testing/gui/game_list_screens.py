from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
from general_functions import GeneralFunctions


class GameListScreenCreator(QWidget):
    def __init__(self, stacked_widget, games_and_high_scores, multiplayer):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.gen_funcs = GeneralFunctions(self.stacked_widget)
        self.games_and_high_scores = games_and_high_scores
        if multiplayer:
            self.index = 0 # Change
        else:
            self.index = 0
    
    def create_screen(self):
        self.setStyleSheet("background-color: black;")
        return self.set_layout(
            self.set_title(),
            self.create_games_layout(),
            self.gen_funcs.create_back_layout(0)
        )
    
    def set_title(self):
        title = QLabel('Single Player Games', self)
        title.setStyleSheet("color: white; font-size: 48px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        return title

    def create_header_layout(self):
        # Game Header
        game_header_title = QLabel('Game', self)
        game_header_title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        game_header_title.setAlignment(Qt.AlignCenter)

        # High Score Header
        high_score_header_title = QLabel('High Score', self)
        high_score_header_title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        high_score_header_title.setAlignment(Qt.AlignCenter)

        header_layout = QHBoxLayout()
        header_layout.addStretch()
        header_layout.addWidget(game_header_title)
        header_layout.addSpacing(250)
        header_layout.addWidget(high_score_header_title)
        header_layout.addStretch()

        return header_layout

    def create_games_layout(self):
        header_layout = self.create_header_layout()

        # Game layouts
        game_layouts = []
        colors = ['blue', 'green', 'purple', 'orange']
        i = self.index
        for game, hs in self.games_and_high_scores.items():
            temp_game_layout = QHBoxLayout()
            hs_title = QLabel(f'{hs}', self)
            hs_title.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
            # Game button
            game_button = QPushButton(game, self)
            game_button.setStyleSheet(f'''
                background-color: {colors[i % len(colors)]}; 
                color: white; 
                border-radius: 10px; 
                width: 250px; 
                height: 250px; 
                font-size: 20px; 
                font-weight: bold;
                height: 50px;
            ''')
            game_button.clicked.connect(lambda checked, i=i: self.go_to_game(i))
            temp_game_layout.addSpacing(180) 
            temp_game_layout.addWidget(game_button)
            temp_game_layout.addSpacing(200)  # Space between button and score
            temp_game_layout.addWidget(hs_title)
            temp_game_layout.addSpacing(300) 

            game_layouts.append(temp_game_layout)
            i += 1

        # Main games layout
        games_layout = QVBoxLayout()
        games_layout.addLayout(header_layout)
        games_layout.addSpacing(30)  # Space between headers and game layouts
        for game_layout in game_layouts:
            games_layout.addLayout(game_layout)
            games_layout.addSpacing(30)  # Space between headers and game layouts

        return games_layout

    def set_layout(self, title, games_layout, back_layout):
        final_layout = QVBoxLayout()
        final_layout.addWidget(title)
        final_layout.addLayout(games_layout)
        final_layout.addLayout(back_layout)
        return final_layout
    
    def go_to_game(self, index):
        if index == 0:
            self.stacked_widget.setCurrentIndex(4)
        

class SPScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        games_and_high_scores = {
            'Memory': 10,
            'Game 2': 12,
            'Game 3': 15,
            'Game 4': 9
        }

        self.gl_creator = GameListScreenCreator(stacked_widget, games_and_high_scores, False)

        self.setLayout(self.gl_creator.create_screen())

class MPScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        games_and_high_scores = {
            'Ping Pong': 10,
            'Game 2': 12,
            'Game 3': 15,
            'Game 4': 9
        }

        self.gl_creator = GameListScreenCreator(stacked_widget, games_and_high_scores, True)

        self.setLayout(self.gl_creator.create_screen())
