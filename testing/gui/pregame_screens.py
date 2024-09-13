from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
from general_functions import GeneralFunctions

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

class FastTapPregameScreen(QWidget):
    def __init__(self, stacked_widget, app_init):
        super().__init__()
        self.app_init = app_init
        self.ps_creator = PregameScreenCreator(stacked_widget, self.app_init)
        description_str = (
            "Press every button that lights up. Try"
            " to get as many as you can before the "
            "time runs out!"
        )
        self.setLayout(self.ps_creator.create_pregame_screen('Fast Tap', description_str, 'green', 1, 9))

class MemoryMultiplayerPregameScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.game_obj = None
        self.ps_creator = PregameScreenCreator(stacked_widget, self.game_obj)
        description_str = (
            "This is a new description for the multiplayer ping pong "
            "game. I have no idea how this will be played."
            "ROTATE SCREEN TO BEGIN!!!"
        )
        self.setLayout(self.ps_creator.create_pregame_screen('Memory', description_str, 'purple', 2, 2))

class TennisPregameScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.game_obj = None
        self.ps_creator = PregameScreenCreator(stacked_widget, self.game_obj)
        description_str = (
            "This is a new description for the multiplayer ping pong "
            "game. I have no idea how this will be played."
            "ROTATE SCREEN TO BEGIN!!!"
        )
        self.setLayout(self.ps_creator.create_pregame_screen('Ping Pong', description_str, 'blue', 2, 2))

# Put classes for other pregame screens below!!!


class PregameScreenCreator(QWidget):
    def __init__(self, stacked_widget, app_init):
        self.stacked_widget = stacked_widget
        self.gen_funcs = GeneralFunctions(self.stacked_widget)
        self.app_init = app_init
        super().__init__()
    
    def create_pregame_screen(self, game_title, game_desc, button_color, game_index, in_game_screen_index):
        self.setStyleSheet("background-color: black;")
        return self.set_layout(
            self.set_title(game_title),
            self.set_description_layout(game_desc),
            self.create_start_button(button_color, in_game_screen_index),
            self.gen_funcs.create_back_layout(game_index)
        )
    
    def set_title(self, game_title):
        title = QLabel(f'{game_title}', self)
        title.setStyleSheet("color: white; font-size: 48px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        return title
    
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

    def set_layout(self, title, description_layout, start_button, back_button):
        final_layout = QVBoxLayout()
        final_layout.addWidget(title)
        final_layout.addSpacing(50)  # Space between title and description
        final_layout.addLayout(description_layout)
        final_layout.addSpacing(75)  # Space between description and start button
        final_layout.addLayout(start_button)
        final_layout.addStretch()  # Push back button to the bottom
        final_layout.addLayout(back_button)

        return final_layout

    def go_to_ingame_screen(self, in_game_screen_index):
        self.stacked_widget.setCurrentIndex(in_game_screen_index)
        if in_game_screen_index == 5:
            self.app_init.memory_ingame_screen.start_game()
        elif in_game_screen_index == 9:
            self.app_init.fast_tap_ingame_screen.start_game()
