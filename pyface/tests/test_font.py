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

from traits.api import HasStrictTraits, TraitError

from pyface.font import Font, FontSize, FontStretch, SIZES, STRETCHES
from pyface.toolkit import toolkit_object


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
        for size in ["badvalue", -1.0, "-1.0", "0pt"]:
            with self.subTest(size=size):
                with self.assertRaises(TraitError):
                    FontSize(size)

    def test_font_size_trait_validate(self):
        dummy = FontSizeDummy()
        for size, expected in [
            (14.0, 14.0),
            ("15.0", 15.0),
            ("16pt", 16.0),
            ("17.0px", 17.0),
        ]:
            with self.subTest(size=size):
                dummy.size = size
                self.assertEqual(dummy.size, expected)

    def test_font_size_trait_invalid_validate(self):
        dummy = FontSizeDummy()
        for size in ["badvalue", -1.0, "-1.0", "0pt"]:
            with self.subTest(size=size):
                with self.assertRaises(TraitError):
                    dummy.size = size


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
        for stretch in ["badvalue", 49.5, "49.5", "49.5%", 200.1]:
            with self.subTest(stretch=stretch):
                with self.assertRaises(TraitError):
                    FontStretch(stretch)

    def test_font_stretch_trait_validate(self):
        dummy = FontStretchDummy()

        for stretch, expected in [
            (150.0, 150.0),
            ("125", 125.0),
            ("50%", 50.0),
            ("ultra-expanded", 200.0)
        ]:
            with self.subTest(stretch=stretch):
                dummy.stretch = stretch
                self.assertEqual(dummy.stretch, expected)

    def test_font_stretch_trait_invalid_validate(self):
        dummy = FontStretchDummy()
        for stretch in ["badvalue", 49.5, "200.1", "49.9%"]:
            with self.subTest(stretch=stretch):
                with self.assertRaises(TraitError):
                    dummy.stretch = stretch


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
            weight='demi-bold',
            stretch='condensed',
            style='italic',
            variants={'small-caps'},
            decorations={'underline'},
        )

        self.assertEqual(font.family, ['Helvetica', 'sans-serif'])
        self.assertEqual(font.size, 14.0)
        self.assertEqual(font.weight, 'demi-bold')
        self.assertEqual(font.weight_, 600)
        self.assertEqual(font.stretch, 75)
        self.assertEqual(font.style, 'italic')
        self.assertEqual(font.variants, {'small-caps'})
        self.assertEqual(font.decorations, {'underline'})

    def test_family_sequence(self):
        font = Font(family=('Helvetica', 'sans-serif'))
        self.assertEqual(font.family, ['Helvetica', 'sans-serif'])

    def test_variants_frozenset(self):
        font = Font(variants=frozenset({'small-caps'}))
        self.assertEqual(font.variants, {'small-caps'})

    def test_decorations_frozenset(self):
        font = Font(decorations=frozenset({'underline'}))
        self.assertEqual(font.decorations, {'underline'})

    def test_str(self):
        font = Font()

        description = str(font)

        self.assertEqual(description, "12pt default")

    def test_str_typical(self):
        font = Font(
            family=['Comic Sans', 'decorative'],
            size='large',
            weight='demi-bold',
            stretch='condensed',
            style='italic',
            variants={'small-caps'},
            decorations={'underline'},
        )

        description = str(font)

        self.assertEqual(
            description,
            "italic small-caps underline demi-bold 75% 14pt "
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
            weight='demi-bold',
            stretch='condensed',
            style='italic',
            variants={'small-caps'},
            decorations={'underline'},
        )

        text = repr(font)

        # this is little more than a smoke check, but good enough
        self.assertTrue(text.startswith('Font('))

    def test_to_toolkit(self):
        font = Font()

        # smoke test
        toolkit_font = font.to_toolkit()
        self.assertIsNotNone(toolkit_font)

    def test_to_toolkit_typical(self):
        font = Font(
            family=['Helvetica', 'sans-serif'],
            size='large',
            weight='demi-bold',
            stretch='condensed',
            style='italic',
            variants={'small-caps'},
            decorations={'underline', 'strikethrough', 'overline'},
        )

        # smoke test
        toolkit_font = font.to_toolkit()
        self.assertIsNotNone(toolkit_font)

    def test_toolkit_default_roundtrip(self):
        font = Font()

        # smoke test
        result = Font.from_toolkit(font.to_toolkit())

        # defaults should round-trip
        self.assertTrue(result.family[-1], 'default')
        self.assertEqual(result.size, font.size)
        self.assertEqual(result.weight, font.weight)
        self.assertEqual(result.stretch, font.stretch)
        self.assertEqual(result.variants, font.variants)
        self.assertEqual(result.decorations, font.decorations)

    def test_from_toolkit_typical(self):
        font = Font(
            family=['Helvetica', 'sans-serif'],
            size='large',
            weight='bold',
            stretch='condensed',
            style='italic',
            variants={'small-caps'},
            decorations={'underline', 'strikethrough', 'overline'},
        )

        # smoke test
        result = Font.from_toolkit(font.to_toolkit())

        # we expect some things should round-trip no matter what system
        self.assertEqual(result.size, font.size)
        self.assertEqual(result.weight, font.weight)
        self.assertEqual(result.style, font.style)

    def test_toolkit_font_to_properties(self):
        toolkit_font_to_properties = toolkit_object(
            'font:toolkit_font_to_properties')

        font = Font(
            family=['Helvetica', 'sans-serif'],
            size='large',
            weight='demi-bold',
            stretch='condensed',
            style='italic',
            variants={'small-caps'},
            decorations={'underline', 'strikethrough', 'overline'},
        )

        properties = toolkit_font_to_properties(font.to_toolkit())

        self.assertEqual(
            set(properties.keys()),
            {
                'family', 'size', 'stretch', 'weight', 'style', 'variants',
                'decorations'
            }
        )
