from __future__ import absolute_import

from traits.testing.unittest_tools import unittest

from ..action import Action
from ..action_controller import ActionController
from ..action_event import ActionEvent


class TestActionController(unittest.TestCase):

    def setUp(self):
        # test whether function is called by updating list
        # XXX should really use mock
        self.memo = []

        def perform():
            self.memo.append('called')

        self.action = Action(name='Test', on_perform=perform)
        self.action_controller = ActionController()

    def test_perform(self):
        # test whether function is called by updating list
        # XXX should really use mock
        event = ActionEvent()
        self.action_controller.perform(self.action, event)
        self.assertEqual(self.memo, ['called'])

    def test_perform_none(self):
        action = Action(name='Test')
        event = ActionEvent()
        # does nothing, but shouldn't error
        self.action_controller.perform(action, event)

    def test_can_add_to_menu(self):
        result = self.action_controller.can_add_to_menu(self.action)
        self.assertTrue(result)

    def test_add_to_menu(self):
        # does nothing, shouldn't fail
        self.action_controller.add_to_menu(self.action)

    def test_can_add_to_toolbar(self):
        result = self.action_controller.can_add_to_toolbar(self.action)
        self.assertTrue(result)

    def test_add_to_toolbar(self):
        # does nothing, shouldn't fail
        self.action_controller.add_to_toolbar(self.action)
