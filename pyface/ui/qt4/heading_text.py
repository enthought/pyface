# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
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


from pyface.qt import QtCore, QtGui


from traits.api import Int, provides, Str


from pyface.i_heading_text import IHeadingText, MHeadingText
from .widget import Widget


@provides(IHeadingText)
class HeadingText(MHeadingText, Widget):
    """ The toolkit specific implementation of a HeadingText.  See the
    IHeadingText interface for the API documentation.
    """

    # 'IHeadingText' interface ---------------------------------------------

    level = Int(1)

    text = Str("Default")

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, parent, **traits):
        """ Creates the panel. """

        # Base class constructor.
        super(HeadingText, self).__init__(**traits)

        # Create the toolkit-specific control that represents the widget.
        self._create_control(parent)

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """

        self.control = QtGui.QLabel(parent)
        self._set_text(self.text)

        self.control.setSizePolicy(
            QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed
        )

    def _set_text(self, text):
        """ Set the text on the toolkit specific widget. """

        # Bold the text. Qt supports a limited subset of HTML for rich text.
        text = "<b>" + text + "</b>"

        self.control.setText(text)

    # Trait event handlers -------------------------------------------------

    def _text_changed(self, new):
        """ Called when the text is changed. """

        if self.control is not None:
            self._set_text(new)
