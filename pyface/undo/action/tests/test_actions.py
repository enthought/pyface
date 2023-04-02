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

from pyface.undo.api import CommandStack, UndoManager
from pyface.undo.tests.testing_commands import SimpleCommand

from pyface.undo.action.api import RedoAction, UndoAction


class TestRedoAction(unittest.TestCase):

    def setUp(self):
        self.stack = CommandStack()
        self.undo_manager = UndoManager()
        self.stack.undo_manager = self.undo_manager
        self.undo_manager.active_stack = self.stack

        self.command = SimpleCommand()

    def test_update(self):
        redo_action = RedoAction(command=self.command, undo_manager=self.undo_manager)
        self.stack.push(self.command)
        self.undo_manager.undo()
        self.assertTrue(redo_action.enabled)
        self.assertEqual(redo_action.name, "&Redo Increment by 1")


class TestUndoAction(unittest.TestCase):

    def setUp(self):
        self.stack = CommandStack()
        self.undo_manager = UndoManager()
        self.stack.undo_manager = self.undo_manager
        self.undo_manager.active_stack = self.stack

        self.command = SimpleCommand()

    def test_update(self):
        undo_action = UndoAction(command=self.command, undo_manager=self.undo_manager)
        self.stack.push(self.command)
        self.assertTrue(undo_action.enabled)
        self.assertEqual(undo_action.name, "&Undo Increment by 1")
