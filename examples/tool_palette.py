# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Example of a Tool Palette. """


import wx

from pyface.api import ApplicationWindow, GUI, ImageResource
from pyface.action.api import Action, MenuManager, MenuBarManager

from pyface.action.api import ToolPaletteManager


class MainWindow(ApplicationWindow):
    """ The main application window. """

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, **traits):
        """ Creates a new application window. """

        # Base class constructor.
        super(MainWindow, self).__init__(**traits)

        # Add a menu bar.
        self.menu_bar_manager = MenuBarManager(
            MenuManager(
                Action(name="E&xit", on_perform=self.close), name="&File"
            )
        )

        return

    def _create_contents(self, parent):
        """ Creates the window contents. """

        actions = []
        for i in range(25):
            actions.append(
                Action(
                    name="Foo", style="radio", image=ImageResource("document")
                )
            )

        tool_palette = ToolPaletteManager(*actions)

        return tool_palette.create_tool_palette(parent).control


# Application entry point.
if __name__ == "__main__":
    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    # Create and open the main window.
    window = MainWindow()
    window.open()

    # Start the GUI event loop!
    gui.start_event_loop()
