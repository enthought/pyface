# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Enthought pyface package component
"""


import builtins
import os
import sys
import types
import warnings


from wx.py.shell import Shell as PyShellBase
import wx


from traits.api import Event, provides


from traits.util.clean_strings import python_name
from pyface.wx.drag_and_drop import PythonDropTarget


from pyface.i_python_shell import IPythonShell, MPythonShell
from pyface.key_pressed_event import KeyPressedEvent
from .layout_widget import LayoutWidget


@provides(IPythonShell)
class PythonShell(MPythonShell, LayoutWidget):
    """ The toolkit specific implementation of a PythonShell.  See the
    IPythonShell interface for the API documentation.
    """

    # 'IPythonShell' interface ---------------------------------------------

    command_executed = Event()

    key_pressed = Event(KeyPressedEvent)

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, parent=None, **traits):
        """ Creates a new pager. """

        create = traits.pop("create", None)

        # Base class constructor.
        super().__init__(parent=parent, **traits)

        if create:
            # Create the widget's toolkit-specific control.
            self.create()
            warnings.warn(
                "automatic widget creation is deprecated and will be removed "
                "in a future Pyface version, code should not pass the create "
                "parameter and should instead call create() explicitly",
                DeprecationWarning,
                stacklevel=2,
            )
        elif create is not None:
            warnings.warn(
                "setting create=False is no longer required",
                DeprecationWarning,
                stacklevel=2,
            )

    # ------------------------------------------------------------------------
    # 'IPythonShell' interface.
    # ------------------------------------------------------------------------

    def interpreter(self):
        return self.control.interp

    def execute_command(self, command, hidden=True):
        if hidden:
            self.control.hidden_push(command)
        else:
            # Replace the edit area text with command, then run it:
            self.control.Execute(command)

    def execute_file(self, path, hidden=True):
        # Note: The code in this function is largely ripped from IPython's
        #       Magic.py, FakeModule.py, and iplib.py.

        filename = os.path.basename(path)

        # Run in a fresh, empty namespace
        main_mod = types.ModuleType("__main__")
        prog_ns = main_mod.__dict__
        prog_ns["__file__"] = filename
        prog_ns["__nonzero__"] = lambda: True

        # Make sure that the running script gets a proper sys.argv as if it
        # were run from a system shell.
        save_argv = sys.argv
        sys.argv = [filename]

        # Make sure that the running script thinks it is the main module
        save_main = sys.modules["__main__"]
        sys.modules["__main__"] = main_mod

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
                self.control.clearCommand()
                self.control.write('# Executing "%s"\n' % path)

            exec(open(path).read(), prog_ns, prog_ns)

            if not hidden:
                self.control.prompt()
        finally:
            # Ensure key global stuctures are restored
            sys.argv = save_argv
            sys.modules["__main__"] = save_main
            sys.stdin = old_stdin
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        # Update the interpreter with the new namespace
        del prog_ns["__name__"]
        del prog_ns["__file__"]
        del prog_ns["__nonzero__"]
        self.interpreter().locals.update(prog_ns)

    def get_history(self):
        """ Return the current command history and index.

        Returns
        -------
        history : list of str
            The list of commands in the new history.
        history_index : int from 0 to len(history)
            The current item in the command history navigation.
        """
        return self.control.history, self.control.historyIndex

    def set_history(self, history, history_index):
        """ Replace the current command history and index with new ones.

        Parameters
        ----------
        history : list of str
            The list of commands in the new history.
        history_index : int from 0 to len(history)
            The current item in the command history navigation.
        """
        if not 0 <= history_index <= len(history):
            history_index = len(history)
        self.control.history = list(history)
        self.control.historyIndex = history_index

    # ------------------------------------------------------------------------
    # 'IWidget' interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        shell = PyShell(parent, -1)

        # Listen for key press events.
        shell.Bind(wx.EVT_CHAR, self._wx_on_char)

        # Enable the shell as a drag and drop target.
        shell.SetDropTarget(PythonDropTarget(self))

        # Set up to be notified whenever a Python statement is executed:
        shell.handlers.append(self._on_command_executed)

        return shell

    # ------------------------------------------------------------------------
    # 'PythonDropTarget' handler interface.
    # ------------------------------------------------------------------------

    def on_drop(self, x, y, obj, default_drag_result):
        """ Called when a drop occurs on the shell. """

        # If we can't create a valid Python identifier for the name of an
        # object we use this instead.
        name = "dragged"

        if (
            hasattr(obj, "name")
            and isinstance(obj.name, str)
            and len(obj.name) > 0
        ):
            py_name = python_name(obj.name)

            # Make sure that the name is actually a valid Python identifier.
            try:
                if eval(py_name, {py_name: True}):
                    name = py_name

            except:
                pass

        self.control.interp.locals[name] = obj
        self.control.run(name)
        self.control.SetFocus()

        # We always copy into the shell since we don't want the data
        # removed from the source
        return wx.DragCopy

    def on_drag_over(self, x, y, obj, default_drag_result):
        """ Always returns wx.DragCopy to indicate we will be doing a copy."""
        return wx.DragCopy

    # ------------------------------------------------------------------------
    # Private handler interface.
    # ------------------------------------------------------------------------

    def _wx_on_char(self, event):
        """ Called whenever a change is made to the text of the document. """

        # This was originally in the python_shell plugin, but is toolkit
        # specific.
        if event.AltDown() and event.GetKeyCode() == 317:
            zoom = self.shell.control.GetZoom()
            if zoom != 20:
                self.control.SetZoom(zoom + 1)

        elif event.AltDown() and event.GetKeyCode() == 319:
            zoom = self.shell.control.GetZoom()
            if zoom != -10:
                self.control.SetZoom(zoom - 1)

        self.key_pressed = KeyPressedEvent(
            alt_down=event.AltDown() == 1,
            control_down=event.ControlDown() == 1,
            shift_down=event.ShiftDown() == 1,
            key_code=event.GetKeyCode(),
            event=event,
        )

        # Give other event handlers a chance.
        event.Skip()


class PyShell(PyShellBase):
    def __init__(
        self,
        parent,
        id=-1,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.CLIP_CHILDREN,
        introText="",
        locals=None,
        InterpClass=None,
        *args,
        **kwds
    ):
        self.handlers = []

        # save a reference to the original raw_input() function since
        # wx.py.shell dosent reassign it back to the original on destruction
        self.raw_input = input

        super().__init__(
            parent,
            id,
            pos,
            size,
            style,
            introText,
            locals,
            InterpClass,
            *args,
            **kwds
        )

    def hidden_push(self, command):
        """ Send a command to the interpreter for execution without adding
            output to the display.
        """
        wx.BeginBusyCursor()
        try:
            self.waiting = True
            self.more = self.interp.push(command)
            self.waiting = False
            if not self.more:
                self.addHistory(command.rstrip())
                for handler in self.handlers:
                    handler()
        finally:
            # This needs to be out here to make this works with
            # traits.util.refresh.refresh()
            wx.EndBusyCursor()

    def push(self, command):
        """Send command to the interpreter for execution."""
        self.write(os.linesep)
        self.hidden_push(command)
        self.prompt()

    def Destroy(self):
        """Cleanup before destroying the control...namely, return std I/O and
        the raw_input() function back to their rightful owners!
        """
        self.redirectStdout(False)
        self.redirectStderr(False)
        self.redirectStdin(False)
        builtins.raw_input = self.raw_input
        self.destroy()
        super().Destroy()


class _NullIO(object):
    """ A portable /dev/null for use with PythonShell.execute_file.
    """

    def tell(self):
        return 0

    def read(self, n=-1):
        return ""

    def readline(self, length=None):
        return ""

    def readlines(self):
        return []

    def write(self, s):
        pass

    def writelines(self, list):
        pass

    def isatty(self):
        return 0

    def flush(self):
        pass

    def close(self):
        pass

    def seek(self, pos, mode=0):
        pass
