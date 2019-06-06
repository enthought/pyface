from __future__ import absolute_import
import mock
import unittest

from pyface.ui.qt4.workbench.split_tab_widget import SplitTabWidget
from pyface.ui.qt4.workbench.workbench_window_layout import \
    WorkbenchWindowLayout


class TestWorkbenchWindowLayout(unittest.TestCase):
    def test_change_of_active_qt_editor(self):
        # Test error condition for enthought/mayavi#321

        mock_split_tab_widget = mock.Mock(spec=SplitTabWidget)

        layout = WorkbenchWindowLayout(_qt4_editor_area=mock_split_tab_widget)

        # This should not throw
        layout._qt4_active_editor_changed(None, None)
        self.assertEqual(mock_split_tab_widget.setTabTextColor.called, False)

        mock_active_editor = mock.Mock()
        layout._qt4_active_editor_changed(None, mock_active_editor)

        self.assertEqual(mock_split_tab_widget.setTabTextColor.called, True)
