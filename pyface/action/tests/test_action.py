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

from ..action import Action
from ..action_event import ActionEvent


class TestAction(unittest.TestCase):
    def test_default_id(self):
        action = Action(name="Test")
        self.assertEqual(action.id, "Test")

    def test_id(self):
        action = Action(name="Test", id="test")
        self.assertEqual(action.id, "test")

    def test_perform(self):
        # test whether function is called by updating list
        # XXX should really use mock
        memo = []

        def perform():
            memo.append("called")

        action = Action(name="Test", on_perform=perform)
        event = ActionEvent()
        action.perform(event)
        self.assertEqual(memo, ["called"])

    def test_perform_none(self):
        action = Action(name="Test")
        event = ActionEvent()
        # does nothing, but shouldn't error
        action.perform(event)

    def test_destroy(self):
        action = Action(name="Test")
        # does nothing, but shouldn't error
        action.destroy()

    def test_widget_action(self):
        # test whether function is called by updating list
        # XXX should really use mock
        memo = []

        def control_factory(parent, action):
            memo.append((parent, action))

        action = Action(
            name="Dummy", style="widget", control_factory=control_factory
        )
        parent = None
        action.create_control(parent)

        self.assertEqual(memo, [(parent, action)])
