# (C) Copyright 2008-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

# ------------------------------------------------------------------------------
# Copyright (c) 2008, Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Riverbank Computing Limited
# Description: <Enthought undo package component>
# ------------------------------------------------------------------------------

# Enthought library imports.
from pyface.action.api import Action
from traits.api import Instance

# Local library imports
from ..i_undo_manager import IUndoManager


class AbstractCommandStackAction(Action):
    """The abstract base class for all actions that operate on a command
    stack.
    """

    #### 'AbstractCommandStackAction' interface ###############################

    #: The undo manager.
    undo_manager = Instance(IUndoManager)

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Initialise the instance. """

        super().__init__(**traits)

        self.undo_manager.observe(
            self._on_stack_updated, "stack_updated"
        )

        # Update the action to initialise it.
        self._update_action()

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def destroy(self):
        """Called when the action is no longer required.

        By default this method does nothing, but this would be a great place to
        unhook trait listeners etc.

        """

        self.undo_manager.observe(
            self._on_stack_updated, "stack_updated", remove=True
        )

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _update_action(self):
        """ Update the state of the action. """

        raise NotImplementedError

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _on_stack_updated(self, event):
        """ Handle changes to the state of a command stack. """
        stack = event.new
        # Ignore unless it is the active stack.
        if stack is self.undo_manager.active_stack:
            self._update_action()
