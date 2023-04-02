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

from ..action import Action
from ..action_item import ActionItem
from ..group import Group


class TestActionItem(unittest.TestCase, UnittestTools):
    def setUp(self):
        # test whether function is called by updating list
        # XXX should really use mock
        self.memo = []

        def perform():
            self.memo.append("called")

        self.perform = perform

        self.action = Action(name="Test", on_perform=perform)
        self.action_item = ActionItem(action=self.action)

    def test_init_action_item(self):
        group = Group(self.action_item)
        self.assertEqual(group.items, [self.action_item])
        self.assertEqual(self.action_item.parent, group)

    def test_init_action(self):
        group = Group(self.action)
        self.assertEqual(len(group.items), 1)
        self.assertEqual(group.items[0].action, self.action)
        self.assertEqual(group.items[0].parent, group)

    def test_init_callable(self):
        group = Group(self.perform)
        self.assertEqual(len(group.items), 1)
        self.assertEqual(group.items[0].action.on_perform, self.perform)
        self.assertEqual(group.items[0].action.name, "Perform")
        self.assertEqual(group.items[0].parent, group)

    def test_init_nothing(self):
        group = Group()
        self.assertEqual(group.items, [])

    def test_append(self):
        group = Group(self.action_item)
        action_item2 = ActionItem(action=Action(name="Action 2"))
        # XXX items doesn't fire a change event.  Should it?
        group.append(action_item2)
        self.assertEqual(group.items, [self.action_item, action_item2])
        self.assertEqual(action_item2.parent, group)

    def test_append_action(self):
        group = Group(self.action_item)
        action2 = Action(name="Action 2")
        # XXX items doesn't fire a change event.  Should it?
        group.append(action2)
        self.assertEqual(len(group.items), 2)
        self.assertEqual(group.items[0], self.action_item)
        self.assertEqual(group.items[1].action, action2)
        self.assertEqual(group.items[1].parent, group)

    def test_append_callable(self):
        group = Group(self.action_item)
        # XXX items doesn't fire a change event.  Should it?
        group.append(self.perform)
        self.assertEqual(len(group.items), 2)
        self.assertEqual(group.items[0], self.action_item)
        self.assertEqual(group.items[1].action.on_perform, self.perform)
        self.assertEqual(group.items[1].action.name, "Perform")
        self.assertEqual(group.items[1].parent, group)

    def test_clear(self):
        group = Group(self.action_item)
        # XXX items doesn't fire a change event.  Should it?
        group.clear()
        self.assertEqual(group.items, [])
        # XXX clear doesn't set items' parent to None, but remove does...
        # self.assertIsNone(self.action_item.parent)

    def test_destroy(self):
        group = Group(self.action_item)
        # XXX items doesn't fire a change event.  Should it?
        # XXX should mock action item's to ensure that destroy is called
        group.destroy()
        self.assertEqual(group.items, [self.action_item])

    def test_insert(self):
        group = Group(self.action_item)
        action_item2 = ActionItem(action=Action(name="Action 2"))
        # XXX items doesn't fire a change event.  Should it?
        group.insert(1, action_item2)
        self.assertEqual(group.items, [self.action_item, action_item2])
        self.assertEqual(action_item2.parent, group)

    def test_insert_action(self):
        group = Group(self.action_item)
        action2 = Action(name="Action 2")
        # XXX items doesn't fire a change event.  Should it?
        group.insert(1, action2)
        self.assertEqual(len(group.items), 2)
        self.assertEqual(group.items[0], self.action_item)
        self.assertEqual(group.items[1].action, action2)
        self.assertEqual(group.items[1].parent, group)

    def test_insert_callable(self):
        group = Group(self.action_item)
        # XXX items doesn't fire a change event.  Should it?
        group.insert(1, self.perform)
        self.assertEqual(len(group.items), 2)
        self.assertEqual(group.items[0], self.action_item)
        self.assertEqual(group.items[1].action.on_perform, self.perform)
        self.assertEqual(group.items[1].action.name, "Perform")
        self.assertEqual(group.items[1].parent, group)

    def test_insert_at_start(self):
        group = Group(self.action_item)
        action_item2 = ActionItem(action=Action(name="Action 2"))
        # XXX items doesn't fire a change event.  Should it?
        group.insert(0, action_item2)
        self.assertEqual(group.items, [action_item2, self.action_item])
        self.assertEqual(action_item2.parent, group)

    def test_remove(self):
        group = Group(self.action_item)
        # XXX items doesn't fire a change event.  Should it?
        group.remove(self.action_item)
        self.assertEqual(group.items, [])
        self.assertIsNone(self.action_item.parent)

    def test_remove_missing(self):
        group = Group()
        with self.assertRaises(ValueError):
            group.remove(self.action_item)

    def test_insert_before(self):
        group = Group(self.action_item)
        action_item2 = ActionItem(action=Action(name="Action 2"))
        # XXX items doesn't fire a change event.  Should it?
        group.insert_before(self.action_item, action_item2)
        self.assertEqual(group.items, [action_item2, self.action_item])
        self.assertEqual(action_item2.parent, group)

    def test_insert_after(self):
        group = Group(self.action_item)
        action_item2 = ActionItem(action=Action(name="Action 2"))
        # XXX items doesn't fire a change event.  Should it?
        group.insert_after(self.action_item, action_item2)
        self.assertEqual(group.items, [self.action_item, action_item2])
        self.assertEqual(action_item2.parent, group)

    def test_find(self):
        group = Group(self.action_item)
        item = group.find("Test")
        self.assertEqual(item, self.action_item)

    def test_find_missing(self):
        group = Group(self.action_item)
        item = group.find("Not here")
        self.assertIsNone(item)

    def test_enabled_changed(self):
        group = Group(self.action_item)
        group.enabled = False
        self.assertFalse(self.action_item.enabled)
        self.assertFalse(self.action.enabled)
        group.enabled = True
        self.assertTrue(self.action_item.enabled)
        self.assertTrue(self.action.enabled)
