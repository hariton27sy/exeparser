from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, qApp,
                             QFileDialog, QLabel, QWidget)


class Resources(QMainWindow):
    def __init__(self, exeFile):
        self.exeFile = exeFile
        self.app = QApplication([])
        super().__init__()
        pass
