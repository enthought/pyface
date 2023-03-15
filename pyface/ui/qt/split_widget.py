# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
# (C) Copyright 2007 Riverbank Computing Limited
# This software is provided without warranty under the terms of the BSD license.
# However, when used with the GPL version of PyQt the additional terms described in the PyQt GPL exception also apply

""" Mix-in class for split widgets. """

from pyface.qt import QtCore, QtGui

from traits.api import provides

from pyface.i_widget import IWidget
from pyface.i_split_widget import ISplitWidget, MSplitWidget


@provides(ISplitWidget)
class SplitWidget(MSplitWidget):
    """ The toolkit specific implementation of a SplitWidget.  See the
    ISPlitWidget interface for the API documentation.
    """

    # ------------------------------------------------------------------------
    # Protected 'ISplitWidget' interface.
    # ------------------------------------------------------------------------

    def _create_splitter(self, parent):
        """ Create the toolkit-specific control that represents the widget. """

        splitter = QtGui.QSplitter(parent)

        # Yes, this is correct.
        if self.direction == "horizontal":
            splitter.setOrientation(QtCore.Qt.Orientation.Vertical)

        # Only because the wx implementation does the same.
        splitter.setChildrenCollapsible(False)

        # Left hand side/top.
        splitter.addWidget(self._create_lhs(splitter))

        # Right hand side/bottom.
        splitter.addWidget(self._create_rhs(splitter))

        # Set the initial splitter position.
        if self.direction == "horizontal":
            pos = splitter.sizeHint().height()
        else:
            pos = splitter.sizeHint().width()

        splitter.setSizes(
            [int(pos * self.ratio), int(pos * (1.0 - self.ratio))]
        )

        return splitter

    def _create_lhs(self, parent):
        """ Creates the left hand/top panel depending on the direction. """

        if self.lhs is not None:
            lhs = self.lhs(parent)
            if isinstance(lhs, IWidget):
                lhs.create()
            if not isinstance(lhs, QtGui.QWidget):
                lhs = lhs.control

        else:
            # Dummy implementation - override!
            lhs = QtGui.QWidget(parent)

        return lhs

    def _create_rhs(self, parent):
        """ Creates the right hand/bottom panel depending on the direction. """

        if self.rhs is not None:
            rhs = self.rhs(parent)
            if isinstance(rhs, IWidget):
                rhs.create()
            if not isinstance(rhs, QtGui.QWidget):
                rhs = rhs.control

        else:
            # Dummy implementation - override!
            rhs = QtGui.QWidget(parent)

        return rhs
