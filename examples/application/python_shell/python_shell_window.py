# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
"""
Example Python Shell Window
===========================

This is an example of an application window subclass that contains a Pyface
Python shell.  This can be used stand-alone, but is also suitable for use as
a window in a GUI application.
"""

import sys
import webbrowser

from pyface.api import (
    ApplicationWindow,
    FileDialog,
    ImageResource,
    OK,
    PythonShell,
    error,
)
from pyface.action.api import (
    Action,
    CloseWindowAction,
    Group,
    MenuBarManager,
    MenuManager,
    StatusBarManager,
    WindowAction,
)
from traits.api import Instance, Str

PYTHON_DOCS = "https://docs.python.org/{}.{}".format(*sys.version_info[:2])


class RunFileAction(WindowAction):
    """ Action that calls the do_run_file method of a PythonShellWindow """

    name = "Run File..."
    accelerator = "Ctrl+R"
    method = "do_run_file"
    window = Instance("PythonShellWindow")


class OpenURLAction(Action):
    """ An action that opens a web page in the system's default browser. """

    #: The URL to open.
    url = Str()

    def perform(self, event=None):
        """ Open a URL in a web browser. """
        try:
            webbrowser.open(self.url)
        except webbrowser.Error as exc:
            error(None, str(exc))


class PythonShellWindow(ApplicationWindow):
    """ An application window that displays a simple Python shell. """

    #: The title of the window.
    title = "Python Shell"

    #: The icon for the window.
    icon = ImageResource("python_icon")

    #: The Python shell widget to use.
    shell = Instance("pyface.i_python_shell.IPythonShell")

    def do_run_file(self):
        """ Run a file selected by the user. """
        dialog = FileDialog(wildcard=FileDialog.WILDCARD_PY)
        result = dialog.open()
        if result == OK:
            self.shell.execute_file(dialog.path)

    def _create_contents(self, parent):
        """ Create the shell widget. """
        self.shell = PythonShell(parent)
        return self.shell.control

    def _menu_bar_manager_default(self):
        menu_bar = MenuBarManager(
            MenuManager(
                Group(CloseWindowAction(window=self), id="close_group"),
                name="&File",
                id="File",
            ),
            MenuManager(
                Group(RunFileAction(window=self), id="run_group"),
                name="&Run",
                id="Run",
            ),
            MenuManager(
                Group(
                    OpenURLAction(
                        name="Python Documentation",
                        id="python_docs",
                        url=PYTHON_DOCS,
                    ),
                    id="documentation_group",
                ),
                name="&Help",
                id="Help",
            ),
        )
        return menu_bar

    def _status_bar_manager_default(self):
        return StatusBarManager()


if __name__ == "__main__":
    from pyface.api import GUI

    window = PythonShellWindow()
    window.open()
    GUI().start_event_loop()
