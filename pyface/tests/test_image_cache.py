from __future__ import absolute_import

import os
import unittest

from ..image_cache import ImageCache

IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'images', 'core.png')


class TestPyfaceResourceFactory(unittest.TestCase):

    def setUp(self):
        self.image_cache = ImageCache(32, 32)

    def test_get_image(self):
        image = self.image_cache.get_image(IMAGE_PATH)

    def test_get_bitmap(self):
        bitmap = self.image_cache.get_bitmap(IMAGE_PATH)

    def test_get_image_twice(self):
        image1 = self.image_cache.get_image(IMAGE_PATH)
        image2 = self.image_cache.get_image(IMAGE_PATH)

    def test_get_bitmap_twice(self):
        bitmap1 = self.image_cache.get_bitmap(IMAGE_PATH)
        bitmap2 = self.image_cache.get_bitmap(IMAGE_PATH)

    def test_get_image_different_sizes(self):
        other_image_cache = ImageCache(48, 48)
        image1 = self.image_cache.get_image(IMAGE_PATH)
        image2 = other_image_cache.get_image(IMAGE_PATH)
        self.assertNotEqual(image1, image2)

    def test_get_bitmap_different_sizes(self):
        other_image_cache = ImageCache(48, 48)
        bitmap1 = self.image_cache.get_bitmap(IMAGE_PATH)
        bitmap2 = other_image_cache.get_bitmap(IMAGE_PATH)
        self.assertNotEqual(bitmap1, bitmap2)
