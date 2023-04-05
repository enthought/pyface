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

from traits.testing.optional_dependencies import numpy as np, requires_numpy

if np is not None:
    from ..array_image import ArrayImage


@requires_numpy
class TestArrayImage(unittest.TestCase):
    def setUp(self):
        self.data = np.full((32, 64, 4), 0xee, dtype='uint8')

    def test_init(self):
        image = ArrayImage(self.data)

        self.assertIs(image.data, self.data)

    def test_init_data_required(self):
        with self.assertRaises(TypeError):
            ArrayImage()

    def test_create_image(self):
        image = ArrayImage(self.data)

        toolkit_image = image.create_image()

        self.assertIsNotNone(toolkit_image)

    def test_create_bitmap(self):
        image = ArrayImage(self.data)

        bitmap = image.create_bitmap()

        self.assertIsNotNone(bitmap)

    def test_create_icon(self):
        image = ArrayImage(self.data)

        icon = image.create_icon()

        self.assertIsNotNone(icon)
