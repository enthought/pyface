# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


from collections.abc import Sequence
import os
import unittest

from ..resource_manager import PyfaceResourceFactory
from ..resource_manager import ResourceManager

IMAGE_PATH = os.path.join(os.path.dirname(__file__), "images", "core.png")


class TestPyfaceResourceFactory(unittest.TestCase):
    def setUp(self):
        self.resource_factory = PyfaceResourceFactory()

    def test_image_from_file(self):
        image = self.resource_factory.image_from_file(IMAGE_PATH)

    def test_image_from_data(self):
        with open(IMAGE_PATH, "rb") as fp:
            data = fp.read()
        image = self.resource_factory.image_from_data(data)

    def test_locate_image(self):
        class ASequence(Sequence):
            def __init__(self, data):
                self.data = data

            def __getitem__(self, i):
                return self.data[i]

            def __len__(self):
                return len(self.data)

        sequence = ASequence([os.path.dirname(IMAGE_PATH)])

        resource_manager = ResourceManager()
        img_ref = resource_manager.locate_image("core.png", sequence)
        self.assertEqual(IMAGE_PATH, img_ref.filename)
