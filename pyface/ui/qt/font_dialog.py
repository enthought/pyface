# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
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

from pyface.font import Font
from pyface.ui_traits import PyfaceFont
from pyface.i_font_dialog import IFontDialog
from .dialog import Dialog


@provides(IFontDialog)
class FontDialog(Dialog):
    """ A dialog that allows the user to choose a font.
    """

    # 'IFontDialog' interface ----------------------------------------------

    #: The font in the dialog.
    font = PyfaceFont()

    # ------------------------------------------------------------------------
    # 'IDialog' interface.
    # ------------------------------------------------------------------------

    def _create_contents(self, parent):
        # In PyQt this is a canned dialog so there are no contents.
        pass

    # ------------------------------------------------------------------------
    # 'IWindow' interface.
    # ------------------------------------------------------------------------

    def close(self):
        if self.control.result() == QtGui.QDialog.DialogCode.Accepted:
            qfont = self.control.selectedFont()
            self.font = Font.from_toolkit(qfont)
        return super(FontDialog, self).close()

    # ------------------------------------------------------------------------
    # 'IWindow' interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        qfont = self.font.to_toolkit()
        dialog = QtGui.QFontDialog(qfont, parent)
        return dialog
