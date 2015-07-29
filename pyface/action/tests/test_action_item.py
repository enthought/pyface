from __future__ import absolute_import

from traits.testing.unittest_tools import UnittestTools, unittest

from ..action import Action
from ..action_item import ActionItem


class TestActionItem(unittest.TestCase, UnittestTools):

    def setUp(self):
        # test whether function is called by updating list
        # XXX should really use mock
        self.memo = []

        def perform():
            self.memo.append('called')

        self.action = Action(name='Test', on_perform=perform)

    def test_default_id(self):
        action_item = ActionItem(action=self.action)
        self.assertEqual(action_item.id, 'Test')

    def test_enabled_changed(self):
        # XXX these are only one-way changes, which seems wrong.
        action_item = ActionItem(action=self.action)
        with self.assertTraitChanges(self.action, 'enabled', count=1):
            action_item.enabled = False
        self.assertFalse(self.action.enabled)
        with self.assertTraitChanges(self.action, 'enabled', count=1):
            action_item.enabled = True
        self.assertTrue(self.action.enabled)

    def test_visible_changed(self):
        # XXX these are only one-way changes, which seems wrong.
        action_item = ActionItem(action=self.action)
        with self.assertTraitChanges(self.action, 'visible', count=1):
            action_item.visible = False
        self.assertFalse(self.action.visible)
        with self.assertTraitChanges(self.action, 'visible', count=1):
            action_item.visible = True
        self.assertTrue(self.action.visible)
