from __future__ import absolute_import

from traits.testing.unittest_tools import UnittestTools, unittest

from ...image_cache import ImageCache
from ...window import Window
from ..action import Action
from ..action_item import ActionItem
from ..group import Group


class TestActionItem(unittest.TestCase, UnittestTools):

    def setUp(self):
        # test whether function is called by updating list
        # XXX should really use mock
        self.memo = []

        def perform():
            self.memo.append('called')

        self.perform = perform

        self.action = Action(name='Test', on_perform=perform)
        self.action_item = ActionItem(action=self.action)

    def test_init_action_item(self):
        group = Group(self.action_item)
        self.assertEqual(group.items, [self.action_item])

    def test_init_action(self):
        group = Group(self.action)
        self.assertEqual(len(group.items), 1)
        self.assertEqual(group.items[0].action, self.action)

    def test_init_callable(self):
        group = Group(self.perform)
        self.assertEqual(len(group.items), 1)
        self.assertEqual(group.items[0].action.on_perform, self.perform)
        self.assertEqual(group.items[0].action.name, "Perform")
