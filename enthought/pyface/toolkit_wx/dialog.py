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
from enthought.pyface.api import OK, CANCEL, YES, NO


RESULT_MAP = {
    wx.ID_OK     : OK,
    wx.ID_CANCEL : CANCEL,
    wx.ID_YES    : YES,
    wx.ID_NO     : NO,
    wx.ID_CLOSE  : CANCEL,
    # fixme: There seems to be a bug in wx.SingleChoiceDialog that allows it to
    # return 0 when it is closed via the window (closing it via the buttons
    # works just fine).
    0            : CANCEL
}

    
class Dialog_wx(object):
    """ The Dialog monkey patch for wx. """

    ###########################################################################
    # 'Widget' toolkit interface.
    ###########################################################################

    def _tk_widget_create(self, parent):
        """ Create the toolkit-specific control that represents the window. """

        style = wx.DEFAULT_DIALOG_STYLE | wx.CLIP_CHILDREN

        if self.resizeable:
            style = style | wx.RESIZE_BORDER
            
        return wx.Dialog(parent, -1, self.title, style=style)

    ###########################################################################
    # 'Window' toolkit interface.
    ###########################################################################

    def _tk_window_add_event_listeners(self, control):
        """ Adds any event listeners required by the window. """

        # For dialogs we don't need to catch any wx events.
        pass

    ###########################################################################
    # 'Dialog' toolkit interface.
    ###########################################################################

    def _tk_dialog_show_modal(self):
        """ Show a modal dialog and return the pyface result. """

        return RESULT_MAP[self.control.ShowModal()]

    def _tk_dialog_create_area(self, parent):
        """ Creates the main content of the dialog. """

        panel = wx.Panel(parent, -1)
        panel.SetBackgroundColour("red")
        panel.SetSize((100, 200))
        
        return panel

    def _tk_dialog_create_buttons(self, parent):
        """ Creates the buttons. """

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 'OK' button.
        if self.ok_button_label:
            label = self.ok_button_label
        else:
            label = "OK"

        self._wx_ok = ok = wx.Button(parent, wx.ID_OK, label)
        ok.SetDefault()
        wx.EVT_BUTTON(parent, wx.ID_OK, self._wx_on_ok)
        sizer.Add(ok)

        # 'Cancel' button.
        if self.cancel_button_label:
            label = self.cancel_button_label
        else:
            label = "Cancel"

        self._wx_cancel = cancel = wx.Button(parent, wx.ID_CANCEL, label)
        wx.EVT_BUTTON(parent, wx.ID_CANCEL, self._wx_on_cancel)
        sizer.Add(cancel, 0, wx.LEFT, 10)

        # 'Help' button.
        if len(self.help_id) > 0:
            if self.help_button_label:
                label = self.help_button_label
            else:
                label = "Help"

            help = wx.Button(parent, wx.ID_HELP, label)
            wx.EVT_BUTTON(parent, wx.ID_HELP, self._wx_on_help)
            sizer.Add(help, 0, wx.LEFT, 10)

        return sizer

    def _tk_dialog_assemble(self, dialog, dialog_area, buttons):
        """ Complete the dialog by assembling the various components. """

        sizer = wx.BoxSizer(wx.VERTICAL)
        dialog.SetSizer(sizer)
        dialog.SetAutoLayout(True)

        # The 'guts' of the dialog.
        sizer.Add(dialog_area, 1, wx.EXPAND | wx.ALL, self.dialog_area_border)

        # The buttons.
        sizer.Add(buttons, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        # Resize the dialog to match the sizer's minimal size.
        if self.size != (-1,-1):
            dialog.SetSize(self.size)

        else:
            sizer.Fit(dialog)

        dialog.CentreOnParent()

    #### wx event handlers ####################################################

    def _wx_on_ok(self, event):
        """ Called when the 'OK' button is pressed. """

        self.return_code = OK
        
        # Let the default handler close the dialog appropriately.
        event.Skip()
        
        return

    def _wx_on_cancel(self, event):
        """ Called when the 'Cancel' button is pressed. """

        self.return_code = CANCEL

        # Let the default handler close the dialog appropriately.
        event.Skip()

        return

    def _wx_on_help(self, event):
        """ Called when the 'Help' button is pressed. """

        print 'Heeeeelllllllllllllpppppppppppppppppppp'
        
        return

#### EOF ######################################################################
