# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
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

from ..font import (
    Font, FontSize, FontStretch, FontParseError, PyfaceFont,
    parse_font_description, SIZES, STRETCHES, STYLES, VARIANTS, WEIGHTS
)


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

        dummy.size = "x-large"
        self.assertEqual(dummy.size, 18.0)

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

    def test_from_description(self):
        font = Font.from_description(
            "italic small-caps underline demibold condensed 14pt Helvetica, "
            "sans-serif"
        )

        self.assertEqual(font.family, ['Helvetica', 'sans-serif'])
        self.assertEqual(font.size, 14.0)
        self.assertEqual(font.weight, 'demibold')
        self.assertEqual(font.weight_, 600)
        self.assertEqual(font.stretch, 75)
        self.assertEqual(font.style, 'italic')
        self.assertEqual(font.variants, {'small-caps', 'underline'})

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


class TestParseFontDescription(unittest.TestCase):

    def test_empty(self):
        properties = parse_font_description("")
        self.assertEqual(
            properties,
            {
                'family': ['default'],
                'size': 12.0,
                'weight': 'normal',
                'stretch': 100,
                'style': 'normal',
                'variants': set()
            }
        )

    def test_typical(self):
        properties = parse_font_description(
            "small-caps underline overline strikethrough condensed demibold "
            "italic 18pt Helvetica, sans-serif"
        )
        self.assertEqual(
            properties,
            {
                'family': ['Helvetica', 'sans-serif'],
                'size': 18.0,
                'weight': 'demibold',
                'stretch': 75,
                'style': 'italic',
                'variants': set(VARIANTS)
            }
        )

    def test_families(self):
        sub_cases = {
            'default': ['default'],
            'san-serif': ['san-serif'],
            'Helvetica': ['Helvetica'],
            '"Comic Sans"': ['Comic Sans'],
            "'Comic Sans'": ['Comic Sans'],
            "Times, serif": ['Times', 'serif'],
            "'Times New Roman', serif": ['Times New Roman', 'serif'],
            '"Times New Roman", serif': ['Times New Roman', 'serif'],
            'serif, "Times New Roman"': ['serif', 'Times New Roman'],
            "Times serif": ['Times', 'serif'],
            "'Times New Roman' serif": ['Times New Roman', 'serif'],
            '"Times New Roman" serif': ['Times New Roman', 'serif'],
            'serif "Times New Roman"': ['serif', 'Times New Roman'],
            '"italic"': ['italic'],
            '"0!@#$%^&*()_+-={}[]\\|;:/?.,<>`~"':
            ['0!@#$%^&*()_+-={}[]\\|;:/?.,<>`~'],
        }
        for text, family in sub_cases.items():
            with self.subTest(text=text):
                properties = parse_font_description(text)
                self.assertEqual(
                    properties,
                    {
                        'family': family,
                        'size': 12.0,
                        'weight': 'normal',
                        'stretch': 100,
                        'style': 'normal',
                        'variants': set(),
                    }
                )

    def test_styles(self):
        for style in STYLES:
            with self.subTest(style=style):
                properties = parse_font_description(style)
                self.assertEqual(
                    properties,
                    {
                        'family': ['default'],
                        'size': 12.0,
                        'weight': 'normal',
                        'stretch': 100,
                        'style': style,
                        'variants': set(),
                    }
                )

    def test_variants(self):
        for variant in VARIANTS:
            with self.subTest(variant=variant):
                properties = parse_font_description(variant)
                self.assertEqual(
                    properties,
                    {
                        'family': ['default'],
                        'size': 12.0,
                        'weight': 'normal',
                        'stretch': 100,
                        'style': 'normal',
                        'variants': {variant},
                    }
                )

    def test_stretches(self):
        for stretch, value in STRETCHES.items():
            with self.subTest(stretch=stretch):
                properties = parse_font_description(stretch)
                self.assertEqual(
                    properties,
                    {
                        'family': ['default'],
                        'size': 12.0,
                        'weight': 'normal',
                        'stretch': value,
                        'style': 'normal',
                        'variants': set(),
                    }
                )

    def test_weights(self):
        sub_cases = WEIGHTS
        for weight in sub_cases:
            with self.subTest(weight=weight):
                properties = parse_font_description(weight)
                self.assertEqual(
                    properties,
                    {
                        'family': ['default'],
                        'size': 12.0,
                        'weight': weight,
                        'stretch': 100,
                        'style': 'normal',
                        'variants': set(),
                    }
                )

    def test_sizes(self):
        sub_cases = {
            '14': 14.0,
            '14.': 14.0,
            '14.5': 14.5,
            '14pt': 14.0,
            '14.pt': 14.0,
            '14.5pt': 14.5
        }
        sub_cases.update(SIZES)
        for size, point_size in sub_cases.items():
            with self.subTest(size=size):
                properties = parse_font_description(size)
                self.assertEqual(
                    properties,
                    {
                        'family': ['default'],
                        'size': point_size,
                        'weight': 'normal',
                        'stretch': 100,
                        'style': 'normal',
                        'variants': set(),
                    }
                )

    def test_weight_size_corner_cases(self):
        sub_cases = {
            '100': {'weight': '100', 'size': 12.0},
            '100pt': {'weight': 'normal', 'size': 100.0},
            '100.': {'weight': 'normal', 'size': 100.0},
            '100.0': {'weight': 'normal', 'size': 100.0},
            '100 100': {'weight': '100', 'size': 100.0},
            '100 200': {'weight': '100', 'size': 200.0},
        }
        for text, output in sub_cases.items():
            with self.subTest(text=text):
                properties = parse_font_description(text)
                expected = {
                    'family': ['default'],
                    'stretch': 100,
                    'style': 'normal',
                    'variants': set(),
                }
                expected.update(output)
                self.assertEqual(properties, expected)

    def test_failures(self):
        sub_cases = [
            'bold demibold',  # two weights
            'extra-condensed ultra-condensed',  # two stretches
            'small-caps small-caps',  # two styles
            '10pt 12pt',  # two sizes
            'default #*@&#*',  # bad token
        ]
        for text in sub_cases:
            with self.subTest(text=text):
                with self.assertRaises(FontParseError):
                    parse_font_description(text)


class TestPyfaceFontTrait(unittest.TestCase):

    def test_simple_init(self):
        trait = PyfaceFont()

        self.assertEqual(trait.default_value, (Font, (), {}))

    def test_dict_init(self):
        trait = PyfaceFont({'size': 12, 'family': ["Comic Sans"]})

        self.assertEqual(
            trait.default_value,
            (Font, (), {'size': 12, 'family': ("Comic Sans",)})
        )

    def test_str_init(self):
        trait = PyfaceFont('12pt "Comic Sans"')

        self.assertEqual(
            trait.default_value,
            (
                Font,
                (),
                {
                    'size': 12,
                    'family': ("Comic Sans",),
                    'weight': 'normal',
                    'style': 'normal',
                    'stretch': 100,
                    'variants': frozenset(),
                }
            )
        )

    def test_font_init(self):
        trait = PyfaceFont(Font(size='12pt', family=["Comic Sans"]))

        self.assertEqual(
            trait.default_value,
            (
                Font,
                (),
                {
                    'size': 12,
                    'family': ("Comic Sans",),
                    'weight': 'normal',
                    'style': 'normal',
                    'stretch': 100,
                    'variants': frozenset(),
                }
            )
        )

    def test_font_validate_str(self):
        trait = PyfaceFont()

        result = trait.validate(None, None, '12pt "Comic Sans"')

        self.assertEqual(result, Font.from_description('12pt "Comic Sans"'))

    def test_font_validate_font(self):
        trait = PyfaceFont()
        font = Font.from_description('12pt "Comic Sans"')

        result = trait.validate(None, None, font)

        self.assertIs(result, font)

    def test_font_validate_invalid_type(self):
        trait = PyfaceFont()

        with self.assertRaises(TraitError):
            trait.validate(None, None, 12)

    def test_font_validate_invalid_string(self):
        trait = PyfaceFont()

        with self.assertRaises(TraitError):
            trait.validate(None, None, 'default #*@&#*')

