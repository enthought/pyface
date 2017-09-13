from pyface.api import ApplicationWindow, FileDialog, OK, PythonShell
from pyface.action.api import WindowAction
from traits.api import Instance


class PythonShellWindow(ApplicationWindow):
    """ An application window that displays a simple Python shell. """

    #: The title of the window.
    title = "Python Shell"

    #: The Python shell widget to use.
    shell = Instance('pyface.i_python_shell.IPythonShell')

    def do_run_file(self):
        """ Run a file selected by the user. """
        dialog = FileDialog(
            wildcard=FileDialog.WILDCARD_PY
        )
        result = dialog.open()
        if result == OK:
            self.shell.execute_file(dialog.path)

    def _create_contents(self, parent):
        """ Create the shell widget. """
        self.shell = PythonShell(parent)
        return self.shell.control


class RunFileAction(WindowAction):
    """ Action that calls the do_run_file method of a PythonShellWindow """
    name = 'Run File...'
    accelerator = 'Ctrl+R'
    method = 'do_run_file'
    window = Instance(PythonShellWindow)
