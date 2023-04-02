# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

# ------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
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
from traits.api import Any, Callable, Instance
from ..i_command_stack import ICommandStack


class CommandAction(Action):
    """The CommandAction class is an Action class that wraps undo/redo
    commands.  It is only useful for commands that do not take any arguments or
    return any result.
    """

    #### 'CommandAction' interface ############################################

    #: The command to create when the action is performed.
    command = Callable()

    #: The command stack onto which the command will be pushed when the action
    #: is performed.
    command_stack = Instance(ICommandStack)

    #: This is the data on which the command operates.
    data = Any()

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """This is reimplemented to push a new command instance onto the
        command stack.
        """

        self.command_stack.push(self.command(data=self.data))

    def _name_default(self):
        """ This gets the action name from the command. """

        if self.command:
            name = self.command().name
        else:
            name = ""

        return name
