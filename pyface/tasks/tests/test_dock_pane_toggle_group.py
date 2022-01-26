# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import unittest


from pyface.action.schema.api import SMenu, SMenuBar, SGroup
from pyface.tasks.action.api import DockPaneToggleGroup
from pyface.tasks.api import DockPane, Task, TaskPane, TaskWindow
from pyface.gui import GUI
from traits.api import List
from traits.etsconfig.api import ETSConfig


USING_WX = ETSConfig.toolkit not in ["", "qt4"]


class BogusTask(Task):

    id = "tests.bogus_task"
    name = "Bogus Task"

    dock_panes = List()

    def create_central_pane(self):
        return TaskPane(id="tests.bogus_task.central_pane")

    def create_dock_panes(self):
        self.dock_panes = dock_panes = [
            DockPane(id="tests.bogus_task.dock_pane_2", name="Dock Pane 2"),
            DockPane(id="tests.bogus_task.dock_pane_1", name="Dock Pane 1"),
        ]

        return dock_panes

    def _menu_bar_default(self):
        menu_bar = SMenuBar(
            SMenu(
                SGroup(
                    group_factory=DockPaneToggleGroup,
                    id="tests.bogus_task.DockPaneToggleGroup",
                ),
                id="View",
                name="&View",
            )
        )

        return menu_bar


class DockPaneToggleGroupTestCase(unittest.TestCase):
    @unittest.skipIf(USING_WX, "TaskWindowBackend is not implemented in WX")
    def setUp(self):
        self.gui = GUI()

        # Set up the bogus task with its window.
        self.task = BogusTask()

        self.window = window = TaskWindow()
        window.add_task(self.task)

        self.task_state = window._get_state(self.task)

        # Fish the dock pane toggle group from the menu bar manager.
        dock_pane_toggle_group = []

        def find_doc_pane_toggle(item):
            if item.id == "tests.bogus_task.DockPaneToggleGroup":
                dock_pane_toggle_group.append(item)

        self.task_state.menu_bar_manager.walk(find_doc_pane_toggle)

        self.dock_pane_toggle_group = dock_pane_toggle_group[0]

    def tearDown(self):
        del self.task
        del self.task_state
        del self.dock_pane_toggle_group

        if self.window.control is not None:
            self.window.destroy()
            self.gui.process_events()
        del self.window
        del self.gui

    def get_dock_pane_toggle_action_names(self):
        names = [
            action_item.action.name
            for action_item in self.dock_pane_toggle_group.items
        ]

        return names

    # Tests ----------------------------------------------------------------

    def test_group_content_at_startup(self):
        # Check that there are 2 dock panes in the group at the beginning.
        self.assertEqual(2, len(self.dock_pane_toggle_group.items))

        # Names are sorted by the group.
        names = self.get_dock_pane_toggle_action_names()
        expected_names = ["Dock Pane 1", "Dock Pane 2"]
        self.assertEqual(list(sorted(expected_names)), list(sorted(names)))

    def test_react_to_dock_pane_added(self):
        # Add a dock pane to the task.
        self.task_state.dock_panes.append(
            DockPane(id="tests.bogus_task.dock_pane_0", name="Dock Pane 0")
        )

        # Check that there are 3 dock panes in the group.
        self.assertEqual(3, len(self.dock_pane_toggle_group.items))

        # Names are sorted by the group.
        names = self.get_dock_pane_toggle_action_names()
        expected_names = ["Dock Pane 0", "Dock Pane 1", "Dock Pane 2"]
        self.assertEqual(list(sorted(expected_names)), list(sorted(names)))

    def test_react_to_dock_pane_removed(self):
        # Remove a dock pane from the task.
        self.task_state.dock_panes.remove(self.task.dock_panes[0])

        # Check that there is only 1 dock pane left in the group.
        self.assertEqual(1, len(self.dock_pane_toggle_group.items))

        names = self.get_dock_pane_toggle_action_names()
        expected_names = ["Dock Pane 1"]
        self.assertEqual(list(sorted(expected_names)), list(sorted(names)))
