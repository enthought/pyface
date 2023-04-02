# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from itertools import chain, combinations
from unittest import TestCase

from ..font_parser import (
    DECORATIONS,
    GENERIC_FAMILIES,
    NOISE,
    STRETCHES,
    STYLES,
    VARIANTS,
    WEIGHTS,
    simple_parser,
)


class TestSimpleParser(TestCase):

    def test_empty(self):
        properties = simple_parser("")
        self.assertEqual(
            properties,
            {
                'family': ["default"],
                'size': 12.0,
                'weight': "normal",
                'stretch': "normal",
                'style': "normal",
                'variants': set(),
                'decorations': set(),
            },
        )

    def test_typical(self):
        properties = simple_parser(
            "10 pt bold condensed italic underline Helvetica sans-serif")
        self.assertEqual(
            properties,
            {
                'family': ["helvetica", "sans-serif"],
                'size': 10.0,
                'weight': "bold",
                'stretch': "condensed",
                'style': "italic",
                'variants': set(),
                'decorations': {"underline"},
            },
        )

    def test_noise(self):
        for noise in NOISE:
            with self.subTest(noise=noise):
                properties = simple_parser(noise)
                self.assertEqual(
                    properties,
                    {
                        'family': ["default"],
                        'size': 12.0,
                        'weight': "normal",
                        'stretch': "normal",
                        'style': "normal",
                        'variants': set(),
                        'decorations': set(),
                    },
                )

    def test_generic_families(self):
        for family in GENERIC_FAMILIES:
            with self.subTest(family=family):
                properties = simple_parser(family)
                self.assertEqual(
                    properties,
                    {
                        'family': [family],
                        'size': 12.0,
                        'weight': "normal",
                        'stretch': "normal",
                        'style': "normal",
                        'variants': set(),
                        'decorations': set(),
                    },
                )

    def test_size(self):
        for size in [12, 24, 12.5]:
            with self.subTest(size=size):
                properties = simple_parser(str(size))
                self.assertEqual(
                    properties,
                    {
                        'family': ["default"],
                        'size': size,
                        'weight': "normal",
                        'stretch': "normal",
                        'style': "normal",
                        'variants': set(),
                        'decorations': set(),
                    },
                )

    def test_weight(self):
        for weight in WEIGHTS:
            with self.subTest(weight=weight):
                properties = simple_parser(weight)
                self.assertEqual(
                    properties,
                    {
                        'family': ["default"],
                        'size': 12.0,
                        'weight': weight,
                        'stretch': "normal",
                        'style': "normal",
                        'variants': set(),
                        'decorations': set(),
                    },
                )

    def test_stretch(self):
        for stretch in STRETCHES:
            with self.subTest(stretch=stretch):
                properties = simple_parser(stretch)
                self.assertEqual(
                    properties,
                    {
                        'family': ["default"],
                        'size': 12.0,
                        'weight': "normal",
                        'stretch': stretch,
                        'style': "normal",
                        'variants': set(),
                        'decorations': set(),
                    },
                )

    def test_style(self):
        for style in STYLES:
            with self.subTest(style=style):
                properties = simple_parser(style)
                self.assertEqual(
                    properties,
                    {
                        'family': ["default"],
                        'size': 12.0,
                        'weight': "normal",
                        'stretch': "normal",
                        'style': style,
                        'variants': set(),
                        'decorations': set(),
                    },
                )

    def test_variant(self):
        for variant in VARIANTS:
            with self.subTest(variant=variant):
                properties = simple_parser(variant)
                self.assertEqual(
                    properties,
                    {
                        'family': ["default"],
                        'size': 12.0,
                        'weight': "normal",
                        'stretch': "normal",
                        'style': "normal",
                        'variants': {variant},
                        'decorations': set(),
                    },
                )

    def test_decorations(self):
        # get powerset iterator of DECORATIONS
        all_decorations = chain.from_iterable(
            combinations(DECORATIONS, n)
            for n in range(len(DECORATIONS) + 1)
        )
        for decorations in all_decorations:
            with self.subTest(decorations=decorations):
                properties = simple_parser(" ".join(decorations))
                self.assertEqual(
                    properties,
                    {
                        'family': ["default"],
                        'size': 12.0,
                        'weight': "normal",
                        'stretch': "normal",
                        'style': "normal",
                        'variants': set(),
                        'decorations': set(decorations),
                    },
                )
