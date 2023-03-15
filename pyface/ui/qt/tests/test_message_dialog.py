# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""
Qt-specific tests for the MessageDialog
"""

import contextlib
import unittest

from pyface.api import MessageDialog
from pyface.qt import QtCore, QtGui
from pyface.ui.qt.util.gui_test_assistant import GuiTestAssistant


class TestMessageDialog(GuiTestAssistant, unittest.TestCase):
    def test_escape_button_no_details(self):
        dialog = MessageDialog(
            parent=None,
            title="Dialog title",
            message="Printer on fire",
            informative="Your printer is on fire",
            severity="error",
            size=(600, 400),
        )

        with self.create_dialog(dialog):
            escape_button = dialog.control.escapeButton()
            ok_button = dialog.control.button(QtGui.QMessageBox.StandardButton.Ok)
            # It's possible for both the above to be None, so double check.
            self.assertIsNotNone(escape_button)
            self.assertIs(escape_button, ok_button)

    def test_escape_button_with_details(self):
        dialog = MessageDialog(
            parent=None,
            title="Dialog title",
            message="Printer on fire",
            informative="Your printer is on fire",
            details="Temperature exceeds 1000 degrees",
            severity="error",
            size=(600, 400),
        )

        with self.create_dialog(dialog):
            escape_button = dialog.control.escapeButton()
            ok_button = dialog.control.button(QtGui.QMessageBox.StandardButton.Ok)
            # It's possible for both the above to be None, so double check.
            self.assertIsNotNone(escape_button)
            self.assertIs(escape_button, ok_button)

    def test_text_format(self):
        dialog = MessageDialog(
            parent=None,
            title="Dialog title",
            message="Printer on fire",
            informative="Your printer is on fire",
            details="Temperature exceeds 1000 degrees",
            severity="error",
            text_format="plain",
            size=(600, 400),
        )

        with self.create_dialog(dialog):
            text_format = dialog.control.textFormat()
            self.assertEqual(text_format, QtCore.Qt.TextFormat.PlainText)

    @contextlib.contextmanager
    def create_dialog(self, dialog):
        """
        Create a dialog, then destroy at the end of a with block.
        """
        with self.event_loop():
            dialog.create()
        try:
            yield
        finally:
            with self.event_loop():
                dialog.destroy()
