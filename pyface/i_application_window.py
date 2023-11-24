# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The interface of a top-level application window. """


from traits.api import HasTraits, Instance, List

from pyface.action.i_menu_bar_manager import IMenuBarManager
from pyface.action.i_status_bar_manager import IStatusBarManager
from pyface.action.i_tool_bar_manager import IToolBarManager
from pyface.i_window import IWindow
from pyface.ui_traits import Image


class IApplicationWindow(IWindow):
    """ The interface for a top-level application window.

    The application window has support for a menu bar, tool bar and a status
    bar (all of which are optional).

    Notes
    -----

    To use, create a sub-class of this class and override the
    :py:meth:`._create_contents` method.
    """

    # 'IApplicationWindow' interface ---------------------------------------

    #: The window icon.  The default is toolkit specific.
    icon = Image()

    #: The menu bar manager for the window.
    menu_bar_manager = Instance(IMenuBarManager)

    #: The status bar manager for the window.
    status_bar_manager = Instance(IStatusBarManager)

    #: The collection of tool bar managers for the window.
    tool_bar_managers = List(Instance(IToolBarManager))

    # ------------------------------------------------------------------------
    # Protected 'IApplicationWindow' interface.
    # ------------------------------------------------------------------------

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


class MApplicationWindow(HasTraits):
    """ The mixin class that contains common code for toolkit specific
    implementations of the :py:class:`IApplicationWindow` interface.

    Implements: destroy(), _create_trim_widgets()
    """

    #: The icon to display in the application window title bar.
    icon = Image()

    #: The menu bar manager for the window.
    menu_bar_manager = Instance(IMenuBarManager)

    #: The status bar manager for the window.
    status_bar_manager = Instance(IStatusBarManager)

    #: The collection of tool bar managers for the window.
    tool_bar_managers = List(Instance(IToolBarManager))

    # ------------------------------------------------------------------------
    # 'IWidget' interface.
    # ------------------------------------------------------------------------

    def destroy(self):
        """ Destroy the control if it exists. """

        if self.menu_bar_manager is not None:
            self.menu_bar_manager.destroy()

        if self.status_bar_manager is not None:
            self.status_bar_manager.destroy()

        for tool_bar_manager in self.tool_bar_managers:
            tool_bar_manager.destroy()

        super().destroy()

    # ------------------------------------------------------------------------
    # Protected 'IApplicationWindow' interface.
    # ------------------------------------------------------------------------

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
