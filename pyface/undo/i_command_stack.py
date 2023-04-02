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
from traits.api import Bool, Instance, Interface, Str

# Local imports.
from .i_undo_manager import IUndoManager


class ICommandStack(Interface):
    """The command stack interface.  A command stack is responsible for
    managing the changes to a data model and recording those changes so that
    they can be undone or redone.
    """

    #### 'ICommandStack' interface ############################################

    #: This is the clean state of the stack.  Its value changes as commands are
    #: undone and redone.  It can also be explicity set to mark the current
    #: stack position as being clean (when the data is saved to disk for
    #: example).
    clean = Bool()

    #: This is the name of the command that can be redone.  It will be empty if
    #: there is no command that can be redone.  It is maintained by the undo
    #: stack.
    redo_name = Str()

    #: This is the undo manager that manages this stack.
    undo_manager = Instance(IUndoManager)

    #: This is the name of the command that can be undone.  It will be empty if
    #: there is no command that can be undone.  It is maintained by the undo
    #: stack.
    undo_name = Str()

    ###########################################################################
    # 'ICommandStack' interface.
    ###########################################################################

    def begin_macro(self, name):
        """This begins a macro by creating an empty command with the given
        'name'.  The commands passed to all subsequent calls to 'push()' will
        be contained in the macro until the next call to 'end_macro()'.  Macros
        may be nested.  The stack is disabled (ie. nothing can be undone or
        redone) while a macro is being created (ie. while there is an
        outstanding 'end_macro()' call).
        """

    def clear(self):
        """This clears the stack, without undoing or redoing any commands, and
        leaves the stack in a clean state.  It is typically used when all
        changes to the data have been abandoned.
        """

    def end_macro(self):
        """ This ends a macro. """

    def push(self, command):
        """This executes a command and saves it on the command stack so that
        it can be subsequently undone and redone.  'command' is an instance
        that implements the ICommand interface.  Its 'do()' method is called
        to execute the command.  If any value is returned by 'do()' then it is
        returned by 'push()'.  The command stack will keep a reference to the
        result so that it can recognise it as an argument to a subsequent
        command (which allows a script to properly save a result needed later).
        """

    def redo(self, sequence_nr=0):
        """If 'sequence_nr' is 0 then the last command that was undone is
        redone and any result returned.  Otherwise commands are redone up to
        and including the given 'sequence_nr' and any result of the last of
        these is returned.
        """

    def undo(self, sequence_nr=0):
        """If 'sequence_nr' is 0 then the last command is undone.  Otherwise
        commands are undone up to and including the given 'sequence_nr'.
        """
