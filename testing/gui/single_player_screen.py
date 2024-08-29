from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout

class SPScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        # Initialize games and high scores
        self.games_and_high_scores = {
            'Memory': 10,
            'Fast Tap': 12,
            'Game 3': 15,
            'Game 4': 9
        }

        # Create screen
        self.create_screen()
    
    def create_screen(self):
        self.setStyleSheet("background-color: black;")
        self.set_layout(
            self.set_title(),
            self.create_games_layout(),
            self.create_back_button()
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
        i = 0
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


    def create_back_button(self):
        back_button = QPushButton('Back', self)
        back_button.setStyleSheet("""
            background-color: red; 
            color: white; 
            border-radius: 0px; 
            font-size: 16px; 
            font-weight: bold;
            width: 150px; 
            height: 50px; 
            padding: 0;
            text-align: center;
            line-height: 50px;
        """)
        back_button.clicked.connect(self.go_back)

        back_layout = QHBoxLayout()
        back_layout.addWidget(back_button)
        back_layout.addStretch()
        back_layout.setContentsMargins(20, 20, 20, 20)

        return back_layout

    def set_layout(self, title, games_layout, back_button):
        final_layout = QVBoxLayout()
        final_layout.addWidget(title)
        final_layout.addSpacing(20)  # Space between title and content
        final_layout.addLayout(games_layout)
        final_layout.addStretch()  # Push back button to the bottom
        final_layout.addLayout(back_button)

        self.setLayout(final_layout)

    def go_back(self):
        self.stacked_widget.setCurrentIndex(0)
    
    def go_to_game(self, index):
        if index == 0:
            self.stacked_widget.setCurrentIndex(0)
