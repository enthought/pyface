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

from ..spin_field import SpinField
from .field_mixin import FieldMixin


class TestSpinField(FieldMixin, unittest.TestCase):

    def _create_widget(self):
        return SpinField(
            parent=self.parent.control,
            value=1,
            bounds=(0, 100),
            tooltip='Dummy',
        )

    # Tests ------------------------------------------------------------------

    def test_spin_field(self):
        self._create_widget_control()

        self.widget.value = 5
        self.gui.process_events()

        self.assertEqual(self.widget._get_control_value(), 5)

    def test_spin_field_set(self):
        self._create_widget_control()

        with self.assertTraitChanges(self.widget, 'value', count=1):
            self.widget._set_control_value(5)
            self.gui.process_events()

        self.assertEqual(self.widget.value, 5)

    def test_spin_field_bounds(self):
        self._create_widget_control()

        self.widget.bounds = (10, 50)
        self.gui.process_events()

        self.assertEqual(self.widget._get_control_bounds(), (10, 50))
        self.assertEqual(self.widget._get_control_value(), 10)
        self.assertEqual(self.widget.value, 10)
