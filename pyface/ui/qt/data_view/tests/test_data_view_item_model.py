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

from traits.testing.optional_dependencies import numpy as np, requires_numpy

from pyface.qt.QtCore import QMimeData
# This import results in an error without numpy installed
# see enthought/pyface#742
if np is not None:
    from pyface.data_view.data_models.api import ArrayDataModel
from pyface.data_view.exporters.row_exporter import RowExporter
from pyface.data_view.data_formats import table_format
from pyface.data_view.value_types.api import FloatValue
from pyface.ui.qt.data_view.data_view_item_model import DataViewItemModel


@requires_numpy
class TestDataViewItemModel(TestCase):

    def setUp(self):
        self.item_model = self._create_item_model()

    def _create_item_model(self):
        self.data = np.arange(120.0).reshape(4, 5, 6)
        self.model = ArrayDataModel(data=self.data, value_type=FloatValue())
        return DataViewItemModel(
            model=self.model,
            selection_type='row',
            exporters=[],
        )

    def _make_indexes(self, indices):
        return [
            self.item_model._to_model_index(row, column)
            for row, column in indices
        ]

    def test_mimeData(self):
        self.item_model.exporters = [RowExporter(format=table_format)]
        indexes = self._make_indexes([
            ((0, row), (column,))
            for column in range(2, 5)
            for row in range(2, 4)
        ])

        mime_data = self.item_model.mimeData(indexes)

        self.assertIsInstance(mime_data, QMimeData)
        self.assertTrue(mime_data.hasFormat('text/plain'))

        raw_data = mime_data.data('text/plain').data()
        data = table_format.deserialize(bytes(raw_data))
        np.testing.assert_array_equal(
            data,
            [
                ['12', '13', '14', '15', '16', '17'],
                ['18', '19', '20', '21', '22', '23'],
            ]
        )

    def test_mimeData_empty(self):
        mime_data = self.item_model.mimeData([])

        self.assertIsInstance(mime_data, QMimeData)
        # exact contents depend on Qt, so won't test more deeply
