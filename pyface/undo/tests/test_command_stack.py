# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from contextlib import contextmanager
import unittest

from pyface.undo.api import CommandStack, UndoManager
from pyface.undo.tests.testing_commands import (
    MergeableCommand, SimpleCommand, UnnamedCommand,
)
from traits.testing.api import UnittestTools


class TestCommandStack(UnittestTools, unittest.TestCase):
    def setUp(self):
        self.stack = CommandStack()
        undo_manager = UndoManager()
        self.stack.undo_manager = undo_manager

        self.command = SimpleCommand()

    # Command pushing tests ---------------------------------------------------

    def test_empty_command_stack(self):
        with self.assert_n_commands_pushed(self.stack, 0):
            pass

    def test_1_command_pushed(self):
        with self.assert_n_commands_pushed(self.stack, 1):
            with self.assertTraitChanges(self.stack.undo_manager,
                                         'stack_updated', count=1):
                self.stack.push(self.command)

    def test_n_command_pushed(self):
        n = 4
        with self.assert_n_commands_pushed(self.stack, n):
            for i in range(n):
                with self.assertTraitChanges(self.stack.undo_manager,
                                             'stack_updated', count=1):
                    self.stack.push(self.command)

    def test_push_after_undo(self):
        with self.assert_n_commands_pushed(self.stack, 1):
            self.stack.push(self.command)
            self.stack.undo()
            with self.assertTraitChanges(self.stack.undo_manager,
                                         'stack_updated', count=1):
                self.stack.push(self.command)

    def test_push_after_n_undo(self):
        with self.assert_n_commands_pushed(self.stack, 1):
            n = 4
            for i in range(n):
                self.stack.push(self.command)
            n = 4
            for i in range(n):
                self.stack.undo()

            with self.assertTraitChanges(self.stack.undo_manager,
                                         'stack_updated', count=1):
                self.stack.push(self.command)

    # Command merging tests ---------------------------------------------------

    def test_1_merge_command_pushed(self):
        self.command = MergeableCommand()
        with self.assert_n_commands_pushed(self.stack, 1):
            with self.assertTraitChanges(self.stack.undo_manager,
                                         'stack_updated', count=1):
                self.stack.push(self.command)

    def test_n_merge_command_pushed(self):
        n = 4
        with self.assert_n_commands_pushed(self.stack, 1):
            self.command = MergeableCommand()
            self.stack.push(self.command)
            for i in range(n):
                command = MergeableCommand()
                with self.assertTraitChanges(self.stack.undo_manager,
                                             'stack_updated', count=1):
                    self.stack.push(command)
        self.assertEqual(self.command.amount, n+1)

    def test_merge_after_undo(self):
        with self.assert_n_commands_pushed(self.stack, 2):
            self.stack.push(self.command)
            command = MergeableCommand()
            self.stack.push(command)
            command = SimpleCommand()
            self.stack.push(command)
            self.stack.undo()
            command = MergeableCommand()
            with self.assertTraitChanges(self.stack.undo_manager,
                                         'stack_updated', count=1):
                self.stack.push(command)

    def test_merge_after_clean(self):
        with self.assert_n_commands_pushed(self.stack, 2):
            command = MergeableCommand()
            self.stack.push(command)
            self.stack.clean = True
            command = MergeableCommand()
            with self.assertTraitChanges(self.stack.undo_manager,
                                         'stack_updated', count=1):
                self.stack.push(command)

    # Undo/Redo tests ---------------------------------------------------------

    def test_undo_1_command(self):
        with self.assert_n_commands_pushed_and_undone(self.stack, 1):
            self.stack.push(self.command)
            self.assertEqual(self.stack.undo_name, self.command.name)
            with self.assertTraitChanges(self.stack.undo_manager,
                                         'stack_updated', count=1):
                self.stack.undo()

    def test_undo_n_command(self):
        n = 4
        with self.assert_n_commands_pushed_and_undone(self.stack, n):
            for i in range(n):
                self.stack.push(self.command)

            for i in range(n):
                self.stack.undo()

    def test_undo_redo_sequence_nr(self):
        n = 4
        for i in range(n):
            self.stack.push(self.command)
        self.assertEqual(self.stack._index, 3)
        # undo back to the 1st command in the stack
        self.stack.undo(1)
        self.assertEqual(self.stack._index, 0)
        # redo back to the 3rd command in the stack
        self.stack.redo(3)
        self.assertEqual(self.stack._index, 2)

    def test_undo_unnamed_command(self):
        unnamed_command = UnnamedCommand()
        with self.assert_n_commands_pushed(self.stack, 1):
            self.stack.push(unnamed_command)

            # But the command cannot be undone because it has no name
            self.assertEqual(self.stack.undo_name, "")
            # This is a no-op
            self.stack.undo()

    def test_undo_redo_1_command(self):
        with self.assert_n_commands_pushed(self.stack, 1):
            self.stack.push(self.command)
            self.stack.undo()
            self.stack.redo()

    # Macro tests -------------------------------------------------------------

    def test_define_macro(self):
        with self.assert_n_commands_pushed(self.stack, 1):
            add_macro(self.stack, num_commands=2)

    def test_undo_macro(self):
        with self.assert_n_commands_pushed_and_undone(self.stack, 1):
            # The 2 pushes are viewed as 1 command
            add_macro(self.stack, num_commands=2)
            self.stack.undo()

    # Cleanliness tests -------------------------------------------------------

    def test_empty_stack_is_clean(self):
        self.assertTrue(self.stack.clean)

    def test_non_empty_stack_is_dirty(self):
        self.stack.push(self.command)
        self.assertFalse(self.stack.clean)

    def test_make_clean(self):
        # This makes it dirty by default
        self.stack.push(self.command)
        # Make the current tip of the stack clean
        self.stack.clean = True
        self.assertTrue(self.stack.clean)

    def test_make_dirty(self):
        # Start from a clean state:
        self.stack.push(self.command)
        self.stack.clean = True

        self.stack.clean = False
        self.assertFalse(self.stack.clean)

    def test_save_push_undo_is_clean(self):
        self.stack.push(self.command)

        self.stack.clean = True
        self.stack.push(self.command)
        self.stack.undo()
        self.assertTrue(self.stack.clean)

    def test_save_push_save_undo_is_clean(self):
        self.stack.push(self.command)

        self.stack.clean = True
        self.stack.push(self.command)
        self.stack.clean = True
        self.stack.undo()
        self.assertTrue(self.stack.clean)

    def test_push_undo_save_redo_is_dirty(self):
        self.stack.push(self.command)
        self.stack.undo()
        self.stack.clean = True
        self.stack.redo()
        self.assertFalse(self.stack.clean)

    def test_clear(self):
        n = 5
        for _ in range(n):
            self.stack.push(self.command)
        self.stack.clear()
        self.assertEqual(self.stack._stack, [])
        self.assertTrue(self.stack.clean)

    # Assertion helpers -------------------------------------------------------

    @contextmanager
    def assert_n_commands_pushed(self, stack, n):
        current_length = len(stack._stack)
        yield
        # N commands have been pushed...
        self.assertEqual(len(stack._stack), current_length + n)
        # ... and the state is at the tip of the stack...
        self.assertEqual(stack._index, current_length + n - 1)

    @contextmanager
    def assert_n_commands_pushed_and_undone(self, stack, n):
        current_length = len(stack._stack)
        yield
        # N commands have been pushed and then reverted. The stack still
        # contains the commands...
        self.assertEqual(len(stack._stack), n)
        # ... but we are back to the initial (clean) state
        self.assertEqual(stack._index, current_length - 1)


def add_macro(stack, num_commands=2):
    command = SimpleCommand()
    stack.begin_macro("Increment n times")
    try:
        for i in range(num_commands):
            stack.push(command)
    finally:
        stack.end_macro()
