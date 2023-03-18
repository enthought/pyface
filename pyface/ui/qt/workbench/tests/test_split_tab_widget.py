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

from pyface.qt import QtCore, QtGui
from pyface.ui.qt.workbench.split_tab_widget import _DragableTabBar


class TestSplitTabWidget(unittest.TestCase):

    def test_mouseReleaseEvent(self):
        widget = _DragableTabBar(None, None)
        event = QtGui.QMouseEvent(
            QtCore.QEvent.Type.MouseButtonRelease,
            QtCore.QPointF(0.0, 0.0),
            QtCore.QPointF(0.0, 0.0),
            QtCore.Qt.MouseButton.RightButton,
            QtCore.Qt.RightButton,
            QtCore.Qt.NoModifier,
        )

        # smoke test: should do nothing
        widget.mouseReleaseEvent(event)

        widget.destroy()
