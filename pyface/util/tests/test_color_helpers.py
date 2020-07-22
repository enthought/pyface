# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from unittest import TestCase

from pyface.util.color_helpers import is_dark, relative_luminance


class TestRelativeLuminance(TestCase):

    def test_white(self):
        rgb = (1.0, 1.0, 1.0)
        result = relative_luminance(rgb)
        self.assertEqual(result, 1.0)

    def test_black(self):
        rgb = (0.0, 0.0, 0.0)
        result = relative_luminance(rgb)
        self.assertEqual(result, 0.0)

    def test_red(self):
        rgb = (1.0, 0.0, 0.0)
        result = relative_luminance(rgb)
        self.assertAlmostEqual(result, 0.2126)

    def test_green(self):
        rgb = (0.0, 1.0, 0.0)
        result = relative_luminance(rgb)
        self.assertAlmostEqual(result, 0.7152)

    def test_blue(self):
        rgb = (0.0, 0.0, 1.0)
        result = relative_luminance(rgb)
        self.assertAlmostEqual(result, 0.0722)

    def test_yellow(self):
        rgb = (1.0, 1.0, 0.0)
        result = relative_luminance(rgb)
        self.assertAlmostEqual(result, 0.2126 + 0.7152)

    def test_cyan(self):
        rgb = (0.0, 1.0, 1.0)
        result = relative_luminance(rgb)
        self.assertAlmostEqual(result, 0.7152 + 0.0722)

    def test_magenta(self):
        rgb = (1.0, 0.0, 1.0)
        result = relative_luminance(rgb)
        self.assertAlmostEqual(result, 0.2126 + 0.0722)

    def test_dark_grey(self):
        rgb = (0.01, 0.01, 0.01)
        result = relative_luminance(rgb)
        self.assertAlmostEqual(result, 0.01/12.92)

    def test_medium_grey(self):
        rgb = (0.5, 0.5, 0.5)
        result = relative_luminance(rgb)
        self.assertAlmostEqual(result, (0.555/1.055)**2.4)


class TestIsDark(TestCase):

    def test_white(self):
        rgb = (1.0, 1.0, 1.0)
        result = is_dark(rgb)
        self.assertFalse(result)

    def test_black(self):
        rgb = (0.0, 0.0, 0.0)
        result = is_dark(rgb)
        self.assertTrue(result)

    def test_red(self):
        rgb = (1.0, 0.0, 0.0)
        result = is_dark(rgb)
        self.assertFalse(result)

    def test_green(self):
        rgb = (0.0, 1.0, 0.0)
        result = is_dark(rgb)
        self.assertFalse(result)

    def test_blue(self):
        rgb = (0.0, 0.0, 1.0)
        result = is_dark(rgb)
        self.assertTrue(result)

    def test_yellow(self):
        rgb = (1.0, 1.0, 0.0)
        result = is_dark(rgb)
        self.assertFalse(result)

    def test_cyan(self):
        rgb = (0.0, 1.0, 1.0)
        result = is_dark(rgb)
        self.assertFalse(result)

    def test_magenta(self):
        rgb = (1.0, 0.0, 1.0)
        result = is_dark(rgb)
        self.assertFalse(result)

    def test_dark_grey(self):
        rgb = (0.01, 0.01, 0.01)
        result = is_dark(rgb)
        self.assertTrue(result)

    def test_medium_grey(self):
        rgb = (0.5, 0.5, 0.5)
        result = is_dark(rgb)
        self.assertFalse(result)
