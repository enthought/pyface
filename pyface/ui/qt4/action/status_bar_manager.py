# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
# (C) Copyright 2007 Riverbank Computing Limited
# This software is provided without warranty under the terms of the BSD license.
# However, when used with the GPL version of PyQt the additional terms described in the PyQt GPL exception also apply

# ------------------------------------------------------------------------------


from pyface.qt import QtGui


from traits.api import Any, Bool, Float, HasTraits, Instance, List, Property, \
    Str
from pyface.timer.api import Timer


class StatusBarManager(HasTraits):
    """ A status bar manager realizes itself in a status bar control. """

    # The message displayed in the first field of the status bar.
    message = Property

    # The messages to be displayed in the status bar fields.
    messages = List(Str)

    # The toolkit-specific control that represents the status bar.
    status_bar = Any()

    # Whether to show a size grip on the status bar.
    size_grip = Bool(False)

    # Whether the status bar is visible.
    visible = Bool(True)

    # Number of seconds to display new messages for [default: indefinitely]
    message_duration_sec = Float

    _timer = Instance(Timer)

    # ------------------------------------------------------------------------
    # 'StatusBarManager' interface.
    # ------------------------------------------------------------------------

    def create_status_bar(self, parent):
        """ Creates a status bar. """

        if self.status_bar is None:
            self.status_bar = QtGui.QStatusBar(parent)
            self.status_bar.setSizeGripEnabled(self.size_grip)
            self.status_bar.setVisible(self.visible)
            self._show_messages()

        return self.status_bar

    def destroy(self):
        """ Destroys the status bar. """
        if self.status_bar is not None:
            if self._timer is not None:
                self._timer.Stop()
                self._timer = None

            self.status_bar.deleteLater()
            self.status_bar = None

    # ------------------------------------------------------------------------
    # Property handlers.
    # ------------------------------------------------------------------------

    def _get_message(self):
        if len(self.messages) > 0:
            message = self.messages[0]
        else:
            message = ""

        return message

    def _set_message(self, value):

        if len(self.messages) > 0:
            old = self.messages[0]
            self.messages[0] = value
        else:
            old = ""
            self.messages.append(old)

        self.trait_property_changed("message", old, value)

    # ------------------------------------------------------------------------
    # Trait event handlers.
    # ------------------------------------------------------------------------

    def _messages_changed(self):
        """ Sets the text displayed on the status bar. """

        if self.status_bar is not None:
            self._show_messages()

    def _messages_items_changed(self):
        """ Sets the text displayed on the status bar. """

        if self.status_bar is not None:
            self._show_messages()

    def _size_grip_changed(self):
        """ Turns the size grip on the status bar on and off. """

        if self.status_bar is not None:
            self.status_bar.setSizeGripEnabled(self.size_grip)

    def _visible_changed(self):
        """ Turns the status bar visibility on and off. """

        if self.status_bar is not None:
            self.status_bar.setVisible(self.visible)

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _show_messages(self):
        """ Display the list of messages.

        Note: not using the msecs argument of the `status_bar.showNessage`
        method to keep this class' message trait in sync with the Qt widget.
        """
        def timed_action():
            self.messages = []
            self._timer.Stop()
            self._timer = None

        if self.status_bar is None:
            return

        # FIXME v3: At the moment we just string them together but we may
        # decide to put all but the first message into separate widgets.  We
        # probably also need to extend the API to allow a "message" to be a
        # widget - depends on what wx is capable of.
        self.status_bar.showMessage("  ".join(self.messages))

        # Schedule removing the message if needed:
        if self.message_duration_sec > 0 and self._timer is None:
            self._timer = Timer(self.message_duration_sec * 1000, timed_action)
