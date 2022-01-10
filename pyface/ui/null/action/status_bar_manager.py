# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A status bar manager realizes itself in a status bar control. """


from traits.api import Any, HasTraits, List, Property, Str


class StatusBarManager(HasTraits):
    """ A status bar manager realizes itself in a status bar control. """

    # The manager's unique identifier (if it has one).
    id = Str()

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

        return self.status_bar

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

        return

    # ------------------------------------------------------------------------
    # Trait event handlers.
    # ------------------------------------------------------------------------

    def _messages_changed(self):
        """ Sets the text displayed on the status bar. """

    def _messages_items_changed(self):
        """ Sets the text displayed on the status bar. """
        return
