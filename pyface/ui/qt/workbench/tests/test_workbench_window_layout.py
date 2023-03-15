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

from pyface.ui.qt.workbench.split_tab_widget import SplitTabWidget
from pyface.ui.qt.workbench.workbench_window_layout import (
    WorkbenchWindowLayout,
)


class TestWorkbenchWindowLayout(unittest.TestCase):

    def test_change_of_active_qt_editor(self):
        # Test error condition for enthought/mayavi#321
        mock_split_tab_widget = mock.Mock(spec=SplitTabWidget)

        layout = WorkbenchWindowLayout(_qt4_editor_area=mock_split_tab_widget)

        class DummyEvent:
            def __init__(self, new):
                self.new = new

        # This should not throw
        layout._qt4_active_editor_changed(DummyEvent(new=None))
        self.assertEqual(mock_split_tab_widget.setTabTextColor.called, False)

        mock_active_editor = mock.Mock()
        layout._qt4_active_editor_changed(mock_active_editor)

        self.assertEqual(mock_split_tab_widget.setTabTextColor.called, True)
