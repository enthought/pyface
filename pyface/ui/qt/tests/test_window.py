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
Qt-specific tests for the Window class
"""

import unittest

from pyface.api import Window
from pyface.qt import QtGui
from pyface.ui.qt.util.gui_test_assistant import GuiTestAssistant


class TestWindow(GuiTestAssistant, unittest.TestCase):

    def test_close_last_window(self):
        window = Window()

        last_window_closed = []

        def handle_last_window_closed():
            last_window_closed.append('fired')

        QtGui.QGuiApplication.instance().lastWindowClosed.connect(
            handle_last_window_closed
        )

        try:
            with self.event_loop():
                window.create()

            self.gui.invoke_later(window.control.close)
            self.event_loop_helper.event_loop_with_timeout()
        finally:
            QtGui.QGuiApplication.instance().lastWindowClosed.disconnect(
                handle_last_window_closed
            )

        self.assertEqual(last_window_closed, ['fired'])
