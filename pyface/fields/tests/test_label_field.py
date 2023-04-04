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


from pyface.image_resource import ImageResource
from ..label_field import LabelField
from .field_mixin import FieldMixin


class TestLabelField(FieldMixin, unittest.TestCase):

    def _create_widget_simple(self, **traits):
        traits.setdefault("value", "Label")
        traits.setdefault("tooltip", "Dummy")
        return LabelField(**traits)

    # Tests ------------------------------------------------------------------

    def test_label_field(self):
        self._create_widget_control()

        self.widget.value = "Test"
        self.gui.process_events()

        self.assertEqual(self.widget._get_control_value(), "Test")

    def test_label_field_image(self):
        self._create_widget_control()
        image = ImageResource("question")

        # XXX can't validate icon values currently, so just a smoke test
        self.widget.image = image
        self.gui.process_events()
