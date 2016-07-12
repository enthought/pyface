import unittest

from traits.testing.unittest_tools import UnittestTools
from pyface.tasks.api import Task
from ..task_window import TaskWindow


class TestTaskWindow(unittest.TestCase, UnittestTools):

    def test_title(self):
        task_1 = Task(name='Test Task')
        task_2 = Task(name='Test Task 2')
        task_window = TaskWindow(tasks=[task_1, task_2])

        # initially nothing
        self.assertEqual(task_window.title, '')

        # activate task
        with self.assertTraitChanges(task_window, 'title', count=1):
            task_window.active_task = task_1
        self.assertEqual(task_window.title, 'Test Task')

        # change task name
        with self.assertTraitChanges(task_window, 'title', count=1):
            task_1.name = 'Changed Name'
        self.assertEqual(task_window.title, 'Changed Name')

        # change active task
        with self.assertTraitChanges(task_window, 'title', count=1):
            task_window.active_task = task_2
        self.assertEqual(task_window.title, 'Test Task 2')

        # no active task
        with self.assertTraitChanges(task_window, 'title', count=1):
            task_window.active_task = None
        self.assertEqual(task_window.title, '')

    def test_set_title(self):
        task_1 = Task(name='Test Task')
        task_2 = Task(name='Test Task 2')
        task_window = TaskWindow(tasks=[task_1, task_2], active_task=task_1)

        # set window title
        with self.assertTraitChanges(task_window, 'title', count=1):
            task_window.title = "Window title"
        self.assertEqual(task_window.title, "Window title")

        # change task name (trait fires, no window title change)
        with self.assertTraitChanges(task_window, 'title', count=1):
            task_1.name = 'Changed Name'
        self.assertEqual(task_window.title, "Window title")

        # change active task (trait fires, no window title change)
        with self.assertTraitChanges(task_window, 'title', count=1):
            task_window.active_task = task_2
        self.assertEqual(task_window.title, "Window title")

        # no active task (trait fires, no window title change)
        with self.assertTraitChanges(task_window, 'title', count=1):
            task_window.active_task = None
        self.assertEqual(task_window.title, "Window title")

        # change window title
        with self.assertTraitChanges(task_window, 'title', count=1):
            task_window.title = "New Window title"
        self.assertEqual(task_window.title, "New Window title")
