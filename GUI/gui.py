#!/usr/bin/python3

from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QAction, qApp, QFileDialog
import sys

from GUI import headers_window
from langs import langs
from core.exe_file import exe_file

WIDTH, HEIGHT = 900, 400


class GUI(QMainWindow):
    def __init__(self):
        # Connection localisation

        self.curr_language = 'English'
        self.lang = langs[self.curr_language]
        self.exe_file = exe_file('examples/pexplorer.exe')
        self.app = QApplication([])
        super().__init__()
        size = self.app.primaryScreen().size()
        self.setGeometry((size.width() - WIDTH) // 2, (size.height() - HEIGHT) // 2, WIDTH, HEIGHT)
        self.draw_menu()
        self.draw_toolbar()
        self.show()
        self.setCentralWidget(headers_window.HeadersInfo(self))
        sys.exit(self.app.exec_())

    def draw_menu(self):
        menu = self.menuBar()
        file = menu.addMenu('File')

        open_file = QAction('Open file', self)
        open_file.setShortcut('Ctrl+O')
        open_file.triggered.connect(self.show_open_dialog)

        exit_menu = QAction('Exit', self)
        exit_menu.triggered.connect(qApp.exit)
        exit_menu.setShortcut('Ctrl+Q')

        file.addAction(open_file)
        file.addAction(exit_menu)

    def show_open_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File')[0]
        print(fname)

    def draw_toolbar(self):
        pass


def main():
    GUI()


if __name__ == '__main__':
    main()
