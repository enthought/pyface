#------------------------------------------------------------------------------
#
#  Copyright (c) 2016, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in enthought/LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
#  Author: Enthought, Inc.
#
#------------------------------------------------------------------------------
""" A dialog that allows the user to chose a single item from a list. """

import wx

from traits.api import Any, Bool, List, Str, provides

from pyface.i_single_choice_dialog import ISingleChoiceDialog, MSingleChoiceDialog
from .dialog import Dialog


@provides(ISingleChoiceDialog)
class SingleChoiceDialog(MSingleChoiceDialog, Dialog):
    """ A dialog that allows the user to chose a single item from a list. """

    #### 'ISingleChoiceDialog' interface ######################################

    #: Whether or not the dialog can be cancelled (Wx Only).
    cancel = Bool(True)

    #: List of objects to choose from.
    choices = List(Any)

    #: The object chosen, if any.
    choice = Any

    #: An optional attribute to use for the name of each object in the dialog.
    name_attribute = Str

    #: The message to display to the user.
    message = Str

    ###########################################################################
    # Protected 'IDialog' interface.
    ###########################################################################

    def _create_contents(self, parent):
        """ Creates the window contents. """
        # In this case, wx does it all for us in 'wx.SingleChoiceDialog'
        pass

    ###########################################################################
    # 'IWindow' interface.
    ###########################################################################

    def close(self):
        """ Closes the window. """

        # Get the chosen object.
        if self.control is not None:
            self.choice = self.choices[self.control.GetSelection()]

        # Let the window close as normal.
        super(SingleChoiceDialog, self).close()

    ###########################################################################
    # Protected 'IWidget' interface.
    ###########################################################################

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the window. """

        style = wx.DEFAULT_DIALOG_STYLE | wx.CLIP_CHILDREN | wx.OK
        if self.cancel:
            style |= wx.CANCEL
        if self.resizeable:
            style |= wx.RESIZE_BORDER

        dialog = wx.SingleChoiceDialog(
            parent,
            self.message,
            self.title,
            self._choice_strings(),
            style,
            self.position
        )

        if self.size != (-1, -1):
            dialog.SetSize(self.size)

        return dialog
