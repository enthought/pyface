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

from traits.testing.api import UnittestTools
from pyface.tasks.api import Task
from ..task_window import TaskWindow


def _task_window_with_named_tasks(*names, **kwargs):
    tasks = [Task(name=name) for name in names]

    first_active = kwargs.pop("first_active", False)
    if first_active:
        kwargs["active_task"] = tasks[0]

    task = TaskWindow(tasks=tasks, **kwargs)
    return task


class TestTaskWindow(unittest.TestCase, UnittestTools):
    def test_title_default(self):
        task_window = TaskWindow()

        # default is empty
        self.assertEqual(task_window.title, "")

    def test_title_no_active_task(self):
        task_window = _task_window_with_named_tasks("Test Task", "Test Task 2")

        # should be empty
        self.assertEqual(task_window.title, "")

    def test_title_activate_task(self):
        task_window = _task_window_with_named_tasks("Test Task")
        task = task_window.tasks[0]

        # activate task
        with self.assertTraitChanges(task_window, "title", count=1):
            task_window.active_task = task
        self.assertEqual(task_window.title, "Test Task")

    def test_title_change_active_task_name(self):
        task_window = _task_window_with_named_tasks(
            "Test Task", first_active=True
        )
        task_1 = task_window.tasks[0]

        # change task name
        with self.assertTraitChanges(task_window, "title", count=1):
            task_1.name = "Changed Name"
        self.assertEqual(task_window.title, "Changed Name")

    def test_title_change_active_task(self):
        task_window = _task_window_with_named_tasks(
            "Test Task 1", "Test Task 2", first_active=True
        )
        task = task_window.tasks[1]

        # change active task
        with self.assertTraitChanges(task_window, "title", count=1):
            task_window.active_task = task
        self.assertEqual(task_window.title, "Test Task 2")

    def test_title_change_deactivate_task(self):
        task_window = _task_window_with_named_tasks(
            "Test Task 1", first_active=True
        )

        # change active task
        with self.assertTraitChanges(task_window, "title", count=1):
            task_window.active_task = None
        self.assertEqual(task_window.title, "")

    def test_set_title_no_tasks(self):
        task_window = _task_window_with_named_tasks()

        # set window title
        with self.assertTraitChanges(task_window, "title", count=1):
            task_window.title = "Window title"
        self.assertEqual(task_window.title, "Window title")

    def test_set_title_change_title(self):
        task_window = _task_window_with_named_tasks(title="Window Title")

        # set window title
        with self.assertTraitChanges(task_window, "title", count=1):
            task_window.title = "New Window title"
        self.assertEqual(task_window.title, "New Window title")

    def test_set_title_no_active_task(self):
        task_window = _task_window_with_named_tasks("Test Task")

        # set window title
        with self.assertTraitChanges(task_window, "title", count=1):
            task_window.title = "Window title"
        self.assertEqual(task_window.title, "Window title")

    def test_set_title_active_task(self):
        task_window = _task_window_with_named_tasks(
            "Test Task", first_active=True
        )

        # set window title
        with self.assertTraitChanges(task_window, "title", count=1):
            task_window.title = "Window title"
        self.assertEqual(task_window.title, "Window title")

    def test_set_title_activate_task(self):
        task_window = _task_window_with_named_tasks(
            "Test Task", title="Window title"
        )
        task = task_window.tasks[0]

        # change activate task (trait fires, no window title change)
        with self.assertTraitChanges(task_window, "title", count=1):
            task_window.active_task = task
        self.assertEqual(task_window.title, "Window title")

    def test_set_title_change_active_task_name(self):
        task_window = _task_window_with_named_tasks(
            "Test Task", title="Window title", first_active=True
        )
        task = task_window.tasks[0]

        # change task name (trait fires, no window title change)
        with self.assertTraitChanges(task_window, "title", count=1):
            task.name = "Changed Name"
        self.assertEqual(task_window.title, "Window title")

    def test_set_title_change_active_task(self):
        task_window = _task_window_with_named_tasks(
            "Test Task", "Test Task 2", title="Window title", active_first=True
        )
        task = task_window.tasks[1]

        # change task name (trait fires, no window title change)
        with self.assertTraitChanges(task_window, "title", count=1):
            task_window.active_task = task
        self.assertEqual(task_window.title, "Window title")

    def test_reset_title_active_task(self):
        task_window = _task_window_with_named_tasks(
            "Test Task", title="Window title", first_active=True
        )

        # reset window title
        with self.assertTraitChanges(task_window, "title", count=1):
            task_window.title = ""
        self.assertEqual(task_window.title, "Test Task")

    def test_reset_title(self):
        task_window = _task_window_with_named_tasks(
            "Test Task", title="Window title"
        )

        # set window title
        with self.assertTraitChanges(task_window, "title", count=1):
            task_window.title = ""
        self.assertEqual(task_window.title, "")
