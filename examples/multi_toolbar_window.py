# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Mulit-tool bar example.
    Note: This demo only works on the wx backend.
"""


import os, sys

# Put the Enthought library on the Python path.
sys.path.append(os.path.abspath(r"..\..\.."))

# FIXME: This is a hack to disable the AUI module which causes the example to
# not layout correctly.
try:
    import wx

    sys.modules["wx.aui"] = None
except:
    pass


from pyface.api import MultiToolbarWindow, GUI
from pyface.action.api import Action, MenuManager, MenuBarManager
from pyface.action.api import ToolBarManager


class MainWindow(MultiToolbarWindow):
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

        # Add a menu bar at each location.
        self.add_tool_bar(
            ToolBarManager(Action(name="Foo"), orientation="horizontal")
        )

        self.add_tool_bar(
            ToolBarManager(Action(name="Bar"), orientation="horizontal"),
            location="bottom",
        )

        self.add_tool_bar(
            ToolBarManager(Action(name="Baz"), orientation="vertical"),
            location="left",
        )

        self.add_tool_bar(
            ToolBarManager(Action(name="Buz"), orientation="vertical"),
            location="right",
        )

        return


# Application entry point.
if __name__ == "__main__":
    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    # Create and open the main window.
    window = MainWindow()
    window.open()

    # Start the GUI event loop.
    gui.start_event_loop()
