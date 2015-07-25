from __future__ import absolute_import

import os

from traits.testing.unittest_tools import unittest

from ..image_cache import ImageCache

IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'images', 'core.png')


class TestPyfaceResourceFactory(unittest.TestCase):

    def setUp(self):
        self.image_cache = ImageCache(32, 32)

    def test_get_image(self):
        image = self.image_cache.get_image(IMAGE_PATH)

    def test_get_bitmap(self):
        bitmap = self.image_cache.get_bitmap(IMAGE_PATH)
