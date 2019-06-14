from __future__ import absolute_import

import unittest

from ..clipboard import clipboard


class TestObject(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __eq__(self, other):
        if isinstance(other, TestObject):
            return all(getattr(other, key) == value
                       for key, value in self.__dict__.items())


class TestClipboard(unittest.TestCase):

    def setUp(self):
        self.clipboard = clipboard

    def test_set_text_data(self):
        self.clipboard.data = 'test'
        self.assertTrue(self.clipboard.has_data)
        self.assertEquals(self.clipboard.data_type, 'str')
        self.assertEquals(self.clipboard.data, 'test')
        self.assertTrue(self.clipboard.has_text_data)
        self.assertEquals(self.clipboard.text_data, 'test')
        self.assertFalse(self.clipboard.has_file_data)
        self.assertFalse(self.clipboard.has_object_data)

    def test_set_text_data_unicode(self):
        self.clipboard.data = u'test'
        self.assertTrue(self.clipboard.has_data)
        self.assertEquals(self.clipboard.data_type, 'str')
        self.assertEquals(self.clipboard.data, u'test')
        self.assertTrue(self.clipboard.has_text_data)
        self.assertEquals(self.clipboard.text_data, u'test')
        self.assertFalse(self.clipboard.has_file_data)
        self.assertFalse(self.clipboard.has_object_data)

    @unittest.skip('backends not consistent')
    def test_set_file_data(self):
        self.clipboard.data = ['file:///images']
        self.assertTrue(self.clipboard.has_data)
        self.assertEquals(self.clipboard.data_type, 'file')
        self.assertEquals(self.clipboard.data, ['/images'])
        self.assertTrue(self.clipboard.has_file_data)
        self.assertEquals(self.clipboard.file_data, ['/images'])
        self.assertFalse(self.clipboard.has_text_data)
        self.assertFalse(self.clipboard.has_object_data)

    def test_set_object_data(self):
        data = TestObject(foo='bar', baz=1)
        self.clipboard.data = data
        self.assertTrue(self.clipboard.has_data)
        self.assertEquals(self.clipboard.data_type, TestObject)
        self.assertEquals(self.clipboard.data, data)
        self.assertTrue(self.clipboard.has_object_data)
        self.assertEquals(self.clipboard.object_type, TestObject)
        self.assertEquals(self.clipboard.object_data, data)
        self.assertFalse(self.clipboard.has_text_data)
        self.assertFalse(self.clipboard.has_file_data)
