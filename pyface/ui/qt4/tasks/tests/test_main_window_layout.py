# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
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

from traits.etsconfig.api import ETSConfig

from pyface.tasks.api import TaskLayout, PaneItem
from pyface.toolkit import toolkit_object
from pyface.window import Window

try:
    from pyface.ui.qt4.tasks.main_window_layout import MainWindowLayout
except ImportError:
    if ETSConfig.toolkit == "qt4":
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
    from pyface.qt import QtGui
    dock_widget = QtGui.QDockWidget(parent)
    content_widget = QtGui.QWidget(parent)
    dock_widget.setWidget(content_widget)
    return dock_widget


@unittest.skipIf(
    ETSConfig.toolkit != "qt4",
    "This test targets Qt specific MainWindowLayout. "
    "Currently toolkit is not Qt."
)
class TestMainWindowLayout(GuiTestAssistant, unittest.TestCase):
    """ Test Qt specific MainWindowLayout.

    Note that MainWindowLayout does not have a toolkit-agnostic interface
    in the ``pyface.tasks`` package. Therefore this test is Qt-only.
    """

    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.window = Window()
        self.window._create()

    def tearDown(self):
        if self.window.control is not None:
            with self.delete_widget(self.window.control):
                self.window.destroy()
        del self.window
        GuiTestAssistant.tearDown(self)

    def test_set_pane_item_layout_in_main_window_layout(self):
        window_layout = MainWindowLayout(control=self.window.control)
        dock_layout = TaskLayout(left=PaneItem(width=200, height=400))

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
        dock_widget.widget().adjustSize()
        size = dock_widget.widget().size()
        self.assertEqual(size.width(), 200)
        self.assertEqual(size.height(), 400)
