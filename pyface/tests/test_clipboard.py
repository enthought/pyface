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

from traits.etsconfig.api import ETSConfig

from ..clipboard import clipboard

is_wx = (ETSConfig.toolkit == 'wx')


class TestObject(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __eq__(self, other):
        if isinstance(other, TestObject):
            return all(
                getattr(other, key) == value
                for key, value in self.__dict__.items()
            )


class TestClipboard(unittest.TestCase):
    def setUp(self):
        self.clipboard = clipboard

    def test_set_text_data(self):
        self.clipboard.data = "test"
        self.assertTrue(self.clipboard.has_data)
        self.assertEqual(self.clipboard.data_type, "str")
        self.assertEqual(self.clipboard.data, "test")
        self.assertTrue(self.clipboard.has_text_data)
        self.assertEqual(self.clipboard.text_data, "test")
        self.assertFalse(self.clipboard.has_file_data)
        self.assertFalse(self.clipboard.has_object_data)

    def test_set_text_data_unicode(self):
        self.clipboard.data = "test"
        self.assertTrue(self.clipboard.has_data)
        self.assertEqual(self.clipboard.data_type, "str")
        self.assertEqual(self.clipboard.data, "test")
        self.assertTrue(self.clipboard.has_text_data)
        self.assertEqual(self.clipboard.text_data, "test")
        self.assertFalse(self.clipboard.has_file_data)
        self.assertFalse(self.clipboard.has_object_data)

    @unittest.skip("backends not consistent")
    def test_set_file_data(self):
        self.clipboard.data = ["file:///images"]
        self.assertTrue(self.clipboard.has_data)
        self.assertEqual(self.clipboard.data_type, "file")
        self.assertEqual(self.clipboard.data, ["/images"])
        self.assertTrue(self.clipboard.has_file_data)
        self.assertEqual(self.clipboard.file_data, ["/images"])
        self.assertFalse(self.clipboard.has_text_data)
        self.assertFalse(self.clipboard.has_object_data)

    def test_set_object_data(self):
        data = TestObject(foo="bar", baz=1)
        self.clipboard.data = data
        self.assertTrue(self.clipboard.has_data)
        self.assertEqual(self.clipboard.data_type, TestObject)
        self.assertEqual(self.clipboard.data, data)
        self.assertTrue(self.clipboard.has_object_data)
        self.assertEqual(self.clipboard.object_type, TestObject)
        self.assertEqual(self.clipboard.object_data, data)
        self.assertFalse(self.clipboard.has_text_data)
        self.assertFalse(self.clipboard.has_file_data)
