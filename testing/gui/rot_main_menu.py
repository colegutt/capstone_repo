import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QTransform, QFontMetrics
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel

# Custom button class with rotated text
class RotatedButton(QPushButton):
    def __init__(self, text, color, parent=None):
        super().__init__(text, parent)
        self.color = color  # Store the color for later use

    def paintEvent(self, event):
        painter = QPainter(self)

        # Set the background color to red
        painter.setBrush(self.color)
        painter.setPen(self.color)
        painter.drawRect(self.rect())  # Draw the red background

        # Apply the transformation for rotating the text
        transform = QTransform()
        transform.translate(self.width(), 0)  # Translate before rotating
        transform.rotate(90)  # Rotate 90 degrees
        painter.setTransform(transform)

        # Set the text color to white
        painter.setPen(Qt.white)

        metrics = QFontMetrics(self.font())
        text_width = metrics.width(self.text())
        text_height = metrics.height()

        # Center the text within the rotated area
        painter.drawText(
            (self.height() - text_width) // 2,
            (self.width() + text_height) // 2,
            self.text()
        )

        painter.end()

# Custom label class with rotated text
class RotatedLabel(QLabel):
    def paintEvent(self, event):
        painter = QPainter(self)
        transform = QTransform()
        transform.translate(self.width(), 0)  # Translate before rotating
        transform.rotate(90)  # Rotate 90 degrees
        painter.setTransform(transform)

        metrics = QFontMetrics(self.font())
        text_width = metrics.width(self.text())
        text_height = metrics.height()

        # Center the text within the rotated area
        painter.drawText(
            (self.height() - text_width) // 2,
            (self.width() + text_height) // 2,
            self.text()
        )
        painter.end()

class RotMainMenu(QWidget):
    def __init__(self, stacked_widget=None):
        super().__init__()
        self.setStyleSheet("background-color: black; border: none;")
        self.stacked_widget = stacked_widget

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Rotated Main Menu')

        # Create rotated title
        rotated_title = RotatedLabel('BEEPY', self)
        rotated_title.setStyleSheet("color: white; font-size: 48px; font-weight: bold; background: transparent;")
        rotated_title.resize(100, 300)

        exit_button = self.create_exit_button()
        # single_player_button = self.create_SP_button()
        # multiplayer_button = self.create_MP_button()
        # settings_button = self.create_SETTINGS_button()



        # (-left/+right, -up/+down)
        rotated_title.move(900, 150)
        exit_button.move(0, 0) 
        # single_player_button.move(0,0)
        # multiplayer_button.move(0,0)
        # settings_button.move(0,0)
    
    def create_exit_button(self):
        exit_button = RotatedButton('Exit', color=Qt.red, parent=self)
        exit_button.setStyleSheet("""
            color: white; 
            border-radius: 0px; 
            font-size: 16px; 
            font-weight: bold;
            padding: 0;
            text-align: center;
            line-height: 50px;
        """)
        exit_button.clicked.connect(QApplication.instance().quit)
        exit_button.resize(50, 150)
        return exit_button
        

