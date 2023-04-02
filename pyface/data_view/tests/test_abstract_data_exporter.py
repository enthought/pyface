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

from pyface.data_view.abstract_data_exporter import AbstractDataExporter
from pyface.data_view.data_view_errors import DataViewGetError
from pyface.data_view.data_wrapper import DataWrapper
from pyface.data_view.i_data_wrapper import DataFormat


trivial_format = DataFormat(
    'null/null',
    lambda x: x,
    lambda x: x,
)

trivial_text_format = DataFormat(
    'text/null',
    lambda x: x,
    lambda x: x,
)


class TrivialExporter(AbstractDataExporter):

    def get_data(self, model, indices):
        if len(indices) == 0:
            raise DataViewGetError('bad data')
        return b'data'


class TestAbstractDataExporter(TestCase):

    def setUp(self):
        self.value_type = Mock()
        self.value_type.has_text = Mock(return_value=True)
        self.value_type.get_text = Mock(return_value='text')
        self.value_type.has_editor_value = Mock(return_value=True)
        self.value_type.get_editor_value = Mock(return_value=1)

        self.model = Mock()
        self.model.get_value = Mock(return_value=0.0)
        self.model.get_value_type = Mock(return_value=self.value_type)

    def test_is_text_default_false(self):
        exporter = TrivialExporter(format=trivial_format)
        self.assertFalse(exporter.is_text)

    def test_is_text_default_true(self):
        exporter = TrivialExporter(format=trivial_text_format)
        self.assertTrue(exporter.is_text)

    def test_add_data(self):
        exporter = TrivialExporter(format=trivial_format)
        data_wrapper = DataWrapper()

        exporter.add_data(data_wrapper, self.model, [((0,), (0,))])

        self.assertTrue(data_wrapper.has_format(trivial_format))
        self.assertEqual(data_wrapper.get_mimedata('null/null'), b'data')

    def test_add_data_fail(self):
        exporter = TrivialExporter(format=trivial_format)
        data_wrapper = DataWrapper()

        exporter.add_data(data_wrapper, self.model, [])

        self.assertFalse(data_wrapper.has_format(trivial_format))

    def test_get_value_is_text(self):
        exporter = TrivialExporter(
            format=trivial_format,
            is_text=True,
        )

        value = exporter.get_value(self.model, (0,), (0,))

        self.assertEqual(value, 'text')

    def test_get_value_is_text_not_has_text(self):
        self.value_type.has_text = Mock(return_value=False)
        exporter = TrivialExporter(
            format=trivial_format,
            is_text=True,
        )

        value = exporter.get_value(self.model, (0,), (0,))

        self.assertEqual(value, '')

    def test_get_value_is_not_text(self):
        exporter = TrivialExporter(
            format=trivial_format,
            is_text=False,
        )

        value = exporter.get_value(self.model, (0,), (0,))

        self.assertEqual(value, 1.0)

    def test_get_value_is_not_text_not_editor_value(self):
        self.value_type.has_editor_value = Mock(return_value=False)
        exporter = TrivialExporter(
            format=trivial_format,
            is_text=False,
        )

        value = exporter.get_value(self.model, (0,), (0,))

        self.assertEqual(value, 0.0)
