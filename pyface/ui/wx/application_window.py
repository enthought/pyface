#------------------------------------------------------------------------------
#
#  Copyright (c) 2005, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in enthought/LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
#  Author: Enthought, Inc.
#
#------------------------------------------------------------------------------

""" Enthought pyface package component
"""

# Standard library imports.
import sys

# Major package imports.
import wx

try:
    import wx.aui
    AUI = True

except ImportError:
    AUI = False

# Enthought library imports.
from pyface.action.api import MenuBarManager, StatusBarManager
from pyface.action.api import ToolBarManager
from traits.api import Instance, List, provides, Unicode
from pyface.i_application_window import IApplicationWindow
from pyface.i_application_window import MApplicationWindow
from pyface.image_resource import ImageResource

# Local imports.
from window import Window
from system_metrics import SystemMetrics


@provides(IApplicationWindow)
class ApplicationWindow(MApplicationWindow, Window):
    """ The toolkit specific implementation of an ApplicationWindow.  See the
    IApplicationWindow interface for the API documentation.
    """


    #### 'IApplicationWindow' interface #######################################

    icon = Instance(ImageResource)

    menu_bar_manager = Instance(MenuBarManager)

    status_bar_manager = Instance(StatusBarManager)

    tool_bar_manager = Instance(ToolBarManager)

    # If the underlying toolkit supports multiple toolbars then you can use
    # this list instead.
    tool_bar_managers = List(ToolBarManager)

    #### 'IWindow' interface ##################################################

    # fixme: We can't set the default value of the actual 'size' trait here as
    # in the toolkit-specific event handlers for window size and position
    # changes, we set the value of the shadow '_size' trait. The problem is
    # that by doing that traits never knows that the trait has been set and
    # hence always returns the default value! Using a trait initializer method
    # seems to work however (e.g. 'def _size_default'). Hmmmm....
##     size = (800, 600)

    title = Unicode("Pyface")

    ###########################################################################
    # Protected 'IApplicationWindow' interface.
    ###########################################################################

    def _create_contents(self, parent):
        panel = wx.Panel(parent, -1)
        panel.SetSize((500, 400))
        panel.SetBackgroundColour('blue')

        return panel

    def _create_menu_bar(self, parent):
        if self.menu_bar_manager is not None:
            menu_bar = self.menu_bar_manager.create_menu_bar(parent)
            self.control.SetMenuBar(menu_bar)

    def _create_status_bar(self, parent):
        if self.status_bar_manager is not None:
            status_bar = self.status_bar_manager.create_status_bar(parent)
            self.control.SetStatusBar(status_bar)

        return

    def _create_tool_bar(self, parent):
        tool_bar_managers = self._get_tool_bar_managers()
        if len(tool_bar_managers) > 0:
            if AUI:
                for tool_bar_manager in reversed(tool_bar_managers):
                    tool_bar = tool_bar_manager.create_tool_bar(parent)
                    self._add_toolbar_to_aui_manager(
                        tool_bar, tool_bar_manager.name
                    )
            else:
                tool_bar = tool_bar_managers[0].create_tool_bar(parent)
                self.control.SetToolBar(tool_bar)

    def _set_window_icon(self):
        if self.icon is None:
            icon = ImageResource('application.ico')
        else:
            icon = self.icon

        if self.control is not None:
            self.control.SetIcon(icon.create_icon())

        return

    ###########################################################################
    # 'Window' interface.
    ###########################################################################

    def _size_default(self):
        """ Trait initialiser. """

        return (800, 600)

    ###########################################################################
    # Protected 'IWidget' interface.
    ###########################################################################

    def _create(self):

        if AUI:
            # fixme: We have to capture the AUI manager as an attribute,
            # otherwise it gets garbage collected and we get a core dump...
            # Ahh, the sweet smell of open-source ;^()
            self._aui_manager = wx.aui.AuiManager()

        super(ApplicationWindow, self)._create()

        if AUI:
            body = self._create_body(self.control)
            contents = self._create_contents(body)
            body.GetSizer().Add(contents, 1, wx.EXPAND)
            body.Fit()

        else:
            contents = self._create_contents(self.control)

        self._create_trim_widgets(self.control)

        if AUI:
            # Updating the AUI manager actually commits all of the pane's added
            # to it (this allows batch updates).
            self._aui_manager.Update()

        return

    def _create_control(self, parent):

        style = wx.DEFAULT_FRAME_STYLE \
                | wx.FRAME_NO_WINDOW_MENU \
                | wx.CLIP_CHILDREN

        control = wx.Frame(
            parent, -1, self.title, style=style, size=self.size,
            pos=self.position
        )

        control.SetBackgroundColour(SystemMetrics().dialog_background_color)

        if AUI:
            # Let the AUI manager look after the frame.
            self._aui_manager.SetManagedWindow(control)

        return control

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _add_toolbar_to_aui_manager(self, tool_bar, name='Tool Bar'):
        """ Add a toolbar to the AUI manager. """

        info = wx.aui.AuiPaneInfo()
        info.Caption(name)
        info.LeftDockable(False)
        info.Name(name)
        info.RightDockable(False)
        info.ToolbarPane()
        info.Top()

        self._aui_manager.AddPane(tool_bar, info)

        return

    def _create_body(self, parent):
        """ Create the body of the frame. """

        panel = wx.Panel(parent, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)

        info = wx.aui.AuiPaneInfo()
        info.Caption('Body')
        info.Dockable(False)
        info.Floatable(False)
        info.Name('Body')
        info.CentrePane()

        self._aui_manager.AddPane(panel, info)

        return panel

    def _get_tool_bar_managers(self):
        """ Return all tool bar managers specified for the window. """

        # fixme: V3 remove the old-style single toolbar option!
        if self.tool_bar_manager is not None:
            tool_bar_managers = [self.tool_bar_manager]

        else:
            tool_bar_managers = self.tool_bar_managers

        return tool_bar_managers

    def _wx_enable_tool_bar(self, tool_bar, enabled):
        """ Enable/Disablea tool bar. """

        if AUI:
            # AUI toolbars cannot be enabled/disabled.
            pass

        else:
            tool_bar.Enable(enabled)

        return

    def _wx_show_tool_bar(self, tool_bar, visible):
        """ Hide/Show a tool bar. """

        if AUI:
            pane = self._aui_manager.GetPane(tool_bar.tool_bar_manager.name)

            if visible:
                pane.Show()

            else:
                pane.Hide()

            self._aui_manager.Update()

        else:
            tool_bar.Show(visible)

        return

    #### Trait change handlers ################################################
    def _icon_changed(self):
        self._set_window_icon()

#### EOF ######################################################################
