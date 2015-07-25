from __future__ import absolute_import

import os

from traits.testing.unittest_tools import unittest

from ..resource_manager import PyfaceResourceFactory

IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'images', 'core.png')


class TestPyfaceResourceFactory(unittest.TestCase):

    def setUp(self):
        self.resource_factory = PyfaceResourceFactory()

    def test_image_from_file(self):
        image = self.resource_factory.image_from_file(IMAGE_PATH)

    def test_image_from_data(self):
        with open(IMAGE_PATH, 'rb') as fp:
            data = fp.read()
        image = self.resource_factory.image_from_data(data)
