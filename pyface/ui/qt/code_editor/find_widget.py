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


class FindWidget(QtGui.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.adv_code_widget = weakref.ref(parent)

        # QFontMetrics.width() is deprecated and Qt docs suggest using
        # horizontalAdvance() instead, but is only available since Qt 5.11
        if QtCore.__version_info__ >= (5, 11):
            self.button_size = self.fontMetrics().horizontalAdvance("Replace All") + 20
        else:
            self.button_size = self.fontMetrics().width("Replace All") + 20

        form_layout = QtGui.QFormLayout()
        form_layout.addRow("Fin&d", self._create_find_control())

        layout = QtGui.QHBoxLayout()
        layout.addLayout(form_layout)

        close_button = QtGui.QPushButton("Close")
        layout.addWidget(close_button, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        close_button.clicked.connect(self.hide)

        self.setLayout(layout)

    def setFocus(self):
        self.line_edit.setFocus()

    def _create_find_control(self):
        control = QtGui.QWidget(self)

        self.line_edit = QtGui.QLineEdit()
        self.next_button = QtGui.QPushButton("&Next")
        self.next_button.setFixedWidth(self.button_size)
        self.prev_button = QtGui.QPushButton("&Prev")
        self.prev_button.setFixedWidth(self.button_size)
        self.options_button = QtGui.QPushButton("&Options")
        self.options_button.setFixedWidth(self.button_size)

        options_menu = QtGui.QMenu(self)
        self.case_action = QtGui.QAction("Match &case", options_menu)
        self.case_action.setCheckable(True)
        self.word_action = QtGui.QAction("Match words", options_menu)
        self.word_action.setCheckable(True)
        self.wrap_action = QtGui.QAction("Wrap search", options_menu)
        self.wrap_action.setCheckable(True)
        self.wrap_action.setChecked(True)
        options_menu.addAction(self.case_action)
        options_menu.addAction(self.word_action)
        options_menu.addAction(self.wrap_action)
        self.options_button.setMenu(options_menu)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.line_edit)
        layout.addWidget(self.next_button)
        layout.addWidget(self.prev_button)
        layout.addWidget(self.options_button)
        layout.addStretch(2)
        layout.setContentsMargins(0, 0, 0, 0)

        control.setLayout(layout)
        return control
