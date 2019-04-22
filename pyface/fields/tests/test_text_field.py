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
from pyface.gui import GUI
from pyface.toolkit import toolkit
from pyface.window import Window
from ..text_field import TextField

is_wx = (toolkit.toolkit == 'wx')


class TestTextField(unittest.TestCase):

    def setUp(self):
        self.gui = GUI()
        self.parent = Window()
        self.parent._create()
        self.parent.open()
        self.addCleanup(self._destroy_parent)

    def _destroy_parent(self):
        self.parent.destroy()
        self.gui.process_events()
        self.parent = None

    def test_text_field(self):
        widget = TextField(
            parent=self.parent.control,
            value='test',
            tooltip='Dummy',
        )

        widget._create()
        try:
            self.gui.process_events()
            widget.show(True)
            self.gui.process_events()
            widget.value = 'new value'
            self.gui.process_events()

            self.assertEqual(widget._get_control_value(), 'new value')
        finally:
            widget.destroy()
            self.gui.process_events()

    def test_text_field_set(self):
        widget = TextField(
            parent=self.parent.control,
            value='test',
            tooltip='Dummy',
        )

        widget._create()
        try:
            self.gui.process_events()
            widget.show(True)
            self.gui.process_events()
            widget._set_control_value('new value')
            self.gui.process_events()

            self.assertEqual(widget.value, 'new value')
        finally:
            widget.destroy()
            self.gui.process_events()

    @unittest.skipIf(is_wx, "Can't change password mode for wx after control creatiomn.")
    def test_text_field_echo(self):
        widget = TextField(
            parent=self.parent.control,
            value='test',
            tooltip='Dummy',
            echo='password'
        )

        widget._create()
        try:
            self.gui.process_events()
            widget.show(True)
            self.gui.process_events()

            self.assertEqual(widget._get_control_echo(), 'password')
        finally:
            widget.destroy()
            self.gui.process_events()

    def test_text_field_tooltip(self):
        widget = TextField(
            parent=self.parent.control,
            value='test',
            tooltip='Dummy',
        )

        widget._create()
        try:
            self.gui.process_events()
            widget.show(True)
            self.gui.process_events()

            widget.tooltip = "New tooltip."
            self.gui.process_events()

            self.assertEqual(widget._get_control_tooltip(), "New tooltip.")
        finally:
            widget.destroy()
            self.gui.process_events()

    def test_text_field_menu(self):
        widget = TextField(
            parent=self.parent.control,
            value='test',
            tooltip='Dummy',
        )

        widget._create()
        try:
            self.gui.process_events()
            widget.show(True)
            self.gui.process_events()
            widget.menu = MenuManager(Action(name='Test'), name='Test')
            self.gui.process_events()
        finally:
            widget.destroy()
            self.gui.process_events()
