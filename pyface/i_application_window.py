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
""" The interface of a top-level application window. """

# Enthought library imports.
from traits.api import Instance, List

# Local imports.
from pyface.action.api import MenuBarManager, StatusBarManager, ToolBarManager
from pyface.i_image_resource import IImageResource
from pyface.i_window import IWindow


class IApplicationWindow(IWindow):
    """ The interface for a top-level application window.

    The application window has support for a menu bar, tool bar and a status
    bar (all of which are optional).

    Usage
    -----

    Create a sub-class of this class and override the
    :py:meth:`._create_contents` method.
    """

    #### 'IApplicationWindow' interface #######################################

    #: The window icon.  The default is toolkit specific.
    icon = Instance(IImageResource)

    #: The menu bar manager (None iff there is no menu bar).
    menu_bar_manager = Instance(MenuBarManager)

    #: The status bar manager (None iff there is no status bar).
    status_bar_manager = Instance(StatusBarManager)

    #: The tool bar manager (None iff there is no tool bar).
    tool_bar_manager = Instance(ToolBarManager)

    #: If the underlying toolkit supports multiple toolbars, you can use this
    #: list instead of the single ToolBarManager instance above.
    tool_bar_managers = List(ToolBarManager)

    ###########################################################################
    # Protected 'IApplicationWindow' interface.
    ###########################################################################

    def _create_contents(self, parent):
        """ Create and return the window's contents.

        Parameters
        ----------
        parent : toolkit control
            The window's toolkit control to be used as the parent for
            widgets in the contents.

        Returns
        -------
        control : toolkit control
            A control to be used for contents of the window.
        """

    def _create_menu_bar(self, parent):
        """ Creates the menu bar (if required).

        Parameters
        ----------
        parent : toolkit control
            The window's toolkit control.
        """

    def _create_status_bar(self, parent):
        """ Creates the status bar (if required).

        Parameters
        ----------
        parent : toolkit control
            The window's toolkit control.
        """

    def _create_tool_bar(self, parent):
        """ Creates the tool bar (if required).

        Parameters
        ----------
        parent : toolkit control
            The window's toolkit control.
        """

    def _create_trim_widgets(self, parent):
        """ Creates the 'trim' widgets (the widgets around the window).

        Parameters
        ----------
        parent : toolkit control
            The window's toolkit control.
        """

    def _set_window_icon(self):
        """ Sets the window icon (if required). """


class MApplicationWindow(object):
    """ The mixin class that contains common code for toolkit specific
    implementations of the :py:class:`IApplicationWindow` interface.

    Implements: destroy(), _create_trim_widgets()
    """

    ###########################################################################
    # 'IWidget' interface.
    ###########################################################################

    def destroy(self):
        """ Destroy the control if it exists. """

        if self.menu_bar_manager is not None:
            self.menu_bar_manager.destroy()

        if self.tool_bar_manager is not None:
            self.tool_bar_manager.destroy()
        for tool_bar_manager in self.tool_bar_managers:
            tool_bar_manager.destroy()

        super(MApplicationWindow, self).destroy()

    ###########################################################################
    # Protected 'IApplicationWindow' interface.
    ###########################################################################

    def _create_trim_widgets(self, parent):
        """ Creates the 'trim' widgets (the widgets around the window).

        Parameters
        ----------
        parent : toolkit control
            The window's toolkit control.
        """

        # All of these are optional.
        self._set_window_icon()
        self._create_menu_bar(parent)
        self._create_tool_bar(parent)
        self._create_status_bar(parent)
