# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from unittest import TestCase
from unittest.mock import Mock

from pyface.data_view.value_types.no_value import NoValue


class TestNoValue(TestCase):

    def setUp(self):
        self.model = Mock()

    def test_has_editor_value(self):
        value_type = NoValue()
        self.assertFalse(value_type.has_editor_value(self.model, [0], [0]))

    def test_has_text(self):
        value_type = NoValue()
        self.assertFalse(value_type.has_text(self.model, [0], [0]))

    def test_has_image(self):
        value_type = NoValue()
        self.assertFalse(value_type.has_image(self.model, [0], [0]))

    def test_has_tooltip(self):
        value_type = NoValue()
        self.assertFalse(value_type.has_tooltip(self.model, [0], [0]))
