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

from pyface.qt import QtGui

from traits.api import provides

from pyface.i_heading_text import IHeadingText, MHeadingText
from .layout_widget import LayoutWidget


@provides(IHeadingText)
class HeadingText(MHeadingText, LayoutWidget):
    """ The Qt-specific implementation of a HeadingText.
    """

    # ------------------------------------------------------------------------
    # 'IWidget' interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """
        control = QtGui.QLabel(parent)
        control.setSizePolicy(
            QtGui.QSizePolicy.Policy.Preferred, QtGui.QSizePolicy.Policy.Fixed
        )
        return control

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _set_control_text(self, text):
        """ Set the text on the toolkit specific widget. """
        # Bold the text. Qt supports a limited subset of HTML for rich text.
        text = f"<b>{text}</b>"
        self.control.setText(text)

    def _get_control_text(self):
        """ Get the text on the toolkit specific widget. """
        text = self.control.text()
        # remove the bolding from the text
        text = text[3:-4]
        return text
