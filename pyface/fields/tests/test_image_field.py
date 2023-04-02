# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import unittest

from traits.testing.optional_dependencies import numpy as np, requires_numpy

from ..image_field import ImageField
from .field_mixin import FieldMixin


@requires_numpy
class ImageFieldMixin(FieldMixin, unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.data = np.full((32, 64, 4), 0xee, dtype='uint8')

    def _create_widget_simple(self, **traits):
        traits.setdefault("tooltip", "Dummy")
        return ImageField(**traits)

    # Tests ------------------------------------------------------------------

    def test_image_field(self):
        self._create_widget_control()

        self.widget.value = 'splash'
        self.gui.process_events()

        self.assertIsNotNone(self.widget._get_control_value())
