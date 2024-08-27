import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout

class MainMenu(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget  # Store reference to the stacked widget
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: black;")  # Set background color to black
        
        # Create and style title label
        title_label = QLabel('BEEPY', self)
        title_label.setStyleSheet("color: white; font-size: 48px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)  # Center the title label text

        # Create and style Single Player button
        single_player_button = QPushButton('Single Player', self)
        single_player_button.setStyleSheet("""
            background-color: green; 
            color: white; 
            border-radius: 100px; 
            font-size: 18px; 
            font-weight: bold;
            width: 200px; 
            height: 200px; 
            padding: 0;
            text-align: center;
            line-height: 200px;
        """)
        single_player_button.clicked.connect(self.show_single_player)  # Connect button to slot

        # Create and style Multiplayer button
        multiplayer_button = QPushButton('Multiplayer', self)
        multiplayer_button.setStyleSheet("""
            background-color: blue; 
            color: white; 
            border-radius: 100px; 
            font-size: 18px; 
            font-weight: bold;
            width: 200px; 
            height: 200px; 
            padding: 0;
            text-align: center;
            line-height: 200px;
        """)
        multiplayer_button.clicked.connect(self.show_multiplayer)  # Connect button to slot
        
        # Create and style Settings button
        settings_button = QPushButton('Settings', self)
        settings_button.setStyleSheet("""
            background-color: gray; 
            color: white; 
            border-radius: 80px; 
            font-size: 16px; 
            font-weight: bold;
            width: 160px; 
            height: 160px; 
            padding: 0;
            text-align: center;
            line-height: 160px;
        """)
        settings_button.clicked.connect(self.show_settings)  # Connect button to slot

        # Create and style Exit button
        exit_button = QPushButton('Exit', self)
        exit_button.setStyleSheet("""
            background-color: red; 
            color: white; 
            border-radius: 50px; 
            font-size: 14px; 
            font-weight: bold;
            width: 100px; 
            height: 100px; 
            padding: 0;
            text-align: center;
            line-height: 100px;
        """)
        exit_button.clicked.connect(QApplication.instance().quit)  # Connect button to quit application

        # Layout for main buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Add space around buttons
        button_layout.addWidget(single_player_button)
        button_layout.addStretch()
        button_layout.addWidget(multiplayer_button)
        button_layout.addStretch()

        # Layout for settings button
        settings_layout = QVBoxLayout()
        settings_layout.addStretch()  # Add space above and below settings button
        settings_layout.addWidget(settings_button, alignment=Qt.AlignCenter)
        settings_layout.addStretch()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(title_label)  # Add title at the top
        main_layout.addStretch()  # Add space between title and buttons
        main_layout.addLayout(button_layout)  # Add buttons layout
        main_layout.addSpacing(20)  # Space between button row and settings button
        main_layout.addLayout(settings_layout)  # Add settings button layout
        main_layout.addStretch()  # Add space below settings button

        # Layout for exit button
        bottom_left_layout = QVBoxLayout()
        bottom_left_layout.addStretch()  # Add space above the exit button
        bottom_left_layout.addWidget(exit_button, alignment=Qt.AlignLeft)
        bottom_left_layout.setContentsMargins(20, 20, 20, 20)  # Margins around the exit button

        # Combine main layout and exit button layout
        final_layout = QHBoxLayout()
        final_layout.addLayout(main_layout)  # Add main content
        final_layout.addLayout(bottom_left_layout)  # Add exit button
        self.setLayout(final_layout)  # Set the final layout for the main menu

    # Slot functions to switch screens
    def show_single_player(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_multiplayer(self):
        self.stacked_widget.setCurrentIndex(2)

    def show_settings(self):
        self.stacked_widget.setCurrentIndex(3)


class SP_Screen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget  # Store reference to the stacked widget
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: black;")  # Set background color to black
        
        # Create and style label
        label = QLabel('Single Player Screen', self)
        label.setStyleSheet("color: white; font-size: 24px;")
        label.setAlignment(Qt.AlignCenter)  # Center the label text

        # Create and style Back button
        back_button = QPushButton('Back', self)
        back_button.clicked.connect(self.go_back)  # Connect button to slot

        # Layout for screen
        layout = QVBoxLayout()
        layout.addWidget(label)  # Add label
        layout.addStretch()  # Add space between label and button
        layout.addWidget(back_button)  # Add Back button
        self.setLayout(layout)  # Set the layout for this screen

    def go_back(self):
        self.stacked_widget.setCurrentIndex(0)  # Switch to main menu


class MP_Screen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget  # Store reference to the stacked widget
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: black;")  # Set background color to black
        
        # Create and style label
        label = QLabel('Multiplayer Screen', self)
        label.setStyleSheet("color: white; font-size: 24px;")
        label.setAlignment(Qt.AlignCenter)  # Center the label text

        # Create and style Back button
        back_button = QPushButton('Back', self)
        back_button.clicked.connect(self.go_back)  # Connect button to slot

        # Layout for screen
        layout = QVBoxLayout()
        layout.addWidget(label)  # Add label
        layout.addStretch()  # Add space between label and button
        layout.addWidget(back_button)  # Add Back button
        self.setLayout(layout)  # Set the layout for this screen

    def go_back(self):
        self.stacked_widget.setCurrentIndex(0)  # Switch to main menu


class Settings_Screen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget  # Store reference to the stacked widget
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: black;")  # Set background color to black
        
        # Create and style label
        label = QLabel('Settings Screen', self)
        label.setStyleSheet("color: white; font-size: 24px;")
        label.setAlignment(Qt.AlignCenter)  # Center the label text

        # Create and style Back button
        back_button = QPushButton('Back', self)
        back_button.clicked.connect(self.go_back)  # Connect button to slot

        # Layout for screen
        layout = QVBoxLayout()
        layout.addWidget(label)  # Add label
        layout.addStretch()  # Add space between label and button
        layout.addWidget(back_button)  # Add Back button
        self.setLayout(layout)  # Set the layout for this screen

    def go_back(self):
        self.stacked_widget.setCurrentIndex(0)  # Switch to main menu


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Navigation Example')  # Set window title
        self.setStyleSheet("background-color: black;")  # Set background color to black
        
        # Create stacked widget and screens
        self.stacked_widget = QStackedWidget()
        self.main_menu = MainMenu(self.stacked_widget)
        self.sp_screen = SP_Screen(self.stacked_widget)
        self.mp_screen = MP_Screen(self.stacked_widget)
        self.settings_screen = Settings_Screen(self.stacked_widget)

        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.sp_screen)
        self.stacked_widget.addWidget(self.mp_screen)
        self.stacked_widget.addWidget(self.settings_screen)

        # Main layout for the app
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)  # Add stacked widget
        self.setLayout(layout)  # Set the layout for the main app window

        self.showFullScreen()  # Show the app in full screen


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()  # Create and show the application
    sys.exit(app.exec_())  # Execute the application
