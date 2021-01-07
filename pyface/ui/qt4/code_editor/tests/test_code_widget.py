# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import unittest
from unittest import mock


from pyface.qt import QtCore, QtGui
from pyface.qt.QtTest import QTest


from pyface.ui.qt4.code_editor.code_widget import (
    CodeWidget,
    AdvancedCodeWidget,
)


class TestCodeWidget(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.qapp = QtGui.QApplication.instance() or QtGui.QApplication([])

    def tearDown(self):
        self.qapp.processEvents()

    def test_different_lexer(self):
        # Setting a different lexer should not fail.
        # See enthought/traitsui#982
        cw = CodeWidget(None, lexer="yaml")
        text = "number: 1"
        cw.setPlainText(text)

    def test_readonly_editor(self):
        cw = CodeWidget(None)
        text = "Some\nText"
        cw.setPlainText(text)

        def check(typed, expected):
            cursor = cw.textCursor()
            cursor.setPosition(0)
            cw.setTextCursor(cursor)
            QTest.keyClicks(cw, typed)
            self.assertEqual(cw.toPlainText(), expected)

        cw.setReadOnly(True)
        check("More", text)

        cw.setReadOnly(False)
        check("Extra", "Extra" + text)

    def test_readonly_replace_widget(self):
        acw = AdvancedCodeWidget(None)
        text = "Some\nText"
        acw.code.setPlainText(text)
        acw.show()

        # On some platforms, Find/Replace do not have default keybindings
        FindKey = QtGui.QKeySequence("Ctrl+F")
        ReplaceKey = QtGui.QKeySequence("Ctrl+H")
        patcher_find = mock.patch("pyface.qt.QtGui.QKeySequence.Find", FindKey)
        patcher_replace = mock.patch(
            "pyface.qt.QtGui.QKeySequence.Replace", ReplaceKey
        )
        patcher_find.start()
        patcher_replace.start()
        self.addCleanup(patcher_find.stop)
        self.addCleanup(patcher_replace.stop)

        def click_key_seq(widget, key_seq):
            if not isinstance(key_seq, QtGui.QKeySequence):
                key_seq = QtGui.QKeySequence(key_seq)
            try:
                # QKeySequence on python3-pyside does not have `len`
                first_key = key_seq[0]
            except IndexError:
                return False
            key = QtCore.Qt.Key(first_key & ~QtCore.Qt.KeyboardModifierMask)
            modifier = QtCore.Qt.KeyboardModifier(
                first_key & QtCore.Qt.KeyboardModifierMask
            )
            QTest.keyClick(widget, key, modifier)
            return True

        acw.code.setReadOnly(True)
        if click_key_seq(acw, FindKey):
            self.assertTrue(acw.find.isVisible())
            acw.find.hide()

        acw.code.setReadOnly(False)
        if click_key_seq(acw, FindKey):
            self.assertTrue(acw.find.isVisible())
            acw.find.hide()

        acw.code.setReadOnly(True)
        if click_key_seq(acw, ReplaceKey):
            self.assertFalse(acw.replace.isVisible())

        acw.code.setReadOnly(False)
        if click_key_seq(acw, ReplaceKey):
            self.assertTrue(acw.replace.isVisible())
        acw.replace.hide()
        self.assertFalse(acw.replace.isVisible())


if __name__ == "__main__":
    unittest.main()
