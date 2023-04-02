# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import weakref

from pyface.qt import QtGui, QtCore

from .find_widget import FindWidget


class ReplaceWidget(FindWidget):
    def __init__(self, parent):
        # We explicitly call __init__ on the classes which FindWidget inherits from
        # instead of calling FindWidget.__init__.
        super(FindWidget, self).__init__(parent)
        self.adv_code_widget = weakref.ref(parent)

        # QFontMetrics.width() is deprecated and Qt docs suggest using
        # horizontalAdvance() instead, but is only available since Qt 5.11
        if QtCore.__version_info__ >= (5, 11):
            self.button_size = self.fontMetrics().horizontalAdvance("Replace All") + 20
        else:
            self.button_size = self.fontMetrics().width("Replace All") + 20

        form_layout = QtGui.QFormLayout()
        form_layout.addRow("Fin&d", self._create_find_control())
        form_layout.addRow("Rep&lace", self._create_replace_control())

        layout = QtGui.QHBoxLayout()
        layout.addLayout(form_layout)

        close_button = QtGui.QPushButton("Close")
        layout.addWidget(close_button, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        close_button.clicked.connect(self.hide)

        self.setLayout(layout)

    def _create_replace_control(self):
        control = QtGui.QWidget(self)

        self.replace_edit = QtGui.QLineEdit()
        self.replace_button = QtGui.QPushButton("&Replace")
        self.replace_button.setFixedWidth(self.button_size)
        self.replace_all_button = QtGui.QPushButton("Replace &All")
        self.replace_all_button.setFixedWidth(self.button_size)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.replace_edit)
        layout.addWidget(self.replace_button)
        layout.addWidget(self.replace_all_button)
        layout.addStretch(2)
        layout.setContentsMargins(0, 0, 0, 0)

        control.setLayout(layout)
        return control
