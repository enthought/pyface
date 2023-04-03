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

from ..spin_field import SpinField
from .field_mixin import FieldMixin


class TestSpinField(FieldMixin, unittest.TestCase):

    def _create_widget_simple(self, **traits):
        traits.setdefault("value", 1)
        traits.setdefault("bounds", (0, 100))
        traits.setdefault("tooltip", "Dummy")
        return SpinField(**traits)

    # Tests ------------------------------------------------------------------

    def test_spin_field(self):
        self._create_widget_control()

        self.widget.value = 5
        self.gui.process_events()

        self.assertEqual(self.widget._get_control_value(), 5)

    def test_spin_field_set(self):
        self._create_widget_control()

        with self.assertTraitChanges(self.widget, "value", count=1):
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

    def test_spin_field_wrap(self):
        self._create_widget_control()

        self.widget.wrap = True
        self.gui.process_events()

        self.assertTrue(self.widget._get_control_wrap())
