# Copyright (c) 2005-2023, Enthought Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

import unittest


class TestImageHelpers(unittest.TestCase):

    def test_imports(self):
        # actual functions are tested in toolkits
        from ..image_helpers import (  # noqa: F401
            AspectRatio, ScaleMode, array_to_image, bitmap_to_icon,
            bitmap_to_image, image_to_array, image_to_bitmap,
            resize_bitmap, resize_image,
        )
