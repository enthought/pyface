# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Dialog example. """


from pyface.api import (
    ApplicationWindow,
    GUI,
    YES,
    choose_one,
    confirm,
    error,
    information,
    warning,
)
from pyface.action.api import Action, MenuBarManager, MenuManager


class MainWindow(ApplicationWindow):
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
                Action(name="E&xit", on_perform=self._on_exit), name="&File"
            )
        )

        return

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _on_exit(self):
        """ Called when the exit action is invoked. """

        parent = self.control

        print(choose_one(parent, "Make a choice", ["one", "two", "three"]))

        information(parent, "Going...")
        warning(parent, "Going......")
        error(parent, "Gone!")

        if confirm(parent, "Should I exit?") == YES:
            self.close()


# Application entry point.
if __name__ == "__main__":
    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    # Create and open the main window.
    window = MainWindow()
    window.open()

    # Start the GUI event loop!
    gui.start_event_loop()
