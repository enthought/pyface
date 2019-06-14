import unittest


class TestPyfaceQtImports(unittest.TestCase):

    def test_imports(self):
        # check that all Qt API imports work
        import pyface.qt.QtCore
        import pyface.qt.QtGui
        import pyface.qt.QtNetwork
        import pyface.qt.QtOpenGL
        import pyface.qt.QtScript
        import pyface.qt.QtSvg
        import pyface.qt.QtTest
        import pyface.qt.QtWebKit