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
from traits.api import Constant

from pyface.api import (
    ApplicationWindow, FileDialog, GUI, OK, PythonEditor
)
from pyface.toolkit import toolkit_object
from pyface.action.api import (
    Action, ActionEvent, Group, MenuManager, MenuBarManager, ToolBarManager
)


class IntFieldAction(Action):
    """ A widget action containing an integer textbox

    This shows one way of creating a widget Action by overriding the
    create_control method and overloading the `perform` methods to pass
    the entered value to a handler.
    """

    style = Constant("widget")

    def create_control(self, parent):
        if toolkit_object.toolkit == 'wx':
            import wx
            from wx.lib.intctrl import IntCtrl
            control = IntCtrl(
                parent,
                value=1,
                style=wx.TE_PROCESS_ENTER
            )

            def handle_enter(event):
                value = control.GetValue()
                action_event = ActionEvent(value=value)
                self.perform(action_event)

            control.Bind(wx.EVT_TEXT_ENTER, handle_enter)

        elif toolkit_object.toolkit == 'qt4':
            from pyface.qt import QtGui
            control = QtGui.QLineEdit(parent)
            control.setText("1")
            control.setValidator(QtGui.QIntValidator())

            def handle_enter():
                value = int(control.text())
                action_event = ActionEvent(value=value)
                self.perform(action_event)

            control.returnPressed.connect(handle_enter)

        else:
            control = None

        return control

    def perform(self, event):
        if self.on_perform is not None:
            self.on_perform(event.value)


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
                        name="Show Line Numbers",
                        style='toggle',
                        on_perform=self.on_show_line_numbers,
                        checked=True,
                    ),
                    IntFieldAction(
                        name="Go to line",
                        on_perform=self.on_go_to_line,
                    )
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

    def on_show_line_numbers(self):
        self._editor.show_line_numbers = not self._editor.show_line_numbers

    def on_go_to_line(self, line_number):
        self._editor.select_line(line_number+1)


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
