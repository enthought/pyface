# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


""" Enthought pyface package component
"""


import sys
import wx


from traits.api import Bool, Enum, Int, provides, Str


from pyface.i_dialog import IDialog, MDialog
from pyface.constant import OK, CANCEL, YES, NO
from .window import Window


# Map wx dialog related constants to the pyface equivalents.
_RESULT_MAP = {
    wx.ID_OK: OK,
    wx.ID_CANCEL: CANCEL,
    wx.ID_YES: YES,
    wx.ID_NO: NO,
    wx.ID_CLOSE: CANCEL,
    # There seems to be a bug in wx.SingleChoiceDialog that allows it to return
    # 0 when it is closed via the window (closing it via the buttons works just
    # fine).
    0: CANCEL,
}


@provides(IDialog)
class Dialog(MDialog, Window):
    """ The toolkit specific implementation of a Dialog.  See the IDialog
    interface for the API documentation.
    """

    # 'IDialog' interface -------------------------------------------------#

    cancel_label = Str()

    help_id = Str()

    help_label = Str()

    ok_label = Str()

    resizeable = Bool(True)

    return_code = Int(OK)

    style = Enum("modal", "nonmodal")

    # 'IWindow' interface -------------------------------------------------#

    title = Str("Dialog")

    # ------------------------------------------------------------------------
    # Protected 'IDialog' interface.
    # ------------------------------------------------------------------------

    def _create_buttons(self, parent):
        sizer = wx.StdDialogButtonSizer()

        # The 'OK' button.
        if self.ok_label:
            label = self.ok_label
        else:
            label = "OK"

        self._wx_ok = ok = wx.Button(parent, wx.ID_OK, label)
        ok.SetDefault()
        parent.Bind(wx.EVT_BUTTON, self._wx_on_ok, id=wx.ID_OK)
        sizer.AddButton(ok)

        # The 'Cancel' button.
        if self.cancel_label:
            label = self.cancel_label
        else:
            label = "Cancel"

        self._wx_cancel = cancel = wx.Button(parent, wx.ID_CANCEL, label)
        parent.Bind(wx.EVT_BUTTON, self._wx_on_cancel, id=wx.ID_CANCEL)
        sizer.AddButton(cancel)

        # The 'Help' button.
        if len(self.help_id) > 0:
            if self.help_label:
                label = self.help_label
            else:
                label = "Help"

            help = wx.Button(parent, wx.ID_HELP, label)
            parent.Bind(wx.EVT_BUTTON, self._wx_on_help, id=wx.ID_HELP)
            sizer.AddButton(help)

        sizer.Realize()
        return sizer

    def _create_contents(self, parent):
        sizer = wx.BoxSizer(wx.VERTICAL)
        parent.SetSizer(sizer)
        parent.SetAutoLayout(True)

        # The 'guts' of the dialog.
        dialog_area = self._create_dialog_area(parent)
        sizer.Add(dialog_area, 1, wx.EXPAND | wx.ALL, 5)

        # The buttons.
        buttons = self._create_buttons(parent)
        sizer.Add(buttons, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        # Resize the dialog to match the sizer's minimal size.
        if self.size != (-1, -1):
            parent.SetSize(self.size)
        else:
            sizer.Fit(parent)

        parent.CentreOnParent()

    def _create_dialog_area(self, parent):
        panel = wx.Panel(parent, -1)
        panel.SetBackgroundColour("red")
        panel.SetSize((100, 200))

        return panel

    def _show_modal(self):
        if sys.platform == "darwin":
            # Calling Show(False) is needed on the Mac for the modal dialog
            # to show up at all.
            self.control.Show(False)
        return _RESULT_MAP[self.control.ShowModal()]

    # ------------------------------------------------------------------------
    # Protected 'IWidget' interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        style = wx.DEFAULT_DIALOG_STYLE | wx.CLIP_CHILDREN

        if self.resizeable:
            style |= wx.RESIZE_BORDER

        return wx.Dialog(
            parent, -1, self.title, self.position, self.size, style
        )

    # wx event handlers ----------------------------------------------------

    def _wx_on_ok(self, event):
        """ Called when the 'OK' button is pressed. """

        self.return_code = OK

        # Let the default handler close the dialog appropriately.
        event.Skip()

    def _wx_on_cancel(self, event):
        """ Called when the 'Cancel' button is pressed. """

        self.return_code = CANCEL

        # Let the default handler close the dialog appropriately.
        event.Skip()

    def _wx_on_help(self, event):
        """ Called when the 'Help' button is pressed. """
        pass
