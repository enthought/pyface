# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import logging
import unittest

# importlib.resources is new in Python 3.7, and importlib.resources.files is
# new in Python 3.9, so for Python < 3.9 we must rely on the 3rd party
# importlib_resources package.
try:
    from importlib.resources import as_file, files
except ImportError:
    from importlib_resources import as_file, files

from pyface.util._optional_dependencies import optional_import

Image = None

with optional_import(
        "PIL",
        msg="PILImage not available due to missing pillow.",
        logger=logging.getLogger(__name__)):

    from PIL import Image
    from ..pil_image import PILImage

image_source = files("pyface.tests") / "images" / "core.png"


@unittest.skipIf(Image is None, "Pillow not available")
class TestPILImage(unittest.TestCase):

    def test_create_image(self):
        with as_file(image_source) as image_path:
            pil_image = Image.open(image_path)
            image = PILImage(pil_image)
            toolkit_image = image.create_image()
            self.assertIsNotNone(toolkit_image)
            self.assertEqual(image.image, pil_image)

    def test_create_bitmap(self):
        with as_file(image_source) as image_path:
            pil_image = Image.open(image_path)
            image = PILImage(pil_image)
            bitmap = image.create_bitmap()
            self.assertIsNotNone(bitmap)

    def test_create_icon(self):
        with as_file(image_source) as image_path:
            pil_image = Image.open(image_path)
            image = PILImage(pil_image)
            icon = image.create_icon()
            self.assertIsNotNone(icon)
