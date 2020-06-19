# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A dialog that allows the user to select a font. """

from pyface.qt import QtGui

from traits.api import provides

from pyface.font import Font, PyfaceFont
from pyface.i_font_dialog import IFontDialog
from .dialog import Dialog


@provides(IFontDialog)
class FontDialog(Dialog):
    """ A dialog for selecting fonts.
    """

    #: A Font instance that holds the initial font at the start and tracks
    #: the selected font during user interactions.
    font = PyfaceFont()

    # ------------------------------------------------------------------------
    # 'IDialog' interface.
    # ------------------------------------------------------------------------

    def _create_contents(self, parent):
        # In PyQt this is a canned dialog.
        pass

    # ------------------------------------------------------------------------
    # 'IWindow' interface.
    # ------------------------------------------------------------------------

    def close(self):
        qt_font = self.control.selectedFont()
        self.font = Font.from_toolkit(qt_font)
        super(FontDialog, self).close()

    # ------------------------------------------------------------------------
    # 'IWidget' interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        qt_font = self.font.to_toolkit()
        dialog = QtGui.QFontDialog(qt_font, parent)
        return dialog
