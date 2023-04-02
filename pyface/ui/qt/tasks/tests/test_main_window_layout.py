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
from unittest import mock

from pyface.tasks.api import TaskLayout, PaneItem
from pyface.toolkit import toolkit_object
from pyface.window import Window

try:
    from pyface.qt import QtGui
    from pyface.ui.qt.tasks.main_window_layout import MainWindowLayout
except ImportError:
    if toolkit_object.toolkit.startswith("qt"):
        raise


GuiTestAssistant = toolkit_object("util.gui_test_assistant:GuiTestAssistant")


def create_dummy_dock_widget(parent):
    """ Create a dummy QDockWidget with a dummy child widget for test.

    Parameters
    ----------
    parent : QObject

    Returns
    -------
    dock_widget : QDockWidget
    """
    dock_widget = QtGui.QDockWidget(parent)
    content_widget = QtGui.QWidget(parent)
    dock_widget.setWidget(content_widget)
    return dock_widget


@unittest.skipIf(
    toolkit_object.toolkit != "qt",
    "This test targets Qt specific MainWindowLayout. "
    "Current toolkit is not Qt."
)
class TestMainWindowLayout(unittest.TestCase, GuiTestAssistant):
    """ Test Qt specific MainWindowLayout.

    Note that MainWindowLayout does not have a toolkit-agnostic interface
    in the ``pyface.tasks`` package. Therefore this test is Qt-only.
    """

    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.window = Window(size=(500, 500))
        self.window.create()

    def tearDown(self):
        if self.window.control is not None:
            with self.delete_widget(self.window.control):
                self.window.destroy()
        del self.window
        GuiTestAssistant.tearDown(self)

    def setup_window_with_central_widget(self):
        # Add a central widget to the main window.
        # The main window takes ownership of the child widget.
        central_widget = QtGui.QWidget(parent=self.window.control)
        self.window.control.setCentralWidget(central_widget)

    def test_set_pane_item_width_in_main_window_layout(self):
        # Test the dock pane width is as expected.

        self.setup_window_with_central_widget()

        # Set the dock widget expected width to be smaller than the window
        # for a meaningful test.
        expected_width = self.window.size[0] // 2
        window_layout = MainWindowLayout(control=self.window.control)
        dock_layout = TaskLayout(
            left=PaneItem(width=expected_width)
        )
        dock_widget = create_dummy_dock_widget(parent=self.window.control)
        patch_get_dock_widget = mock.patch.object(
            MainWindowLayout, "_get_dock_widget",
            return_value=dock_widget,
        )

        # when
        with self.event_loop():
            with patch_get_dock_widget:
                window_layout.set_layout(dock_layout)

        # then
        size = dock_widget.widget().size()
        self.assertEqual(size.width(), expected_width)

    def test_set_pane_item_height_in_main_window_layout(self):
        # Test the dock pane height is as expected.

        self.setup_window_with_central_widget()

        # Set the dock widget expected height to be smaller than the window
        # for a meaningful test.
        expected_height = self.window.size[1] // 2
        window_layout = MainWindowLayout(control=self.window.control)
        dock_layout = TaskLayout(
            bottom=PaneItem(height=expected_height)
        )
        dock_widget = create_dummy_dock_widget(parent=self.window.control)
        patch_get_dock_widget = mock.patch.object(
            MainWindowLayout, "_get_dock_widget",
            return_value=dock_widget,
        )

        # when
        with self.event_loop():
            with patch_get_dock_widget:
                window_layout.set_layout(dock_layout)

        # then
        size = dock_widget.widget().size()
        self.assertEqual(size.height(), expected_height)
