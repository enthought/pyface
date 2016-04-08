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
        workbench_window.active_perspective = with_editor
        workbench_window.layout.is_editor_area_visible = mock.MagicMock(return_value=True)

        # show_editor_area should be called
        # hide_editor_area should not be called
        self.assertEqual(workbench_window.show_editor_area.call_count, 1)
        self.assertEqual(workbench_window.hide_editor_area.call_count, 0)

        # Show a perspective with editor area
        workbench_window.show_editor_area.reset_mock()
        workbench_window.hide_editor_area.reset_mock()        
        workbench_window.active_perspective = without_editor
        workbench_window.layout.is_editor_area_visible = mock.MagicMock(return_value=False)

        # show_editor_area should not be called
        # hide_editor_area should be called
        self.assertEqual(workbench_window.show_editor_area.call_count, 0)
        self.assertEqual(workbench_window.hide_editor_area.call_count, 1)

        # The with_editor has been seen so this will read from the memento
        workbench_window.show_editor_area.reset_mock()
        workbench_window.hide_editor_area.reset_mock()
        workbench_window.active_perspective = with_editor
        workbench_window.layout.is_editor_area_visible = mock.MagicMock(return_value=True)

        # show_editor_area should be called
        self.assertEqual(workbench_window.show_editor_area.call_count, 1)
        self.assertEqual(workbench_window.hide_editor_area.call_count, 0)
