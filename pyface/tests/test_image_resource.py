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
import platform
import runpy
import shutil
import tempfile
import textwrap
import unittest

from importlib_resources import files

import pyface
import pyface.tests
from ..image_resource import ImageResource
from ..toolkit import toolkit_object


is_qt = toolkit_object.toolkit == "qt4"
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

    @unittest.skip("For now")
    def test_create_image_from_main(self):
        # When ImageResource is defined in a script, the module name is
        # __main__. Even if all search paths fail, the module calculated from
        # the caller's stack (``resource_module()``) is used for locating the
        # images.

        with tempfile.TemporaryDirectory() as tmp_dir:
            images_dir = os.path.join(tmp_dir, "images")
            os.makedirs(images_dir)
            shutil.copyfile(IMAGE_PATH, os.path.join(images_dir, "random.png"))
            script_path = os.path.join(tmp_dir, "main.py")

            non_existing_dir = os.path.join(tmp_dir, "not_a_dir")
            code = textwrap.dedent(f"""\
                import os
                from pyface.api import ImageResource

                image = ImageResource(
                    'random.png', search_path={non_existing_dir!r}
                )
            """)

            with open(script_path, "w", encoding="utf-8") as fp:
                fp.write(code)

            context = runpy.run_path(script_path, run_name="__main__")
            image = context["image"]

            # Should not fail
            image.create_image()

            # The image should be found.
            self.assertIsNotNone(image._get_ref())
