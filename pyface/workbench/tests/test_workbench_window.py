# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import tempfile
import shutil
import unittest
from unittest import mock

from traits.testing.api import UnittestTools

from pyface.workbench.perspective import Perspective
from pyface.workbench.api import Workbench
from pyface.workbench.workbench_window import (
    WorkbenchWindow,
    WorkbenchWindowLayout,
    WorkbenchWindowMemento,
)


class TestWorkbenchWindowUserPerspective(unittest.TestCase, UnittestTools):
    def setUp(self):
        # A perspective with show_editor_area switched on
        self.with_editor = Perspective(
            show_editor_area=True, id="test_id", name="test_name"
        )

        # A perspective with show_editor_area switched off
        self.without_editor = Perspective(
            show_editor_area=False, id="test_id2", name="test_name2"
        )

        # Where the state file should be saved
        self.state_location = tempfile.mkdtemp(dir="./")

        # Make sure the temporary directory is removed
        self.addCleanup(self.rm_tempdir)

    def rm_tempdir(self):
        shutil.rmtree(self.state_location)

    def get_workbench_with_window(self):
        workbench = Workbench()
        workbench_window = WorkbenchWindow()
        workbench.windows = [workbench_window]

        # Saved perspectives should go to the temporary directory
        workbench.state_location = self.state_location

        # Mock the layout for the workbench window
        workbench_window.layout = mock.MagicMock(spec=WorkbenchWindowLayout)
        workbench_window.layout.window = workbench_window

        return workbench, workbench_window

    def show_perspective(self, workbench_window, perspective):
        workbench_window.active_perspective = perspective
        workbench_window.layout.is_editor_area_visible = mock.MagicMock(
            return_value=perspective.show_editor_area
        )

    def test_editor_area_with_perspectives(self):
        """ Test show_editor_area is respected while switching perspective"""

        # The workbench and workbench window with layout mocked
        workbench, workbench_window = self.get_workbench_with_window()
        workbench.active_window = workbench_window

        # Add perspectives
        workbench.user_perspective_manager.add(self.with_editor)
        workbench.user_perspective_manager.add(self.without_editor)

        # There are the methods we want to test if they are called
        workbench_window.show_editor_area = mock.MagicMock()
        workbench_window.hide_editor_area = mock.MagicMock()

        # Mock more things for initialing the Workbench Window
        workbench_window._memento = WorkbenchWindowMemento()
        workbench_window._initial_layout = workbench_window._memento

        # Show a perspective with an editor area
        self.show_perspective(workbench_window, self.with_editor)

        # show_editor_area should be called
        self.assertTrue(workbench_window.show_editor_area.called)

        # Show a perspective withOUT an editor area
        workbench_window.hide_editor_area.reset_mock()
        self.show_perspective(workbench_window, self.without_editor)

        # hide_editor_area should be called
        self.assertTrue(workbench_window.hide_editor_area.called)

        # The with_editor has been seen so this will be restored from the memento
        workbench_window.show_editor_area.reset_mock()
        self.show_perspective(workbench_window, self.with_editor)

        # show_editor_area should be called
        self.assertTrue(workbench_window.show_editor_area.called)

    def test_editor_area_restore_from_saved_state(self):
        """ Test if show_editor_area is restored properly from saved state """

        # The workbench and workbench window with layout mocked
        workbench, workbench_window = self.get_workbench_with_window()
        workbench.active_window = workbench_window

        # Add perspectives
        workbench.user_perspective_manager.add(self.with_editor)
        workbench.user_perspective_manager.add(self.without_editor)

        # Mock for initialising the workbench window
        workbench_window._memento = WorkbenchWindowMemento()
        workbench_window._initial_layout = workbench_window._memento

        # Mock layout functions for pickling
        # We only care about show_editor_area and not the layout in this test
        layout_functions = {
            "get_view_memento.return_value": (0, (None, None)),
            "get_editor_memento.return_value": (0, (None, None)),
            "get_toolkit_memento.return_value": (0, dict(geometry="")),
        }

        workbench_window.layout.configure_mock(**layout_functions)

        # The following records perspective mementos to workbench_window._memento
        self.show_perspective(workbench_window, self.without_editor)
        self.show_perspective(workbench_window, self.with_editor)

        # Save the window layout to a state file
        workbench._save_window_layout(workbench_window)

        # We only needed the state file for this test
        del workbench_window
        del workbench

        # We create another workbench which uses the state location
        # and we test if we can retore the saved perspective correctly
        workbench, workbench_window = self.get_workbench_with_window()

        # Mock window factory since we already created a workbench window
        workbench.window_factory = mock.MagicMock(
            return_value=workbench_window
        )

        # There are the methods we want to test if they are called
        workbench_window.show_editor_area = mock.MagicMock()
        workbench_window.hide_editor_area = mock.MagicMock()

        # This restores the perspectives and mementos
        workbench.create_window()

        # Create contents
        workbench_window._create_contents(mock.Mock())

        # Perspective mementos should be restored
        self.assertIn(
            self.with_editor.id, workbench_window._memento.perspective_mementos
        )
        self.assertIn(
            self.without_editor.id,
            workbench_window._memento.perspective_mementos,
        )

        # Since the with_editor perspective is used last,
        # it should be used as initial perspective
        self.assertTrue(workbench_window.show_editor_area.called)

        # Try restoring the perspective without editor
        # The restored perspectives are not the same instance as before
        # We need to get them using their id
        perspective_without_editor = workbench_window.get_perspective_by_id(
            self.without_editor.id
        )

        # Show the perspective with editor area
        workbench_window.hide_editor_area.reset_mock()
        self.show_perspective(workbench_window, perspective_without_editor)

        # make sure hide_editor_area is called
        self.assertTrue(workbench_window.hide_editor_area.called)
