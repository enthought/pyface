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
from pyface.api import ApplicationWindow, GUI
from pyface.action.api import Action, MenuManager, MenuBarManager
from pyface.action.api import StatusBarManager, ToolBarManager, Group


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
        self.exit_action = exit_action
        
        # Test action to toggle visibility of exit action and some action groups
        test_action = Action(name='&Toggle', on_perform=self.toggle)

        # Add a menu bar.
        self.menu_bar_manager = MenuBarManager(
            MenuManager(exit_action, name='&File')
        )

        # Add some tool bars, with the first one subdivided into action groups
        self.tool_bar_managers = [
            ToolBarManager(
                Group(exit_action, exit_action, id='a'),
                Group(id='b'),  # empty, so will remain hidden
                Group(exit_action, exit_action, id='c'),
                Group(exit_action, test_action, exit_action, id='d'),
                name='Tool Bar 1', show_tool_names=False
            ),

            ToolBarManager(
                exit_action, name='Tool Bar 2', show_tool_names=False
            ),

            ToolBarManager(
                test_action, name='Tool Bar 3', show_tool_names=False
            ),
        ]

        # Add a status bar.
        self.status_bar_manager = StatusBarManager()
        self.status_bar_manager.message = 'Example application window'

        return
    
    def toggle(self):
        """ Toggle the visibility of the exit action and of the first 3 groups
        in the first toolbar, which contain only exit actions.
        """
        visible = not self.exit_action.visible
        self.exit_action.visible = visible
        for group in self.tool_bar_managers[0].groups[:-1]:
            group.visible = visible


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
