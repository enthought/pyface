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

# Local imports.
from .abstract_command_stack_action import AbstractCommandStackAction


class UndoAction(AbstractCommandStackAction):
    """ An action that undos the last command of the active command stack. """

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Perform the action. """

        self.undo_manager.undo()

    ###########################################################################
    # 'AbstractUndoAction' interface.
    ###########################################################################

    def _update_action(self):
        """ Update the state of the action. """

        name = self.undo_manager.undo_name

        if name:
            name = "&Undo " + name
            self.enabled = True
        else:
            name = "&Undo"
            self.enabled = False

        self.name = name
