from __future__ import absolute_import

from traits.testing.unittest_tools import unittest, UnittestTools

from ..widget import Widget


class TestWidget(unittest.TestCase, UnittestTools):

    def setUp(self):
        self.widget = Widget()

    def test_create(self):
        # create is not Implemented
        with self.assertRaises(NotImplementedError):
            self.widget._create()

    def test_destroy(self):
        # test that destroy works even when no control
        self.widget.destroy()
