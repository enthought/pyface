# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Tree example. """


import os

from traits.api import Float, Str
from traits.observation.api import match

from pyface.api import GUI, PythonShell, SplitApplicationWindow

from file_tree import FileTree


class MainWindow(SplitApplicationWindow):
    """ The main application window. """

    # 'SplitApplicationWindow' interface -----------------------------------

    # The ratio of the size of the left/top pane to the right/bottom pane.
    ratio = Float(0.3)

    # The direction in which the window is split.
    direction = Str("vertical")

    # ------------------------------------------------------------------------
    # Protected 'SplitApplicationWindow' interface.
    # ------------------------------------------------------------------------

    def _create_lhs(self, parent):
        """ Creates the left hand side or top depending on the split. """

        self._tree = FileTree(parent, root=os.path.abspath(os.curdir))

        self._tree.observe(
            self._on_tree_anytrait_changed,
            match(lambda name, ctrait: True)  # listen to all traits
        )

        return self._tree.control

    def _create_rhs(self, parent):
        """ Creates the right hand side or bottom depending on the split. """

        self._python_shell = PythonShell(parent)
        self._python_shell.bind("widget", self._tree)
        self._python_shell.bind("w", self._tree)

        return self._python_shell.control

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    # Trait event handlers -------------------------------------------------

    def _on_tree_anytrait_changed(self, event):
        """ Called when any trait on the tree has changed. """

        print("trait", event.name, "value", event.new)

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
