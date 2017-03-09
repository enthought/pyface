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
""" A top-level application window that supports multiple toolbars. """
from __future__ import absolute_import

# Major package imports.
import wx

# Enthought library imports
from pyface.action.api import ToolBarManager
from traits.api import Trait, TraitDict, TraitEnum, TraitList

# Local imports
from .application_window import ApplicationWindow


class MultiToolbarWindow(ApplicationWindow):
    """ A top-level application window that supports multiple toolbars.

    The multi-toolbar window has support for a menu bar, status bar, and
    multiple toolbars (all of which are optional).

    """

    # The toolbars in the order they were added to the window.
    _tool_bar_managers = Trait([], TraitList(Trait(ToolBarManager)))

    # Map of toolbar to screen location.
    _tool_bar_locations = Trait({},
                                TraitDict(Trait(ToolBarManager),
                                          TraitEnum('top', 'bottom',
                                                    'left', 'right')))

    ###########################################################################
    # Protected 'Window' interface.
    ###########################################################################
    def _create_contents(self, parent):
        panel = super(MultiToolbarWindow, self)._create_contents(parent)
        self._create_trim_widgets(parent)

        return panel

    def _create_trim_widgets(self, parent):

        # The frame's icon.
        self._set_window_icon()

        # Add the (optional) menu bar.
        self._create_menu_bar(parent)

        # Add the (optional) status bar.
        self._create_status_bar(parent)

        # Add the (optional) tool bars.
        self.sizer = self._create_tool_bars(parent)

        return

    def _create_tool_bars(self, parent):
        """ Create the tool bars for this window. """

        if len(self._tool_bar_managers) > 0:
            # Create a top level sizer to handle to main layout and attach
            # it to the parent frame.
            self.main_sizer = sizer = wx.BoxSizer(wx.VERTICAL)
            parent.SetSizer(sizer)
            parent.SetAutoLayout(True)

            for tool_bar_manager in self._tool_bar_managers:
                location = self._tool_bar_locations[tool_bar_manager]
                sizer = self._create_tool_bar(parent, sizer, tool_bar_manager,
                                              location)

            return sizer

        return None

    def _create_tool_bar(self, parent, sizer, tool_bar_manager, location):
        """ Create and add the toolbar to the parent window at the specified
        location.

        Returns the sizer where the remaining content should be added.  For
        'top' and 'left' toolbars, we can return the same sizer that contains
        the toolbar, because subsequent additions will be added below or to
        the right of those toolbars.  For 'right' and 'bottom' toolbars, we
        create a spacer toolbar to hold the content.
        """

        tool_bar = tool_bar_manager.create_tool_bar(parent)

        if location == 'top':
            child_sizer = wx.BoxSizer(wx.VERTICAL)
            child_sizer.Add(tool_bar, 0, wx.ALL | wx.ALIGN_LEFT | wx.EXPAND)
            sizer.Add(child_sizer, 1, wx.ALL | wx.EXPAND)

        if location == 'bottom':
            toolbar_sizer = wx.BoxSizer(wx.VERTICAL)

            # Add the placeholder for the content before adding the toolbar.
            child_sizer = self._create_content_spacer(toolbar_sizer)

            # Add the tool bar.
            toolbar_sizer.Add(tool_bar, 0, wx.ALL | wx.ALIGN_TOP | wx.EXPAND)
            sizer.Add(toolbar_sizer, 1, wx.ALL | wx.EXPAND)

        if location == 'left':
            child_sizer = wx.BoxSizer(wx.HORIZONTAL)
            child_sizer.Add(tool_bar, 0, wx.ALL | wx.ALIGN_TOP | wx.EXPAND)
            sizer.Add(child_sizer, 1, wx.ALL | wx.EXPAND)

        if location == 'right':
            toolbar_sizer = wx.BoxSizer(wx.HORIZONTAL)

            # Add the placeholder for the content before adding the toolbar.
            child_sizer = self._create_content_spacer(toolbar_sizer)

            # Add the tool bar.
            toolbar_sizer.Add(tool_bar, 0, wx.ALL | wx.ALIGN_TOP | wx.EXPAND)
            sizer.Add(toolbar_sizer, 1, wx.ALL | wx.EXPAND)

        return child_sizer

    def _create_content_spacer(self, sizer):
        spacer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(spacer, 1, wx.ALL | wx.EXPAND)

        return spacer

    ###########################################################################
    # Public MultiToolbarWindow interface
    ###########################################################################

    def add_tool_bar(self, tool_bar_manager, location='top'):
        """ Add a toolbar in the specified location.

        Valid locations are 'top', 'bottom', 'left', and 'right'
        """

        self._tool_bar_managers.append(tool_bar_manager)
        self._tool_bar_locations[tool_bar_manager] = location

#### EOF ######################################################################
