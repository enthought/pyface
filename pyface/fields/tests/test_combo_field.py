# Copyright (c) 2019, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import unittest

from six import text_type

from pyface.image_resource import ImageResource
from ..combo_field import ComboField
from .field_mixin import FieldMixin


class TestComboField(FieldMixin, unittest.TestCase):

    def _create_widget(self):
        return ComboField(
            parent=self.parent.control,
            value='one',
            values=['one', 'two', 'three', 'four'],
            tooltip='Dummy',
        )

    # Tests ------------------------------------------------------------------

    def test_combo_field(self):
        self._create_widget_control()

        self.widget.value = 'two'
        self.gui.process_events()

        self.assertEqual(self.widget._get_control_value(), 'two')
        self.assertEqual(self.widget._get_control_text(), 'two')

    def test_combo_field_set(self):
        self._create_widget_control()

        with self.assertTraitChanges(self.widget, 'value', count=1):
            self.widget._set_control_value('two')
            self.gui.process_events()

        self.assertEqual(self.widget.value, 'two')

    def test_combo_field_formatter(self):
        self.widget.formatter = text_type
        self.widget.values = [0, 1, 2, 3]
        self._create_widget_control()

        self.widget.value = 2
        self.gui.process_events()

        self.assertEqual(self.widget._get_control_value(), 2)
        self.assertEqual(self.widget._get_control_text(), '2')

    def test_combo_field_formatter_changed(self):
        self.widget.values = [1, 2, 3, 4]
        self.widget.value = 2
        self.widget.formatter = text_type
        self._create_widget_control()

        self.widget.formatter = 'Number {}'.format
        self.gui.process_events()

        self.assertEqual(self.widget._get_control_value(), 2)
        self.assertEqual(self.widget._get_control_text(), 'Number 2')

    def test_combo_field_formatter_set(self):
        self.widget.values = [1, 2, 3, 4]
        self.widget.formatter = text_type
        self._create_widget_control()

        with self.assertTraitChanges(self.widget, 'value', count=1):
            self.widget._set_control_value(2)
            self.gui.process_events()

        self.assertEqual(self.widget.value, 2)

    def test_combo_field_icon_formatter(self):
        image = ImageResource('question')
        self.widget.values = [1, 2, 3, 4]
        self.widget.formatter = lambda x: (image, str(x))
        self._create_widget_control()

        self.widget.value = 2
        self.gui.process_events()

        self.assertEqual(self.widget._get_control_value(), 2)
        self.assertEqual(self.widget._get_control_text(), '2')

    def test_combo_field_values(self):
        self._create_widget_control()

        self.widget.values = ['four', 'five', 'one', 'six']
        self.gui.process_events()

        # XXX different results in Wx and Qt
        # As best I can tell, difference is at the Traits level
        # On Qt setting 'values' sets 'value' to "four" before combofield
        # handler sees it.  On Wx it remains  as "one" at point of handler
        # call.  Possibly down to dictionary ordering or something
        # similar.
        self.assertIn(self.widget.value, {'one', 'four'})
