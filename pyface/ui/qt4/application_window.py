from pyface.qt import QtGui
from .window import Window


class ApplicationWindow(Window):
    def _create(self):
        super()._create()
        contents = QtGui.QWidget(self.control)
        self.control.setCentralWidget(contents)

    def _create_control(self, parent):
        return super()._create_control(parent)
