# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The interface for a dialog that allows the user to select a color. """

import wx

from traits.api import Bool, provides

from pyface.color import Color, PyfaceColor
from pyface.i_color_dialog import IColorDialog
from .dialog import Dialog


@provides(IColorDialog)
class ColorDialog(Dialog):
    """ A dialog for selecting colors.
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
        # In wx this is a canned dialog.
        pass

    # ------------------------------------------------------------------------
    # 'IWindow' interface.
    # ------------------------------------------------------------------------

    def close(self):
        colour_data = self.control.GetColourData()
        wx_colour = colour_data.GetColour()
        self.color = Color.from_toolkit(wx_colour)
        super(ColorDialog, self).close()

    # ------------------------------------------------------------------------
    # 'IWidget' interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        wx_colour = self.color.to_toolkit()
        data = wx.ColourData()
        data.SetInitialColour(wx_colour)
        data.SetChooseAlpha(self.show_alpha)
        dialog = wx.ColourDialog(parent, data)
        return dialog