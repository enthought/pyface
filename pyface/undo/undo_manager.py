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
from traits.api import (
    Bool,
    Event,
    HasTraits,
    Instance,
    Int,
    Property,
    Str,
    provides,
    observe,
)

# Local imports.
from .i_undo_manager import IUndoManager


@provides(IUndoManager)
class UndoManager(HasTraits):
    """The UndoManager class is the default implementation of the
    IUndoManager interface.
    """

    #### 'IUndoManager' interface #############################################

    #: This is the currently active command stack and may be None. Typically it
    #: is set when some sort of editor becomes active.
    active_stack = Instance("pyface.undo.api.ICommandStack")

    #: This reflects the clean state of the currently active command stack. It
    #: is intended to support a "document modified" indicator in the GUI. It is
    #: maintained by the undo manager.
    active_stack_clean = Property(Bool)

    #: This is the name of the command that can be redone. It will be empty if
    #: there is no command that can be redone. It is maintained by the undo
    #: manager.
    redo_name = Property(Str)

    #: This is the sequence number of the next command to be performed. It is
    #: incremented immediately before a command is invoked (by its 'do()'
    #: method).
    sequence_nr = Int()

    #: This event is fired when the index of a command stack changes. The value
    #: of the event is the stack that has changed. Note that it may not be the
    #: active stack.
    stack_updated = Event()

    #: This is the name of the command that can be undone. It will be empty if
    #: there is no command that can be undone. It is maintained by the undo
    #: manager.
    undo_name = Property(Str)

    ###########################################################################
    # 'IUndoManager' interface.
    ###########################################################################

    def redo(self):
        """ Redo the last undone command of the active command stack. """

        if self.active_stack is not None:
            self.active_stack.redo()

    def undo(self):
        """ Undo the last command of the active command stack. """

        if self.active_stack is not None:
            self.active_stack.undo()

    ###########################################################################
    # Private interface.
    ###########################################################################

    @observe("active_stack")
    def _update_stack_updated(self, event):
        """ Handle a different stack becoming active. """
        new = event.new
        # Pretend that the stack contents have changed.
        self.stack_updated = new

    def _get_active_stack_clean(self):
        """ Get the current clean state. """

        if self.active_stack is None:
            active_stack_clean = True
        else:
            active_stack_clean = self.active_stack.clean

        return active_stack_clean

    def _get_redo_name(self):
        """ Get the current redo name. """

        if self.active_stack is None:
            redo_name = ""
        else:
            redo_name = self.active_stack.redo_name

        return redo_name

    def _get_undo_name(self):
        """ Get the current undo name. """

        if self.active_stack is None:
            undo_name = ""
        else:
            undo_name = self.active_stack.undo_name

        return undo_name
