#------------------------------------------------------------------------------
#
#  Copyright (c) 2009, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in enthought/LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
#------------------------------------------------------------------------------
""" Python shell example. """

# Enthought library imports.
from pyface.api import ApplicationWindow, GUI, PythonShell
from pyface.action.api import Action, MenuManager, MenuBarManager


class MainWindow(ApplicationWindow):
    """ The main application window. """

    #### 'IWindow' interface ##################################################

    # The size of the window.
    size = (640, 480)

    # The window title.
    title = 'Python'

    ###########################################################################
    # Protected 'IApplication' interface.
    ###########################################################################

    def _create_contents(self, parent):
        """ Create the editor. """

        self._shell = PythonShell(parent)

        return self._shell.control


# Application entry point.
if __name__ == '__main__':
    # Create the GUI.
    gui = GUI()

    # Create and open the main window.
    window = MainWindow()
    window.open()

    # Start the GUI event loop!
    gui.start_event_loop()

##### EOF #####################################################################
