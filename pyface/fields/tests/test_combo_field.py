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
from pyface.image_resource import ImageResource
from pyface.window import Window
from ..combo_field import ComboField


class TestComboField(unittest.TestCase):

    def setUp(self):
        self.gui = GUI()
        self.parent = Window()
        self.parent._create()
        self.parent.open()
        self.addCleanup(self._destroy_parent)
        self.gui.process_events()

    def _destroy_parent(self):
        self.parent.destroy()
        self.gui.process_events()
        self.parent = None

    def test_combo_field(self):
        widget = ComboField(
            parent=self.parent.control,
            value='one',
            values=['one', 'two', 'three', 'four'],
            tooltip='Dummy',
        )

        widget._create()
        try:
            self.gui.process_events()
            widget.show(True)
            self.gui.process_events()

            widget.value = 'two'
            self.gui.process_events()

            self.assertEqual(widget._get_control_value(), 'two')
            self.assertEqual(widget._get_control_text(), 'two')
        finally:
            widget.destroy()
            self.gui.process_events()

    def test_combo_field_set(self):
        widget = ComboField(
            parent=self.parent.control,
            values=['one', 'two', 'three', 'four'],
            tooltip='Dummy',
        )

        widget._create()
        try:
            self.gui.process_events()
            widget.show(True)
            self.gui.process_events()
            widget._set_control_value('two')
            self.gui.process_events()

            self.assertEqual(widget.value, 'two')
        finally:
            widget.destroy()
            self.gui.process_events()

    def test_combo_field_formatter(self):
        widget = ComboField(
            parent=self.parent.control,
            values=[1, 2, 3, 4],
            tooltip='Dummy',
            formatter=str,
        )

        widget._create()
        try:
            self.gui.process_events()
            widget.show(True)
            self.gui.process_events()
            widget.value = 2
            self.gui.process_events()

            self.assertEqual(widget._get_control_value(), 2)
            self.assertEqual(widget._get_control_text(), '2')
        finally:
            widget.destroy()
            self.gui.process_events()

    def test_combo_field_formatter_changed(self):
        widget = ComboField(
            parent=self.parent.control,
            values=[1, 2, 3, 4],
            value=2,
            tooltip='Dummy',
            formatter=str,
        )

        widget._create()
        try:
            self.gui.process_events()
            widget.show(True)
            self.gui.process_events()
            widget.formatter = 'Number {}'.format
            self.gui.process_events()

            self.assertEqual(widget._get_control_value(), 2)
            self.assertEqual(widget._get_control_text(), 'Number 2')
        finally:
            widget.destroy()
            self.gui.process_events()

    def test_combo_field_formatter_set(self):
        widget = ComboField(
            parent=self.parent.control,
            values=[1, 2, 3, 4],
            tooltip='Dummy',
            formatter=str,
        )

        widget._create()
        try:
            self.gui.process_events()
            widget.show(True)
            self.gui.process_events()
            widget._set_control_value(2)
            self.gui.process_events()

            self.assertEqual(widget.value, 2)
        finally:
            widget.destroy()
            self.gui.process_events()

    def test_combo_field_icon_formatter(self):
        image = ImageResource('question')
        widget = ComboField(
            parent=self.parent.control,
            values=[1, 2, 3, 4],
            tooltip='Dummy',
            formatter=lambda x: (image, str(x)),
        )

        widget._create()
        try:
            self.gui.process_events()
            widget.show(True)
            self.gui.process_events()
            widget.value = 2
            self.gui.process_events()

            self.assertEqual(widget._get_control_value(), 2)
            self.assertEqual(widget._get_control_text(), '2')
        finally:
            widget.destroy()
            self.gui.process_events()

    def test_combo_field_values(self):
        widget = ComboField(
            parent=self.parent.control,
            values=['one', 'two', 'three', 'four'],
            tooltip='Dummy',
        )

        widget._create()
        try:
            self.gui.process_events()
            widget.show(True)
            self.gui.process_events()
            widget.values = ['four', 'five', 'one', 'six']
            self.gui.process_events()

            # XXX different results in Wx and Qt
            # As best I can tell, difference is at the Traits level
            # On Qt setting 'values' sets 'value' to "four" before combofield
            # handler sees it.  On Wx it remains  as "one" at point of handler
            # call.  Possibly down to dictionary ordering or something
            # similar.
            self.assertIn(widget.value, {'one', 'four'})
        finally:
            widget.destroy()
            self.gui.process_events()

    def test_combo_field_tooltip(self):
        widget = ComboField(
            parent=self.parent.control,
            values=['one', 'two', 'three', 'four'],
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

    def test_combo_field_menu(self):
        widget = ComboField(
            parent=self.parent.control,
            values=['one', 'two', 'three', 'four'],
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
