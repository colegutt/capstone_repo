import sys
from PyQt5.QtWidgets import QApplication
from application_init import ApplicationInit


def main():
    app = QApplication(sys.argv)
    ex = ApplicationInit()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()