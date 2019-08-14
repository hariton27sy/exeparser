#!/usr/bin/python3

from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, qApp, QFileDialog, QLabel, QWidget
from PyQt5.QtGui import QFont
import sys
import webbrowser  # for open external link in browser

from GUI import headers_window
from langs import langs
from core.exe_file import exe_file

WIDTH, HEIGHT = 900, 400


def open_external():
    webbrowser.open('https://habr.com/ru/post/266831/')


class GUI(QMainWindow):
    def __init__(self):
        # Connection localisation
        self.curr_language = 'Russian'
        self.lang = langs[self.curr_language]
        self.exe_file = None

        self.app = QApplication([])
        super().__init__()
        size = self.app.primaryScreen().size()
        self.setGeometry((size.width() - WIDTH) // 2, (size.height() - HEIGHT) // 2, WIDTH, HEIGHT)
        self.draw_menu()
        self.draw_toolbar()
        self.draw_main_win()
        self.test_interface()
        self.show()
        sys.exit(self.app.exec_())

    def draw_menu(self):
        """Drawing menu"""
        menu = self.menuBar()
        file = menu.addMenu('File')

        open_file = QAction('Open file', self)
        open_file.setShortcut('Ctrl+O')
        open_file.triggered.connect(self.show_open_dialog)

        exit_menu = QAction('Exit', self)
        exit_menu.triggered.connect(qApp.exit)
        exit_menu.setShortcut('Ctrl+Q')

        help = menu.addMenu('Help')
        help.addAction('Article about EXE format', open_external)



        file.addAction(open_file)
        file.addAction(exit_menu)

    def show_open_dialog(self):
        """Open file and preparing workspace"""
        fname = QFileDialog.getOpenFileName(self, 'Open File', filter='executable files (*.exe)')[0]
        print(fname)

    def draw_toolbar(self):
        pass

    def draw_main_win(self):
        """Drawing tab when a file are not opened"""
        widget = QWidget(self)
        label = QLabel(self.lang.main_page, widget)
        label.setFont(QFont('sans Serif', 12))
        self.setCentralWidget(widget)
        label.move(10, 10)

    def test_interface(self):
        self.exe_file = exe_file('../examples/qoob.exe')
        self.setCentralWidget(headers_window.HeadersInfo(self))

def main():
    GUI()


if __name__ == '__main__':
    main()
