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


from traits.api import Any, Float, HasTraits, Instance, List, on_trait_change,\
    Property, Str
from pyface.timer.api import Timer


class StatusBarManager(HasTraits):
    """ A status bar manager realizes itself in a status bar control. """

    # The message displayed in the first field of the status bar.
    message = Property

    # The messages to be displayed in the status bar fields.
    messages = List(Str)

    # The toolkit-specific control that represents the status bar.
    status_bar = Any()

    # Number of seconds to display new messages for [default: indefinitely]
    message_duration_sec = Float

    _timer = Instance(Timer)

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

            self.messages_changed()

        return self.status_bar

    def destroy(self):
        """ Removes a status bar. """

        if self.status_bar is not None:
            if self._timer is not None:
                self._timer.Stop()
                self._timer = None

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

    @on_trait_change("messages[]", post_init=True)
    def messages_changed(self):
        """ Sets the text displayed on the status bar. """

        def timed_action():
            self.messages = []
            self._timer.Stop()
            self._timer = None

        if self.status_bar is None:
            return

        for i in range(len(self.messages)):
            self.status_bar.SetStatusText(self.messages[i], i)

        # Schedule removing the message if needed:
        if self.message_duration_sec > 0 and self._timer is None:
            self._timer = Timer(self.message_duration_sec * 1000, timed_action)
