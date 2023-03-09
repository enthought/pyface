# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
"""
Module defining a simple Python shell task.

This task provides a view with a simple Python shell.  This shouldn't be
confused with a more full-featured shell, such as those provided by IPython.
"""


import logging


from traits.api import Str, List, Dict, Instance
from pyface.api import PythonShell, FileDialog, OK
from pyface.action.schema.api import SMenu, SMenuBar
from pyface.tasks.api import Task, TaskPane
from pyface.tasks.action.api import TaskAction

# set up logging
logger = logging.getLogger()


class PythonShellPane(TaskPane):
    """ A Tasks Pane containing a Pyface PythonShell
    """

    id = "pyface.tasks.contrib.python_shell.pane"
    name = "Python Shell"

    editor = Instance(PythonShell)

    bindings = List(Dict)
    commands = List(Str)

    def create(self, parent):
        """ Create the python shell task pane

        This wraps the standard pyface PythonShell
        """
        logger.debug("PythonShellPane: creating python shell pane")
        self.editor = PythonShell(parent)
        self.control = self.editor.control

        # bind namespace
        logger.debug("PythonShellPane: binding variables")
        for binding in self.bindings:
            for name, value in binding.items():
                self.editor.bind(name, value)

        # execute commands
        logger.debug("PythonShellPane: executing startup commands")
        for command in self.commands:
            self.editor.execute_command(command)

        logger.debug("PythonShellPane: created")

    def destroy(self):
        """ Destroy the python shell task pane
        """
        if self.editor is not None:
            logger.debug("PythonShellPane: destroying python shell pane")
            self.editor.destroy()
            self.editor = None
        logger.debug("PythonShellPane: destroyed")
        super().destroy()


class PythonShellTask(Task):
    """
    A task which provides a simple Python Shell to the user.
    """

    # Task Interface

    id = "pyface.tasks.contrib.python_shell"
    name = "Python Shell"

    # The list of bindings for the shell
    bindings = List(Dict)

    # The list of commands to run on shell startup
    commands = List(Str)

    # the IPythonShell instance that we are interacting with
    pane = Instance(PythonShellPane)

    # Task Interface

    menu_bar = SMenuBar(
        SMenu(
            TaskAction(name="Open...", method="open", accelerator="Ctrl+O"),
            id="File",
            name="&File",
        ),
        SMenu(id="View", name="&View"),
    )

    def create_central_pane(self):
        """ Create a view pane with a Python shell
        """
        logger.debug("Creating Python shell pane in central pane")
        self.pane = PythonShellPane(
            bindings=self.bindings, commands=self.commands
        )
        return self.pane

    # PythonShellTask API

    def open(self):
        """ Shows a dialog to open a file.
        """
        logger.debug("PythonShellTask: opening file")
        dialog = FileDialog(parent=self.window.control, wildcard="*.py")
        if dialog.open() == OK:
            self._open_file(dialog.path)

    # Private API

    def _open_file(self, path):
        """ Execute the selected file in the editor's interpreter
        """
        logger.debug('PythonShellTask: executing file "%s"' % path)
        self.pane.editor.execute_file(path)
