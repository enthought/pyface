# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


from collections.abc import Sequence
import importlib.util
import os
import shutil
import tempfile
import unittest

import pyface     # a package with images as package resources
from ..resource_manager import PyfaceResourceFactory
from ..resource_manager import ResourceManager

IMAGE_PATH = os.path.join(os.path.dirname(__file__), "images", "core.png")


class TestPyfaceResourceFactory(unittest.TestCase):
    def setUp(self):
        self.resource_factory = PyfaceResourceFactory()

    def test_image_from_file(self):
        self.resource_factory.image_from_file(IMAGE_PATH)

    def test_image_from_data(self):
        with open(IMAGE_PATH, "rb") as fp:
            data = fp.read()
        self.resource_factory.image_from_data(data)

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

    def test_locate_image_with_module(self):
        # ResourceManager should be able to find the images/close.png which
        # is included in pyface package data.
        resource_manager = ResourceManager()
        image_ref = resource_manager.locate_image("close.png", [pyface])
        self.assertGreater(len(image_ref.data), 0)

    def test_locate_image_with_module_missing_file(self):
        # The required image is not found, locate_image should return None.
        resource_manager = ResourceManager()
        image_ref = resource_manager.locate_image(
            "does_not_exist.png", [pyface]
        )
        self.assertIsNone(image_ref)

    def test_locate_image_with_name_being_dunder_main(self):
        # When a module is not a package, we will fall back to use __file__

        # given a module from which there is an image in the same folder
        with tempfile.TemporaryDirectory() as tmp_dir:
            shutil.copyfile(IMAGE_PATH, os.path.join(tmp_dir, "random.png"))
            # create an empty file for creating a module.
            py_filepath = os.path.join(tmp_dir, "tmp.py")
            with open(py_filepath, "w", encoding="utf-8"):
                pass
            spec = importlib.util.spec_from_file_location(
                "__main__", py_filepath
            )
            module = importlib.util.module_from_spec(spec)

            resource_manager = ResourceManager(
                resource_factory=PyfaceResourceFactory()
            )
            # when
            image_ref = resource_manager.load_image("random.png", [module])

            # then
            self.assertIsNotNone(image_ref)
