# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import sys
import unittest
import warnings


class TestPyfaceQtImports(unittest.TestCase):

    def test_imports(self):
        # check that all Qt API imports work
        import pyface.qt.QtCore  # noqa: F401
        import pyface.qt.QtGui  # noqa: F401
        import pyface.qt.QtNetwork  # noqa: F401
        import pyface.qt.QtOpenGL  # noqa: F401
        import pyface.qt.QtOpenGLWidgets  # noqa: F401
        import pyface.qt.QtSvg  # noqa: F401
        import pyface.qt.QtSvgWidgets  # noqa: F401
        import pyface.qt.QtTest  # noqa: F401
        import pyface.qt.QtMultimedia  # noqa: F401
        import pyface.qt.QtMultimediaWidgets  # noqa: F401
        import pyface.qt.QtWidgets  # noqa: F401

    @unittest.skipIf(sys.version_info > (3, 6), "WebKit is not available")
    def test_import_web_kit(self):
        import pyface.qt.QtWebKit  # noqa: F401

    def test_import_QtScript(self):
        # QtScript is not supported on PyQt5/PySide2 and
        # this import will raise a deprecation warning.
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always", category=DeprecationWarning)

            import pyface.qt.QtScript  # noqa: F401

        self.assertTrue(len(w) == 1)
        for warn in w:
            self.assertEqual(warn.category, DeprecationWarning)

    def test_import_qopenglwidget(self):
        # smoke test
        from pyface.qt.QtOpenGL import QOpenGLWidget  # noqa: F401
