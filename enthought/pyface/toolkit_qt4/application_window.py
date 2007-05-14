#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
# 
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

# Major package imports.
from PyQt4 import QtGui

# Enthought library imports.
from enthought.pyface.api import ImageResource


class ApplicationWindow_qt4(object):
    """ The ApplicationWindow monkey patch for Qt4. """

    ###########################################################################
    # 'Widget' toolkit interface.
    ###########################################################################

    def _tk_widget_destroy(self):
        """ Destroy the control. """

        self.control.deleteLater()

        # I'm not sure why this is needed as it should be handled by the
        # last-window-closed mechanism.
        QtGui.QApplication.instance().exit()

    ###########################################################################
    # 'Window' toolkit interface.
    ###########################################################################

    def _tk_window_create(self, parent):
        """ Create and return the toolkit specific control that represents the
        widget.
        """

        control = QtGui.QMainWindow(parent)
        control.setWindowTitle(self.title)

        if self.position != (-1, -1):
            control.move(*self.position)

        if self.size != (-1, -1):
            control.resize(*self.size)

        control.setDockNestingEnabled(True)

        return control

    ###########################################################################
    # 'ApplicationWindow' toolkit interface.
    ###########################################################################

    def _tk_applicationwindow_set_icon(self, control, icon):
        """ Sets the window icon. """

        if icon is None:
            icon = ImageResource('application.png')

        control.setWindowIcon(icon.create_icon())
    
    def _tk_applicationwindow_set_menu_bar(self, control, menu_bar):
        """ Sets the menu bar. """

        control.setMenuBar(menu_bar)

        # Make sure that the menu bar has a name so that state can be saved.
        if menu_bar.objectName().isEmpty():
            menu_bar.setObjectName('__menubar__')

    def _tk_applicationwindow_set_status_bar(self, control, status_bar):
        """ Sets the status bar. """

        control.setStatusBar(status_bar)

    def _tk_applicationwindow_set_tool_bar(self, control, tool_bar):
        """ Sets the tool bar. """
        
        control.addToolBar(tool_bar)

        # Make sure that the tool bar has a name so that state can be saved.
        if tool_bar.objectName().isEmpty():
            tool_bar.setObjectName('__toolbar__')
