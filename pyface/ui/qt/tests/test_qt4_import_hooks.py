# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from contextlib import contextmanager
import os
import sys
import unittest

from traits.etsconfig.api import ETSConfig

from pyface.ui import ShadowedModuleFinder


class TestQt4ImportHooks(unittest.TestCase):

    def test_qt4_import_no_hook(self):
        with self._unload_modules([
            "pyface.ui.qt4",
            "pyface.ui.qt4.tests",
            "pyface.ui.qt4.tests.good_package",
            "pyface.ui.qt4.tests.good_package.good_import",
        ]):
            with self._clean_meta_path():
                with self.assertWarns(FutureWarning):
                    with self.assertRaises(ModuleNotFoundError) as cm:
                        import pyface.ui.qt4.tests.good_package.good_import  # noqa F401

                    self.assertEqual(cm.exception.name, "pyface.ui.qt4.tests")

    def test_qt4_import_other_package_hook(self):
        with self._unload_modules([
            "pyface.ui.qt4",
            "pyface.ui.qt4.tests",
            "pyface.ui.qt4.tests.good_package",
            "pyface.ui.qt4.tests.good_package.good_import",
        ]):
            with self._clean_meta_path():
                # test with shadow module finder for different package
                # (eg. another ETS package using the same code)
                sys.meta_path.append(ShadowedModuleFinder(
                    package='foo.bar.',
                    true_package='foo.baz.',
                ))
                with self.assertWarns(FutureWarning):
                    with self.assertRaises(ModuleNotFoundError) as cm:
                        import pyface.ui.qt4.tests.good_package.good_import  # noqa F401

                    self.assertEqual(cm.exception.name, "pyface.ui.qt4.tests")

    def test_qt4_import_with_hook(self):
        with self._unload_modules([
            "pyface.ui.qt4",
            "pyface.ui.qt4.tests",
            "pyface.ui.qt4.tests.good_package",
            "pyface.ui.qt4.tests.good_package.good_import",
        ]):
            with self._clean_meta_path():
                sys.meta_path.append(ShadowedModuleFinder())

                with self.assertWarns(DeprecationWarning):
                    import pyface.ui.qt4.tests.good_package.good_import  # noqa F401

                import pyface.ui.qt.tests.good_package.good_import

                self.assertIs(
                    pyface.ui.qt4.tests.good_package.good_import,
                    pyface.ui.qt.tests.good_package.good_import,
                )

                self.assertIs(
                    pyface.ui.qt4.tests.good_package,
                    pyface.ui.qt.tests.good_package,
                )

                self.assertIs(
                    pyface.ui.qt4.tests,
                    pyface.ui.qt.tests,
                )

    def test_qt4_import_with_hook_no_module(self):
        with self._unload_modules([
            "pyface.ui.qt4",
            "pyface.ui.qt4.tests",
            "pyface.ui.qt4.tests.good_package",
        ]):
            with self._clean_meta_path():
                sys.meta_path.append(ShadowedModuleFinder())

                with self.assertWarns(DeprecationWarning):
                    with self.assertRaises(ModuleNotFoundError) as cm:
                        import pyface.ui.qt4.tests.good_package.no_module  # noqa F401

                    self.assertEqual(
                        cm.exception.name,
                        "pyface.ui.qt4.tests.good_package.no_module",
                    )

    def test_qt4_import_with_hook_module_has_bad_import(self):
        with self._unload_modules([
            "pyface.ui.qt4",
            "pyface.ui.qt4.tests",
            "pyface.ui.qt4.tests.good_package",
        ]):
            with self._clean_meta_path():
                sys.meta_path.append(ShadowedModuleFinder())

                with self.assertWarns(DeprecationWarning):
                    with self.assertRaises(ModuleNotFoundError) as cm:
                        import pyface.ui.qt4.tests.good_package.has_bad_import  # noqa F401

                    self.assertEqual(cm.exception.name, "nonexistent_module")

    def test_qt4_import_with_ets_qt4_imports(self):
        with self._unload_modules([
            "pyface.ui.qt4",
            "pyface.ui.qt4.tests",
            "pyface.ui.qt4.tests.good_package",
            "pyface.ui.qt4.tests.good_package.good_import",
        ]):
            with self._clean_meta_path():
                with self._set_environment("ETS_QT4_IMPORTS", "1"):

                    with self.assertWarns(DeprecationWarning):
                        import pyface.ui.qt4.tests.good_package.good_import

                    import pyface.ui.qt.tests.good_package.good_import

                    self.assertIs(
                        pyface.ui.qt4.tests.good_package.good_import,
                        pyface.ui.qt.tests.good_package.good_import,
                    )

    def test_qt4_import_with_ets_toolkit_qt4(self):
        with self._unload_modules([
            "pyface.ui.qt4",
            "pyface.ui.qt4.tests",
            "pyface.ui.qt4.tests.good_package",
            "pyface.ui.qt4.tests.good_package.good_import",
        ]):
            with self._clean_meta_path():
                with self._set_environment("ETS_TOOLKIT", "qt4"):

                    with self.assertWarns(DeprecationWarning):
                        import pyface.ui.qt4.tests.good_package.good_import

                    import pyface.ui.qt.tests.good_package.good_import

                    self.assertIs(
                        pyface.ui.qt4.tests.good_package.good_import,
                        pyface.ui.qt.tests.good_package.good_import,
                    )

    def test_qt4_import_with_ets_toolkit_qt(self):
        with self._unload_modules([
            "pyface.ui.qt4",
            "pyface.ui.qt4.tests",
            "pyface.ui.qt4.tests.good_package",
            "pyface.ui.qt4.tests.good_package.good_import",
        ]):
            with self._clean_meta_path():
                with self._set_environment("ETS_TOOLKIT", "qt"):
                    with self.assertWarns(FutureWarning):
                        with self.assertRaises(ModuleNotFoundError):
                            import pyface.ui.qt4.tests.good_package.good_import  # noqa F401

    def test_qt4_import_with_etsconfig_toolkit_qt4(self):
        with self._unload_modules([
            "pyface.ui.qt4",
            "pyface.ui.qt4.tests",
            "pyface.ui.qt4.tests.good_package",
            "pyface.ui.qt4.tests.good_package.good_import",
        ]):
            with self._clean_meta_path():
                with self._set_etsconfig_toolkit("qt4"):

                    with self.assertWarns(DeprecationWarning):
                        import pyface.ui.qt4.tests.good_package.good_import

                    import pyface.ui.qt.tests.good_package.good_import

                    self.assertIs(
                        pyface.ui.qt4.tests.good_package.good_import,
                        pyface.ui.qt.tests.good_package.good_import,
                    )

    def test_qt4_import_with_etsconfig_toolkit_qt(self):
        with self._unload_modules([
            "pyface.ui.qt4",
            "pyface.ui.qt4.tests",
            "pyface.ui.qt4.tests.good_package",
            "pyface.ui.qt4.tests.good_package.good_import",
        ]):
            with self._clean_meta_path():
                with self._set_etsconfig_toolkit("qt"):
                    with self.assertWarns(FutureWarning):
                        with self.assertRaises(ModuleNotFoundError):
                            import pyface.ui.qt4.tests.good_package.good_import  # noqa F401

    @contextmanager
    def _clean_meta_path(self):
        """Temporarily remove ShadowedModuleFinder instances from sys.meta_path"""
        old_meta_path = sys.meta_path[:]
        sys.meta_path[:] = [
            finder for finder in sys.meta_path
            if not isinstance(finder, ShadowedModuleFinder)
        ]
        try:
            yield
        finally:
            sys.meta_path[:] = old_meta_path

    @contextmanager
    def _unload_modules(self, names):
        """Temporarily remove listed modules from sys.modules"""
        old_modules = {
            name: sys.modules.pop(name, None)
            for name in names
        }
        try:
            yield
        finally:
            for name, old_module in old_modules.items():
                if old_module:
                    sys.modules[name] = old_module
                else:
                    sys.modules.pop(name, None)

    @contextmanager
    def _set_environment(self, name, value):
        """Temporarily set an environment variable to a value"""
        old_value = os.environ.get(name, None)
        os.environ[name] = value
        try:
            yield
        finally:
            if old_value is None:
                del os.environ[name]
            else:
                os.environ[name] = old_value

    @contextmanager
    def _set_etsconfig_toolkit(self, value):
        """Temporarily set ETSConfig.toolkit to a value"""
        old_value = ETSConfig._toolkit
        ETSConfig._toolkit = value
        try:
            yield
        finally:
            ETSConfig._toolkit = old_value
