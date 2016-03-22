from __future__ import absolute_import
import mock

from traits.testing.unittest_tools import unittest

from pyface.ui.qt4.workbench.split_tab_widget import SplitTabWidget
from pyface.ui.qt4.workbench.workbench_window_layout import \
    WorkbenchWindowLayout


class TestWorkbenchWindowLayout(unittest.TestCase):
    def test_change_of_active_qt_editor(self):
        # Test error condition for enthought/mayavi#321

        layout = WorkbenchWindowLayout(
            _qt4_editor_area=mock.Mock(
                spec=SplitTabWidget))

        layout._qt4_active_editor_changed(None, None)
