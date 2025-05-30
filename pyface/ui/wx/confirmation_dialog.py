# (C) Copyright 2005-2025 Enthought, Inc., Austin, TX
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


import wx

from traits.api import Bool, Enum, provides, Str

from pyface.i_confirmation_dialog import (
    IConfirmationDialog,
    MConfirmationDialog,
)
from pyface.constant import CANCEL, YES, NO
from pyface.ui_traits import Image
from .dialog import Dialog
from .image_resource import ImageResource


@provides(IConfirmationDialog)
class ConfirmationDialog(MConfirmationDialog, Dialog):
    """ The toolkit specific implementation of a ConfirmationDialog.  See the
    IConfirmationDialog interface for the API documentation.
    """

    # 'IConfirmationDialog' interface -------------------------------------#

    cancel = Bool(False)

    default = Enum(NO, YES, CANCEL)

    image = Image()

    message = Str()

    informative = Str()

    detail = Str()

    no_label = Str()

    yes_label = Str()

    # ------------------------------------------------------------------------
    # Protected 'IDialog' interface.
    # ------------------------------------------------------------------------

    def _create_buttons(self, parent):
        sizer = wx.StdDialogButtonSizer()

        # 'YES' button.
        if self.yes_label:
            label = self.yes_label
        else:
            label = "Yes"

        self._yes = yes = wx.Button(parent, wx.ID_YES, label)
        if self.default == YES:
            yes.SetDefault()
        parent.Bind(wx.EVT_BUTTON, self._on_yes, yes)
        sizer.AddButton(yes)

        # 'NO' button.
        if self.no_label:
            label = self.no_label
        else:
            label = "No"

        self._no = no = wx.Button(parent, wx.ID_NO, label)
        if self.default == NO:
            no.SetDefault()
        parent.Bind(wx.EVT_BUTTON, self._on_no, no)
        sizer.AddButton(no)

        if self.cancel:
            # 'Cancel' button.
            if self.no_label:
                label = self.cancel_label
            else:
                label = "Cancel"

            self._cancel = cancel = wx.Button(parent, wx.ID_CANCEL, label)
            if self.default == CANCEL:
                cancel.SetDefault()

            parent.Bind(wx.EVT_BUTTON, self._wx_on_cancel, cancel)
            sizer.AddButton(cancel)

        sizer.Realize()
        return sizer

    def _create_dialog_area(self, parent):
        panel = wx.Panel(parent, -1)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        panel.SetSizer(sizer)
        panel.SetAutoLayout(True)

        # The image.
        if self.image is None:
            image_rc = ImageResource("warning")
        else:
            image_rc = self.image

        image = wx.StaticBitmap(panel, -1, image_rc.create_bitmap())
        sizer.Add(image, 0, wx.EXPAND | wx.ALL, 10)

        # The message.
        if self.informative:
            message = self.message + "\n\n" + self.informative
        else:
            message = self.message
        message = wx.StaticText(panel, -1, message)
        sizer.Add(message, 1, wx.EXPAND | wx.TOP, 15)

        # Resize the panel to match the sizer.
        sizer.Fit(panel)

        return panel

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    # wx event handlers ----------------------------------------------------

    def _on_yes(self, event):
        """ Called when the 'Yes' button is pressed. """

        self.control.EndModal(wx.ID_YES)

    def _on_no(self, event):
        """ Called when the 'No' button is pressed. """

        self.control.EndModal(wx.ID_NO)
