"""
Qt-specific tests for the MessageDialog
"""

import unittest

from pyface.api import MessageDialog
from pyface.qt import QtGui
from pyface.ui.qt4.util.gui_test_assistant import GuiTestAssistant


class TestMessageDialog(GuiTestAssistant, unittest.TestCase):
    def test_escape_button_no_details(self):
        dialog = MessageDialog(
            parent=None,
            title=u"Dialog title",
            message=u"Printer on fire",
            informative=u"Your printer is on fire",
            severity=u"error",
            size=(600, 400),
        )

        with self.event_loop():
            dialog._create()

        try:
            escape_button = dialog.control.escapeButton()
            ok_button = dialog.control.button(QtGui.QMessageBox.Ok)
            # It's possible for both the above to be None, so double check.
            self.assertIsNotNone(escape_button)
            self.assertIs(escape_button, ok_button)
        finally:
            with self.event_loop():
                dialog.destroy()

    def test_escape_button_with_details(self):
        dialog = MessageDialog(
            parent=None,
            title=u"Dialog title",
            message=u"Printer on fire",
            informative=u"Your printer is on fire",
            details=u"Temperature exceeds 1000 degrees",
            severity=u"error",
            size=(600, 400),
        )

        with self.event_loop():
            dialog._create()

        try:
            escape_button = dialog.control.escapeButton()
            ok_button = dialog.control.button(QtGui.QMessageBox.Ok)
            # It's possible for both the above to be None, so double check.
            self.assertIsNotNone(escape_button)
            self.assertIs(escape_button, ok_button)
        finally:
            with self.event_loop():
                dialog.destroy()
