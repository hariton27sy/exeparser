#!/usr/bin/python3

import os
import sys
from webbrowser import open as openweb  # for open external link in browser

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, qApp,
                             QFileDialog, QLabel, QWidget)

from GUI import headers_window
from core.exefile import ExeFile
from langs import langs

WIDTH, HEIGHT = 900, 400


def open_external():
    openweb('https://habr.com/ru/post/266831/')


class GUI(QMainWindow):
    def __init__(self, argv):
        """Initialize Graphical user interface. It is a little bit abandoned
        till I finished parsing and CLI"""
        # Connection localisation
        self.curr_language = 'English'
        self.lang = langs[self.curr_language]
        self.exe_file = None

        self.app = QApplication([])
        super().__init__()
        self.setWindowTitle('EXE Parser')
        size = self.app.primaryScreen().size()
        self.setGeometry((size.width() - WIDTH) // 2, (size.height() - HEIGHT)
                         // 2, WIDTH, HEIGHT)
        self.draw_menu()
        self.draw_toolbar()
        self.draw_main_win()
        # self.auto_open_file()
        # headers_window.DataDirectoryTab(self)
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
        fname = QFileDialog.getOpenFileName(
            self, 'Open File',
            filter='PE Files (*.exe , *.dll)')[0]
        # TODO: Check variable if it is empty or is not exe file
        if not fname:
            return
        self.exe_file = ExeFile(fname)
        self.toolbar.setDisabled(False)
        self.setWindowTitle('EXE Parser - ' + fname)
        self.setCentralWidget(headers_window.HeadersInfo(self))

    def draw_toolbar(self):
        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.setDisabled(True)

        action = QAction('H', self)
        action.triggered.connect(lambda _: self.setCentralWidget(
            headers_window.HeadersInfo(self)))
        self.toolbar.addAction(action)

        action = QAction('D', self)
        action.triggered.connect(lambda _: self.setCentralWidget(
            headers_window.DataDirectoryTab(self)))
        self.toolbar.addAction(action)

        action = QAction('S', self)
        action.triggered.connect(lambda _: self.setCentralWidget(
            headers_window.SectionHeadersTab(self)))
        self.toolbar.addAction(action)
        # TODO: Make toolbar

    def draw_main_win(self):
        """Drawing tab when a file are not opened"""
        widget = QWidget(self)
        label = QLabel(self.lang.main_page, widget)
        label.setFont(QFont('sans Serif', 12))
        self.setCentralWidget(widget)
        label.move(10, 10)

    def auto_open_file(self, file='examples/qoob.exe'):
        file = os.path.abspath(file)
        self.exe_file = ExeFile(file)
        self.toolbar.setDisabled(False)
        self.setWindowTitle('EXE Parser - ' + file)


def main():
    GUI(sys.argv)


if __name__ == '__main__':
    main()
