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

        with self.assertTraitChanges(action, "object", 1):
            action.application = self.application

        self.assertEqual(action.object, self.application)

        with self.assertTraitChanges(action, "object", 1):
            action.application = None

        self.assertIsNone(action.object)

    def test_destroy(self):
        action = GUIApplicationAction(application=self.application)

        action.destroy()

        self.assertEqual(action.object, None)
