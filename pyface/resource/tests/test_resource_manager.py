# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from os.path import dirname, join
import unittest

from pyface.image_resource import ImageResource


class TestResourceManager(unittest.TestCase):

    def test_locate_image_same_directory(self):
        # this used to fail, not just result in None
        a = ImageResource('non_existent_image')._get_ref()

        b = ImageResource('e-logo-rev')._get_ref()

        self.assertIsNone(a)
        self.assertIsNotNone(b)

    def test_locate_image_different_directory(self):
        # this used to fail, not just result in None
        a = ImageResource(
            'non_existent_image',
            search_path=join(dirname(__file__), '..', '..')
        )._get_ref()

        b = ImageResource(
            'question',
            search_path=join(dirname(__file__), '..', '..')
        )._get_ref()

        self.assertIsNone(a)
        self.assertIsNotNone(b)
