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

from pyface.undo.api import CommandStack, UndoManager
from pyface.undo.tests.testing_commands import SimpleCommand


class TestUndoManager(unittest.TestCase, UnittestTools):

    def setUp(self):
        self.stack_a = CommandStack()
        self.stack_b = CommandStack()
        self.undo_manager = UndoManager()
        self.stack_a.undo_manager = self.undo_manager
        self.stack_b.undo_manager = self.undo_manager

        self.undo_manager.active_stack = self.stack_a

        self.command = SimpleCommand()

    # Command pushing tests ---------------------------------------------------

    def test_undo(self):
        self.assertEqual(self.stack_a._index, -1)
        self.stack_a.push(self.command)
        self.assertEqual(self.stack_a._index, 0)
        with self.assertTraitChanges(
                self.undo_manager, 'stack_updated', count=1):
            self.undo_manager.undo()
        self.assertEqual(self.stack_a._index, -1)

    def test_redo(self):
        self.assertEqual(self.stack_a._index, -1)
        self.stack_a.push(self.command)
        self.undo_manager.undo()
        self.assertEqual(self.stack_a._index, -1)
        with self.assertTraitChanges(
                self.undo_manager, 'stack_updated', count=1):
            self.undo_manager.redo()
        self.assertEqual(self.stack_a._index, 0)

    def test_change_active_stack(self):
        for _ in range(5):
            self.stack_a.push(self.command)
        self.assertEqual(self.stack_a._index, 4)
        self.undo_manager.active_stack = self.stack_b
        for _ in range(5):
            self.stack_b.push(self.command)
        self.assertEqual(self.stack_b._index, 4)
        for _ in range(3):
            self.undo_manager.undo()
        self.undo_manager.redo()

        self.assertEqual(self.stack_a._index, 4)
        self.assertEqual(self.stack_b._index, 2)

    def test_active_stack_clean(self):
        self.assertTrue(self.undo_manager.active_stack_clean)
        self.stack_a.push(self.command)
        self.assertFalse(self.undo_manager.active_stack_clean)
        self.undo_manager.active_stack = None
        self.assertTrue(self.undo_manager.active_stack_clean)
