import pkg_resources

from traits.testing.unittest_tools import unittest

import pyface.toolkit


class TestToolkit(unittest.TestCase):

    def test_missing_import(self):
        # test that we get an undefined object if no toolkit implementation
        cls = pyface.toolkit.toolkit_object('tests:Missing')
        with self.assertRaises(NotImplementedError):
            obj = cls()

    def test_bad_import(self):
        # test that we don't filter unrelated import errors
        with self.assertRaises(ImportError):
            cls = pyface.toolkit.toolkit_object('tests.bad_import:Missing')

    def test_core_plugins(self):
        # test that we can see appropriate core entrypoints
        plugins = set(entry_point.name for entry_point in
                      pkg_resources.iter_entry_points('pyface.toolkits'))

        self.assertLessEqual({'qt4', 'wx', 'null'}, plugins)

    def test_toolkit_object(self):
        # test that the Toolkit class works as expected
        # note that if this fails many other things will too
        from pyface.tests.test_new_toolkit.init import toolkit_object
        from pyface.tests.test_new_toolkit.widget import Widget as TestWidget

        Widget = toolkit_object('widget:Widget')

        self.assertEqual(Widget, TestWidget)

    def test_toolkit_object_override(self):
        # test that the Toolkit class works as expected
        # note that if this fails many other things will too
        from pyface.tests.test_new_toolkit.widget import Widget as TestWidget

        toolkit_object = pyface.toolkit.toolkit_object

        old_packages = toolkit_object.packages
        toolkit_object.packages = ['pyface.tests.test_new_toolkit'] + old_packages
        try:
            Widget = toolkit_object('widget:Widget')
            self.assertEqual(Widget, TestWidget)
        finally:
            toolkit_object.packages = old_packages
