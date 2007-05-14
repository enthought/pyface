#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
# 
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
# 
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------

# Major package imports.
import wx

# Enthought library imports.
from enthought.pyface.api import CANCEL, NO, YES, ImageResource, ImageWidget
from enthought.traits.api import Bool, Enum, Instance, Str


class ConfirmationDialog_wx(object):
    """ The ConfirmationDialog monkey patch for wx. """

    ###########################################################################
    # 'Dialog' toolkit interface.
    ###########################################################################

    def _tk_dialog_create_area(self, parent):
        """ Creates the main content of the dialog. """

        panel = wx.Panel(parent, -1)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        panel.SetSizer(sizer)
        panel.SetAutoLayout(True)

        # The image.
        if self.image is None:
            image_rc = ImageResource('warning.png')
        else:
            image_rc = self.image

        image = ImageWidget(panel, bitmap=image_rc.create_bitmap())
        sizer.Add(image.control, 0, wx.EXPAND)

        # The message.
        message = wx.StaticText(panel, -1, self.message)
        sizer.Add(message, 1, wx.EXPAND | wx.TOP, 15)

        # Resize the panel to match the sizer.
        sizer.Fit(panel)

        return panel

    def _tk_dialog_create_buttons(self, parent):
        """ Creates the buttons. """

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 'YES' button.
        if self.yes_label:
            label = self.yes_label
        else:
            label = "Yes"

        self._yes = yes = wx.Button(parent, wx.ID_YES, label)
        if self.default == YES:
            yes.SetDefault()
        wx.EVT_BUTTON(parent, wx.ID_YES, self._on_yes)
        sizer.Add(yes)

        # 'NO' button.
        if self.no_label:
            label = self.no_label
        else:
            label = "No"

        self._no = no = wx.Button(parent, wx.ID_NO, label)
        if self.default == NO:
            no.SetDefault()
        wx.EVT_BUTTON(parent, wx.ID_NO, self._on_no)
        sizer.Add(no, 0, wx.LEFT, 10)

        if self.cancel:
            # 'Cancel' button.
            if self.no_label:
                label = self.cancel_label
            else:
                label = "Cancel"

            self._cancel = cancel = wx.Button(parent, wx.ID_CANCEL, label)
            if self.default == CANCEL:
                cancel.SetDefault()

            wx.EVT_BUTTON(parent, wx.ID_CANCEL, self._on_cancel)
            sizer.Add(cancel, 0, wx.LEFT, 10)

        return sizer

    #### wx event handlers ####################################################

    def _on_yes(self, event):
        """ Called when the 'Yes' button is pressed. """

        self.control.EndModal(wx.ID_YES)
        
        return

    def _on_no(self, event):
        """ Called when the 'No' button is pressed. """

        self.control.EndModal(wx.ID_NO)

        return

#### EOF ######################################################################
