import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class FullScreenWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set the window to be frameless and full-screen
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()
        
        # Create an Exit button
        exit_button = QPushButton('Exit', self)
        exit_button.clicked.connect(self.close)
        
        # Create a layout and add the button
        layout = QVBoxLayout()
        layout.addStretch()  # Add stretchable space before the button
        layout.addWidget(exit_button)  # Add button to the layout
        self.setLayout(layout)
   
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    if os.environ.get('WAYLAND_DISPLAY'):
        print('yes')
    else:
        print('no')
    app = QApplication([])
    window = FullScreenWindow()
    app.exec()
