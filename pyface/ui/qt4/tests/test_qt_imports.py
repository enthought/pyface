# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import unittest
import warnings


class TestPyfaceQtImports(unittest.TestCase):
    def test_imports(self):
        # check that all Qt API imports work
        import pyface.qt.QtCore
        import pyface.qt.QtGui
        import pyface.qt.QtNetwork
        import pyface.qt.QtOpenGL
        import pyface.qt.QtSvg
        import pyface.qt.QtTest
        import pyface.qt.QtWebKit
        import pyface.qt.QtMultimedia
        import pyface.qt.QtMultimediaWidgets

    def test_import_QtScript(self):
        # QtScript is not supported on PyQt5/PySide2 and
        # this import will raise a deprecation warning.
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always", category=DeprecationWarning)

            import pyface.qt.QtScript

        self.assertTrue(len(w) == 1)
        for warn in w:
            self.assertEqual(warn.category, DeprecationWarning)
