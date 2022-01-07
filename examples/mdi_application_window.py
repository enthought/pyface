# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Application window example.

This example only works with the WxPython toolkit.
"""

from pyface.api import MDIApplicationWindow, MDIWindowMenu, GUI
from pyface.action.api import Action, MenuManager, MenuBarManager


class MainWindow(MDIApplicationWindow):
    """ The main application window. """

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, **traits):
        """ Creates a new application window. """

        # Base class constructor.
        super().__init__(**traits)

        # Add a menu bar.
        self.menu_bar_manager = MenuBarManager(
            MenuManager(
                Action(name="E&xit", on_perform=self.close), name="&File"
            ),
            MDIWindowMenu(self),
        )

        # Set the size of the window
        self.size = (640, 480)

        return


# Application entry point.
if __name__ == "__main__":
    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    # Create and open the main window.
    window = MainWindow()
    window.open()

    # Add some child windows
    for i in range(2):
        child = window.create_child_window()
        child.Show()

    # Start the GUI event loop!
    gui.start_event_loop()
