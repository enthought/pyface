# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" IPython widget example. """


from pyface.api import ApplicationWindow, GUI
from pyface.ipython_widget import IPythonWidget


class MainWindow(ApplicationWindow):
    """ The main application window. """

    # 'IWindow' interface --------------------------------------------------

    # The size of the window.
    size = (640, 480)

    # The window title.
    title = "IPython"

    # ------------------------------------------------------------------------
    # Protected 'IApplication' interface.
    # ------------------------------------------------------------------------

    def _create_contents(self, parent):
        """ Create the editor. """

        self._shell = IPythonWidget(parent)

        return self._shell.control


# Application entry point.
if __name__ == "__main__":
    # Create the GUI.
    gui = GUI()

    # Create and open the main window.
    window = MainWindow()
    window.open()

    # Start the GUI event loop!
    gui.start_event_loop()
