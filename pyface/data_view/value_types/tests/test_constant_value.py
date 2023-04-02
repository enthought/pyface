# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from unittest import TestCase
from unittest.mock import Mock

from traits.testing.api import UnittestTools

from pyface.color import Color
from pyface.data_view.value_types.constant_value import ConstantValue
from pyface.image_resource import ImageResource


class TestConstantValue(UnittestTools, TestCase):

    def setUp(self):
        self.model = Mock()

    def test_defaults(self):
        value_type = ConstantValue()
        self.assertEqual(value_type.text, "")
        self.assertEqual(value_type.tooltip, "")

    def test_has_editor_value(self):
        value_type = ConstantValue()
        self.assertFalse(value_type.has_editor_value(self.model, [0], [0]))

    def test_has_text(self):
        value_type = ConstantValue()
        self.assertFalse(value_type.has_text(self.model, [0], [0]))

    def test_has_text_true(self):
        value_type = ConstantValue(text="something")
        self.assertTrue(value_type.has_text(self.model, [0], [0]))

    def test_get_text(self):
        value_type = ConstantValue(text="something")
        self.assertEqual(
            value_type.get_text(self.model, [0], [0]),
            "something"
        )

    def test_text_changed(self):
        value_type = ConstantValue()
        with self.assertTraitChanges(value_type, 'updated'):
            value_type.text = 'something'
        self.assertEqual(value_type.text, 'something')

    def test_has_color_default(self):
        value_type = ConstantValue()
        self.assertFalse(value_type.has_color(self.model, [0], [0]))

    def test_has_color(self):
        value_type = ConstantValue(color=Color(rgba=(0.4, 0.2, 0.6, 0.8)))
        self.assertTrue(value_type.has_color(self.model, [0], [0]))

    def test_get_color_default(self):
        value_type = ConstantValue()
        self.assertIsNone(value_type.get_color(self.model, [0], [0]))

    def test_get_color(self):
        value_type = ConstantValue(color='rebeccapurple')
        self.assertEqual(
            value_type.get_color(self.model, [0], [0]),
            Color(rgba=(0.4, 0.2, 0.6, 1.0))
        )

    def test_get_color_changed(self):
        value_type = ConstantValue()
        with self.assertTraitChanges(value_type, 'updated'):
            value_type.color = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        self.assertEqual(
            value_type.get_color(self.model, [0], [0]),
            Color(rgba=(0.4, 0.2, 0.6, 0.8))
        )

    def test_get_color_rgba_changed(self):
        value_type = ConstantValue(color=Color())
        with self.assertTraitChanges(value_type, 'updated'):
            value_type.color.rgba = (0.4, 0.2, 0.6, 0.8)
        self.assertEqual(
            value_type.get_color(self.model, [0], [0]),
            Color(rgba=(0.4, 0.2, 0.6, 0.8))
        )

    def test_has_image(self):
        value_type = ConstantValue()
        self.assertFalse(value_type.has_image(self.model, [0], [0]))

    def test_has_image_true(self):
        value_type = ConstantValue(image="question")
        self.assertTrue(value_type.has_image(self.model, [0], [0]))

    def test_get_image(self):
        image = ImageResource("question")
        value_type = ConstantValue(image=image)
        self.assertEqual(
            value_type.get_image(self.model, [0], [0]),
            image
        )

    def test_get_image_none(self):
        value_type = ConstantValue()
        image = value_type.get_image(self.model, [0], [0])
        self.assertEqual(image.name, "image_not_found")

    def test_image_changed(self):
        value_type = ConstantValue()
        image = ImageResource("question")
        with self.assertTraitChanges(value_type, 'updated'):
            value_type.image = image
        self.assertEqual(value_type.image, image)

    def test_has_tooltip(self):
        value_type = ConstantValue()
        self.assertFalse(value_type.has_tooltip(self.model, [0], [0]))

    def test_has_tooltip_true(self):
        value_type = ConstantValue(tooltip="something")
        self.assertTrue(value_type.has_tooltip(self.model, [0], [0]))

    def test_get_tooltip(self):
        value_type = ConstantValue(tooltip="something")
        self.assertEqual(
            value_type.get_tooltip(self.model, [0], [0]),
            "something"
        )

    def test_tooltip_changed(self):
        value_type = ConstantValue()
        with self.assertTraitChanges(value_type, 'updated'):
            value_type.tooltip = 'something'
        self.assertEqual(value_type.tooltip, 'something')
