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
""" Dialog example. """


# Standard library imports.
import os, sys

# Put the Enthought library on the Python path.
sys.path.append(os.path.abspath(r'..\..\..'))

# Enthought library imports.
from enthought.pyface.api import confirm, error, information, warning, YES
from enthought.pyface.api import ApplicationWindow, GUI
from enthought.pyface.action.api import Action, MenuBarManager, MenuManager


class MainWindow(ApplicationWindow):
    """ The main application window. """

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Creates a new application window. """

        # Base class constructor.
        super(MainWindow, self).__init__(**traits)

        # Add a menu bar.
        self.menu_bar_manager = MenuBarManager(
            MenuManager(
                Action(name='E&xit', on_perform=self._on_exit),
                name = '&File',
            )  
        )

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _on_exit(self):
        """ Called when the exit action is invoked. """

        parent = self.control
        
        information(parent, 'Going...')
        warning(parent, 'Going......')
        error(parent, 'Gone!')

        if confirm(parent, 'Should I exit?') == YES:
            self.close()

        return
    

# Application entry point.
if __name__ == '__main__':
    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    # Create and open the main window.
    window = MainWindow()
    window.open()

    # Start the GUI event loop!
    gui.start_event_loop()

##### EOF #####################################################################
