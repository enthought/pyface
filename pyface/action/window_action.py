# Copyright (c) 2005-2017, Enthought, Inc.
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
""" Abstract base class for all window actions. """

# Enthought library imports.
from pyface.window import Window
from traits.api import Instance, Property

# Local imports.
from pyface.action.listening_action import ListeningAction


class WindowAction(ListeningAction):
    """ Abstract base class for window actions. """

    # 'ListeningAction' interface --------------------------------------------

    object = Property(depends_on='window')

    # 'WindowAction' interface -----------------------------------------------

    #: The window that the action is associated with.
    window = Instance(Window)

    # ------------------------------------------------------------------------
    # Protected interface.
    # ------------------------------------------------------------------------

    def _get_object(self):
        return self.window

    def destroy(self):
        # Disconnect listeners to window and dependent properties.
        self.window = None
        super(WindowAction, self).destroy()


class CloseWindowAction(WindowAction):
    """ Close the specified window """
    name = u'Close'
    accelerator = 'Ctrl+W'
    method = 'close'