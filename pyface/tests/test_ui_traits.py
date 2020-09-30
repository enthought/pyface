# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import os
import unittest

from traits.api import DefaultValue, HasTraits, TraitError
from traits.testing.optional_dependencies import numpy as np, requires_numpy
from traits.testing.unittest_tools import UnittestTools

from ..color import Color
from ..i_image_resource import IImageResource
from ..image_resource import ImageResource
from ..ui_traits import (
    Border,
    HasBorder,
    HasMargin,
    Image,
    Margin,
    PyfaceColor,
    image_resource_cache,
    image_bitmap_cache,
)


IMAGE_PATH = os.path.join(os.path.dirname(__file__), "images", "core.png")


class ImageClass(HasTraits):

    image = Image


class ColorClass(HasTraits):

    color = PyfaceColor()


class HasMarginClass(HasTraits):

    margin = HasMargin


class HasBorderClass(HasTraits):

    border = HasBorder


class TestImageTrait(unittest.TestCase, UnittestTools):
    def setUp(self):
        # clear all cached images
        image_resource_cache.clear()
        image_bitmap_cache.clear()
        # clear cached "not found" image
        ImageResource._image_not_found = None

    def test_defaults(self):
        image_class = ImageClass()

        self.assertIsNone(image_class.image)

    def test_init_local_image(self):
        from pyface.image_resource import ImageResource

        image_class = ImageClass(image=ImageResource("core.png"))

        self.assertIsInstance(image_class.image, ImageResource)
        self.assertEqual(image_class.image.name, "core.png")
        self.assertEqual(
            image_class.image.absolute_path, os.path.abspath(IMAGE_PATH)
        )

    def test_init_pyface_image(self):
        from pyface.image_resource import ImageResource

        image_class = ImageClass(image="about")
        im = image_class.image.create_image()

        self.assertIsInstance(image_class.image, ImageResource)
        self.assertEqual(image_class.image.name, "about")
        self.assertIsNone(image_class.image._image_not_found)
        self.assertIsNotNone(image_class.image._ref.data)

    def test_init_pyface_image_library(self):
        from pyface.image_resource import ImageResource

        image_class = ImageClass(image="@icons:dialog-warning")

        self.assertIsInstance(image_class.image, ImageResource)
        self.assertEqual(image_class.image.name, "dialog-warning.png")
        self.assertIsNone(image_class.image._image_not_found)
        self.assertEqual(
            image_class.image._ref.file_name, "dialog-warning.png"
        )
        self.assertEqual(image_class.image._ref.volume_name, "icons")


class TestMargin(unittest.TestCase):
    def test_defaults(self):
        margin = Margin()
        self.assertEqual(margin.top, 0)
        self.assertEqual(margin.bottom, 0)
        self.assertEqual(margin.left, 0)
        self.assertEqual(margin.right, 0)

    def test_init_one_arg(self):
        margin = Margin(4)
        self.assertEqual(margin.top, 4)
        self.assertEqual(margin.bottom, 4)
        self.assertEqual(margin.left, 4)
        self.assertEqual(margin.right, 4)

    def test_init_two_args(self):
        margin = Margin(4, 2)
        self.assertEqual(margin.top, 2)
        self.assertEqual(margin.bottom, 2)
        self.assertEqual(margin.left, 4)
        self.assertEqual(margin.right, 4)

    def test_init_four_args(self):
        margin = Margin(4, 2, 3, 1)
        self.assertEqual(margin.top, 3)
        self.assertEqual(margin.bottom, 1)
        self.assertEqual(margin.left, 4)
        self.assertEqual(margin.right, 2)


class TestPyfaceColor(unittest.TestCase):

    def test_init(self):
        trait = PyfaceColor()
        self.assertEqual(trait.default_value, (Color, (), {}))
        self.assertEqual(
            trait.default_value_type,
            DefaultValue.callable_and_args,
        )

    def test_init_name(self):
        trait = PyfaceColor("rebeccapurple")
        self.assertEqual(
            trait.default_value,
            (Color, (), {'rgba': (0.4, 0.2, 0.6, 1.0)})
        )

    def test_init_hex(self):
        trait = PyfaceColor("#663399ff")
        self.assertEqual(
            trait.default_value,
            (Color, (), {'rgba': (0.4, 0.2, 0.6, 1.0)})
        )

    def test_init_color(self):
        trait = PyfaceColor(Color(rgba=(0.4, 0.2, 0.6, 1.0)))
        self.assertEqual(
            trait.default_value,
            (Color, (), {'rgba': (0.4, 0.2, 0.6, 1.0)})
        )

    def test_init_tuple(self):
        trait = PyfaceColor((0.4, 0.2, 0.6, 1.0))
        self.assertEqual(
            trait.default_value,
            (Color, (), {'rgba': (0.4, 0.2, 0.6, 1.0)})
        )

    def test_init_list(self):
        trait = PyfaceColor([0.4, 0.2, 0.6, 1.0])
        self.assertEqual(
            trait.default_value,
            (Color, (), {'rgba': (0.4, 0.2, 0.6, 1.0)})
        )

    @requires_numpy
    def test_init_array(self):
        trait = PyfaceColor(np.array([0.4, 0.2, 0.6, 1.0]))
        self.assertEqual(
            trait.default_value,
            (Color, (), {'rgba': (0.4, 0.2, 0.6, 1.0)})
        )

    @requires_numpy
    def test_init_array_structured_dtype(self):
        """ Test if "typical" RGBA structured array value works. """
        arr = np.array(
            [(0.4, 0.2, 0.6, 1.0)],
            dtype=np.dtype([
                ('red', float),
                ('green', float),
                ('blue', float),
                ('alpha', float),
            ]),
        )
        trait = PyfaceColor(arr[0])
        self.assertEqual(
            trait.default_value,
            (Color, (), {'rgba': (0.4, 0.2, 0.6, 1.0)})
        )

    def test_init_invalid(self):
        with self.assertRaises(TraitError):
            PyfaceColor((0.4, 0.2))

    def test_validate_color(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 1.0))
        trait = PyfaceColor()
        validated = trait.validate(None, None, color)
        self.assertIs(
            validated, color
        )

    def test_validate_name(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 1.0))
        trait = PyfaceColor()
        validated = trait.validate(None, None, "rebeccapurple")
        self.assertEqual(
            validated, color
        )

    def test_validate_hex(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 1.0))
        trait = PyfaceColor()
        validated = trait.validate(None, None, "#663399ff")
        self.assertEqual(
            validated, color
        )

    def test_validate_tuple(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        trait = PyfaceColor()
        validated = trait.validate(None, None, (0.4, 0.2, 0.6, 0.8))
        self.assertEqual(
            validated, color
        )

    def test_validate_list(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        trait = PyfaceColor()
        validated = trait.validate(None, None, [0.4, 0.2, 0.6, 0.8])
        self.assertEqual(
            validated, color
        )

    def test_validate_rgb_list(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 1.0))
        trait = PyfaceColor()
        validated = trait.validate(None, None, [0.4, 0.2, 0.6])
        self.assertEqual(
            validated, color
        )

    def test_validate_bad_string(self):
        trait = PyfaceColor()
        with self.assertRaises(TraitError):
            trait.validate(None, None, "not a color")

    def test_validate_bad_object(self):
        trait = PyfaceColor()
        with self.assertRaises(TraitError):
            trait.validate(None, None, object())

    def test_info(self):
        trait = PyfaceColor()
        self.assertIsInstance(trait.info(), str)

    def test_default_trait(self):
        color_class = ColorClass()
        self.assertEqual(color_class.color, Color())

    def test_set_color(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 1.0))
        color_class = ColorClass(color=color)
        self.assertIs(color_class.color, color)

    def test_set_name(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 1.0))
        color_class = ColorClass(color="rebeccapurple")
        self.assertEqual(color_class.color, color)

    def test_set_hex(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 1.0))
        color_class = ColorClass(color="#663399ff")
        self.assertEqual(color_class.color, color)

    def test_set_tuple(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 1.0))
        color_class = ColorClass(color=(0.4, 0.2, 0.6, 1.0))
        self.assertEqual(color_class.color, color)

    def test_set_list(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 1.0))
        color_class = ColorClass(color=[0.4, 0.2, 0.6, 1.0])
        self.assertEqual(color_class.color, color)

    @requires_numpy
    def test_set_array(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 1.0))
        color_class = ColorClass(color=np.array([0.4, 0.2, 0.6, 1.0]))
        self.assertEqual(color_class.color, color)

    @requires_numpy
    def test_set_structured_dtype(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 1.0))
        arr = np.array(
            [(0.4, 0.2, 0.6, 1.0)],
            dtype=np.dtype([
                ('red', float),
                ('green', float),
                ('blue', float),
                ('alpha', float),
            ]),
        )
        color_class = ColorClass(color=arr[0])
        self.assertEqual(color_class.color, color)


class TestHasMargin(unittest.TestCase, UnittestTools):
    def test_defaults(self):
        has_margin = HasMarginClass()
        margin = has_margin.margin

        self.assertEqual(margin.top, 0)
        self.assertEqual(margin.bottom, 0)
        self.assertEqual(margin.left, 0)
        self.assertEqual(margin.right, 0)

    def test_unspecified_default(self):
        trait = HasMargin()
        trait.default_value_type = DefaultValue.unspecified

        (dvt, dv) = trait.get_default_value()

        self.assertEqual(dvt, DefaultValue.callable_and_args)
        self.assertEqual(
            dv, (Margin, (), {"top": 0, "bottom": 0, "left": 0, "right": 0})
        )

    def test_default_int(self):
        class HasMarginClass(HasTraits):

            margin = HasMargin(4)

        has_margin = HasMarginClass()
        margin = has_margin.margin

        self.assertEqual(margin.top, 4)
        self.assertEqual(margin.bottom, 4)
        self.assertEqual(margin.left, 4)
        self.assertEqual(margin.right, 4)

    def test_default_one_tuple(self):
        class HasMarginClass(HasTraits):

            margin = HasMargin((4,))

        has_margin = HasMarginClass()
        margin = has_margin.margin

        self.assertEqual(margin.top, 4)
        self.assertEqual(margin.bottom, 4)
        self.assertEqual(margin.left, 4)
        self.assertEqual(margin.right, 4)

    def test_default_two_tuple(self):
        class HasMarginClass(HasTraits):

            margin = HasMargin((4, 2))

        has_margin = HasMarginClass()
        margin = has_margin.margin

        self.assertEqual(margin.top, 2)
        self.assertEqual(margin.bottom, 2)
        self.assertEqual(margin.left, 4)
        self.assertEqual(margin.right, 4)

    def test_default_four_tuple(self):
        class HasMarginClass(HasTraits):

            margin = HasMargin((4, 2, 3, 1))

        has_margin = HasMarginClass()
        margin = has_margin.margin

        self.assertEqual(margin.top, 3)
        self.assertEqual(margin.bottom, 1)
        self.assertEqual(margin.left, 4)
        self.assertEqual(margin.right, 2)

    def test_default_margin(self):
        m = Margin(left=4, right=2, top=3, bottom=1)

        class HasMarginClass(HasTraits):

            margin = HasMargin(m)

        has_margin = HasMarginClass()
        margin = has_margin.margin

        self.assertEqual(margin.top, 3)
        self.assertEqual(margin.bottom, 1)
        self.assertEqual(margin.left, 4)
        self.assertEqual(margin.right, 2)

    def test_init_int(self):
        has_margin = HasMarginClass(margin=4)
        margin = has_margin.margin

        self.assertEqual(margin.top, 4)
        self.assertEqual(margin.bottom, 4)
        self.assertEqual(margin.left, 4)
        self.assertEqual(margin.right, 4)

    def test_init_one_tuple(self):
        has_margin = HasMarginClass(margin=(4,))
        margin = has_margin.margin

        self.assertEqual(margin.top, 4)
        self.assertEqual(margin.bottom, 4)
        self.assertEqual(margin.left, 4)
        self.assertEqual(margin.right, 4)

    def test_init_two_tuple(self):
        has_margin = HasMarginClass(margin=(4, 2))
        margin = has_margin.margin

        self.assertEqual(margin.top, 2)
        self.assertEqual(margin.bottom, 2)
        self.assertEqual(margin.left, 4)
        self.assertEqual(margin.right, 4)

    def test_init_four_tuple(self):
        has_margin = HasMarginClass(margin=(4, 2, 3, 1))
        margin = has_margin.margin

        self.assertEqual(margin.top, 3)
        self.assertEqual(margin.bottom, 1)
        self.assertEqual(margin.left, 4)
        self.assertEqual(margin.right, 2)

    def test_init_margin(self):
        margin = Margin()
        has_margin = HasMarginClass(margin=margin)

        self.assertEqual(has_margin.margin, margin)

    def test_set_int(self):
        has_margin = HasMarginClass()
        with self.assertTraitChanges(has_margin, "margin", 1):
            has_margin.margin = 4

        margin = has_margin.margin
        self.assertEqual(margin.top, 4)
        self.assertEqual(margin.bottom, 4)
        self.assertEqual(margin.left, 4)
        self.assertEqual(margin.right, 4)

    def test_set_one_tuple(self):
        has_margin = HasMarginClass()
        with self.assertTraitChanges(has_margin, "margin", 1):
            has_margin.margin = (4,)

        margin = has_margin.margin

        self.assertEqual(margin.top, 4)
        self.assertEqual(margin.bottom, 4)
        self.assertEqual(margin.left, 4)
        self.assertEqual(margin.right, 4)

    def test_set_two_tuple(self):
        has_margin = HasMarginClass()
        with self.assertTraitChanges(has_margin, "margin", 1):
            has_margin.margin = (4, 2)

        margin = has_margin.margin

        self.assertEqual(margin.top, 2)
        self.assertEqual(margin.bottom, 2)
        self.assertEqual(margin.left, 4)
        self.assertEqual(margin.right, 4)

    def test_set_four_tuple(self):
        has_margin = HasMarginClass()
        with self.assertTraitChanges(has_margin, "margin", 1):
            has_margin.margin = (4, 2, 3, 1)

        margin = has_margin.margin
        self.assertEqual(margin.top, 3)
        self.assertEqual(margin.bottom, 1)
        self.assertEqual(margin.left, 4)
        self.assertEqual(margin.right, 2)

    def test_set_margin(self):
        margin = Margin()
        has_margin = HasMarginClass()
        with self.assertTraitChanges(has_margin, "margin", 1):
            has_margin.margin = margin

        self.assertEqual(has_margin.margin, margin)

    def test_set_invalid(self):
        has_margin = HasMarginClass()
        with self.assertRaises(TraitError):
            has_margin.margin = (1, 2, 3)


class TestBorder(unittest.TestCase):
    def test_defaults(self):
        border = Border()
        self.assertEqual(border.top, 0)
        self.assertEqual(border.bottom, 0)
        self.assertEqual(border.left, 0)
        self.assertEqual(border.right, 0)

    def test_init_one_arg(self):
        border = Border(4)
        self.assertEqual(border.top, 4)
        self.assertEqual(border.bottom, 4)
        self.assertEqual(border.left, 4)
        self.assertEqual(border.right, 4)

    def test_init_two_args(self):
        border = Border(4, 2)
        self.assertEqual(border.top, 2)
        self.assertEqual(border.bottom, 2)
        self.assertEqual(border.left, 4)
        self.assertEqual(border.right, 4)

    def test_init_four_args(self):
        border = Border(4, 2, 3, 1)
        self.assertEqual(border.top, 3)
        self.assertEqual(border.bottom, 1)
        self.assertEqual(border.left, 4)
        self.assertEqual(border.right, 2)


class TestHasBorder(unittest.TestCase, UnittestTools):
    def test_defaults(self):
        has_border = HasBorderClass()
        border = has_border.border

        self.assertEqual(border.top, 0)
        self.assertEqual(border.bottom, 0)
        self.assertEqual(border.left, 0)
        self.assertEqual(border.right, 0)

    def test_unspecified_default(self):
        trait = HasBorder()
        trait.default_value_type = DefaultValue.unspecified

        (dvt, dv) = trait.get_default_value()

        self.assertEqual(dvt, DefaultValue.callable_and_args)
        self.assertEqual(
            dv, (Border, (), {"top": 0, "bottom": 0, "left": 0, "right": 0})
        )

    def test_default_int(self):
        class HasBorderClass(HasTraits):

            border = HasBorder(4)

        has_border = HasBorderClass()
        border = has_border.border

        self.assertEqual(border.top, 4)
        self.assertEqual(border.bottom, 4)
        self.assertEqual(border.left, 4)
        self.assertEqual(border.right, 4)

    def test_default_one_tuple(self):
        class HasBorderClass(HasTraits):

            border = HasBorder((4,))

        has_border = HasBorderClass()
        border = has_border.border

        self.assertEqual(border.top, 4)
        self.assertEqual(border.bottom, 4)
        self.assertEqual(border.left, 4)
        self.assertEqual(border.right, 4)

    def test_default_two_tuple(self):
        class HasBorderClass(HasTraits):

            border = HasBorder((4, 2))

        has_border = HasBorderClass()
        border = has_border.border

        self.assertEqual(border.top, 2)
        self.assertEqual(border.bottom, 2)
        self.assertEqual(border.left, 4)
        self.assertEqual(border.right, 4)

    def test_default_four_tuple(self):
        class HasBorderClass(HasTraits):

            border = HasBorder((4, 2, 3, 1))

        has_border = HasBorderClass()
        border = has_border.border

        self.assertEqual(border.top, 3)
        self.assertEqual(border.bottom, 1)
        self.assertEqual(border.left, 4)
        self.assertEqual(border.right, 2)

    def test_default_border(self):
        m = Margin(left=4, right=2, top=3, bottom=1)

        class HasBorderClass(HasTraits):

            border = HasBorder(m)

        has_border = HasBorderClass()
        border = has_border.border

        self.assertEqual(border.top, 3)
        self.assertEqual(border.bottom, 1)
        self.assertEqual(border.left, 4)
        self.assertEqual(border.right, 2)

    def test_init_int(self):
        has_border = HasBorderClass(border=4)
        border = has_border.border

        self.assertEqual(border.top, 4)
        self.assertEqual(border.bottom, 4)
        self.assertEqual(border.left, 4)
        self.assertEqual(border.right, 4)

    def test_init_one_tuple(self):
        has_border = HasBorderClass(border=(4,))
        border = has_border.border

        self.assertEqual(border.top, 4)
        self.assertEqual(border.bottom, 4)
        self.assertEqual(border.left, 4)
        self.assertEqual(border.right, 4)

    def test_init_two_tuple(self):
        has_border = HasBorderClass(border=(4, 2))
        border = has_border.border

        self.assertEqual(border.top, 2)
        self.assertEqual(border.bottom, 2)
        self.assertEqual(border.left, 4)
        self.assertEqual(border.right, 4)

    def test_init_four_tuple(self):
        has_border = HasBorderClass(border=(4, 2, 3, 1))
        border = has_border.border

        self.assertEqual(border.top, 3)
        self.assertEqual(border.bottom, 1)
        self.assertEqual(border.left, 4)
        self.assertEqual(border.right, 2)

    def test_init_border(self):
        border = Border()
        has_border = HasBorderClass(border=border)

        self.assertEqual(has_border.border, border)

    def test_set_int(self):
        has_border = HasBorderClass()
        with self.assertTraitChanges(has_border, "border", 1):
            has_border.border = 4

        border = has_border.border
        self.assertEqual(border.top, 4)
        self.assertEqual(border.bottom, 4)
        self.assertEqual(border.left, 4)
        self.assertEqual(border.right, 4)

    def test_set_one_tuple(self):
        has_border = HasBorderClass()
        with self.assertTraitChanges(has_border, "border", 1):
            has_border.border = (4,)

        border = has_border.border

        self.assertEqual(border.top, 4)
        self.assertEqual(border.bottom, 4)
        self.assertEqual(border.left, 4)
        self.assertEqual(border.right, 4)

    def test_set_two_tuple(self):
        has_border = HasBorderClass()
        with self.assertTraitChanges(has_border, "border", 1):
            has_border.border = (4, 2)

        border = has_border.border

        self.assertEqual(border.top, 2)
        self.assertEqual(border.bottom, 2)
        self.assertEqual(border.left, 4)
        self.assertEqual(border.right, 4)

    def test_set_four_tuple(self):
        has_border = HasBorderClass()
        with self.assertTraitChanges(has_border, "border", 1):
            has_border.border = (4, 2, 3, 1)

        border = has_border.border
        self.assertEqual(border.top, 3)
        self.assertEqual(border.bottom, 1)
        self.assertEqual(border.left, 4)
        self.assertEqual(border.right, 2)

    def test_set_border(self):
        border = Border()
        has_border = HasBorderClass()
        with self.assertTraitChanges(has_border, "border", 1):
            has_border.border = border

        self.assertEqual(has_border.border, border)

    def test_set_invalid(self):
        has_border = HasBorderClass()
        with self.assertRaises(TraitError):
            has_border.border = (1, 2, 3)
