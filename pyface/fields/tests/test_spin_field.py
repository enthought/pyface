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
from ..spin_field import SpinField


is_wx = (toolkit.toolkit == 'wx')


#@unittest.skipIf(is_wx, "SpinField not supported in Wx")
class TestSpinField(unittest.TestCase):

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

    def test_spin_field(self):
        widget = SpinField(
            parent=self.parent.control,
            value=1,
            bounds=(0, 100),
            tooltip='Dummy',
        )

        widget._create()
        try:
            self.gui.process_events()
            widget.show(True)
            self.gui.process_events()
            widget.value = 5
            self.gui.process_events()

            self.assertEqual(widget._get_control_value(), 5)
        finally:
            widget.destroy()
            self.gui.process_events()

    def test_spin_field_set(self):
        widget = SpinField(
            parent=self.parent.control,
            value=1,
            bounds=(0, 100),
            tooltip='Dummy',
        )

        widget._create()
        try:
            self.gui.process_events()
            widget.show(True)
            self.gui.process_events()
            widget._set_control_value(5)
            self.gui.process_events()

            self.assertEqual(widget.value, 5)
        finally:
            widget.destroy()
            self.gui.process_events()

    def test_spin_field_bounds(self):
        widget = SpinField(
            parent=self.parent.control,
            value=1,
            bounds=(0, 100),
            tooltip='Dummy',
        )

        widget._create()
        try:
            self.gui.process_events()
            widget.show(True)
            self.gui.process_events()

            widget.bounds = (10, 50)
            self.gui.process_events()

            self.assertEqual(widget._get_control_bounds(), (10, 50))
            self.assertEqual(widget._get_control_value(), 10)
            self.assertEqual(widget.value, 10)
        finally:
            widget.destroy()
            self.gui.process_events()

    def test_spin_field_tooltip(self):
        widget = SpinField(
            parent=self.parent.control,
            value=1,
            bounds=(0, 100),
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

    def test_spin_field_menu(self):
        widget = SpinField(
            parent=self.parent.control,
            value=1,
            bounds=(0, 100),
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
