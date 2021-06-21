# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
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

# importlib.resources is new in Python 3.7, and importlib.resources.files is
# new in Python 3.9, so for Python < 3.9 we must rely on the 3rd party
# importlib_resources package.
try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

from PIL import Image

from ..pil_image import PILImage

IMAGE_PATH = os.fspath(files("pyface.tests") / "images" / "core.png")


class TestPILImage(unittest.TestCase):
    def setUp(self):
        self.pil_image = Image.open(IMAGE_PATH)

    def test_create_image(self):
        image = PILImage(self.pil_image)
        toolkit_image = image.create_image()
        self.assertIsNotNone(toolkit_image)
        self.assertEqual(image.image, self.pil_image)

    def test_create_bitmap(self):
        image = PILImage(self.pil_image)
        bitmap = image.create_bitmap()
        self.assertIsNotNone(bitmap)

    def test_create_icon(self):
        image = PILImage(self.pil_image)
        icon = image.create_icon()
        self.assertIsNotNone(icon)

