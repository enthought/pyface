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

from traits.api import HasTraits, Int, Str
from traits.testing.optional_dependencies import numpy as np, requires_numpy
from traits.version import version

from pyface.data_view.data_formats import (
    from_csv, from_csv_column, from_csv_row, from_npy, from_json,
    to_csv, to_csv_column, to_csv_row, to_npy, to_json,
)


def default_extractor(obj):
    return obj.__getstate__()


def object_hook(data):
    obj = ExampleObject()
    obj.__setstate__(data)
    return obj


class ExampleObject(HasTraits):
    a = Int(1)
    b = Str("two")
    c = Str("three", transient=True)


class TestJSON(TestCase):

    def test_to_json(self):
        test_data = {'a': 1, 'b': 'two'}

        raw_data = to_json(test_data)

        self.assertEqual(raw_data, b'{"a":1,"b":"two"}')

    def test_to_json_default(self):
        test_data = ExampleObject()

        raw_data = to_json(test_data, default=default_extractor)

        self.assertEqual(
            raw_data,
            b'{"a":1,"b":"two","__traits_version__":"'
            + version.encode('utf-8')
            + b'"}'
        )

    def test_from_json(self):
        raw_data = b'{"a":1,"b":"two"}'

        data = from_json(raw_data)

        self.assertEqual(data, {'a': 1, 'b': 'two'})

    def test_from_json_object_hook(self):
        raw_data = (
            b'{"a":2,"b":"four","__traits_version__":"'
            + version.encode('utf-8')
            + b'"}'
        )

        data = from_json(raw_data, object_hook=object_hook)

        self.assertIsInstance(data, ExampleObject)
        self.assertEqual(data.a, 2)
        self.assertEqual(data.b, 'four')
        self.assertEqual(data.c, 'three')


class TestCSV(TestCase):

    def test_to_csv(self):
        test_data = [['one', 2], ['three,four', 5]]

        raw_data = to_csv(test_data)

        self.assertEqual(raw_data, b'one,2\r\n"three,four",5\r\n')

    def test_to_csv_delimiter(self):
        test_data = [['one', 2], ['three,four', 5]]

        raw_data = to_csv(test_data, delimiter='\t')

        self.assertEqual(raw_data, b'one\t2\r\nthree,four\t5\r\n')

    def test_to_csv_encoding(self):
        test_data = [['øne', 2], ['three,four', 5]]

        raw_data = to_csv(test_data, encoding='latin-1')

        self.assertEqual(raw_data, b'\xf8ne,2\r\n"three,four",5\r\n')

    def test_from_csv(self):
        raw_data = b'one,2\r\n"three,four",5\r\n'

        data = from_csv(raw_data)

        self.assertEqual(data, [['one', '2'], ['three,four', '5']])

    def test_from_csv_delimiter(self):
        raw_data = b'one\t2\r\nthree,four\t5\r\n'

        data = from_csv(raw_data, delimiter='\t')

        self.assertEqual(data, [['one', '2'], ['three,four', '5']])

    def test_from_csv_encoding(self):
        raw_data = b'\xf8ne,2\r\n"three,four",5\r\n'

        data = from_csv(raw_data, encoding='latin-1')

        self.assertEqual(data, [['øne', '2'], ['three,four', '5']])

    def test_to_csv_column(self):
        test_data = ['one', 2, 'three,four']

        raw_data = to_csv_column(test_data)

        self.assertEqual(raw_data, b'one\r\n2\r\n"three,four"\r\n')

    def test_to_csv_column_delimiter(self):
        test_data = ['one', 2, 'three,four']

        raw_data = to_csv_column(test_data, delimiter='\t')

        self.assertEqual(raw_data, b'one\r\n2\r\nthree,four\r\n')

    def test_to_csv_column_encoding(self):
        test_data = ['øne', 2, 'three,four']

        raw_data = to_csv_column(test_data, encoding='latin-1')

        self.assertEqual(raw_data, b'\xf8ne\r\n2\r\n"three,four"\r\n')

    def test_from_csv_column(self):
        raw_data = b'one\r\n2\r\n"three,four"\r\n'

        data = from_csv_column(raw_data)

        self.assertEqual(data, ['one', '2', 'three,four'])

    def test_from_csv_column_delimiter(self):
        raw_data = b'one\r\n2\r\nthree,four\r\n'

        data = from_csv_column(raw_data, delimiter='\t')

        self.assertEqual(data, ['one', '2', 'three,four'])

    def test_from_csv_column_encoding(self):
        raw_data = b'\xf8ne\r\n2\r\n"three,four"\r\n'

        data = from_csv_column(raw_data, encoding='latin-1')

        self.assertEqual(data, ['øne', '2', 'three,four'])

    def test_to_csv_row(self):
        test_data = ['one', 2, 'three,four']

        raw_data = to_csv_row(test_data)

        self.assertEqual(raw_data, b'one,2,"three,four"\r\n')

    def test_to_csv_row_delimiter(self):
        test_data = ['one', 2, 'three,four']

        raw_data = to_csv_row(test_data, delimiter='\t')

        self.assertEqual(raw_data, b'one\t2\tthree,four\r\n')

    def test_to_csv_row_encoding(self):
        test_data = ['øne', 2, 'three,four']

        raw_data = to_csv_row(test_data, encoding='latin-1')

        self.assertEqual(raw_data, b'\xf8ne,2,"three,four"\r\n')

    def test_from_csv_row(self):
        raw_data = b'one,2,"three,four"\r\n'

        data = from_csv_row(raw_data)

        self.assertEqual(data, ['one', '2', 'three,four'])

    def test_from_csv_row_delimiter(self):
        raw_data = b'one\t2\tthree,four\r\n'

        data = from_csv_row(raw_data, delimiter='\t')

        self.assertEqual(data, ['one', '2', 'three,four'])

    def test_from_csv_row_encoding(self):
        raw_data = b'\xf8ne,2,"three,four"\r\n'

        data = from_csv_row(raw_data, encoding='latin-1')

        self.assertEqual(data, ['øne', '2', 'three,four'])


@requires_numpy
class TestNpy(TestCase):

    def test_to_npy(self):
        data = np.array([[1, 2, 3], [4, 5, 6]], dtype='uint8')

        raw_data = to_npy(data)

        self.assertEqual(
            raw_data,
            b"\x93NUMPY\x01\x00v\x00{'descr': '|u1', 'fortran_order': False, 'shape': (2, 3), }                                                          \n"  # noqa: E501
            + b"\x01\x02\x03\x04\x05\x06"
        )

    def test_from_npy(self):
        raw_data = (
            b"\x93NUMPY\x01\x00v\x00{'descr': '|u1', 'fortran_order': False, 'shape': (2, 3), }                                                          \n"  # noqa: E501
            + b"\x01\x02\x03\x04\x05\x06"
        )

        data = from_npy(raw_data)

        np.testing.assert_array_equal(
            data,
            np.array([[1, 2, 3], [4, 5, 6]], dtype='uint8')
        )
