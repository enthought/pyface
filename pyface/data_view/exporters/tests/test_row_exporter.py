# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from itertools import count
from unittest import TestCase
from unittest.mock import Mock

from pyface.data_view.exporters.row_exporter import RowExporter
from pyface.data_view.i_data_wrapper import DataFormat


trivial_format = DataFormat(
    'null/null',
    lambda x: str(x).encode('utf-8'),
    lambda x: x,
)


class TestRowExporter(TestCase):

    def setUp(self):
        self.value_type = Mock()
        self.value_type.has_text = Mock(return_value=False)
        self.value_type.has_editor_value = Mock(return_value=True)
        self.value_type.get_editor_value = Mock(
            return_value=1,
            side_effect=count(),
        )

        self.model = Mock()
        self.model.get_column_count = Mock(return_value=3)
        self.model.get_value = Mock(return_value=0)
        self.model.get_value_type = Mock(return_value=self.value_type)

    def test_get_data(self):
        exporter = RowExporter(format=trivial_format)

        result = exporter.get_data(self.model, [((0,), (0,)), ((1,), ())])

        self.assertEqual(result, [[0, 1, 2], [3, 4, 5]])

    def test_get_data_deduplicate(self):
        exporter = RowExporter(format=trivial_format)

        result = exporter.get_data(
            self.model,
            [
                ((0,), (0,)),
                ((0,), (2,)),
                ((1,), ()),
            ])

        self.assertEqual(result, [[0, 1, 2], [3, 4, 5]])

    def test_get_data_row_headers(self):
        exporter = RowExporter(format=trivial_format, row_headers=True)

        result = exporter.get_data(self.model, [((0,), (0,)), ((1,), ())])

        self.assertEqual(result, [[0, 1, 2, 3], [4, 5, 6, 7]])

    def test_get_data_column_headers(self):
        exporter = RowExporter(format=trivial_format, column_headers=True)

        result = exporter.get_data(self.model, [((0,), (0,)), ((1,), ())])

        self.assertEqual(result, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
