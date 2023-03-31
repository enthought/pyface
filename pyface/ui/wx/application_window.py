# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


""" Enthought pyface package component
"""

import wx

from traits.api import Str, observe, provides

from pyface.i_application_window import IApplicationWindow, MApplicationWindow
from pyface.wx.aui import aui, PyfaceAuiManager
from .image_resource import ImageResource
from .window import Window


@provides(IApplicationWindow)
class ApplicationWindow(MApplicationWindow, Window):
    """ The toolkit specific implementation of an ApplicationWindow.  See the
    IApplicationWindow interface for the API documentation.
    """

    # 'IWindow' interface -------------------------------------------------#

    title = Str("Pyface")

    # ------------------------------------------------------------------------
    # Protected 'IApplicationWindow' interface.
    # ------------------------------------------------------------------------

    def _create_contents(self, parent):
        panel = wx.Panel(parent, -1, name="ApplicationWindow")
        panel.SetBackgroundColour("blue")
        return panel

    def _create_menu_bar(self, parent):
        if self.menu_bar_manager is not None:
            menu_bar = self.menu_bar_manager.create_menu_bar(parent)
            self.control.SetMenuBar(menu_bar)

    def _create_status_bar(self, parent):
        if self.status_bar_manager is not None:
            status_bar = self.status_bar_manager.create_status_bar(parent)
            self.control.SetStatusBar(status_bar)

    def _create_tool_bar(self, parent):
        tool_bar_managers = self.tool_bar_managers
        if len(tool_bar_managers) > 0:
            for tool_bar_manager in reversed(tool_bar_managers):
                tool_bar = tool_bar_manager.create_tool_bar(parent, aui=True)
                self._add_toolbar_to_aui_manager(tool_bar)
            self._aui_manager.Update()

    def _set_window_icon(self):
        if self.icon is None:
            icon = ImageResource("application.ico")
        else:
            icon = self.icon

        if self.control is not None:
            self.control.SetIcon(icon.create_icon())

    # ------------------------------------------------------------------------
    # 'Window' interface.
    # ------------------------------------------------------------------------

    def _size_default(self):
        """ Trait initialiser. """
        return (800, 600)

    # ------------------------------------------------------------------------
    # Protected 'IWidget' interface.
    # ------------------------------------------------------------------------

    def create(self, parent=None):

        super().create(parent=parent)

        self._aui_manager = PyfaceAuiManager()
        self._aui_manager.SetManagedWindow(self.control)

        # Keep a reference to the AUI Manager in the control because Panes
        # will need to access it in order to lay themselves out
        self.control._aui_manager = self._aui_manager

        contents = self._create_contents(self.control)
        self._aui_manager.AddPane(contents, aui.AuiPaneInfo().CenterPane())

        self._create_trim_widgets(self.control)

        # Updating the AUI manager actually commits all of the pane's added
        # to it (this allows batch updates).
        self._aui_manager.Update()

    def _create_control(self, parent):

        style = (
            wx.DEFAULT_FRAME_STYLE | wx.FRAME_NO_WINDOW_MENU | wx.CLIP_CHILDREN
        )

        control = wx.Frame(
            parent,
            -1,
            self.title,
            style=style,
            size=self.size,
            pos=self.position,
        )

        # Mac/Win needs this, otherwise background color is black
        attr = control.GetDefaultAttributes()
        control.SetBackgroundColour(attr.colBg)

        return control

    def destroy(self):
        if self.control:
            self._aui_manager.UnInit()
        super().destroy()

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _add_toolbar_to_aui_manager(self, tool_bar):
        """ Add a toolbar to the AUI manager. """

        info = self._get_tool_bar_pane_info(tool_bar)
        self._aui_manager.AddPane(tool_bar, info)

    def _get_tool_bar_pane_info(self, tool_bar):
        info = aui.AuiPaneInfo()
        info.Caption(tool_bar.tool_bar_manager.name)
        info.LeftDockable(False)
        info.Name(tool_bar.tool_bar_manager.id)
        info.RightDockable(False)
        info.ToolbarPane()
        info.Top()

        return info

    def _wx_enable_tool_bar(self, tool_bar, enabled):
        """ Enable/Disablea tool bar. """

        # AUI toolbars cannot be enabled/disabled.

    def _wx_show_tool_bar(self, tool_bar, visible):
        """ Hide/Show a tool bar. """

        pane = self._aui_manager.GetPane(tool_bar.tool_bar_manager.id)

        if visible:
            pane.Show()

        else:
            # Without this workaround, toolbars know the sizes of other
            # hidden toolbars and leave gaps in the toolbar dock
            pane.window.Show(False)
            self._aui_manager.DetachPane(pane.window)
            info = self._get_tool_bar_pane_info(pane.window)
            info.Hide()
            self._aui_manager.AddPane(pane.window, info)

        self._aui_manager.Update()

        return

    # Trait change handlers ------------------------------------------------

    def _menu_bar_manager_changed(self):
        if self.control is not None:
            self._create_menu_bar(self.control)

    def _status_bar_manager_changed(self, old, new):
        if self.control is not None:
            if old is not None:
                self.control.SetStatusBar(None)
                old.destroy()
            self._create_status_bar(self.control)

    @observe("tool_bar_managers.items")
    def _update_tool_bar_managers(self, event):
        if self.control is not None:
            self._create_tool_bar(self.control)

    def _icon_changed(self):
        self._set_window_icon()
