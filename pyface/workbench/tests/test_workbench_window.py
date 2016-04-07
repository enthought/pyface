import mock

from traits.testing.unittest_tools import unittest, UnittestTools

from pyface.workbench.perspective import Perspective
from pyface.workbench.workbench_window import (WorkbenchWindow,
                                               WorkbenchWindowLayout,
                                               WorkbenchWindowMemento)


class TestWindow(unittest.TestCase, UnittestTools):

    def test_restore_perspective_editor_area(self):
        # A perspective with show_editor_area switched on
        with_editor = Perspective(show_editor_area=True,
                                  id="test_id", name="test_name")

        # A perspective with show_editor_area switched off
        without_editor = Perspective(show_editor_area=False,
                                     id="test_id2", name="test_name2")

        # Set up the WorkbenchWindow
        workbench_window = WorkbenchWindow(
            perspectives=[with_editor, without_editor])

        # mock a bunch of objects
        workbench_window._memento = WorkbenchWindowMemento()
        workbench_window._initial_layout = workbench_window._memento
        workbench_window.layout = mock.Mock(spec=WorkbenchWindowLayout)

        # There are the methods we want to test if they are called
        workbench_window.show_editor_area = mock.MagicMock()
        workbench_window.hide_editor_area = mock.MagicMock()

        # Show a perspective with editor area
        workbench_window._show_perspective(None, with_editor)

        # show_editor_area should be called
        # hide_editor_area should not be called when there was
        # no old perspective
        self.assertTrue(workbench_window.show_editor_area.called)
        self.assertFalse(workbench_window.hide_editor_area.called)

        # Show a perspective with editor area
        workbench_window.show_editor_area.reset_mock()
        workbench_window.hide_editor_area.reset_mock()
        workbench_window._show_perspective(with_editor, without_editor)

        # show_editor_area should not be called and hide_editor_area is called
        self.assertFalse(workbench_window.show_editor_area.called)
        self.assertTrue(workbench_window.hide_editor_area.called)
