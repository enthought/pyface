from traits.testing.unittest_tools import unittest
import pyface.toolkit


class TestToolkit(unittest.TestCase):

    def test_missing_import(self):
        # test that we get an undefined object if no Qt implementation
        cls = pyface.toolkit.toolkit_object('tests:Missing')
        with self.assertRaises(NotImplementedError):
            obj = cls()

    def test_bad_import(self):
        # test that we don't filter unrelated import errors
        with self.assertRaises(ImportError):
            cls = pyface.toolkit.toolkit_object('tests.bad_import:Missing')
