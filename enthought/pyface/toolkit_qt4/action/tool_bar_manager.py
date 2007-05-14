#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
# 
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

# Major package imports.
from PyQt4 import QtCore, QtGui


class ToolBarManager_qt4(object):
    """ The ToolBarManager monkey patch for Qt4. """

    ###########################################################################
    # 'ToolBarManager' toolkit interface.
    ###########################################################################

    def _tk_toolbarmanager_create_tool_bar(self, parent):
        """ Create a tool bar with the given parent. """

        # Create the control.
        tool_bar = QtGui.QToolBar(parent)

        tool_bar.setObjectName(self.id)

        if self.show_tool_names:
            tool_bar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        if self.orientation == 'horizontal':
            tool_bar.setOrientation(QtCore.Qt.Horizontal)
        else:
            tool_bar.setOrientation(QtCore.Qt.Vertical)

        # We would normally leave it to the current style to determine the icon
        # size.
        w, h = self.image_size
        tool_bar.setIconSize(QtCore.QSize(w, h))

        return tool_bar

    def _tk_toolbarmanager_add_separator(self, tool_bar):
        """ Add a separator to a toolbar. """

        tool_bar.addSeparator()
