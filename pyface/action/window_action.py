# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
""" Abstract base class for all window actions. """


from traits.api import Instance, Property

from pyface.action.listening_action import ListeningAction
from pyface.i_window import IWindow


class WindowAction(ListeningAction):
    """ Abstract base class for window actions. """

    # 'ListeningAction' interface --------------------------------------------

    object = Property(observe="window")

    # 'WindowAction' interface -----------------------------------------------

    #: The window that the action is associated with.
    window = Instance(IWindow)

    # ------------------------------------------------------------------------
    # Protected interface.
    # ------------------------------------------------------------------------

    def _get_object(self):
        return self.window

    def destroy(self):
        # Disconnect listeners to window and dependent properties.
        self.window = None
        super().destroy()


class CloseWindowAction(WindowAction):
    """ Close the specified window """

    name = "Close"
    accelerator = "Ctrl+W"
    method = "close"
