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

try:
    # Starting Python 3.8, importlib.metadata is available in the Python
    # standard library and starting Python 3.10, the "select" interface is
    # available on EntryPoints.
    from importlib.metadata import entry_points
except ImportError:
    from importlib_metadata import entry_points

import pyface.toolkit


class TestToolkit(unittest.TestCase):
    def test_missing_import(self):
        # test that we get an undefined object if no toolkit implementation
        cls = pyface.toolkit.toolkit_object("tests:Missing")
        with self.assertRaises(NotImplementedError):
            cls()

    def test_bad_import(self):
        # test that we don't filter unrelated import errors
        with self.assertRaises(ImportError):
            pyface.toolkit.toolkit_object("tests.bad_import:Missing")

    def test_core_plugins(self):
        # test that we can see appropriate core entrypoints

        # This compatibility layer can be removed when we drop support for
        # Python < 3.10. Ref https://github.com/enthought/pyface/issues/999.
        all_entry_points = entry_points()
        if hasattr(all_entry_points, "select"):
            plugins = {
                ep.name
                for ep in entry_points().select(group='pyface.toolkits')
            }
        else:
            plugins = {
                ep.name for ep in entry_points()['pyface.toolkits']
            }
        self.assertLessEqual({"qt4", "wx", "qt", "null"}, plugins)

    def test_toolkit_object(self):
        # test that the Toolkit class works as expected
        # note that if this fails many other things will too
        from pyface.tests.test_new_toolkit.init import toolkit_object
        from pyface.tests.test_new_toolkit.widget import Widget as TestWidget

        Widget = toolkit_object("widget:Widget")

        self.assertEqual(Widget, TestWidget)

    def test_toolkit_object_overriden(self):
        # test that the Toolkit class search paths can be overridden
        from pyface.tests.test_new_toolkit.widget import Widget as TestWidget

        toolkit_object = pyface.toolkit.toolkit_object

        old_packages = toolkit_object.packages
        toolkit_object.packages = [
            "pyface.tests.test_new_toolkit"
        ] + old_packages
        try:
            Widget = toolkit_object("widget:Widget")
            self.assertEqual(Widget, TestWidget)
        finally:
            toolkit_object.packages = old_packages

    def test_toolkit_object_not_overriden(self):
        # test that the Toolkit class works when object not overridden
        toolkit_object = pyface.toolkit.toolkit_object
        TestWindow = toolkit_object("window:Window")

        old_packages = toolkit_object.packages
        toolkit_object.packages = [
            "pyface.tests.test_new_toolkit"
        ] + old_packages
        try:
            Window = toolkit_object("window:Window")
            self.assertEqual(Window, TestWindow)
        finally:
            toolkit_object.packages = old_packages
