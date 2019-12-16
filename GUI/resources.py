import sys

from PyQt5 import QtWidgets, QtGui, QtCore

from common_funcs import formatted_output
from core.exefile import ExeFile
from core.resources import ResourceTable

WIDTH, HEIGHT = 600, 400


class ResourcesWidget(QtWidgets.QWidget):
    def __init__(self, exeFile):
        app = QtWidgets.QApplication([])
        super().__init__()
        self.exeFile = exeFile
        self.resize(WIDTH, HEIGHT)

        self.lt = QtWidgets.QHBoxLayout(self)

        self.viewer = ResourceViewer(self)
        self.lt.addWidget(ResourcesList(self), 0)
        self.lt.addWidget(self.viewer, 1)

        self.show()

        sys.exit(app.exec_())


def pix_map_from_data(data):
    qp = QtGui.QPixmap()
    qp.loadFromData(data)
    return qp


class ResourcesList(QtWidgets.QTreeWidget):
    def __init__(self, parent: ResourcesWidget):
        self.parent = parent
        super().__init__(parent)
        self.setHeaderHidden(True)
        self.setFixedWidth(200)

        self.table = parent.exeFile.resources().table
        self.itemClicked.connect(self.onClick)
        for e in self.table.elements:
            self.addTopLevelItem(self.make_tree(e))

    def onClick(self, item):
        if item.element.elements[0].type == 1:
            data = self.parent.exeFile.get_resource(
                self.table, item.element.elements[0])

            with open("test.png", 'wb') as f:
                f.write(data)

            widget = HexDumpWidget(data, self.parent.viewer)
            if item.element.resourceType == "ICON":
                scrollArea = QtWidgets.QScrollArea(self.parent.viewer)

                widget = QtWidgets.QLabel(self.parent)
                pq = pix_map_from_data(data)
                widget.setPixmap(pq)
                widget.resize(pq.size())
                scrollArea.setWidget(widget)
                widget = scrollArea

            self.parent.viewer.setWidget(widget)
            self.parent.show()

        else:
            print("No")

    def make_tree(self, item):
        result = TreeListItem(item)
        for e in item.elements:
            if e.type == 0:
                result.addChild(self.make_tree(e))

        return result


class ResourceViewer(QtWidgets.QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.white)
        self.setPalette(p)


class TreeListItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, element: ResourceTable, *args, **kwargs):
        self.element = element
        super().__init__([str(element.name)], *args, **kwargs)


class HexDumpWidget(QtWidgets.QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent)

        result = "".join(formatted_output(0, data))

        label = QtWidgets.QLabel(result, self)
        label.setFont(QtGui.QFont("Courier"))
        lt = QtWidgets.QGridLayout(self)
        self.setLayout(lt)
        lt.addWidget(label, 1, 1)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    a = ResourcesWidget(ExeFile("../examples/firefox2.exe"))
    sys.exit(app.exec_())
