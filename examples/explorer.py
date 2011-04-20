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
""" A file explorer example. """


# Standard library imports.
import os, sys

# Put the Enthought library on the Python path.
sys.path.append(os.path.abspath(r'..\..\..'))

# Enthought library imports.
from pyface.api import ApplicationWindow, GUI, PythonShell, SplashScreen
from pyface.api import SplitApplicationWindow, SplitPanel
from pyface.action.api import Action, Group, MenuBarManager, MenuManager
from pyface.action.api import Separator, StatusBarManager, ToolBarManager
from traits.api import Float, Str

# Local imports.
from file_filters import AllowOnlyFolders
from file_sorters import FileSorter
from file_table_viewer import FileTableViewer
from file_tree_viewer import FileTreeViewer


class ExampleAction(Action):
    """ An example action. """

    accelerator = Str('Ctrl-K')

    def perform(self):
        """ Performs the action. """

        print 'Performing', self.name

        return


class MainWindow(SplitApplicationWindow):
    """ The main application window. """

    #### 'SplitApplicationWindow' interface ###################################

    # The ratio of the size of the left/top pane to the right/bottom pane.
    ratio = Float(0.3)

    # The direction in which the panel is split.
    direction = Str('vertical')

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Creates a new window. """

        # Base class constructor.
        super(MainWindow, self).__init__(**traits)

        # Create the window's menu, tool and status bars.
        self._create_action_bars()

        return

    ###########################################################################
    # Protected 'SplitApplicationWindow' interface.
    ###########################################################################

    def _create_lhs(self, parent):
        """ Creates the left hand side or top depending on the style. """

        return self._create_file_tree(parent, os.path.abspath(os.curdir))

    def _create_rhs(self, parent):
        """ Creates the panel containing the selected preference page. """

        self._rhs = SplitPanel(
            parent    = parent,
            lhs       = self._create_file_table,
            rhs       = self._create_python_shell,
            direction = 'horizontal'
        )

        return self._rhs.control

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_action_bars(self):
        """ Creates the window's menu, tool and status bars. """

        # Common actions.
        highest = Action(name='Highest', style='radio')
        higher  = Action(name='Higher',  style='radio', checked=True)
        lower   = Action(name='Lower',   style='radio')
        lowest  = Action(name='Lowest',  style='radio')

        self._actions = [highest, higher, lower, lowest]

        # Menu bar.
        self.menu_bar_manager = MenuBarManager(
            MenuManager(
                ExampleAction(name='Foogle'),
                Separator(),
                highest,
                higher,
                lower,
                lowest,
                Separator(),
                Action(name='E&xit', on_perform=self.close),

                name = '&File',
            )
        )

        # Tool bar.
        self.tool_bar_manager = ToolBarManager(
            ExampleAction(name='Foo'),
            Separator(),
            ExampleAction(name='Bar'),
            Separator(),
            ExampleAction(name='Baz'),
            Separator(),
            highest,
            higher,
            lower,
            lowest
        )

        # Status bar.
        self.status_bar_manager = StatusBarManager()

        return

    def _create_file_tree(self, parent, dirname):
        """ Creates the file tree. """

        self._tree_viewer = tree_viewer = FileTreeViewer(
            parent,
            input   = os.path.abspath(os.curdir),
            filters = [AllowOnlyFolders()]
        )

        tree_viewer.on_trait_change(self._on_selection_changed, 'selection')

        return tree_viewer.control

    def _create_file_table(self, parent):
        """ Creates the file table. """

        self._table_viewer = table_viewer = FileTableViewer(
            parent,
            sorter             = FileSorter(),
            odd_row_background = "white"
        )

        return table_viewer.control

    def _create_python_shell(self, parent):
        """ Creates the Python shell. """

        self._python_shell = python_shell = PythonShell(parent)
        python_shell.bind('widget', self._tree_viewer)
        python_shell.bind('w', self._tree_viewer)
        python_shell.bind('window', self)
        python_shell.bind('actions', self._actions)

        return python_shell.control

    #### Trait event handlers #################################################

    def _on_selection_changed(self, selection):
        """ Called when the selection in the tree is changed. """

        if len(selection) > 0:
            self._table_viewer.input = selection[0]

        return


# Application entry point.
if __name__ == '__main__':
    # Create the GUI and put up a splash screen (this does NOT start the GUI
    # event loop).
    gui = GUI(splash_screen=SplashScreen())

    # Create and open the main window.
    window = MainWindow()
    window.open()

    # Start the GUI event loop.
    gui.start_event_loop()

##### EOF #####################################################################
