from __future__ import absolute_import

import unittest

from traits.testing.unittest_tools import UnittestTools

from pyface.gui_application import GUIApplication
from ..gui_application_action import GUIApplicationAction
from ..action_event import ActionEvent


class TestAction(unittest.TestCase, UnittestTools):
    def setUp(self):
        self.application = GUIApplication()

    def test_defaults(self):
        action = GUIApplicationAction()
        event = ActionEvent()

        # does nothing, but shouldn't error
        action.perform(event)

        self.assertTrue(action.enabled)
        self.assertTrue(action.visible)
        self.assertIsNone(action.object)

    def test_application(self):
        action = GUIApplicationAction(application=self.application)
        event = ActionEvent()

        # does nothing, but shouldn't error
        action.perform(event)

        self.assertTrue(action.enabled)
        self.assertTrue(action.visible)
        self.assertEqual(action.object, self.application)

    def test_application_changed(self):
        action = GUIApplicationAction()

        self.assertIsNone(action.object)

        with self.assertTraitChanges(action, 'object', 1):
            action.application = self.application

        self.assertEqual(action.object, self.application)

        with self.assertTraitChanges(action, 'object', 1):
            action.application = None

        self.assertIsNone(action.object)

    def test_destroy(self):
        action = GUIApplicationAction(application=self.application)

        action.destroy()

        self.assertEqual(action.object, None)