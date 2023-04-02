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
from traits.api import Bool, Event, Instance, Int, Interface, Str


class IUndoManager(Interface):
    """The undo manager interface.  An undo manager is responsible for one or
    more command stacks.  Typically an application would have a single undo
    manager.
    """

    #### 'IUndoManager' interface #############################################

    #: This is the currently active command stack and may be None.  Typically it
    #: is set when some sort of editor becomes active.
    #: IUndoManager and ICommandStack depend on one another, hence we can't
    #: directly import ICommandStack and use it here.
    active_stack = Instance("pyface.undo.api.ICommandStack")

    #: This reflects the clean state of the currently active command stack.  It
    #: is intended to support a "document modified" indicator in the GUI.  It is
    #: maintained by the undo manager.
    active_stack_clean = Bool()

    #: This is the name of the command that can be redone.  It will be empty if
    #: there is no command that can be redone.  It is maintained by the undo
    #: manager.
    redo_name = Str()

    #: This is the sequence number of the next command to be performed.  It is
    #: incremented immediately before a command is invoked (by its 'do()'
    #: method).
    sequence_nr = Int()

    #: This event is fired when the index of a command stack changes.  Note that
    #: it may not be the active stack.
    stack_updated = Event(Instance("pyface.undo.api.ICommandStack"))

    #: This is the name of the command that can be undone.  It will be empty if
    #: there is no command that can be undone.  It is maintained by the undo
    #: manager.
    undo_name = Str()

    ###########################################################################
    # 'IUndoManager' interface.
    ###########################################################################

    def redo(self):
        """ Redo the last undone command of the active command stack. """

    def undo(self):
        """ Undo the last command of the active command stack. """
