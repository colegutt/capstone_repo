from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout 

class GeneralFunctions(QWidget):
    def __init__(self, stacked_widget):
        self.stacked_widget = stacked_widget
        super().__init__()
    
    def create_back_layout(self, index):
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
        back_button.clicked.connect(lambda checked, index=index: self.go_back(index))

        back_layout = QHBoxLayout()
        back_layout.addWidget(back_button)
        back_layout.addStretch()
        back_layout.setContentsMargins(20, 20, 20, 20)

        return back_layout
    
    def go_back(self, index):
        self.stacked_widget.setCurrentIndex(0)