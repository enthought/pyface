# Copyright (c) 2014-2023 by Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

import sys
import unittest

from pyface.qt import QtCore
from pyface.tasks.api import (
    DockPane, EditorAreaPane, PaneItem, Task, TaskFactory, TaskLayout,
    TasksApplication)


class MyDockPane(DockPane):
    id = "my_dock_pane"
    name = u"My dock pane"


class MyTask(Task):
    id = "my_task"
    name = u"My task"

    def _default_layout_default(self):
        return TaskLayout(left=PaneItem("my_dock_pane", width=200))

    def create_central_pane(self):
        return EditorAreaPane()

    def create_dock_panes(self):
        return [MyDockPane()]


class MyApplication(TasksApplication):
    id = "my_application"
    name = u"My application"

    def _task_factories_default(self):
        return [
            TaskFactory(
                id="my_task_factory",
                name=u"My task factory",
                factory=MyTask,
            ),
        ]


class TestDockPane(unittest.TestCase):

    @unittest.skipUnless(sys.platform == "darwin", "only applicable to macOS")
    def test_dock_windows_visible_on_macos(self):
        # Regression test for enthought/pyface#427: check that dock panes
        # are displayed on macOS even when the application doesn't have
        # focus.

        tool_attributes = []

        def check_panes_and_exit(app_event):
            app = app_event.application
            for window in app.windows:
                for dock_pane in window.dock_panes:
                    attr = dock_pane.control.testAttribute(
                        QtCore.Qt.WidgetAttribute.WA_MacAlwaysShowToolWindow)
                    tool_attributes.append(attr)

            app.exit()

        app = MyApplication()
        app.on_trait_change(check_panes_and_exit, "application_initialized")
        app.run()

        self.assertTrue(tool_attributes)
        for attr in tool_attributes:
            self.assertTrue(attr)

    def test_dock_windows_undock(self):
        # Regression test for enthought/pyface#1028: check that undocking
        # dockpanes doesn't crash

        tool_attributes = []

        def check_panes_and_exit(app_event):
            app = app_event.application
            app.windows[0].dock_panes[0].control.setFloating(True)
            for window in app.windows:
                for dock_pane in window.dock_panes:
                    attr = dock_pane.dock_area
                    tool_attributes.append(attr)

            app.exit()

        app = MyApplication()
        app.on_trait_change(check_panes_and_exit, "application_initialized")
        app.run()

        self.assertTrue(tool_attributes)
        for attr in tool_attributes:
            self.assertEqual(attr, 'left')
