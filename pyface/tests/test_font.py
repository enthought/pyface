# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import unittest

from traits.api import HasStrictTraits, TraitError

from pyface.font import Font, FontSize, FontStretch, SIZES, STRETCHES


class FontSizeDummy(HasStrictTraits):

    size = FontSize()
    size_default_1 = FontSize(14.0)
    size_default_2 = FontSize("14.0")
    size_default_3 = FontSize("14.0pt")
    size_default_4 = FontSize("large")


class TestFontSizeTrait(unittest.TestCase):

    def test_font_size_trait_defaults(self):
        dummy = FontSizeDummy()

        self.assertEqual(dummy.size, 12.0)
        self.assertEqual(dummy.size_default_1, 14.0)
        self.assertEqual(dummy.size_default_2, 14.0)
        self.assertEqual(dummy.size_default_3, 14.0)
        self.assertEqual(dummy.size_default_4, 14.0)

    def test_font_sizes(self):
        dummy = FontSizeDummy()
        for size, value in SIZES.items():
            with self.subTest(size=size):
                dummy.size = size
                self.assertEqual(dummy.size, value)

    def test_font_size_trait_invalid_default(self):
        with self.assertRaises(TraitError):
            FontSize("badvalue")

        with self.assertRaises(TraitError):
            FontSize(-1.0)

        with self.assertRaises(TraitError):
            FontSize("-1.0")

        with self.assertRaises(TraitError):
            FontSize("0pt")

    def test_font_size_trait_validate(self):
        dummy = FontSizeDummy()

        dummy.size = 14.0
        self.assertEqual(dummy.size, 14.0)

        dummy.size = "15.0"
        self.assertEqual(dummy.size, 15.0)

        dummy.size = "16.0pt"
        self.assertEqual(dummy.size, 16.0)

        dummy.size = "17.0px"
        self.assertEqual(dummy.size, 17.0)

    def test_font_size_trait_invalid_validate(self):
        dummy = FontSizeDummy()

        with self.assertRaises(TraitError):
            dummy.size = "badvalue"

        with self.assertRaises(TraitError):
            dummy.size = -1.0

        with self.assertRaises(TraitError):
            dummy.size = "-1.0"

        with self.assertRaises(TraitError):
            dummy.size = "0pt"


class FontStretchDummy(HasStrictTraits):

    stretch = FontStretch()
    stretch_default_1 = FontStretch(150)
    stretch_default_2 = FontStretch("150.0")
    stretch_default_3 = FontStretch("150.0%")
    stretch_default_4 = FontStretch("expanded")


class TestFontStretchTrait(unittest.TestCase):

    def test_font_stretch_trait_defaults(self):
        dummy = FontStretchDummy()

        self.assertEqual(dummy.stretch, 100.0)
        self.assertEqual(dummy.stretch_default_1, 150.0)
        self.assertEqual(dummy.stretch_default_2, 150.0)
        self.assertEqual(dummy.stretch_default_3, 150.0)
        self.assertEqual(dummy.stretch_default_4, 125.0)

    def test_font_stretches(self):
        dummy = FontStretchDummy()
        for stretch, value in STRETCHES.items():
            with self.subTest(stretch=stretch):
                dummy.stretch = stretch
                self.assertEqual(dummy.stretch, value)

    def test_font_stretch_trait_invalid_default(self):
        with self.assertRaises(TraitError):
            FontStretch("badvalue")

        with self.assertRaises(TraitError):
            FontStretch(49.5)

        with self.assertRaises(TraitError):
            FontStretch("49.5")

        with self.assertRaises(TraitError):
            FontStretch("49.5%")

        with self.assertRaises(TraitError):
            FontStretch(200.1)

    def test_font_stretch_trait_validate(self):
        dummy = FontStretchDummy()

        dummy.stretch = 150.0
        self.assertEqual(dummy.stretch, 150.0)

        dummy.stretch = "125"
        self.assertEqual(dummy.stretch, 125.0)

        dummy.stretch = "50%"
        self.assertEqual(dummy.stretch, 50.0)

        dummy.stretch = "ultra-expanded"
        self.assertEqual(dummy.stretch, 200.0)

    def test_font_stretch_trait_invalid_validate(self):
        dummy = FontStretchDummy()

        with self.assertRaises(TraitError):
            dummy.stretch = "badvalue"

        with self.assertRaises(TraitError):
            dummy.stretch = 49.5

        with self.assertRaises(TraitError):
            dummy.stretch = "200.1"

        with self.assertRaises(TraitError):
            dummy.stretch = "49.9%"


class TestFont(unittest.TestCase):

    def test_default(self):
        font = Font()

        self.assertEqual(font.family, ['default'])
        self.assertEqual(font.size, 12.0)
        self.assertEqual(font.weight, 'normal')
        self.assertEqual(font.stretch, 100)
        self.assertEqual(font.style, 'normal')
        self.assertEqual(font.variants, set())

    def test_typical(self):
        font = Font(
            family=['Helvetica', 'sans-serif'],
            size='large',
            weight='demibold',
            stretch='condensed',
            style='italic',
            variants={'small-caps', 'underline'},
        )

        self.assertEqual(font.family, ['Helvetica', 'sans-serif'])
        self.assertEqual(font.size, 14.0)
        self.assertEqual(font.weight, 'demibold')
        self.assertEqual(font.weight_, 600)
        self.assertEqual(font.stretch, 75)
        self.assertEqual(font.style, 'italic')
        self.assertEqual(font.variants, {'small-caps', 'underline'})

    def test_family_sequence(self):
        font = Font(family=('Helvetica', 'sans-serif'))
        self.assertEqual(font.family, ['Helvetica', 'sans-serif'])

    def test_variants_frozenset(self):
        font = Font(variants=frozenset({'small-caps', 'underline'}))
        self.assertEqual(font.variants, {'small-caps', 'underline'})

    def test_str(self):
        font = Font()

        description = str(font)

        self.assertEqual(description, "12pt default")

    def test_str_typical(self):
        font = Font(
            family=['Comic Sans', 'decorative'],
            size='large',
            weight='demibold',
            stretch='condensed',
            style='italic',
            variants={'small-caps', 'underline'},
        )

        description = str(font)

        self.assertEqual(
            description,
            "italic small-caps underline demibold 75% 14pt "
            "'Comic Sans', decorative"
        )

    def test_repr(self):
        font = Font()

        text = repr(font)

        # this is little more than a smoke check, but good enough
        self.assertTrue(text.startswith('Font('))

    def test_repr_typical(self):
        font = Font(
            family=['Helvetica', 'sans-serif'],
            size='large',
            weight='demibold',
            stretch='condensed',
            style='italic',
            variants={'small-caps', 'underline'},
        )

        text = repr(font)

        # this is little more than a smoke check, but good enough
        self.assertTrue(text.startswith('Font('))

    def test_to_toolkit(self):
        font = Font()

        # smoke test
        toolkit_font = font.to_toolkit()

    def test_to_toolkit_typical(self):
        font = Font(
            family=['Helvetica', 'sans-serif'],
            size='large',
            weight='demibold',
            stretch='condensed',
            style='italic',
            variants={'small-caps', 'underline'},
        )

        # smoke test
        toolkit_font = font.to_toolkit()

    def test_from_toolkit(self):
        font = Font()

        # smoke test
        result = Font.from_toolkit(font.to_toolkit())

    def test_from_toolkit_typical(self):
        font = Font(
            family=['Helvetica', 'sans-serif'],
            size='large',
            weight='demibold',
            stretch='condensed',
            style='italic',
            variants={'small-caps', 'underline'},
        )

        # smoke test
        result = Font.from_toolkit(font.to_toolkit())
