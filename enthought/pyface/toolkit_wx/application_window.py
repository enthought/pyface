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

# Major package imports.
import wx

# Enthought library imports.
from enthought.pyface.api import ImageResource


class ApplicationWindow_wx(object):
    """ The ApplicationWindow monkey patch for wx. """

    ###########################################################################
    # 'Window' toolkit interface.
    ###########################################################################

    def _tk_window_create(self, parent):
        """ Create and return the toolkit specific control that represents the
        widget.
        """

        style = wx.DEFAULT_FRAME_STYLE | wx.FRAME_NO_WINDOW_MENU | wx.CLIP_CHILDREN

        return wx.Frame(parent, -1, self.title, style=style, size=self.size,
                pos=self.position)

    ###########################################################################
    # 'ApplicationWindow' toolkit interface.
    ###########################################################################

    def _tk_applicationwindow_set_icon(self, control, icon):
        """ Sets the window icon. """

        if icon is None:
            icon = ImageResource('application.ico')

        control.SetIcon(icon.create_icon())

        return
    
    def _tk_applicationwindow_set_menu_bar(self, control, menu_bar):
        """ Sets the menu bar. """

        control.SetMenuBar(menu_bar)

        return
    
    def _tk_applicationwindow_set_status_bar(self, control, status_bar):
        """ Sets the status bar. """
        
        control.SetStatusBar(status_bar)

        return

    def _tk_applicationwindow_set_tool_bar(self, control, tool_bar):
        """ Sets the tool bar. """
        
        control.SetToolBar(tool_bar)

        return
    
#### EOF ######################################################################
