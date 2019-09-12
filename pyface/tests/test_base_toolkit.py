import unittest

from traits.etsconfig.api import ETSConfig

from pyface.base_toolkit import find_toolkit, import_toolkit


class TestToolkit(unittest.TestCase):

    def test_import_null_toolkit(self):
        toolkit = import_toolkit('null')
        self.assertEqual(toolkit.package, 'pyface')
        self.assertEqual(toolkit.toolkit, 'null')

    def test_missing_toolkit(self):
        # test that we get an error with an undefined toolkit
        with self.assertRaises(RuntimeError):
            import_toolkit('nosuchtoolkit')

    def test_find_current_toolkit_no_etsconfig(self):
        old_etsconfig_toolkit = ETSConfig._toolkit
        ETSConfig._toolkit = ''
        try:
            toolkit = find_toolkit('pyface.toolkits', old_etsconfig_toolkit)
            self.assertEqual(toolkit.package, 'pyface')
            self.assertEqual(toolkit.toolkit, old_etsconfig_toolkit)
            self.assertEqual(ETSConfig.toolkit, old_etsconfig_toolkit)
        finally:
            ETSConfig._toolkit = old_etsconfig_toolkit

    def test_find_null_toolkit_no_etsconfig(self):
        old_etsconfig_toolkit = ETSConfig._toolkit
        ETSConfig._toolkit = ''
        try:
            toolkit = find_toolkit('pyface.toolkits', 'null')
            self.assertEqual(toolkit.package, 'pyface')
            self.assertEqual(toolkit.toolkit, 'null')
            self.assertEqual(ETSConfig.toolkit, 'null')
        finally:
            ETSConfig._toolkit = old_etsconfig_toolkit

    def test_find_nonexistent_toolkit_no_etsconfig(self):
        old_etsconfig_toolkit = ETSConfig._toolkit
        ETSConfig._toolkit = ''
        try:
            toolkit = find_toolkit('pyface.toolkits', 'nonexistent')
            self.assertEqual(toolkit.package, 'pyface')
            self.assertEqual(toolkit.toolkit, 'null')
            self.assertEqual(ETSConfig.toolkit, 'null')
        finally:
            ETSConfig._toolkit = old_etsconfig_toolkit
