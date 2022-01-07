# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Grid example.

This is currently only supported by the WxPython toolkit.
"""
import os

from traits.api import Float, Str
from traits.observation.api import match

from pyface.api import GUI, PythonShell, SplitApplicationWindow
from pyface.ui.wx.grid.api import (
    Grid,
    TraitGridModel,
    GridRow,
    GridColumn,
    TraitGridColumn,
)

from file_tree import FileTree


class MainWindow(SplitApplicationWindow):
    """ The main application window. """

    # 'SplitApplicationWindow' interface -----------------------------------

    # The ratio of the size of the left/top pane to the right/bottom pane.
    ratio = Float(0.3)

    # The direction in which the window is split.
    direction = Str("vertical")

    # The data used to create the SimpleGridModel
    data = [
        ["bob", 1, True, Float],
        ["sarah", 45, True, Str],
        ["jonas", -3, False, direction],
    ]

    rows = [
        GridRow(name="Row 1"),
        GridRow(name="Row 2"),
        GridRow(name="Row 3"),
    ]

    cols = [
        GridColumn(name="Name"),
        GridColumn(name="Index", read_only=True),
        GridColumn(name="Veracity"),
        GridColumn(name="Object"),
    ]

    # The data used to create the TraitGridModel
    trait_data = [
        GridRow(name="Bob", index=1, veracity=True, object=Float),
        GridRow(name="Sarah", index=45, veracity=True, object=Str),
        GridRow(name="Jonas", index=-3, veracity=False, object=direction),
    ]

    trait_col = [
        TraitGridColumn(name="name", label="Name"),
        TraitGridColumn(name="index", label="Index", read_only=True),
        TraitGridColumn(name="veracity", label="Veracity"),
        TraitGridColumn(name="object", label="Object"),
    ]

    # ------------------------------------------------------------------------
    # Protected 'SplitApplicationWindow' interface.
    # ------------------------------------------------------------------------

    def _create_lhs(self, parent):
        """ Creates the left hand side or top depending on the split. """

        self._model = model = TraitGridModel(
            data=self.trait_data, columns=self.trait_col, row_name_trait="name"
        )

        self._grid = grid = Grid(parent, model=model)

        self._grid.observe(
            self._on_grid_anytrait_changed,
            match(lambda name, ctrait: True)  # listen to all traits
        )

        return grid.control

    def _create_rhs(self, parent):
        """ Creates the right hand side or bottom depending on the split. """

        widget = self._grid

        self._python_shell = PythonShell(parent)
        self._python_shell.bind("widget", widget)
        self._python_shell.bind("w", widget)

        return self._python_shell.control

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _create_content(self, parent):
        """ Create some context for an expandable panel. """

        tree = FileTree(parent, root=os.path.abspath(os.curdir))

        return tree.control

    # Trait event handlers -------------------------------------------------

    def _on_grid_anytrait_changed(self, event):
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
