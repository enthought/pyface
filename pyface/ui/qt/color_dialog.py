# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A dialog that allows the user to select a color. """

from pyface.qt import QtGui

from traits.api import Bool, provides

from pyface.color import Color
from pyface.ui_traits import PyfaceColor
from pyface.i_color_dialog import IColorDialog
from .dialog import Dialog


@provides(IColorDialog)
class ColorDialog(Dialog):
    """ A dialog that allows the user to choose a color.
    """

    # 'IColorDialog' interface ----------------------------------------------

    #: The color in the dialog.
    color = PyfaceColor()

    #: Whether or not to allow the user to chose an alpha value.
    show_alpha = Bool(False)

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
            qcolor = self.control.selectedColor()
            self.color = Color.from_toolkit(qcolor)
        return super(ColorDialog, self).close()

    # ------------------------------------------------------------------------
    # 'IWindow' interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        qcolor = self.color.to_toolkit()
        dialog = QtGui.QColorDialog(qcolor, parent)
        if self.show_alpha:
            dialog.setOptions(QtGui.QColorDialog.ColorDialogOption.ShowAlphaChannel)
        return dialog
