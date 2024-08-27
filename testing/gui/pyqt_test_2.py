import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

class FullScreenWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()
        
        exit_button = QPushButton('Exit', self)
        exit_button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(exit_button)
        layout.addStretch(1)
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
