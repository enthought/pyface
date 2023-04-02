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


import wx


from traits.api import Enum, provides, Str


from pyface.i_message_dialog import IMessageDialog, MMessageDialog
from .dialog import Dialog


# Map the ETS severity to the corresponding wx standard icon.
_SEVERITY_TO_ICON_MAP = {
    "information": wx.ICON_INFORMATION,
    "warning": wx.ICON_WARNING,
    "error": wx.ICON_ERROR,
}


@provides(IMessageDialog)
class MessageDialog(MMessageDialog, Dialog):
    """ The toolkit specific implementation of a MessageDialog.  See the
    IMessageDialog interface for the API documentation.
    """

    # 'IMessageDialog' interface -------------------------------------------

    message = Str()

    informative = Str()

    detail = Str()

    severity = Enum("information", "warning", "error")

    # unused trait, this functionality is only supported on Qt
    text_format = Enum("auto", "plain", "rich")

    # ------------------------------------------------------------------------
    # Protected 'IDialog' interface.
    # ------------------------------------------------------------------------

    def _create_contents(self, parent):
        # In wx this is a canned dialog.
        pass

    # ------------------------------------------------------------------------
    # Protected 'IWidget' interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        # The message.
        if self.informative:
            message = self.message + "\n\n" + self.informative
        else:
            message = self.message

        style = _SEVERITY_TO_ICON_MAP[self.severity] | wx.OK | wx.STAY_ON_TOP
        if self.resizeable:
            style |= wx.RESIZE_BORDER

        dlg = wx.MessageDialog(
            parent, message, self.title, style, self.position
        )
        if self.size != (-1, -1):
            dlg.SetSize(self.size)

        return dlg
