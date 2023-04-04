# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The action controller for workbench menu and tool bars. """


from pyface.action.api import ActionController as PyfaceActionController
from pyface.workbench.api import WorkbenchWindow
from traits.api import Instance


class ActionController(PyfaceActionController):
    """ The action controller for workbench menu and tool bars.

    The controller is used to 'hook' the invocation of every action on the menu
    and tool bars. This is done so that additional (and workbench specific)
    information can be added to action events. Currently, we attach a reference
    to the workbench window.

    """

    # 'ActionController' interface -----------------------------------------

    # The workbench window that this is the controller for.
    window = Instance(WorkbenchWindow)

    # ------------------------------------------------------------------------
    # 'ActionController' interface.
    # ------------------------------------------------------------------------

    def perform(self, action, event):
        """ Control an action invocation. """

        # Add a reference to the window and the application to the event.
        event.window = self.window

        return action.perform(event)
