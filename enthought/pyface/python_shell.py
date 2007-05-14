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
""" An interactive Python shell. """

# Enthought library imports.
from enthought.pyface.api import KeyPressedEvent
from enthought.traits.api import Event

# Local imports.
from widget import Widget


class PythonShell(Widget):
    """ An interactive Python shell. """

    __tko__ = 'PythonShell'

    # fixme: Hack for demo.
    command_executed = Event

    #### 'PythonShell' interface ##############################################

    # A key has been pressed.
    key_pressed = Event(KeyPressedEvent)

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, parent, **traits):
        """ Creates a new pager. """

        # Base class constructor.
        super(PythonShell, self).__init__(**traits)

        # Create the toolkit-specific control that represents the widget.
        self.control = self._create_control(parent)

        # Set up to be notified whenever a Python statement is executed:
        self._tk_pythonshell_set_execute_callback(self._on_command_executed)

        return

    ###########################################################################
    # 'PythonShell' interface.
    ###########################################################################

    def interpreter(self):
        """ Returns the code.InteractiveInterpreter instance. """

        return self._tk_pythonshell_get_interpreter()

    def bind(self, name, value):
        """ Binds a name to a value in the interpreter's namespace. """

        self.interpreter().locals[name] = value

        return

    def execute_command(self, command, hidden=True):
        """ Execute a command in the interpreter.

        If 'hidden' is True then nothing is shown in the shell - not even
        a blank line.
        """

        self._tk_pythonshell_execute(command, hidden)

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    ##### trait event handlers ################################################

    def _on_command_executed(self):
        """ Called when a command has been executed in the shell. """

        self.command_executed = self

        return

    ###########################################################################
    # 'PythonShell' toolkit interface.
    ###########################################################################

    def _tk_pythonshell_get_interpreter(self):
        """ Return a reference to the InteractiveInterpreter instance.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_pythonshell_set_execute_callback(self, cb):
        """ Set the callback to be invoked when a command is executed.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_pythonshell_execute(self, command, hidden):
        """ Execute a command in the interpreter.

        This must be reimplemented.
        """

        raise NotImplementedError

#### EOF ######################################################################
