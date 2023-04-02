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
from ..action_manager import ActionManager
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
        self.group = Group(id="test")

    def test_init_group(self):
        action_manager = ActionManager(self.group)
        default_group = action_manager._get_default_group()
        self.assertEqual(action_manager.groups, [self.group, default_group])
        self.assertEqual(self.group.parent, action_manager)

    def test_init_string(self):
        action_manager = ActionManager("Test")
        default_group = action_manager._get_default_group()
        self.assertEqual(len(action_manager.groups), 2)
        self.assertEqual(action_manager.groups[0].id, "Test")
        self.assertEqual(action_manager.groups[-1], default_group)
        self.assertEqual(action_manager.groups[0].parent, action_manager)

    def test_init_action_item(self):
        action_manager = ActionManager(self.action_item)
        default_group = action_manager._get_default_group()
        self.assertEqual(action_manager.groups, [default_group])
        self.assertEqual(default_group.items, [self.action_item])
        self.assertEqual(self.action_item.parent, default_group)

    def test_init_group_action_item(self):
        action_manager = ActionManager(self.group, self.action_item)
        default_group = action_manager._get_default_group()
        self.assertEqual(action_manager.groups, [self.group, default_group])
        self.assertEqual(self.group.items, [self.action_item])
        self.assertEqual(self.action_item.parent, self.group)

    def test_init_action(self):
        action_manager = ActionManager(self.action)
        default_group = action_manager._get_default_group()
        self.assertEqual(action_manager.groups, [default_group])
        self.assertEqual(default_group.items[0].action, self.action)
        self.assertEqual(default_group.items[0].parent, default_group)

    def test_init_nothing(self):
        action_manager = ActionManager()
        default_group = action_manager._get_default_group()
        self.assertEqual(action_manager.groups, [default_group])
        self.assertEqual(len(default_group.items), 0)

    def test_append(self):
        action_manager = ActionManager()
        action_manager.append(self.group)
        default_group = action_manager._get_default_group()
        self.assertEqual(action_manager.groups, [default_group, self.group])
        self.assertEqual(self.group.parent, action_manager)

    def test_append_2(self):
        action_manager = ActionManager(self.group)
        group2 = Group()
        action_manager.append(group2)
        default_group = action_manager._get_default_group()
        self.assertEqual(
            action_manager.groups, [self.group, default_group, group2]
        )
        self.assertEqual(group2.parent, action_manager)

    def test_append_string(self):
        action_manager = ActionManager(self.group)
        action_manager.append("Test string")
        self.assertEqual(len(action_manager.groups), 3)
        self.assertEqual(action_manager.groups[2].id, "Test string")

    def test_append_item(self):
        action_manager = ActionManager()
        action_manager.append(self.action_item)
        default_group = action_manager._get_default_group()
        self.assertEqual(action_manager.groups, [default_group])
        self.assertEqual(default_group.items, [self.action_item])

    def test_append_item_2(self):
        action_manager = ActionManager()
        action_manager.append(self.group)
        action_manager.append(self.action_item)
        default_group = action_manager._get_default_group()
        self.assertEqual(action_manager.groups, [default_group, self.group])
        self.assertEqual(default_group.items, [self.action_item])

    def test_append_item_order(self):
        # Regression test for enthought/pyface#289
        expected = [
            self.action_item,
            ActionItem(action=Action(name="Test2")),
            ActionItem(action=Action(name="Test3")),
        ]
        action_manager = ActionManager()
        for item in expected:
            action_manager.append(item)

        default_group = action_manager._get_default_group()
        self.assertEqual(default_group.items, expected)

    def test_destroy(self):
        action_manager = ActionManager(self.group)
        # XXX items doesn't fire a change event.  Should it?
        # XXX should mock group to ensure that destroy is called
        action_manager.destroy()

    def test_insert(self):
        action_manager = ActionManager()
        action_manager.insert(0, self.group)
        default_group = action_manager._get_default_group()
        self.assertEqual(action_manager.groups, [self.group, default_group])
        self.assertEqual(self.group.parent, action_manager)

    def test_insert_2(self):
        action_manager = ActionManager(self.group)
        group2 = Group()
        action_manager.insert(1, group2)
        default_group = action_manager._get_default_group()
        self.assertEqual(
            action_manager.groups, [self.group, group2, default_group]
        )
        self.assertEqual(group2.parent, action_manager)

    def test_insert_string(self):
        action_manager = ActionManager(self.group)
        action_manager.insert(0, "Test string")
        self.assertEqual(len(action_manager.groups), 3)
        self.assertEqual(action_manager.groups[0].id, "Test string")

    def test_insert_item(self):
        action_manager = ActionManager()
        action_manager.insert(0, self.action_item)
        default_group = action_manager._get_default_group()
        self.assertEqual(action_manager.groups, [default_group])
        self.assertEqual(default_group.items, [self.action_item])

    def test_insert_item_2(self):
        action_manager = ActionManager()
        action_manager.append(self.group)
        action_manager.insert(0, self.action_item)
        default_group = action_manager._get_default_group()
        self.assertEqual(action_manager.groups, [default_group, self.group])
        self.assertEqual(default_group.items, [self.action_item])

    def test_find_group(self):
        action_manager = ActionManager(self.group)
        group = action_manager.find_group("test")
        self.assertEqual(group, self.group)

    def test_find_group_missing(self):
        action_manager = ActionManager(self.group)
        group = action_manager.find_group("not here")
        self.assertIsNone(group)

    def test_find_item(self):
        self.group.append(self.action_item)
        action_manager = ActionManager(self.group)
        item = action_manager.find_item("Test")
        self.assertEqual(item, self.action_item)

    def test_find_item_missing(self):
        self.group.append(self.action_item)
        action_manager = ActionManager(self.group)
        item = action_manager.find_item("Not here")
        self.assertIsNone(item)

    def test_find_item_hierarchy(self):
        action_manager = ActionManager(self.group)
        action_manager_2 = ActionManager(self.action_item, id="test2")
        self.group.append(action_manager_2)
        item = action_manager.find_item("test2/Test")
        self.assertEqual(item, self.action_item)

    def test_walk_hierarchy(self):
        action_manager = ActionManager(self.group)
        action_manager_2 = ActionManager(self.action_item, id="test2")
        self.group.append(action_manager_2)
        result = []
        action_manager.walk(result.append)
        self.assertEqual(
            result,
            [
                action_manager,
                self.group,
                action_manager_2,
                action_manager_2._get_default_group(),
                self.action_item,
                action_manager._get_default_group(),
            ],
        )

    def test_enabled_changed(self):
        self.group.append(self.action_item)
        action_manager = ActionManager(self.group)
        action_manager.enabled = False
        self.assertFalse(self.group.enabled)
        self.assertFalse(self.action_item.enabled)
        self.assertFalse(self.action.enabled)
        action_manager.enabled = True
        self.assertTrue(self.group.enabled)
        self.assertTrue(self.action_item.enabled)
        self.assertTrue(self.action.enabled)

    def test_visible_changed(self):
        self.group.append(self.action_item)
        action_manager = ActionManager(self.group)
        action_manager.visible = False
        self.assertFalse(self.group.visible)
        # XXX group doesn't make items invisible
        # self.assertFalse(self.action_item.enabled)
        # self.assertFalse(self.action.enabled)
        action_manager.visible = True
        self.assertTrue(self.group.visible)
        # XXX group doesn't make items visible
        # self.assertTrue(self.action_item.enabled)
        # self.assertTrue(self.action.enabled)
