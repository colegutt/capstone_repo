import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QTransform, QFontMetrics
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel

# Custom button class with rotated text
class RotatedButton(QPushButton):
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
        rotated_title.move(900, 150)

        # Create rotated exit button
        exit_button = RotatedButton('Exit', self)
        exit_button.setStyleSheet("""
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
        exit_button.clicked.connect(QApplication.instance().quit)
        exit_button.resize(50, 150)
        exit_button.move(200, 400)  # Adjust position as needed

if __name__ == '__main__':
    app = QApplication([])
    main_win = RotMainMenu()
    main_win.show()
    sys.exit(app.exec_())
