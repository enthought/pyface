# Copyright (c) 2019, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

from __future__ import absolute_import

from traits.testing.unittest_tools import unittest

from pyface.action.api import Action, MenuManager
from ..text_field import TextField


class TestTextField(unittest.TestCase):

    def test_text_field(self):
        widget = TextField(
            parent=None,
            value='test',
            tooltip='Dummy',
        )

        widget._create()
        try:
            widget.show(True)
            widget.value = 'new value'

            self.assertEqual(widget._get_control_value(), 'new value')
        finally:
            widget.destroy()

    def test_text_field_set(self):
        widget = TextField(
            parent=None,
            value='test',
            tooltip='Dummy',
        )

        widget._create()
        try:
            widget.show(True)
            widget._set_control_value('new value')

            self.assertEqual(widget.value, 'new value')
        finally:
            widget.destroy()

    def test_text_field_echo(self):
        widget = TextField(
            parent=None,
            value='test',
            tooltip='Dummy',
            echo='password'
        )

        widget._create()
        try:
            widget.show(True)
            self.assertEqual(widget._get_control_echo(), 'password')
        finally:
            widget.destroy()

    def test_text_field_tooltip(self):
        widget = TextField(
            parent=None,
            value='test',
            tooltip='Dummy',
        )

        widget._create()
        try:
            widget.show(True)

            widget.tooltip = "New tooltip."

            self.assertEqual(widget._get_control_tooltip(), "New tooltip.")
        finally:
            widget.destroy()

    def test_text_field_menu(self):
        widget = TextField(
            parent=None,
            value='test',
            tooltip='Dummy',
        )

        widget._create()
        try:
            widget.show(True)
            widget.menu = MenuManager(Action(name='Test'), name='Test')
        finally:
            widget.destroy()
