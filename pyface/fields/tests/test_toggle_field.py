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


from pyface.image_resource import ImageResource
from ..toggle_field import (
    CheckBoxField, RadioButtonField, ToggleButtonField
)
from .field_mixin import FieldMixin


class ToggleFieldMixin(FieldMixin):

    # Tests ------------------------------------------------------------------

    def test_toggle_field(self):
        self._create_widget_control()

        self.widget.value = True
        self.gui.process_events()

        self.assertEqual(self.widget._get_control_value(), True)

    def test_toggle_field_set(self):
        self._create_widget_control()

        with self.assertTraitChanges(self.widget, "value", count=1):
            self.widget._set_control_value(True)
            self.gui.process_events()

        self.assertEqual(self.widget.value, True)

    def test_text_field_text(self):
        self._create_widget_control()
        self.assertEqual(self.widget._get_control_text(), "Toggle")

        self.widget.text = "Test"
        self.gui.process_events()

        self.assertEqual(self.widget._get_control_text(), "Test")

    def test_text_field_image(self):
        self._create_widget_control()
        image = ImageResource("question")

        # XXX can't validate icon values currently, so just a smoke test
        self.widget.image = image
        self.gui.process_events()


class TestCheckboxField(ToggleFieldMixin, unittest.TestCase):

    def _create_widget_simple(self, **traits):
        traits.setdefault("text", "Toggle")
        traits.setdefault("tooltip", "Dummy")
        return CheckBoxField(**traits)


class TestRadioButtonField(ToggleFieldMixin, unittest.TestCase):

    def _create_widget_simple(self, **traits):
        traits.setdefault("text", "Toggle")
        traits.setdefault("tooltip", "Dummy")
        return RadioButtonField(**traits)


class TestToggleButtonField(ToggleFieldMixin, unittest.TestCase):

    def _create_widget_simple(self, **traits):
        traits.setdefault("text", "Toggle")
        traits.setdefault("tooltip", "Dummy")
        return ToggleButtonField(**traits)
