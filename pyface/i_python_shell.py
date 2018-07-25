#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
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
#------------------------------------------------------------------------------
""" The interface for an interactive Python shell. """

# Enthought library imports.
from traits.api import Event

# Local imports.
from pyface.key_pressed_event import KeyPressedEvent
from pyface.i_widget import IWidget


class IPythonShell(IWidget):
    """ The interface for an interactive Python shell. """

    #### 'IPythonShell' interface #############################################

    #: A command has been executed.
    command_executed = Event

    #: A key has been pressed.
    key_pressed = Event(KeyPressedEvent)

    ###########################################################################
    # 'IPythonShell' interface.
    ###########################################################################

    def interpreter(self):
        """ Get the shell's interpreter

        Returns
        -------
        interpreter : InteractiveInterpreter instance
            Returns the InteractiveInterpreter instance.
        """

    def bind(self, name, value):
        """ Binds a name to a value in the interpreter's namespace.

        Parameters
        ----------
        name : str
            The python idetifier to bind the value to.
        value : any
            The python object to be bound into the interpreter's namespace.
        """

    def execute_command(self, command, hidden=True):
        """ Execute a command in the interpreter.

        Parameters
        ----------
        command : str
            A Python command to execute.
        hidden : bool
            If 'hidden' is True then nothing is shown in the shell - not even
            a blank line.
        """

    def execute_file(self, path, hidden=True):
        """ Execute a file in the interpeter.

        Parameters
        ----------
        path : str
            The path to the Python file to execute.
        hidden : bool
            If 'hidden' is True then nothing is shown in the shell - not even
            a blank line.
        """

    def get_history(self):
        """ Return the current command history and index.

        Returns
        -------
        history : list of str
            The list of commands in the new history.
        history_index : int from 0 to len(history)
            The current item in the command history navigation.
        """

    def set_history(self, history, history_index):
        """ Replace the current command history and index with new ones.

        Parameters
        ----------
        history : list of str
            The list of commands in the new history.
        history_index : int
            The current item in the command history navigation.
        """


class MPythonShell(object):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IPythonShell interface.

    Implements: bind(), _on_command_executed()
    """

    ###########################################################################
    # 'IPythonShell' interface.
    ###########################################################################

    def bind(self, name, value):
        """ Binds a name to a value in the interpreter's namespace.

        Parameters
        ----------
        name : str
            The python idetifier to bind the value to.
        value : any
            The python object to be bound into the interpreter's namespace.
        """
        self.interpreter().locals[name] = value

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _on_command_executed(self):
        """ Called when a command has been executed in the shell. """

        self.command_executed = self
