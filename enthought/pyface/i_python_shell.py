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

# Standard library imports.
import os
import types
import sys

# Enthought library imports.
from enthought.traits.api import Event

# Local imports.
from key_pressed_event import KeyPressedEvent
from i_widget import IWidget


class IPythonShell(IWidget):
    """ The interface for an interactive Python shell. """

    #### 'IPythonShell' interface #############################################

    # A command has been executed.
    command_executed = Event

    # A key has been pressed.
    key_pressed = Event(KeyPressedEvent)

    ###########################################################################
    # 'IPythonShell' interface.
    ###########################################################################

    def interpreter(self):
        """ Returns the code.InteractiveInterpreter instance. """

    def bind(self, name, value):
        """ Binds a name to a value in the interpreter's namespace. """

    def execute_command(self, command, hidden=True):
        """ Execute a command in the interpreter.

        If 'hidden' is True then nothing is shown in the shell - not even
        a blank line.
        """

    def execute_file(self, path, hidden=True):
        """ Execute a file in the interpeter.

        If 'hidden' is True then nothing is shown in the shell - not even
        a blank line.
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
        """ Binds a name to a value in the interpreter's namespace. """

        self.interpreter().locals[name] = value

    def execute_file(self, path, hidden=True):
        """ Execute a file in the interpeter.

        If 'hidden' is True then nothing is shown in the shell - not even
        a blank line.
        """
        # Note: The code in this function is largely ripped from IPython's
        #       Magic.py, FakeModule.py, and iplib.py.

        filename = os.path.basename(path)

        # Run in a fresh, empty namespace
        main_mod = types.ModuleType('__main__')
        prog_ns = main_mod.__dict__
        prog_ns['__file__'] = filename
        prog_ns['__nonzero__'] = lambda: True

        # Make sure that the running script gets a proper sys.argv as if it
        # were run from a system shell.
        save_argv = sys.argv
        sys.argv = [ filename ]

        # Make sure that the running script thinks it is the main module
        save_main = sys.modules['__main__']
        sys.modules['__main__'] = main_mod

        # Redirect sys.std* to control or null
        old_stdin = sys.stdin
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        if hidden:
            sys.stdin = sys.stdout = sys.stderr = _NullIO()
        else:
            sys.stdin = sys.stdout = sys.stderr = self.control

        # Execute the file
        try:
            if not hidden:
                self._set_input_buffer('# Executing "%s"' % path)
                self.control.write('\n')

            if sys.platform == 'win32' and sys.version_info < (2,5,1):
                # Work around a bug in Python for Windows. For details, see:
                # http://projects.scipy.org/ipython/ipython/ticket/123
                exec file(path) in prog_ns, prog_ns
            else:
                execfile(path, prog_ns, prog_ns)

            if not hidden:
                self._new_prompt()
        finally:
            # Ensure key global stuctures are restored
            sys.argv = save_argv
            sys.modules['__main__'] = save_main
            sys.stdin = old_stdin
            sys.stdout = old_stderr
            sys.stderr = old_stdout

        # Update the interpreter with the new namespace
        del prog_ns['__name__']
        del prog_ns['__file__']
        del prog_ns['__nonzero__']
        self.interpreter().locals.update(prog_ns)

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _on_command_executed(self):
        """ Called when a command has been executed in the shell. """

        self.command_executed = self

    def _new_prompt(self):
        """ Make a new prompt. Must be implemented if using the default
        implementation of execute_file. """

        raise NotImplementedError

    def _set_input_buffer(self, command):
        """ Set the input area text to 'command'. Must be implemented if using
        the default implementation of execute_file. """

        raise NotImplementedError


class _NullIO:
    """ A portable /dev/null for use with MPythonShell.execute_file.
    """
    def tell(self): return 0
    def read(self, n = -1): return ""
    def readline(self, length = None): return ""
    def readlines(self): return []
    def write(self, s): pass
    def writelines(self, list): pass
    def isatty(self): return 0
    def flush(self): pass
    def close(self): pass
    def seek(self, pos, mode = 0): pass

#### EOF ######################################################################
