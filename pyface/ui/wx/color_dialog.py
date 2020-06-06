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
        color_data = self.control.GetColorData()
        wx_color = color_data.GetColor()
        self.color = Color.from_toolkit(wx_color)
        super(ColorDialog, self).close()

    # ------------------------------------------------------------------------
    # 'IWidget' interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        wx_color = self.color.to_toolkit()
        data = wx.ColorData()
        data.SetInitialColor(wx_color)
        data.SetChooseAlpha(self.show_alpha)
        dialog = wx.ColorDialog(parent, data)
        return dialog
