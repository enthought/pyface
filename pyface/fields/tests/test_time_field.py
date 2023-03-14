# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


from datetime import time
import unittest

from ..time_field import TimeField
from .field_mixin import FieldMixin


class TestTimeField(FieldMixin, unittest.TestCase):

    def _create_widget_simple(self, **traits):
        traits.setdefault("value", time(12, 0, 0))
        traits.setdefault("tooltip", "Dummy")
        return TimeField(**traits)

    # Tests ------------------------------------------------------------------

    def test_time_field(self):
        self._create_widget_control()

        self.widget.value = time(13, 1, 1)
        self.gui.process_events()

        self.assertEqual(self.widget._get_control_value(), time(13, 1, 1))

    def test_time_field_set(self):
        self._create_widget_control()

        with self.assertTraitChanges(self.widget, "value", count=1):
            self.widget._set_control_value(time(13, 1, 1))
            self.gui.process_events()

        self.assertEqual(self.widget.value, time(13, 1, 1))
