import sys

from PyQt5 import QtWidgets, QtGui, QtCore

from common_funcs import formatted_output
from common_funcs import get_resource_type, get_strings_from_data
from core.resources import ResourceTable


def get_resource_widget_as_main(exeFile):
    app = QtWidgets.QApplication([])
    widget = ResourcesWidget(exeFile)
    sys.exit(app.exec_())


class ResourcesWidget(QtWidgets.QWidget):
    WIDTH, HEIGHT = 600, 400

    def __init__(self, exeFile):
        super().__init__()
        self.exeFile = exeFile
        self.resize(self.WIDTH, self.HEIGHT)

        self.lt = QtWidgets.QHBoxLayout(self)

        self.viewer = ResourceViewer(self)
        self.lt.addWidget(ResourcesList(self), 0)
        self.lt.addWidget(self.viewer, 1)

        self.show()


def pix_map_from_data(data):
    qp = QtGui.QPixmap()
    qp.loadFromData(data)
    return qp


class ResourcesList(QtWidgets.QTreeWidget):
    image_types = {"ICON", "BITMAP", "CURSOR"}

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
        if item.element.name == 'STRING':
            widget = StringsWidget(self.parent.exeFile, self.parent.viewer)
            self.parent.viewer.setWidget(widget)
            self.parent.show()
        elif item.element.elements[0].type == 1:
            data = self.parent.exeFile.get_resource(item.element.elements[0])

            widget = None
            if (item.element.resourceType in self.image_types or
                    get_resource_type(data) == "image"):
                scrollArea = QtWidgets.QScrollArea(self.parent.viewer)

                widget = QtWidgets.QLabel(self.parent)
                pq = pix_map_from_data(data)
                widget.setPixmap(pq)
                widget.resize(pq.size())
                scrollArea.setWidget(widget)
                widget = scrollArea

            if item.element.resourceType == "STRING":
                widget = StringsWidget(data, self.parent.viewer)

            if item.element.resourceType == "MANIFEST":
                try:
                    data = data.decode('utf-8')
                    widget = QtWidgets.QLabel(data, self.parent.viewer)
                except Exception:
                    pass

            if not widget:
                widget = HexDumpWidget(data, self.parent.viewer)

            self.parent.viewer.setWidget(widget)
            self.parent.show()

    def make_tree(self, item):
        result = TreeListItem(item)
        if item.name != "STRING":
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


class StringsWidget(QtWidgets.QWidget):
    def __init__(self, exeFile, parent=None):
        """Need full sub-table with strings"""
        super().__init__(parent)

        label = QtWidgets.QLabel("\n".join(exeFile.string_resources()), self)
        label.setFont(QtGui.QFont("Courier"))
        lt = QtWidgets.QGridLayout(self)
        self.setLayout(lt)

        lt.addWidget(label)
