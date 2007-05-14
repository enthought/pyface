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
""" A top-level application window. """


# Enthought library imports.
from enthought.traits.api import Instance, Int, Str

# Local imports.
from action.api import MenuBarManager, StatusBarManager, ToolBarManager
from image_resource import ImageResource
from window import Window


class ApplicationWindow(Window):
    """ A top-level application window.
    
    The application window has support for a menu bar, tool bar and a status
    bar (all of which are optional).

    Usage: Create a sub-class of this class and override the protected
    '_create_contents' method.
    """

    __tko__ = 'ApplicationWindow'

    #### 'Window' interface ###################################################

    # The size of the window.
    size = (800, 600)
    
    # The window title.
    title = Str('Pyface')

    #### 'ApplicationWindow' interface ########################################

    # The window icon.  The default is toolkit specific.
    icon = Instance(ImageResource)

    # The menu bar manager (None iff there is no menu bar).
    menu_bar_manager = Instance(MenuBarManager)

    # The status bar manager (None iff there is no status bar).
    status_bar_manager = Instance(StatusBarManager)

    # The tool bar manager (None iff there is no tool bar).
    tool_bar_manager = Instance(ToolBarManager)
    
    ###########################################################################
    # Protected 'Window' interface.
    ###########################################################################

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """

        # FIXME v3: This should probably invoke the superclass method rather
        # than the toolkit method.  It's done this way at the moment to exactly
        # replicate the v2 behaviour.
        control = self._tk_window_create(parent)

        # Create the 'trim' widgets (menu, tool and status bars etc).
        self._create_trim_widgets(control)

        # FIXME v3: What's this for? To create a circular reference?
        control._pyface_reference = self

        return control
    
    ###########################################################################
    # Protected 'ApplicationWindow' interface.
    ###########################################################################

    # FIXME v3: The parent argument is always self.control.
    def _create_trim_widgets(self, parent):
        """ Creates the 'trim' widgets (the widgets around the window).

        Currently these are the menu, tool and status bars.
        """

        # All of these are optional.
        self._set_window_icon(parent)
        self._create_menu_bar(parent)
        self._create_tool_bar(parent)
        self._create_status_bar(parent)
        
        return

    def _set_window_icon(self, parent):
        """ Sets the window icon (if required). """

        self._tk_applicationwindow_set_icon(parent, self.icon)

        return
    
    def _create_menu_bar(self, parent):
        """ Creates the menu bar (if required). """
        
        if self.menu_bar_manager is not None:
            menu_bar = self.menu_bar_manager.create_menu_bar(parent)
            self._tk_applicationwindow_set_menu_bar(parent, menu_bar)

        return
    
    def _create_tool_bar(self, parent):
        """ Creates the tool bar (if required). """
        
        if self.tool_bar_manager is not None:
            tool_bar = self.tool_bar_manager.create_tool_bar(parent)
            self._tk_applicationwindow_set_tool_bar(parent, tool_bar)

        return
    
    def _create_status_bar(self, parent):
        """ Creates the status bar (if required). """
        
        if self.status_bar_manager is not None:
            status_bar = self.status_bar_manager.create_status_bar(parent)
            self._tk_applicationwindow_set_status_bar(parent, status_bar)

        return

    ###########################################################################
    # 'ApplicationWindow' toolkit interface.
    ###########################################################################

    def _tk_applicationwindow_set_icon(self, control, icon):
        """ Sets the window icon.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_applicationwindow_set_menu_bar(self, control, menu_bar):
        """ Sets the menu bar.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_applicationwindow_set_status_bar(self, control, status_bar):
        """ Sets the status bar.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_applicationwindow_set_tool_bar(self, control, tool_bar):
        """ Sets the tool bar.

        This must be reimplemented.
        """

        raise NotImplementedError
    
#### EOF ######################################################################
