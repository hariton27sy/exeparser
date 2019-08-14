from PyQt5.QtWidgets import (QWidget, QTableWidget, QTableWidgetItem, QGridLayout, QLabel, QAbstractItemView,
                             QHeaderView, QPushButton, QTableView)
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QFont


def count_positions(dic: dict):
    count = 0
    for name in dic:
        if dic[name] is not None:
            count += 1
    return count


def fill_table(table, data, descriptions):
    headers = table.horizontalHeader()
    headers.setSectionResizeMode(0, QHeaderView.ResizeToContents)
    headers.setSectionResizeMode(1, QHeaderView.ResizeToContents)
    headers.setSectionResizeMode(2, QHeaderView.Stretch)

    pos = 0
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    for name in data:
        if name not in descriptions or descriptions[name] is None:
            continue

        if isinstance(descriptions[name], str):
            item = QTableWidgetItem(descriptions[name])
        else:
            item = QTableWidgetItem(descriptions[name][0])
        item.setToolTip(item.text())
        table.setItem(pos, 0, item)

        item = QTableWidgetItem(hex(int.from_bytes(data[name][0], 'little')))
        item.setToolTip(item.text())
        table.setItem(pos, 1, item)

        if isinstance(data[name][1], str):
            item = QTableWidgetItem(data[name][1])
            item.setToolTip(item.text())
            table.setItem(pos, 2, item)

        pos += 1


class HeadersInfo(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        grid = QGridLayout()
        self.setLayout(grid)
        name = QLabel(parent.lang.headers_info[0])
        name.setFont(QFont('sansSerif', 14, QFont.Bold))
        name.setAlignment(Qt.AlignCenter)
        grid.addWidget(name, 0, 0, 1, 2)
        grid.addWidget(self.draw_subwidget(self.parent.lang.headers_info[1]['file_header'][0],
                                           self.draw_file_header_table()), 1, 0)
        grid.addWidget(self.draw_subwidget(self.parent.lang.headers_info[1]['optional_header'][0],
                                           self.draw_optional_header_table()), 1, 1)

    def draw_file_header_table(self):
        header_lang = self.parent.lang.headers_info[1]['file_header']
        table = QTableWidget(count_positions(header_lang[2]), 3)

        table.verticalHeader().setVisible(False)
        table.setHorizontalHeaderLabels(header_lang[1])

        fill_table(table, self.parent.exe_file.file_header, header_lang[2])

        fields = self.parent.exe_file.file_header

        date_index = (list(fields.keys()).index('creatingTime'))
        form = header_lang[2]['creatingTime'][1] if isinstance(
            header_lang[2]['creatingTime'], tuple) else fields['creatingTime'][2]
        item = QTableWidgetItem(fields['creatingTime'][1](form))
        item.setToolTip(item.text())
        table.setItem(date_index, 2, item)

        char_index = (list(fields.keys()).index('characteristics'))
        item = QPushButton('click me')
        self.char_menu = self.draw_characteristics()
        item.clicked.connect(self.char_menu.show)
        table.setIndexWidget(table.model().index(char_index, 2), item)

        return table

    def draw_optional_header_table(self):
        header_lang = self.parent.lang.headers_info[1]['optional_header']
        table = QTableWidget(count_positions(header_lang[2]), 3)
        table.verticalHeader().setVisible(False)
        table.setHorizontalHeaderLabels(header_lang[1])

        fill_table(table, self.parent.exe_file.optional_header, header_lang[2])

        return table

    def draw_subwidget(self, name: str, table: QWidget):
        widget = QWidget(self)
        grid = QGridLayout()
        widget.setLayout(grid)

        name = QLabel(name)
        name.setAlignment(Qt.AlignCenter)
        grid.addWidget(name, 0, 0)
        grid.addWidget(table, 1, 0)
        return widget

    def draw_characteristics(self):
        widget = QWidget()
        grid = QGridLayout()
        widget.setLayout(grid)
        description = self.parent.lang.headers_info[1]['file_header'][2]['characteristics']
        data = self.parent.exe_file.file_header['characteristics'][1]
        for i in range(len(data)):
            if description[1][i] is None:
                continue
            grid.addWidget(QLabel(description[1][i]), i, 0)
            grid.addWidget(QLabel('YES' if data[i] else 'NO'), i, 1)

        return widget
