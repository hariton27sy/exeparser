from PyQt5.QtWidgets import (QWidget, QTableWidget, QTableWidgetItem,
                             QGridLayout, QLabel, QAbstractItemView,
                             QHeaderView, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from common_funcs import hex_from_bytes


def count_positions(dic: dict):
    """Simple counter of positions that are not None"""
    count = 0
    for name in dic:
        if (isinstance(dic, dict) and dic[name] is not None or
                isinstance(dic, (tuple, list)) and name is not None):
            count += 1
    return count


def fill_table(table, data, descriptions):
    """Function for HeaderInfoClass. It fills file_header
    and optional_header tables"""
    headers = table.horizontalHeader()
    headers.setSectionResizeMode(0, QHeaderView.ResizeToContents)
    headers.setSectionResizeMode(1, QHeaderView.ResizeToContents)
    headers.setSectionResizeMode(2, QHeaderView.Stretch)

    pos = 0
    for name in data:
        if name not in descriptions or descriptions[name] is None:
            continue

        # Filling names of Fields
        if isinstance(descriptions[name], str):
            item = QTableWidgetItem(descriptions[name])
        else:
            item = QTableWidgetItem(descriptions[name][0])
        item.setToolTip(item.text())
        table.setItem(pos, 0, item)

        # Filling hex values of fields
        item = QTableWidgetItem(hex(int.from_bytes(data[name][0], 'little')))
        item.setToolTip(item.text())
        table.setItem(pos, 1, item)

        # Filling interpreted values of fields
        # if they are strings, special cases are processed in senders
        if isinstance(data[name][1], str):
            item = QTableWidgetItem(data[name][1])
            item.setToolTip(item.text())
            table.setItem(pos, 2, item)

        pos += 1


def draw_characteristics(description, data):
    """Function for HeaderInfo class. It creates new Widget
    that didn't have parent"""
    widget = QWidget()
    widget.setWindowTitle(description[0])
    grid = QGridLayout()
    widget.setLayout(grid)
    for i in range(len(data)):
        if description[1][i] is None:
            continue
        grid.addWidget(QLabel(description[1][i]), i, 0)
        grid.addWidget(QLabel('YES' if data[i] else 'NO'), i, 1)

    return widget


class HeadersInfo(QWidget):
    """Class that creates widget with main
    info about headers of executable file"""

    def __init__(self, parent):
        super().__init__()
        self.parent_ = parent

        # Separate windows
        self.characteristics = draw_characteristics(
            self.parent_.lang.
            headers_info[1]['file_header'][2]['characteristics'],
            self.parent_.exe_file.file_header['characteristics'][1])

        self.dll_characteristics = draw_characteristics(
            self.parent_.lang.headers_info[1]['optional_header'][2]
            ['dllCharacteristics'],
            self.parent_.exe_file.optional_header['dllCharacteristics'][1])

        grid = QGridLayout()
        self.setLayout(grid)
        name = QLabel(parent.lang.headers_info[0])
        name.setFont(QFont('sansSerif', 14, QFont.Bold))
        name.setAlignment(Qt.AlignCenter)
        grid.addWidget(name, 0, 0, 1, 2)
        grid.addWidget(self.draw_subwidget(
            self.parent_.lang.headers_info[1]['file_header'][0],
            self.draw_file_header_table()), 1, 0)
        grid.addWidget(self.draw_subwidget(
            self.parent_.lang.headers_info[1]['optional_header'][0],
            self.draw_optional_header_table()), 1, 1)

    def draw_file_header_table(self):
        header_lang = self.parent_.lang.headers_info[1]['file_header']
        table = QTableWidget(count_positions(header_lang[2]), 3)

        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        table.setHorizontalHeaderLabels(header_lang[1])

        fill_table(table, self.parent_.exe_file.file_header, header_lang[2])

        fields = self.parent_.exe_file.file_header

        date_index = (list(fields.keys()).index('creatingTime'))
        form = header_lang[2]['creatingTime'][1] if isinstance(
            header_lang[2]['creatingTime'],
            tuple) else fields['creatingTime'][2]
        item = QTableWidgetItem(fields['creatingTime'][1](form))
        item.setToolTip(item.text())
        table.setItem(date_index, 2, item)

        char_index = (list(fields.keys()).index('characteristics'))
        item = QPushButton('click me')
        item.clicked.connect(self.characteristics.show)
        table.setIndexWidget(table.model().index(char_index, 2), item)

        return table

    def draw_optional_header_table(self):
        header_lang = self.parent_.lang.headers_info[1]['optional_header']
        table = QTableWidget(count_positions(header_lang[2]), 3)

        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        table.setHorizontalHeaderLabels(header_lang[1])

        fill_table(table,
                   self.parent_.exe_file.optional_header, header_lang[2])

        char_index = (list(
            self.parent_.exe_file.optional_header.keys()).
                      index('dllCharacteristics'))
        item = QPushButton('click me')
        item.clicked.connect(self.dll_characteristics.show)
        table.setIndexWidget(table.model().index(char_index, 2), item)

        subsystem_index = (list(self.parent_.exe_file.optional_header.keys()).
                           index('subsystem'))
        subsystem = (header_lang[2]['subsystem'][1][int(
            self.parent_.exe_file.optional_header['subsystem'][1])]
            if int(self.parent_.exe_file.optional_header['subsystem'][1]) in
            header_lang[2]['subsystem'][1]
            else header_lang[2]['subsystem'][2])
        item = QTableWidgetItem(subsystem)
        item.setToolTip(subsystem)
        table.setItem(subsystem_index, 2, item)

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


class DataDirectoryTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent_ = parent
        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(QLabel(self.parent_.lang.data_directory_tab[0]), 0, 0)
        grid.addWidget(self.make_table(), 1, 0)

    def make_table(self):
        table = QTableWidget(count_positions(
            self.parent_.lang.data_directory_tab[2]), 3)
        table.setHorizontalHeaderLabels(
            self.parent_.lang.data_directory_tab[1])
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        headers = table.horizontalHeader()
        headers.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        headers.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        headers.setSectionResizeMode(2, QHeaderView.Stretch)

        data = self.parent_.exe_file.optional_header['dataDirectory']
        description = self.parent_.lang.data_directory_tab[2]
        for i in range(int(self.
                           parent_.
                           exe_file.
                           optional_header['numberOfRvaAndSizes'][1])):
            if description[i] is None:
                continue

            item = QTableWidgetItem(description[i])
            item.setToolTip(item.text())
            table.setItem(i, 0, item)

            item = QTableWidgetItem(hex(
                int.from_bytes(data[i][0], 'little'))[2:])
            item.setToolTip(item.text())
            table.setItem(i, 1, item)

            item = QTableWidgetItem(
                hex(int.from_bytes(data[i][1], 'little'))[2:])
            item.setToolTip(str(int(item.text(), 16)) + ' bytes')
            table.setItem(i, 2, item)

        return table


class SectionHeadersTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent_ = parent
        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(QLabel(self.parent_.lang.section_headers_tab[0]), 0, 0)
        grid.addWidget(self.make_table(), 1, 0)

    def make_table(self):
        # TODO: Rewrite filling section_headers table
        horizontal = count_positions(self.parent_.lang.section_headers_tab[1])
        vertical = len(self.parent_.exe_file.section_headers)
        table = QTableWidget(vertical, horizontal)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Edit headers
        table.verticalHeader().setVisible(False)
        table.setHorizontalHeaderLabels(
            self.parent_.lang.section_headers_tab[1])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i in range(horizontal):
            (table.
             horizontalHeaderItem(i).
             setToolTip(table.horizontalHeaderItem(i).text()))

        # Filling data
        v_pos = 0
        for section in self.parent_.exe_file.section_headers:
            h_pos = 0
            for item in section.values():
                table.setItem(
                    v_pos, h_pos,
                    QTableWidgetItem(hex_from_bytes(item)
                                     if item[0] != '.' else item))
                table.item(v_pos, h_pos).setToolTip(
                    str(int.from_bytes(item, 'little'))
                    if item[0] != '.' else item)
                h_pos += 1
            v_pos += 1

        return table
