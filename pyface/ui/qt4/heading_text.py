# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
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

from traits.api import observe, provides

from pyface.i_heading_text import IHeadingText, MHeadingText
from .widget import Widget


@provides(IHeadingText)
class HeadingText(MHeadingText, Widget):
    """ The toolkit specific implementation of a HeadingText.  See the
    IHeadingText interface for the API documentation.
    """

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """

        control = QtGui.QLabel(parent)
        control.setText(self.text)
        control.setSizePolicy(
            QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed
        )
        return control

    def _set_text(self, text):
        """ Set the text on the toolkit specific widget. """

        # Bold the text. Qt supports a limited subset of HTML for rich text.
        text = "<b>" + text + "</b>"

        self.control.setText(text)

    # Trait event handlers -------------------------------------------------

    @observe("text")
    def _update_text(self, event):
        """ Called when the text is changed. """
        new = event.new
        if self.control is not None:
            self._set_text(new)
