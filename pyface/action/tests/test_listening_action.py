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

from traits.api import Any, Bool, HasTraits
from traits.testing.api import UnittestTools

from ..listening_action import ListeningAction
from ..action_event import ActionEvent


class WatchedObject(HasTraits):

    #: Trait to watch for enabled state
    is_enabled = Bool(True)

    #: Other trait to watch for enabled state
    is_also_enabled = Bool(True)

    #: Trait to watch for visible state
    is_visible = Bool(True)

    #: Other trait to watch for visible state
    is_also_visible = Bool(True)

    #: Flag that is set when method called
    was_called = Bool()

    #: Child object to test dotted lookup
    child = Any()

    def callback(self):
        self.was_called = True


class TestListeningAction(unittest.TestCase, UnittestTools):
    def setUp(self):
        self.object = WatchedObject()

    def perform_with_callback(self, action):
        # test whether function is called by updating list
        # XXX should really use mock
        memo = []

        def perform():
            memo.append("called")

        action.on_perform = perform
        event = ActionEvent()

        action.perform(event)

        return memo

    def test_defaults(self):
        action = ListeningAction()
        event = ActionEvent()

        # does nothing, but shouldn't error
        action.perform(event)

        self.assertTrue(action.enabled)
        self.assertTrue(action.visible)

    def test_perform_no_object(self):
        action = ListeningAction()

        memo = self.perform_with_callback(action)

        self.assertEqual(memo, ["called"])

    def test_perform_no_method(self):
        action = ListeningAction(object=self.object)

        memo = self.perform_with_callback(action)

        self.assertFalse(self.object.was_called)
        self.assertEqual(memo, ["called"])

    def test_perform_method(self):
        action = ListeningAction(object=self.object, method="callback")

        memo = self.perform_with_callback(action)

        self.assertTrue(self.object.was_called)
        self.assertEqual(memo, [])

    def test_perform_method_missing(self):
        action = ListeningAction(object=self.object, method="fallback")

        # does nothing, but shouldn't error
        memo = self.perform_with_callback(action)

        self.assertFalse(self.object.was_called)
        self.assertEqual(memo, [])

    def test_perform_child_method(self):
        self.object.child = WatchedObject()
        action = ListeningAction(object=self.object, method="child.callback")

        memo = self.perform_with_callback(action)

        self.assertTrue(self.object.child.was_called)
        self.assertFalse(self.object.was_called)
        self.assertEqual(memo, [])

    def test_perform_missing_child_method(self):
        action = ListeningAction(object=self.object, method="child.callback")

        # does nothing, but shouldn't error
        memo = self.perform_with_callback(action)

        self.assertFalse(self.object.was_called)
        self.assertEqual(memo, [])

    def test_enabled(self):
        action = ListeningAction(object=self.object, enabled_name="is_enabled")

        self.assertTrue(action.enabled)

        with self.assertTraitChanges(action, "enabled", 1):
            self.object.is_enabled = False

        self.assertFalse(action.enabled)

        with self.assertTraitChanges(action, "enabled", 1):
            self.object.is_enabled = True

        self.assertTrue(action.enabled)

    def test_enabled_child(self):
        self.object.child = WatchedObject()
        action = ListeningAction(
            object=self.object, enabled_name="child.is_enabled"
        )

        self.assertTrue(action.enabled)

        with self.assertTraitChanges(action, "enabled", 1):
            self.object.child.is_enabled = False

        self.assertFalse(action.enabled)

        with self.assertTraitChanges(action, "enabled", 1):
            self.object.child.is_enabled = True

        self.assertTrue(action.enabled)

    def test_enabled_missing_child(self):
        action = ListeningAction(
            object=self.object, enabled_name="child.is_enabled"
        )

        self.assertFalse(action.enabled)

        with self.assertTraitChanges(action, "enabled", 1):
            self.object.child = WatchedObject()

        self.assertTrue(action.enabled)

        with self.assertTraitChanges(action, "enabled", 1):
            self.object.child = None

        self.assertFalse(action.enabled)

    def test_enabled_name_change(self):
        self.object.is_also_enabled = False
        action = ListeningAction(object=self.object, enabled_name="is_enabled")

        self.assertTrue(action.enabled)

        with self.assertTraitChanges(action, "enabled", 1):
            action.enabled_name = "is_also_enabled"

        self.assertFalse(action.enabled)

    def test_visible(self):
        action = ListeningAction(object=self.object, visible_name="is_visible")

        self.assertTrue(action.visible)

        with self.assertTraitChanges(action, "visible", 1):
            self.object.is_visible = False

        self.assertFalse(action.visible)

        with self.assertTraitChanges(action, "visible", 1):
            self.object.is_visible = True

        self.assertTrue(action.visible)

    def test_visible_child(self):
        self.object.child = WatchedObject()
        action = ListeningAction(
            object=self.object, visible_name="child.is_visible"
        )

        self.assertTrue(action.visible)

        with self.assertTraitChanges(action, "visible", 1):
            self.object.child.is_visible = False

        self.assertFalse(action.visible)

        with self.assertTraitChanges(action, "visible", 1):
            self.object.child.is_visible = True

        self.assertTrue(action.visible)

    def test_visible_missing_child(self):
        action = ListeningAction(
            object=self.object, visible_name="child.is_visible"
        )

        self.assertFalse(action.visible)

        with self.assertTraitChanges(action, "visible", 1):
            self.object.child = WatchedObject()

        self.assertTrue(action.visible)

        with self.assertTraitChanges(action, "visible", 1):
            self.object.child = None

        self.assertFalse(action.visible)

    def test_visible_name_change(self):
        self.object.is_also_visible = False
        action = ListeningAction(object=self.object, visible_name="is_visible")

        self.assertTrue(action.visible)

        with self.assertTraitChanges(action, "visible", 1):
            action.visible_name = "is_also_visible"

        self.assertFalse(action.visible)

    def test_destroy(self):
        action = ListeningAction(object=self.object)

        action.destroy()
