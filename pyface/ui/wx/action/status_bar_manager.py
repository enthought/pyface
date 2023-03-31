# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


""" A status bar manager realizes itself in a status bar control.
"""


import wx


from traits.api import Any, HasTraits, List, Property, Str, provides

from pyface.action.i_status_bar_manager import IStatusBarManager


@provides(IStatusBarManager)
class StatusBarManager(HasTraits):
    """ A status bar manager realizes itself in a status bar control. """

    # The message displayed in the first field of the status bar.
    message = Property

    # The messages to be displayed in the status bar fields.
    messages = List(Str)

    # The toolkit-specific control that represents the status bar.
    status_bar = Any()

    # ------------------------------------------------------------------------
    # 'StatusBarManager' interface.
    # ------------------------------------------------------------------------

    def create_status_bar(self, parent):
        """ Creates a status bar. """

        if self.status_bar is None:
            self.status_bar = wx.StatusBar(parent)
            self.status_bar._pyface_control = self
            if len(self.messages) > 1:
                self.status_bar.SetFieldsCount(len(self.messages))
                for i in range(len(self.messages)):
                    self.status_bar.SetStatusText(self.messages[i], i)
            else:
                self.status_bar.SetStatusText(self.message)

        return self.status_bar

    def destroy(self):
        """ Removes a status bar. """

        if self.status_bar is not None:
            self.status_bar.Destroy()
            self.status_bar._pyface_control = None
            self.status_bar = None

    # ------------------------------------------------------------------------
    # Property handlers.
    # ------------------------------------------------------------------------

    def _get_message(self):
        """ Property getter. """

        if len(self.messages) > 0:
            message = self.messages[0]

        else:
            message = ""

        return message

    def _set_message(self, value):
        """ Property setter. """

        if len(self.messages) > 0:
            old = self.messages[0]
            self.messages[0] = value

        else:
            old = ""
            self.messages.append(value)

        self.trait_property_changed("message", old, value)

        return

    # ------------------------------------------------------------------------
    # Trait event handlers.
    # ------------------------------------------------------------------------

    def _messages_changed(self):
        """ Sets the text displayed on the status bar. """

        if self.status_bar is not None:
            for i in range(len(self.messages)):
                self.status_bar.SetStatusText(self.messages[i], i)

    def _messages_items_changed(self):
        """ Sets the text displayed on the status bar. """

        if self.status_bar is not None:
            for i in range(len(self.messages)):
                self.status_bar.SetStatusText(self.messages[i], i)

        return
