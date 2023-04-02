# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import os
import platform
import unittest

# importlib.resources is new in Python 3.7, and importlib.resources.files is
# new in Python 3.9, so for Python < 3.9 we must rely on the 3rd party
# importlib_resources package.
try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

import pyface
import pyface.tests
from ..image_resource import ImageResource
from ..toolkit import toolkit_object


is_qt = toolkit_object.toolkit.startswith("qt")
if is_qt:
    from pyface.qt import qt_api
is_pyqt4_windows = (
    is_qt and qt_api == "pyqt" and platform.system() == "Windows"
)


SEARCH_PATH = os.fspath(files("pyface") / "images")
IMAGE_PATH = os.fspath(files("pyface.tests") / "images" / "core.png")


class TestImageResource(unittest.TestCase):
    def setUp(self):
        # clear cached "not found" image
        ImageResource._image_not_found = None

    def test_create_image(self):
        image_resource = ImageResource("core")
        image = image_resource.create_image()
        self.assertIsNotNone(image)
        self.assertEqual(image_resource.absolute_path, IMAGE_PATH)

    def test_create_image_again(self):
        image_resource = ImageResource("core")
        image = image_resource.create_image()
        self.assertIsNotNone(image)
        self.assertEqual(image_resource.absolute_path, IMAGE_PATH)

    def test_create_image_search_path(self):
        image_resource = ImageResource("splash", [SEARCH_PATH])
        self.assertEqual(
            image_resource.search_path, [SEARCH_PATH, pyface.tests]
        )
        image = image_resource.create_image()
        self.assertIsNotNone(image)
        self.assertEqual(
            image_resource.absolute_path,
            os.path.join(SEARCH_PATH, "splash.png"),
        )

    def test_create_image_search_path_string(self):
        image_resource = ImageResource("splash", SEARCH_PATH)
        self.assertEqual(
            image_resource.search_path, [SEARCH_PATH, pyface.tests]
        )
        image = image_resource.create_image()
        self.assertIsNotNone(image)
        self.assertEqual(
            image_resource.absolute_path,
            os.path.join(SEARCH_PATH, "splash.png"),
        )

    def test_create_image_missing(self):
        image_resource = ImageResource("doesnt_exist.png")
        image = image_resource.create_image()
        self.assertIsNotNone(image)
        self.assertIsNotNone(image_resource._image_not_found)

    def test_create_bitmap(self):
        image_resource = ImageResource("core.png")
        image = image_resource.create_bitmap()
        self.assertIsNotNone(image)
        self.assertEqual(image_resource.absolute_path, IMAGE_PATH)

    def test_create_icon(self):
        image_resource = ImageResource("core.png")
        image = image_resource.create_icon()
        self.assertIsNotNone(image)
        self.assertEqual(image_resource.absolute_path, IMAGE_PATH)

    def test_image_size(self):
        image_resource = ImageResource("core")
        image = image_resource.create_image()
        size = image_resource.image_size(image)
        self.assertEqual(image_resource._ref.filename, IMAGE_PATH)
        self.assertEqual(size, (64, 64))

    @unittest.skipIf(
        is_pyqt4_windows, "QPixmap bug returns (0, 0).  Issue #301."
    )  # noqa
    def test_image_size_search_path(self):
        image_resource = ImageResource("splash", [SEARCH_PATH])
        image = image_resource.create_image()
        size = image_resource.image_size(image)
        self.assertEqual(
            image_resource.absolute_path,
            os.path.join(SEARCH_PATH, "splash.png"),
        )
        self.assertEqual(size, (601, 203))
