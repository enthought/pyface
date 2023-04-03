# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


from traits.api import Any, Bool, Interface, List, Str


class IStatusBarManager(Interface):
    """ The interface for a status bar manager. """

    # The message displayed in the first field of the status bar.
    message = Str()

    # The messages to be displayed in the status bar fields.
    messages = List(Str)

    # The toolkit-specific control that represents the status bar.
    status_bar = Any()

    # Whether to show a size grip on the status bar.
    size_grip = Bool(False)

    # Whether the status bar is visible.
    visible = Bool(True)

    def create_status_bar(self, parent):
        """ Creates a status bar.

        Parameters
        ----------
        parent : toolkit control
            The toolkit control that owns the status bar.
        """

    def destroy(self):
        """ Destroys the status bar. """
