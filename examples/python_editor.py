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

from __future__ import print_function, unicode_literals

from pyface.api import (
    ApplicationWindow, FileDialog, GUI, OK, PythonEditor
)
from pyface.action.api import (
    Action, FieldAction, Group, MenuManager, MenuBarManager,
    ToolBarManager
)
from pyface.fields.api import ComboField
from pyface.toolkit import toolkit_object


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

        # Add a tool bar if we are using qt4 - wx has layout issues
        if toolkit_object.toolkit == 'qt4':
            from pygments.styles import STYLE_MAP
            styles = list(STYLE_MAP)

            self.tool_bar_manager = ToolBarManager(
                Group(
                    Action(
                        name='Open...',
                        on_perform=self.on_open_file
                    ),
                    Action(
                        name='Save',
                        on_perform=self.on_save_file
                    ),
                    Action(
                        name='Close',
                        on_perform=self.close
                    ),
                    id='document_group',
                ),
                Group(
                    Action(
                        name="Lines",
                        style='toggle',
                        on_perform=self.on_show_line_numbers,
                        checked=True,
                    ),
                    FieldAction(
                        name='Style',
                        field_type=ComboField,
                        field_defaults={
                            'values': styles,
                            'value': 'default',
                            'tooltip': 'Style',
                        },
                        on_perform=self.on_style_changed,
                    ),
                )
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
            dlg = FileDialog(parent=self.control, wildcard='*.py')

            if dlg.open() == OK:
                self._editor.path = dlg.path

    def on_save_file(self):
        """ Save the file. """

        if self.control:
            try:
                self._editor.save()
            except IOError:
                # If you are trying to save to a file that doesn't exist,
                # open up a FileDialog with a 'save as' action.
                dlg = FileDialog(parent=self.control, action='save as',
                                 wildcard="*.py")
                if dlg.open() == OK:
                    self._editor.save(dlg.path)

    def on_show_line_numbers(self):
        self._editor.show_line_numbers = not self._editor.show_line_numbers

    def on_style_changed(self, value):
        from pygments.styles import get_style_by_name

        # XXX surface this to a proper API on the editor widget
        # XXX Qt backend only
        highlighter = self._editor.control.code.highlighter
        highlighter._style = get_style_by_name(value)
        highlighter._brushes = {}
        highlighter._formats = {}
        highlighter.rehighlight()


# Application entry point.
if __name__ == '__main__':
    # Create the GUI.
    gui = GUI()

    # Create and open the main window.
    window = MainWindow(size=(800, 600))
    window.open()

    # Start the GUI event loop!
    gui.start_event_loop()
