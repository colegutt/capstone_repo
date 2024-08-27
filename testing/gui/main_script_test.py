import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QStackedWidget
from main_menu import MainMenu


def main():
    # Initialize application
    app = QApplication(sys.argv)

    # # Create stacked widget and screens
    # stacked_widget = QStackedWidget()
    # main_menu = MainMenu(stacked_widget)
    # sp_screen = SP_Screen(stacked_widget)
    # mp_screen = MP_Screen(stacked_widget)
    # ssettings_screen = Settings_Screen(stacked_widget)

    # # Create stacked widget and add screens
    # stacked_widget = QStackedWidget()
    # stacked_widget.addWidget(MainMenu(stacked_widget))
    # stacked_widget.addWidget(SP_Screen(stacked_widget))
    # stacked_widget.addWidget(MP_Screen(stacked_widget))
    # stacked_widget.addWidget(Settings_Screen(stacked_widget))

    # # Main layout for the application
    # layout = QVBoxLayout()
    # layout.addWidget(self.stacked_widget)
    # self.setLayout(layout)

    window = MainMenu(QStackedWidget())
    window.showFullScreen()  # Show the window in full screen
    sys.exit(app.exec_())  # Start the event loop

if __name__ == '__main__':
    main()
