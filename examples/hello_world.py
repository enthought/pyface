# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Hello world example. """


from pyface.api import ApplicationWindow, GUI, HeadingText


class MainWindow(ApplicationWindow):
    """ The main application window. """

    # --------------------------------------------------------------------------
    # 'IWindow' interface
    # --------------------------------------------------------------------------

    # The window title.
    title = "Hello World"

    # --------------------------------------------------------------------------
    # 'IApplicationWindow' interface.
    # --------------------------------------------------------------------------

    def _create_contents(self, parent):
        """ Create the editor. """

        self._label = HeadingText(parent, text="Hello World")

        return self._label.control


def main():
    # Create the GUI.
    gui = GUI()

    # Create and open the main window.
    window = MainWindow()
    window.open()

    # Start the GUI event loop!
    gui.start_event_loop()


# Application entry point.
if __name__ == "__main__":
    main()
