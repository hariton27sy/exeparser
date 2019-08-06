#!/usr/bin/python3
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QAction, qApp
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtGui import QIcon
import sys


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_menu()
        self.show()

    def add_menu(self):
        pass

    def set_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu('File')
        exit_action = QAction('Quit', self)
        exit_action.triggered.connect(qApp.exit)
        file_menu.addAction(exit_action)
        self.setMenuBar(menu)



def main():
    app = QApplication(sys.argv)

    gui = GUI()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


