from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
def main():
    app = QApplication([])
    window = QWidget()
    
    window.setWindowFlag(Qt.FramelessWindowHint)
    window.showFullScreen()

    # Create label
    label = QLabel(window)

    # Give label text
    label.setText("Hello World!")

    # Give label font
    label.setFont(QFont("Arial", 16))
    
    # Determine where label is located
    label.move(50,100)


    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
