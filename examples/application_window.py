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
""" Application window example. """


# Enthought library imports.
from enthought.pyface.api import ApplicationWindow, GUI
from enthought.pyface.action.api import Action, MenuManager, MenuBarManager
from enthought.pyface.action.api import StatusBarManager, ToolBarManager


class MainWindow(ApplicationWindow):
    """ The main application window. """

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Creates a new application window. """

        # Base class constructor.
        super(MainWindow, self).__init__(**traits)

        # Create an action that exits the application.
        exit_action = Action(name='E&xit', on_perform=self.close)

        # Add a menu bar.
        self.menu_bar_manager = MenuBarManager(
            MenuManager(exit_action, name='&File')
        )

        # Add some tool bars.
        self.tool_bar_managers = [
            ToolBarManager(
                exit_action, name='Tool Bar 1', show_tool_names=False
            ),

            ToolBarManager(
                exit_action, name='Tool Bar 2', show_tool_names=False
            ),

            ToolBarManager(
                exit_action, name='Tool Bar 3', show_tool_names=False
            ),
        ]

        # Add a status bar.
        self.status_bar_manager = StatusBarManager()
        self.status_bar_manager.message = 'Example application window'
        
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
