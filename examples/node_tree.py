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
""" Node tree example. """


# Standard library imports.
import os, sys

# Put the Enthought library on the Python path.
sys.path.append(os.path.abspath(r'..\..\..'))

# Enthought library imports.
from pyface.api import GUI, PythonShell, SplitApplicationWindow
from traits.api import Float, Str

# Local imports.
from file_node_tree import node_manager
from pyface.tree.api import NodeTree, NodeTreeModel


class MainWindow(SplitApplicationWindow):
    """ The main application window. """

    #### 'SplitApplicationWindow' interface ###################################

    # The ratio of the size of the left/top pane to the right/bottom pane.
    ratio = Float(0.3)

    # The direction in which the window is split.
    direction = Str('vertical')

    ###########################################################################
    # Protected 'SplitApplicationWindow' interface.
    ###########################################################################

    def _create_lhs(self, parent):
        """ Creates the left hand side or top depending on the split. """

        model = NodeTreeModel(node_manager=node_manager)
        model.root = os.path.abspath(os.curdir)

        self._tree = NodeTree(parent, model=model)
        self._tree.on_trait_change(self._on_tree_anytrait_changed)

        return self._tree.control

    def _create_rhs(self, parent):
        """ Creates the right hand side or bottom depending on the split. """

        self._python_shell = PythonShell(parent)
        self._python_shell.bind('widget', self._tree)
        self._python_shell.bind('w', self._tree)

        return self._python_shell.control

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait event handlers #################################################

    def _on_tree_anytrait_changed(self, tree, trait_name, old, new):
        """ Called when any trait on the tree has changed. """

        print 'trait', trait_name, 'value', new

        return


# Application entry point.
if __name__ == '__main__':
    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    # Create and open the main window.
    window = MainWindow()
    window.open()

    # Start the GUI event loop.
    gui.start_event_loop()

##### EOF #####################################################################
