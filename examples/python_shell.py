# (C) Copyright 2005-2025 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Python shell example. """


from pyface.api import ApplicationWindow, GUI, PythonShell
from pyface.i_python_shell import IPythonShell
from traits.api import Instance


class MainWindow(ApplicationWindow):
    """ The main application window. """

    #: The PythonShell that forms the contents of the window
    _shell = Instance(IPythonShell, allow_none=False)

    # 'IWindow' interface --------------------------------------------------

    # The size of the window.
    size = (640, 480)

    # The window title.
    title = "Python"

    # ------------------------------------------------------------------------
    # Protected 'IApplication' interface.
    # ------------------------------------------------------------------------

    def _create_contents(self, parent):
        """ Create the editor. """
        self._shell.create(parent)
        return self._shell.control

    def destroy(self):
        self._shell.destroy()
        super().destroy()

    def __shell_default(self):
        return PythonShell()


# Application entry point.
if __name__ == "__main__":
    # Create the GUI.
    gui = GUI()

    # Create and open the main window.
    window = MainWindow()
    window.open()

    # Start the GUI event loop!
    gui.start_event_loop()
