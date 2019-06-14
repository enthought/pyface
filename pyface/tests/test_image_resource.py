from __future__ import absolute_import

import os
import platform
import pkg_resources
import unittest

import pyface
import pyface.tests
from ..image_resource import ImageResource
from ..toolkit import toolkit_object


is_qt = toolkit_object.toolkit == 'qt4'
if is_qt:
    from pyface.qt import qt_api
is_pyqt4_windows = (is_qt and qt_api == 'pyqt' and platform.system() == 'Windows')


SEARCH_PATH = pkg_resources.resource_filename('pyface', 'images')
IMAGE_DIR = pkg_resources.resource_filename(__name__, 'images')
IMAGE_PATH = os.path.join(IMAGE_DIR, 'core.png')


class TestImageResource(unittest.TestCase):

    def setUp(self):
        # clear cached "not found" image
        ImageResource._image_not_found = None

    def test_create_image(self):
        image_resource = ImageResource('core')
        image = image_resource.create_image()
        self.assertIsNotNone(image)
        self.assertEqual(image_resource.absolute_path, IMAGE_PATH)

    def test_create_image_again(self):
        image_resource = ImageResource('core')
        image = image_resource.create_image()
        self.assertIsNotNone(image)
        self.assertEqual(image_resource.absolute_path, IMAGE_PATH)

    def test_create_image_search_path(self):
        image_resource = ImageResource('splash.jpg', [SEARCH_PATH])
        self.assertEqual(image_resource.search_path,
                         [SEARCH_PATH, pyface.tests])
        image = image_resource.create_image()
        self.assertIsNotNone(image)
        self.assertEqual(image_resource.absolute_path,
                         os.path.join(SEARCH_PATH, 'splash.jpg'))

    def test_create_image_search_path_string(self):
        image_resource = ImageResource('splash.jpg', SEARCH_PATH)
        self.assertEqual(image_resource.search_path,
                         [SEARCH_PATH, pyface.tests])
        image = image_resource.create_image()
        self.assertIsNotNone(image)
        self.assertEqual(image_resource.absolute_path,
                         os.path.join(SEARCH_PATH, 'splash.jpg'))

    def test_create_image_missing(self):
        image_resource = ImageResource('doesnt_exist.png')
        image = image_resource.create_image()
        self.assertIsNotNone(image)
        self.assertIsNotNone(image_resource._image_not_found)

    def test_create_bitmap(self):
        image_resource = ImageResource('core.png')
        image = image_resource.create_bitmap()
        self.assertIsNotNone(image)
        self.assertEqual(image_resource.absolute_path, IMAGE_PATH)

    def test_create_icon(self):
        image_resource = ImageResource('core.png')
        image = image_resource.create_icon()
        self.assertIsNotNone(image)
        self.assertEqual(image_resource.absolute_path, IMAGE_PATH)

    def test_image_size(self):
        image_resource = ImageResource('core')
        image = image_resource.create_image()
        size = image_resource.image_size(image)
        self.assertEqual(image_resource._ref.filename, IMAGE_PATH)
        self.assertEqual(size, (64, 64))

    @unittest.skipIf(is_pyqt4_windows, "QPixmap bug returns (0, 0).  Issue #301.")  # noqa
    def test_image_size_search_path(self):
        image_resource = ImageResource('splash.jpg', [SEARCH_PATH])
        image = image_resource.create_image()
        size = image_resource.image_size(image)
        self.assertEqual(image_resource.absolute_path,
                         os.path.join(SEARCH_PATH, 'splash.jpg'))
        self.assertEqual(size, (450, 296))
