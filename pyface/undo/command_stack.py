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
    HasTraits,
    Instance,
    Int,
    List,
    Property,
    Str,
    provides,
)

# Local imports.
from .abstract_command import AbstractCommand
from .i_command import ICommand
from .i_command_stack import ICommandStack
from .i_undo_manager import IUndoManager


class _StackEntry(HasTraits):
    """ The _StackEntry class is a single entry on a command stack. """

    #### '_StackEntry' interface ##############################################

    #: Set if the entry corresponds to a clean point on the stack.
    clean = Bool(False)

    #: The command instance.
    command = Instance(ICommand)

    #: The sequence number of the entry.
    sequence_nr = Int()


class _MacroCommand(AbstractCommand):
    """ The _MacroCommand class is an internal command that handles macros. """

    #### '_MacroCommand' interface ############################################

    #: The commands that make up this macro.
    macro_commands = List(Instance(ICommand))

    ###########################################################################
    # 'ICommand' interface.
    ###########################################################################

    def do(self):
        """ Invoke the command. """

        # This is a dummy.
        return None

    def merge(self, other):
        """ Try and merge a command. """

        if len(self.macro_commands) == 0:
            merged = False
        else:
            merged = self.macro_commands[-1].merge(other)

        return merged

    def redo(self):
        """ Redo the sub-commands. """

        for cmd in self.macro_commands:
            cmd.redo()

        # Macros cannot return values.
        return None

    def undo(self):
        """ Undo the sub-commands. """

        for cmd in self.macro_commands:
            cmd.undo()


@provides(ICommandStack)
class CommandStack(HasTraits):
    """The CommandStack class is the default implementation of the
    ICommandStack interface.
    """

    #### 'ICommandStack' interface ############################################

    #: This is the clean state of the stack.  Its value changes as commands are
    #: undone and redone.  It can also be explicity set to mark the current
    #: stack position as being clean (when the data is saved to disk for
    #: example).
    clean = Property(Bool)

    #: This is the name of the command that can be redone.  It will be empty if
    #: there is no command that can be redone.  It is maintained by the undo
    #: stack.
    redo_name = Property(Str)

    #: This is the undo manager that manages this stack.
    undo_manager = Instance(IUndoManager)

    #: This is the name of the command that can be undone.  It will be empty if
    #: there is no command that can be undone.  It is maintained by the undo
    #: stack.
    undo_name = Property(Str)

    #### Private interface ####################################################

    # The current index into the stack (ie. the last command that was done).
    _index = Int(-1)

    # The current macro stack.
    _macro_stack = List(Instance(_MacroCommand))

    # The stack itself.
    _stack = List(Instance(_StackEntry))

    ###########################################################################
    # 'ICommandStack' interface.
    ###########################################################################

    def begin_macro(self, name):
        """This begins a macro by creating an empty command with the given
        'name'.  All subsequent calls to 'push()' create commands that will be
        children of the empty command until the next call to 'end_macro()'.
        Macros may be nested.  The stack is disabled (ie. nothing can be undone
        or redone) while a macro is being created (ie. while there is an
        outstanding 'end_macro()' call).
        """

        command = _MacroCommand(name=name)
        self.push(command)
        self._macro_stack.append(command)

    def clear(self):
        """This clears the stack, without undoing or redoing any commands, and
        leaves the stack in a clean state.  It is typically used when all
        changes to the data have been abandoned.
        """

        self._index = -1
        self._stack = []
        self._macro_stack = []

        self.undo_manager.stack_updated = self

    def end_macro(self):
        """ This ends a macro. """

        try:
            self._macro_stack.pop()
        except IndexError:
            pass

    def push(self, command):
        """This executes a command and saves it on the command stack so that
        it can be subsequently undone and redone.  'command' is an instance
        that implements the ICommand interface.  Its 'do()' method is called
        to execute the command.  If any value is returned by 'do()' then it is
        returned by 'push()'.
        """

        # See if the command can be merged with the previous one.
        if len(self._macro_stack) == 0:
            if self._index >= 0 and not self._stack[self._index].clean:
                merged = self._stack[self._index].command.merge(command)
            else:
                merged = False
        else:
            merged = self._macro_stack[-1].merge(command)

        # Increment the global sequence number.
        if not merged:
            self.undo_manager.sequence_nr += 1

        # Execute the command.
        result = command.do()

        # Update the stack state for a merged command.
        if merged:
            if len(self._macro_stack) == 0:
                # If not in macro mode, remove everything after the current
                # command from the stack.
                del self._stack[self._index+1:]
            self.undo_manager.stack_updated = self
            return result

        # Only update the command stack if there is no current macro.
        if len(self._macro_stack) == 0:
            # Remove everything on the stack after the last command that was
            # done.
            self._index += 1
            del self._stack[self._index:]

            # Create a new stack entry and add it to the stack.
            entry = _StackEntry(
                command=command, sequence_nr=self.undo_manager.sequence_nr
            )

            self._stack.append(entry)
            self.undo_manager.stack_updated = self
        else:
            # Add the command to the parent macro command.
            self._macro_stack[-1].macro_commands.append(command)

        return result

    def redo(self, sequence_nr=0):
        """If 'sequence_nr' is 0 then the last command that was undone is
        redone and any result returned.  Otherwise commands are redone up to
        and including the given 'sequence_nr' and any result of the last of
        these is returned.
        """

        # Make sure a redo is valid in the current context.
        if self.redo_name == "":
            return None

        if sequence_nr == 0:
            result = self._redo_one()
        else:
            result = None

            while self._index + 1 < len(self._stack):
                if self._stack[self._index + 1].sequence_nr > sequence_nr:
                    break

                result = self._redo_one()

        self.undo_manager.stack_updated = self

        return result

    def undo(self, sequence_nr=0):
        """If 'sequence_nr' is 0 then the last command is undone.  Otherwise
        commands are undone up to and including the given 'sequence_nr'.
        """

        # Make sure an undo is valid in the current context.
        if self.undo_name == "":
            return

        if sequence_nr == 0:
            self._undo_one()
        else:
            while self._index >= 0:
                if self._stack[self._index].sequence_nr <= sequence_nr:
                    break

                self._undo_one()

        self.undo_manager.stack_updated = self

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _redo_one(self):
        """ Redo the command at the current index and return the result. """

        self._index += 1
        entry = self._stack[self._index]

        return entry.command.redo()

    def _undo_one(self):
        """ Undo the command at the current index. """

        entry = self._stack[self._index]
        self._index -= 1

        entry.command.undo()

    def _get_clean(self):
        """ Get the clean state of the stack. """

        if self._index >= 0:
            clean = self._stack[self._index].clean
        else:
            clean = True

        return clean

    def _set_clean(self, clean):
        """ Set the clean state of the stack. """

        if self._index >= 0:
            self._stack[self._index].clean = clean

    def _get_redo_name(self):
        """ Get the name of the redo command, if any. """

        redo_name = ""

        if len(self._macro_stack) == 0 and self._index + 1 < len(self._stack):
            redo_name = self._stack[self._index + 1].command.name.replace(
                "&", ""
            )

        return redo_name

    def _get_undo_name(self):
        """ Get the name of the undo command, if any. """

        undo_name = ""

        if len(self._macro_stack) == 0 and self._index >= 0:
            command = self._stack[self._index].command
            undo_name = command.name.replace("&", "")

        return undo_name
