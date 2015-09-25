#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Riverbank Computing Limited.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
""" Python editor example. """


# Enthought library imports.
from pyface.api import ApplicationWindow, FileDialog, GUI, OK, \
        PythonEditor
from pyface.action.api import Action, Group, MenuManager, MenuBarManager


class MainWindow(ApplicationWindow):
    """ The main application window. """

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Creates a new application window. """

        # Base class constructor.
        super(MainWindow, self).__init__(**traits)

        # Add a menu bar.
        self.menu_bar_manager = MenuBarManager(
            MenuManager(
                Group(
                    Action(
                        name='&Open...',
                        accelerator='Ctrl+O',
                        on_perform=self.on_open_file
                    ),
                    Action(
                        name='&Save',
                        accelerator='Ctrl+S',
                        on_perform=self.on_save_file
                    ),
                    id='document_group',
                ),
                Action(
                    name='&Close',
                    accelerator='Ctrl+W',
                    on_perform=self.close
                ),
                name='&File')
        )

    ###########################################################################
    # Protected 'IApplication' interface.
    ###########################################################################

    def _create_contents(self, parent):
        """ Create the editor. """

        self._editor = PythonEditor(parent)

        return self._editor.control

    ###########################################################################
    # Private interface.
    ###########################################################################

    def on_open_file(self):
        """ Open a new file. """

        if self.control:
            dlg = FileDialog(parent=self.control, wildcard="*.py")

            if dlg.open() == OK:
                self._editor.path = dlg.path

    def on_save_file(self):
        """ Save the file. """

        if self.control:
            try:
                self._editor.save()
            except IOError as e:
                # If you are trying to save to a file that doesn't exist,
                # open up a FileDialog with a 'save as' action.
                dlg = FileDialog(parent=self.control, action='save as', wildcard="*.py")
                if dlg.open() == OK:
                    self._editor.save(dlg.path)

# Application entry point.
if __name__ == '__main__':
    # Create the GUI.
    gui = GUI()

    # Create and open the main window.
    window = MainWindow()
    window.open()

    # Start the GUI event loop!
    gui.start_event_loop()

##### EOF #####################################################################
