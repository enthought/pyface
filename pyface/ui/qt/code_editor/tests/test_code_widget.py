# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import unittest


from pyface.qt import QtGui
from pyface.qt.QtTest import QTest


from pyface.ui.qt.code_editor.code_widget import (
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

        def click_key_seq(widget, key_seq):
            if not isinstance(key_seq, QtGui.QKeySequence):
                key_seq = QtGui.QKeySequence(key_seq)
            QTest.keySequence(widget, key_seq)
            return True

        acw.code.setReadOnly(True)
        if click_key_seq(acw, acw.find_key):
            self.assertTrue(acw.find.isVisible())
            acw.find.hide()

        acw.code.setReadOnly(False)
        if click_key_seq(acw, acw.find_key):
            self.assertTrue(acw.find.isVisible())
            acw.find.hide()

        acw.code.setReadOnly(True)
        if click_key_seq(acw, acw.replace_key):
            self.assertFalse(acw.replace.isVisible())

        acw.code.setReadOnly(False)
        if click_key_seq(acw, acw.replace_key):
            self.assertTrue(acw.replace.isVisible())
        acw.replace.hide()
        self.assertFalse(acw.replace.isVisible())
