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

from pyface.data_view.exporters.item_exporter import ItemExporter
from pyface.data_view.data_wrapper import DataWrapper
from pyface.data_view.i_data_wrapper import DataFormat


trivial_format = DataFormat(
    'null/null',
    lambda x: str(x).encode('utf-8'),
    lambda x: x,
)


class TestItemExporter(TestCase):

    def setUp(self):
        self.value_type = Mock()
        self.value_type.has_text = Mock(return_value=True)
        self.value_type.get_text = Mock(return_value='text')
        self.value_type.has_editor_value = Mock(return_value=True)
        self.value_type.get_editor_value = Mock(return_value=1)

        self.model = Mock()
        self.model.get_value = Mock(return_value=0.0)
        self.model.get_value_type = Mock(return_value=self.value_type)

    def test_get_data_(self):
        exporter = ItemExporter(format=trivial_format)

        result = exporter.get_data(self.model, [((0,), (0,))])

        self.assertEqual(result, 1)

    def test_add_data_(self):
        exporter = ItemExporter(format=trivial_format)
        data_wrapper = DataWrapper()

        exporter.add_data(data_wrapper, self.model, [((0,), (0,))])

        self.assertTrue(data_wrapper.has_format(trivial_format))
        self.assertEqual(data_wrapper.get_mimedata('null/null'), b'1')

    def test_add_data_length_0(self):
        exporter = ItemExporter(format=trivial_format)
        data_wrapper = DataWrapper()

        exporter.add_data(data_wrapper, self.model, [])

        self.assertFalse(data_wrapper.has_format(trivial_format))

    def test_add_data_length_2(self):
        exporter = ItemExporter(format=trivial_format)
        data_wrapper = DataWrapper()

        exporter.add_data(data_wrapper, self.model, [((), ()), ((0,), (0,))])

        self.assertFalse(data_wrapper.has_format(trivial_format))
